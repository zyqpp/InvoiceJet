#!/usr/bin/env pwsh
# stop-docs.ps1 — zatrzymuje serwery MkDocs

Write-Host "Zatrzymuję serwery MkDocs na portach 8001 i 8002..." -ForegroundColor Yellow

foreach ($port in @(8001, 8002)) {
  $pids = netstat -ano | Select-String ":$port\s" | Select-String "LISTENING" |
    ForEach-Object { ($_ -split '\s+')[-1] } | Sort-Object -Unique
  foreach ($pid in $pids) {
    if ($pid -match '^\d+$') {
      try { Stop-Process -Id $pid -Force -ErrorAction Stop; Write-Host "✅ Zatrzymano PID $pid (port $port)" -ForegroundColor Green }
      catch { Write-Host "ℹ️  PID $pid już nieaktywny" -ForegroundColor Gray }
    }
  }
}
Write-Host "Gotowe." -ForegroundColor Green
