@echo off
IF "%1."=="." GOTO nomodel
cls
python analyze_repo.py --repo_path ..\horde-client-bad --model %1 --note %1
goto end
:nomodel
echo You need to specify a model as the first parameter, such as gpt-4
echo.
:end
