# app/tasks/pipeline.py

import sys
import os
import asyncio
import logging
from celery import Celery
import pandas as pd

# Adjust paths to match root context
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.config import settings
from app.database import SessionLocal
from app import models
from data_ingestion.orchestrator import StateIngestionOrchestrator
from comparison_engine import SnapshotComparisonEngine

logger = logging.getLogger("nmls_radar.celery_pipeline")

# Initialize Celery app instance linking to configured Redis brokers
celery_app = Celery("nmls_radar_tasks", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "execute-national-ingestion-cron": {
            "task": "app.tasks.pipeline.trigger_national_ingestion_sync",
            "schedule": 24 * 3600.0, # Run periodic every 24 hours as system daemon fallback
        }
    }
)

def run_state_comparison_and_event_dispatch(state_code: str, raw_csv_filepath: str):
    db = SessionLocal()
    try:
        current_df = pd.read_csv(raw_csv_filepath)
        previous_los = db.query(models.LoanOfficer).filter(models.LoanOfficer.current_state == state_code.upper()).all()
        previous_records = []
        
        for lo in previous_los:
            comp = db.query(models.Company).filter(models.Company.id == lo.current_company_id).first()
            previous_records.append({
                "nmls_id": lo.nmls_id,
                "first_name": lo.first_name,
                "last_name": lo.last_name,
                "company_name": comp.company_name if comp else None,
                "company_nmls": comp.company_nmls if comp else None,
                "license_status": lo.license_status,
                "state": lo.current_state
            })
            
        previous_df = pd.DataFrame(previous_records)
        if previous_df.empty:
            logger.info("Day T-1 registry represents null active status for State: " + state_code)
            for _, row in current_df.iterrows():
                if pd.notna(row["company_nmls"]):
                    comp = db.query(models.Company).filter(models.Company.company_nmls == int(row["company_nmls"])).first()
                    if not comp:
                        comp = models.Company(
                            company_name=row["company_name"],
                            company_nmls=int(row["company_nmls"]),
                            state=row["state"]
                        )
                        db.add(comp)
                        db.commit()
                        db.refresh(comp)
                
                lo_exists = db.query(models.LoanOfficer).filter(models.LoanOfficer.nmls_id == int(row["nmls_id"])).first()
                if not lo_exists:
                    comp_id = comp.id if pd.notna(row["company_nmls"]) else None
                    new_lo = models.LoanOfficer(
                        nmls_id=row["nmls_id"],
                        first_name=row["first_name"],
                        last_name=row["last_name"],
                        current_company_id=comp_id,
                        current_state=row["state"],
                        license_status=row["license_status"]
                    )
                    db.add(new_lo)
            db.commit()
            return

        comparison = SnapshotComparisonEngine(current_df, previous_df)
        events = comparison.execute_comparison_pipeline()
        
        for e in events:
            comp_ref = None
            if e["new_value"] and e["new_value"].get("company_nmls"):
                target_nmls = int(e["new_value"]["company_nmls"])
                comp_ref = db.query(models.Company).filter(models.Company.company_nmls == target_nmls).first()
                if not comp_ref:
                    comp_ref = models.Company(
                        company_name=e["new_value"]["company_name"],
                        company_nmls=target_nmls,
                        state=e["new_value"]["state"]
                    )
                    db.add(comp_ref)
                    db.commit()
                    db.refresh(comp_ref)
            
            officer = db.query(models.LoanOfficer).filter(models.LoanOfficer.nmls_id == e["nmls_id"]).first()
            if e["event_type"] == "NEW_LICENSE" and not officer:
                new_lo = models.LoanOfficer(
                    nmls_id=e["nmls_id"],
                    first_name=e["new_value"]["first_name"],
                    last_name=e["new_value"]["last_name"],
                    current_company_id=comp_ref.id if comp_ref else None,
                    current_state=e["new_value"]["state"],
                    license_status=e["new_value"]["license_status"]
                )
                db.add(new_lo)
            elif e["event_type"] == "COMPANY_TRANSFER" and officer:
                officer.current_company_id = comp_ref.id if comp_ref else None
            elif e["event_type"] == "LICENSE_STATUS_CHANGE" and officer:
                officer.license_status = e["new_value"]["license_status"]

            change_evt = models.ChangeEvent(
                event_type=e["event_type"],
                nmls_id=e["nmls_id"],
                old_value=str(e["old_value"]) if e["old_value"] else None,
                new_value=str(e["new_value"]) if e["new_value"] else None,
                event_description=e["event_description"]
            )
            db.add(change_evt)
            
        db.commit()
        logger.info("Symmetric Snapshot Pipeline run successfully completed for State Code: " + state_code)
    except Exception as err:
        db.rollback()
        logger.error("Failed pipeline run processes: " + str(err))
    finally:
        db.close()


@celery_app.task
def trigger_national_ingestion_sync():
    logger.info("Initializing Daily National Ingestion Pipeline daemon...")
    orchestrator = StateIngestionOrchestrator(use_sftp_fallback=True)
    loop = asyncio.get_event_loop()
    ingest_report = loop.run_until_complete(orchestrator.execute_national_pipeline(max_concurrency=4))
    
    logger.info("Parsing sync outputs, compiling datasets, and trigger comparatives...")
    for item in ingest_report:
        if item["success"] and item["filepath"]:
            logger.info("Dispatched diff calculations task for state code: " + item["state"])
            run_state_comparison_and_event_dispatch(item["state"], item["filepath"])
            
    return {"status": "SUCCESS", "processed_states": len(ingest_report)}