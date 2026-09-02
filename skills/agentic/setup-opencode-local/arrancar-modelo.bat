#cd /d C:\Users\brjap\llama.cpp
# llama-server.exe -m models\Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf --jinja -ngl 99 -fa on -c 8192 --cache-type-k q8_0 --cache-type-v q8_0 --port 8080 --no-webui

@echo off
cd /d "%~dp0"

echo Arrancando llama-server...
llama-server.exe -m models\Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf --jinja -ngl 24 -fa auto -c 4096 --port 11434 --ui

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo El servidor se cerro con codigo de error %ERRORLEVEL%
    pause
)
