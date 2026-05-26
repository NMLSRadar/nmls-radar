# NMLS Radar - AI-Powered Mortgage Industry Intelligence

NMLS Radar is an enterprise-grade SaaS platform designed to monitor, track, and organize newly licensed mortgage loan officers (MLOs) and company sponsorship transfers across all 50 states.

## Quick Start (Bootstrap Workspace)

We have packaged the entire Multi-Stage FastAPI and Next.js codebase within an automatic cloud-restoration installer. To bootstrap your local workspace, simply run:

```bash
# 1. Restore the backend and frontend code structures
python3 retrieve_workspace.py
python3 populate_frontend.py

# 2. Run the application containers
docker-compose up --build
```