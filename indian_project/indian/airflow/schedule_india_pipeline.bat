@echo off
cd /d "%~dp0"
python run_india_pipeline.py >> india_pipeline_log.txt 2>&1
