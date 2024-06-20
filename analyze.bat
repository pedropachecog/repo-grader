@echo off 
cls
python analyze_repo.py --repo_path ..\horde-client-bad --endpoint http://localhost:1234/v1 --note %1