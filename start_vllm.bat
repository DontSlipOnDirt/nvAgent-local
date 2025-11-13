@echo off
REM start_vllm.bat
REM Quick launcher for vLLM server

echo Starting vLLM Server...
python core/vllm_server.py
pause
