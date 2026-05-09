@echo off
setlocal
for %%I in ("%~dp0.") do set "REPO_ROOT=%%~fI"
set "WORKSPACE_ROOT=%REPO_ROOT%\example_workspace"
set "APP_ROOT=%REPO_ROOT%\organizer"
set "STATE_FILE=%APP_ROOT%\server_state.json"
set "HOST=127.0.0.1"
set "PORT=8765"
set "URL=http://%HOST%:%PORT%"
chcp 65001 >nul
set "PYTHONIOENCODING=utf-8"

if not exist "%WORKSPACE_ROOT%" mkdir "%WORKSPACE_ROOT%"

if exist "%STATE_FILE%" (
  powershell -NoProfile -ExecutionPolicy Bypass -Command "try { $state = Get-Content '%STATE_FILE%' -Raw | ConvertFrom-Json; if ($state.pid) { Get-Process -Id $state.pid -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue }; if ($state.port) { Get-NetTCPConnection -LocalPort $state.port -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1 | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue } } } catch {}"
  del "%STATE_FILE%" >nul 2>nul
)

timeout /t 1 /nobreak >nul

powershell -NoProfile -ExecutionPolicy Bypass -Command "$repo='%REPO_ROOT%'; $root='%WORKSPACE_ROOT%'; $host='%HOST%'; $port='%PORT%'; if (Get-Command py -ErrorAction SilentlyContinue) { $file='py'; $args=@('-3','-m','organizer.server','--root',$root,'--host',$host,'--port',$port) } elseif (Get-Command python -ErrorAction SilentlyContinue) { $file='python'; $args=@('-m','organizer.server','--root',$root,'--host',$host,'--port',$port) } else { Write-Error 'Python 3 was not found. Please install Python 3 and try again.'; exit 1 }; Start-Process -FilePath $file -ArgumentList $args -WorkingDirectory $repo -WindowStyle Hidden"
if errorlevel 1 (
  echo Python 3 was not found. Please install Python 3 and try again.
  pause
  exit /b 1
)

for /f "usebackq delims=" %%U in (`powershell -NoProfile -ExecutionPolicy Bypass -Command "$stateFile='%STATE_FILE%'; for ($i = 0; $i -lt 20; $i++) { if (Test-Path $stateFile) { try { $state = Get-Content $stateFile -Raw | ConvertFrom-Json; if ($state.url) { try { $page = Invoke-WebRequest -UseBasicParsing ($state.url + '/index.html'); if ($page.StatusCode -eq 200) { Write-Output $state.url; exit 0 } } catch {} } } catch {} }; Start-Sleep -Milliseconds 500 }; exit 1"`) do set "URL=%%U"

start "" "%URL%/index.html"
