import os
import urllib.request

ARTEFACTS = {
    # 1. Base Framework & API Router Engine
    "https://d2ol7oe51mr4n9.cloudfront.net/user_3Cfrs4UEzyBfibhWL8hkQ0WuLXI/5196e5f1-921f-402d-9b59-32e6837816e3.py": "backend/app/config.py",
    "https://d2ol7oe51mr4n9.cloudfront.net/user_3Cfrs4UEzyBfibhWL8hkQ0WuLXI/d750073c-6d3b-4e88-86bc-03de618e53ea.py": "backend/app/database.py",
    "https://d2ol7oe51mr4n9.cloudfront.net/user_3Cfrs4UEzyBfibhWL8hkQ0WuLXI/0314f57e-58ad-484b-9df2-da6d2f774b37.py": "backend/app/models.py",
    "https://d2ol7oe51mr4n9.cloudfront.net/user_3Cfrs4UEzyBfibhWL8hkQ0WuLXI/b982b729-c08e-4d76-ab2e-11019ab6a426.py": "backend/app/schemas/officer.py",
    "https://d2ol7oe51mr4n9.cloudfront.net/user_3Cfrs4UEzyBfibhWL8hkQ0WuLXI/7d02d920-84bc-47ee-8d3e-58e314657970.py": "backend/app/routers/officers.py",
    "https://d2ol7oe51mr4n9.cloudfront.net/user_3Cfrs4UEzyBfibhWL8hkQ0WuLXI/f7eee471-4320-4a2f-abe6-b0842a906f84.py": "backend/app/routers/companies.py",
    "https://d2ol7oe51mr4n9.cloudfront.net/user_3Cfrs4UEzyBfibhWL8hkQ0WuLXI/5acb0412-f407-411e-bf45-aab75875e9f5.py": "backend/app/routers/events.py",
    "https://d2ol7oe51mr4n9.cloudfront.net/user_3Cfrs4UEzyBfibhWL8hkQ0WuLXI/5bfb6ac8-8fce-4acd-ba0b-45bdfd8a026d.py": "backend/app/routers/imports.py",
    "https://d2ol7oe51mr4n9.cloudfront.net/user_3Cfrs4UEzyBfibhWL8hkQ0WuLXI/6eea762e-bf34-4e43-aeb1-5099c4f4ed18.py": "backend/app/main.py",
    
    # 2. Scrapers, Delta Engine, and Seeder Scripts
    "https://d2ol7oe51mr4n9.cloudfront.net/user_3Cfrs4UEzyBfibhWL8hkQ0WuLXI/9c570419-4f9e-4a7e-8fe6-4ec3bd89f4c8.py": "backend/scripts/mock_pipeline.py",
    "https://d2ol7oe51mr4n9.cloudfront.net/user_3Cfrs4UEzyBfibhWL8hkQ0WuLXI/c6ad2785-5390-4190-bbdb-f792e71c28e7.py": "backend/comparison_engine.py",
    "https://d2ol7oe51mr4n9.cloudfront.net/user_3Cfrs4UEzyBfibhWL8hkQ0WuLXI/0751e1eb-c484-4180-879b-4cd1b420e9ea.py": "backend/tests/test_comparison.py",
    
    # 3. 50-State Data Ingestion Ecosystem
    "https://d2ol7oe51mr4n9.cloudfront.net/user_3Cfrs4UEzyBfibhWL8hkQ0WuLXI/d8896e3e-a9ec-4f02-b806-50dc0c185350.py": "backend/data_ingestion/base.py",
    "https://d2ol7oe51mr4n9.cloudfront.net/user_3Cfrs4UEzyBfibhWL8hkQ0WuLXI/16aafcc5-7677-4cff-a8a6-b496f77d4ae3.py": "backend/data_ingestion/adapters/apify_adapter.py",
    "https://d2ol7oe51mr4n9.cloudfront.net/user_3Cfrs4UEzyBfibhWL8hkQ0WuLXI/c8be3931-3a86-461c-8a20-8cd921d35e38.py": "backend/data_ingestion/adapters/fallback_sftp_adapter.py",
    "https://d2ol7oe51mr4n9.cloudfront.net/user_3Cfrs4UEzyBfibhWL8hkQ0WuLXI/c9eeb883-b496-4716-9854-b7d94da3df04.py": "backend/data_ingestion/orchestrator.py",

    # 4. Architecture and Schema specs
    "https://d2ol7oe51mr4n9.cloudfront.net/user_3Cfrs4UEzyBfibhWL8hkQ0WuLXI/b4eecd3b-0a5b-41a0-a0e4-c81518472a1d.md": "backend/ARCHITECTURE.md",
    "https://d2ol7oe51mr4n9.cloudfront.net/user_3Cfrs4UEzyBfibhWL8hkQ0WuLXI/79821021-3707-4465-98b9-27f51a5e5fe3.sql": "backend/schema.sql",
    "https://d2ol7oe51mr4n9.cloudfront.net/user_3Cfrs4UEzyBfibhWL8hkQ0WuLXI/f127cb28-cf81-4be3-a264-ad81bbcf3891.md": "backend/api_endpoints.md",
    "https://d2ol7oe51mr4n9.cloudfront.net/user_3Cfrs4UEzyBfibhWL8hkQ0WuLXI/0bcc3a90-e317-44fe-b039-acd7ac0e7a93.md": "backend/security_compliance_roadmap.md"
}

def retrieve_all_artefacts():
    print("Initiating retrieval sequence from Cloudfront...")
    headers = {"User-Agent": "Mozilla/5.0"}
    for url, dest_path in ARTEFACTS.items():
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as r:
                with open(dest_path, "wb") as f:
                    f.write(r.read())
        except Exception as e:
            print(f"Error {dest_path}: {e}")