@echo off
REM start_nl2vis_vllm.bat
REM Complete startup script for NL2Vis with vLLM

echo ============================================================
echo Starting NL2Vis with vLLM Backend
echo ============================================================
echo.

REM Check if vLLM is enabled
python -c "from core.vllm_config import USE_VLLM; print(f'vLLM Enabled: {USE_VLLM}')" 2>nul
if errorlevel 1 (
    echo ERROR: Cannot import vLLM config. Please check installation.
    pause
    exit /b 1
)

echo Step 1: Starting vLLM server in background...
echo Note: This will open a new window. Do NOT close it!
echo.
start "vLLM Server - DO NOT CLOSE" cmd /k "python core/vllm_server.py"

echo.
echo Step 2: Waiting for server to initialize (30 seconds)...
echo You can check the other window for server status.
echo.
timeout /t 30 /nobreak

echo.
echo Step 3: Testing server connection...
python test_vllm.py 2>nul
if errorlevel 1 (
    echo.
    echo WARNING: Server test failed. The server might still be starting.
    echo You can:
    echo   1. Wait a bit longer and press any key to continue
    echo   2. Check the vLLM server window for errors
    echo.
    pause
)

echo.
echo ============================================================
echo Step 4: Running NL2Vis...
echo ============================================================
echo.

REM You can customize this to run your specific script
python run_evaluate.py

echo.
echo ============================================================
echo NL2Vis execution completed!
echo.
echo To stop the vLLM server, close the "vLLM Server" window.
echo ============================================================
pause
