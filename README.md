# Shipment Exception Manager
Case 3 of Kunal Kishore's independent seller-experience portfolio.

Fictional data, illustrative rules, session-only workflow. Not affiliated with Shiprocket. No customer messages or tickets are sent.

## Run
`pip install -r requirements.txt`
`streamlit run app.py`

## Deploy
Upload these files at a GitHub repository root. In Streamlit Community Cloud select that repository, main branch and app.py. No API keys needed.

## Demo
Filter P1 → open a case → assign owner → save In progress → prepare message draft → resolve with a note → inspect/export audit log. Refresh/session termination may discard edits.

## Documents
PRD.md includes journey, users, acceptance criteria, rules, edge cases, metrics and rollout. prioritization.csv contains assumption-based RICE scores. Run `python -m unittest test_rules.py` for deterministic rule tests.

## Honest resume description
Designed and prototyped a shipment-exception workflow using 120 synthetic shipments; authored a PRD, acceptance criteria, assumption-based RICE prioritization and a measurement plan, with seven passing rule tests. No real business improvement measured.
