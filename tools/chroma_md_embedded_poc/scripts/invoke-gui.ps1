param(
    [int]$Port = 8501
)

$ErrorActionPreference = "Stop"

$moduleRoot = Split-Path -Parent $PSScriptRoot
$repoRoot = Split-Path -Parent (Split-Path -Parent $moduleRoot)
$tempRoot = Join-Path $repoRoot ".tmp"

New-Item -ItemType Directory -Force -Path (Join-Path $tempRoot "temp") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $tempRoot "home") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $tempRoot "pip-cache") | Out-Null

$env:TEMP = Join-Path $tempRoot "temp"
$env:TMP = Join-Path $tempRoot "temp"
$env:USERPROFILE = Join-Path $tempRoot "home"
$env:HOME = Join-Path $tempRoot "home"
$env:PIP_CACHE_DIR = Join-Path $tempRoot "pip-cache"
$env:PYTHONPATH = $moduleRoot

$streamlit = Join-Path $moduleRoot ".venv\Scripts\streamlit.exe"
$app = Join-Path $moduleRoot "chroma_gui_app.py"
if (-not (Test-Path $streamlit)) {
    throw "Missing streamlit in venv: $streamlit"
}
if (-not (Test-Path $app)) {
    throw "Missing app file: $app"
}

& $streamlit run $app --server.port $Port --server.address "127.0.0.1" --server.headless true --browser.gatherUsageStats false
