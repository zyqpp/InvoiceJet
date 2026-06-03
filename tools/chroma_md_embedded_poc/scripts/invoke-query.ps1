param(
    [Parameter(Mandatory = $true)]
    [string]$Question,
    [int]$TopK = 5,
    [string]$SourceContains = ""
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

$python = Join-Path $moduleRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    throw "Missing venv python: $python"
}

$args = @("-m", "chroma_md_poc.query", "--q", $Question, "--top-k", $TopK)
if ($SourceContains) {
    $args += @("--source-contains", $SourceContains)
}

& $python @args
