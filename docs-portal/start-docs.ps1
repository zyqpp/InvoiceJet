#!/usr/bin/env pwsh
# start-docs.ps1 — uruchamia oba portale MkDocs InvoiceJet
# doc_AI   → http://127.0.0.1:8001
# doc_user → http://127.0.0.1:8002

$MKDOCS    = "C:\Users\kamil\AppData\Roaming\Python\Python314\Scripts\mkdocs.exe"
$ROOT      = Split-Path -Parent $MyInvocation.MyCommand.Path
$AI_DIR    = Join-Path $ROOT "doc-ai"
$USER_DIR  = Join-Path $ROOT "doc-user"
$PORT_AI   = 8001
$PORT_USER = 8002

Write-Host "================================================" -ForegroundColor Cyan
Write-Host " InvoiceJet Docs Portal" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# Sprawdź porty
foreach ($port in @($PORT_AI, $PORT_USER)) {
  $used = netstat -ano | Select-String ":$port\s" | Select-String "LISTENING"
  if ($used) {
    Write-Host "⚠️  Port $port zajęty! Uruchom stop-docs.ps1 najpierw." -ForegroundColor Red
    exit 1
  }
}

Write-Host ""
Write-Host "▶ doc_AI   → http://127.0.0.1:$PORT_AI" -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", `
  "Set-Location '$AI_DIR'; Write-Host '📚 doc_AI http://127.0.0.1:$PORT_AI' -ForegroundColor Cyan; & '$MKDOCS' serve --dev-addr=127.0.0.1:$PORT_AI"

Start-Sleep 3

Write-Host "▶ doc_user → http://127.0.0.1:$PORT_USER" -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", `
  "Set-Location '$USER_DIR'; Write-Host '👤 doc_user http://127.0.0.1:$PORT_USER' -ForegroundColor Magenta; & '$MKDOCS' serve --dev-addr=127.0.0.1:$PORT_USER"

Write-Host ""
Write-Host "Czekam aż serwery wystartują (~15s dla doc_AI)..." -ForegroundColor Yellow
Start-Sleep 15

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host " GOTOWE! Otwóz w przeglądarce:" -ForegroundColor Green
Write-Host ""
Write-Host "  📚 Dokumentacja Techniczna : http://127.0.0.1:$PORT_AI"  -ForegroundColor Yellow
Write-Host "  👤 Dokumentacja Użytkownika: http://127.0.0.1:$PORT_USER" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Edycja: zmień plik .md → przeglądarka auto-odświeży" -ForegroundColor Gray
Write-Host "  Stop:   uruchom stop-docs.ps1" -ForegroundColor Gray
Write-Host "================================================" -ForegroundColor Green

Start-Process "http://127.0.0.1:$PORT_AI"
Start-Sleep 1
Start-Process "http://127.0.0.1:$PORT_USER"
