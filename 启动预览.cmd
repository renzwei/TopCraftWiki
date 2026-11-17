@echo off
setlocal
set "WIKI_NODE="
for /f "delims=" %%N in ('where node.exe 2^>nul') do if not defined WIKI_NODE set "WIKI_NODE=%%N"
if not defined WIKI_NODE if exist "%ProgramFiles%\nodejs\node.exe" set "WIKI_NODE=%ProgramFiles%\nodejs\node.exe"
if not defined WIKI_NODE if exist "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe" set "WIKI_NODE=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe"
if not defined WIKI_NODE (
  echo Node.js was not found. Install Node.js or restore the existing runtime.
  pause
  exit /b 1
)
echo Starting TopCraft Wiki preview...
echo Keep this window open. Press Ctrl+C to stop.
echo.
"%WIKI_NODE%" "%~dp0scripts\preview.mjs"
if errorlevel 1 pause
endlocal
