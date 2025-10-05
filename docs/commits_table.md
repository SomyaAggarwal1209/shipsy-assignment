Commit history table
| Commit | Date | Message |
|---|---:|---|
| d10d60a | 2025-10-04 13:51:56 +0530 | Initial commit |
| f47f806 | 2025-10-04 13:50:11 +0530 | project init ΓÇö virtualenv, requirements, basic flask app |
| 6dd1a7a | 2025-10-04 15:05:55 +0530 | hour-1: setup Flask app, database models, env config, tables created |
| 9fc2f41 | 2025-10-04 15:08:08 +0530 | remove .env from repo and add to gitignore |
| ea24f83 | 2025-10-04 16:54:52 +0530 | add auth (register/login/logout) dashboard and templates |
| 515cfb9 | 2025-10-04 17:11:27 +0530 | add shipment add and edit functionality |
| 6215394 | 2025-10-04 19:47:07 +0530 | add initial README with project description |
| 6f6f99f | 2025-10-04 20:35:37 +0530 | add search functionality to shipments list (by description) |
| 4f48c47 | 2025-10-05 06:31:00 +0530 | integrated Gemini CLI UI improvements (search/filter form + CSS styling) |
| 3245ae1 | 2025-10-05 08:15:31 +0530 | add sorting to shipments list (date and total_cost) with UI selector |
| fe606e6 | 2025-10-05 08:51:01 +0530 | add OpenAPI spec and Swagger UI at /api-docs (spec saved from Gemini CLI) |
| 49fa5c0 | 2025-10-05 09:30:12 +0530 | add pytest tests for Shipment.total_cost and test setup |
| 8112cf7 | 2025-10-05 11:35:47 +0530 | simplify endpoint test - removed unstable create POST; insert shipment via DB context; all tests pass |
| da3df8f | 2025-10-05 12:34:27 +0530 | add waitress for Windows local testing; keep gunicorn for deployment |
| 6835002 | 2025-10-05 13:10:58 +0530 | update homepage UI and show recent shipments; added Gemini output to docs |
| c052ef1 | 2025-10-05 13:33:56 +0530 | fix: ensure wsgi.py present at repo root for Render |
| e384af7 | 2025-10-05 13:43:46 +0530 | deployed app to Render and added deployment link to docs |
| 3040f77 | 2025-10-05 15:34:39 +0530 | fix: save edited shipment fields (status, is_fragile, base_cost, tax_rate, handling_fee); remove origin/destination from edit form |
| 869cc2c | 2025-10-05 15:48:44 +0530 | feat: add Home navigation button to Dashboard, Shipments, and global navbar |
| 6333f8a | 2025-10-05 17:21:32 +0530 | final sync: add all templates, docs, and recent UI changes |
