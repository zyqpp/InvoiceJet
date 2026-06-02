$ErrorActionPreference = "Stop"

$Script:OracleToolRoot = Split-Path -Parent $PSScriptRoot
$Script:OracleRepoRoot = Split-Path -Parent (Split-Path -Parent $Script:OracleToolRoot)
$Script:OracleTempRoot = Join-Path $Script:OracleRepoRoot ".tmp"

New-Item -ItemType Directory -Force -Path (Join-Path $Script:OracleTempRoot "temp") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $Script:OracleTempRoot "home") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $Script:OracleTempRoot "pip-cache") | Out-Null

$env:TEMP = Join-Path $Script:OracleTempRoot "temp"
$env:TMP = Join-Path $Script:OracleTempRoot "temp"
$env:USERPROFILE = Join-Path $Script:OracleTempRoot "home"
$env:HOME = Join-Path $Script:OracleTempRoot "home"
$env:PIP_CACHE_DIR = Join-Path $Script:OracleTempRoot "pip-cache"
$env:PYTHONPATH = $Script:OracleToolRoot
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

function Get-OraclePython {
    $venvPython = Join-Path $Script:OracleToolRoot ".venv\Scripts\python.exe"
    if (Test-Path $venvPython) {
        return $venvPython
    }
    return "python"
}
