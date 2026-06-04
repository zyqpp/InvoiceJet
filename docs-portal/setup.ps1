#!/usr/bin/env pwsh
<#
.SYNOPSIS
    InvoiceJet Docs Portal - jednorazowy setup + start na nowym komputerze.

.DESCRIPTION
    Skrypt:
    1. Sprawdza Python 3.8+.
    2. Instaluje mkdocs + mkdocs-material + pluginy.
    3. Finalizuje porty dla obu portali.
    4. Generuje mkdocs.yml z lokalnymi sciezkami i URL-ami portali.
    5. Aktualizuje lokalny Oracle .env.
    6. Uruchamia oba serwery MkDocs.

.PARAMETER HostName
    Host/bind address dla MkDocs. Domyslnie: 127.0.0.1. Alias: -Host.

.PARAMETER PortAI
    Port dla dokumentacji technicznej (doc_AI). Domyslnie: 8201.

.PARAMETER PortUser
    Port dla dokumentacji uzytkownika (doc_user). Domyslnie: 8301.

.PARAMETER OracleEnvPath
    Lokalna sciezka do pliku .env narzedzia Oracle InvoiceJet.
#>

param(
    [Alias("Host")]
    [string]$HostName = "127.0.0.1",
    [int]$PortAI = 8201,
    [int]$PortUser = 8301,
    [string]$OracleEnvPath
)

$ErrorActionPreference = "Stop"

function OK { Write-Host "  OK  $args" -ForegroundColor Green }
function INFO { Write-Host "  ->  $args" -ForegroundColor Cyan }
function WARN { Write-Host "  !!  $args" -ForegroundColor Yellow }
function FAIL { Write-Host "  XX  $args" -ForegroundColor Red; exit 1 }

function Test-PortInUse {
    param([Parameter(Mandatory = $true)][int]$Port)

    $used = netstat -ano 2>$null | Select-String ":$Port\s" | Select-String "LISTENING"
    return [bool]$used
}

function Resolve-FreePort {
    param([Parameter(Mandatory = $true)][int]$RequestedPort)

    $port = $RequestedPort
    while (Test-PortInUse -Port $port) {
        WARN "Port $port zajety. Probuje $($port + 10)."
        $port += 10
    }
    return $port
}

function Get-DefaultOracleEnvPath {
    $repoRoot = Split-Path -Parent $SCRIPT_DIR
    return Join-Path $repoRoot "tools\oracle_invoicejet\.env"
}

function Update-OracleEnv {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$DocAIUrl,
        [Parameter(Mandatory = $true)][string]$DocUserUrl
    )

    $envDir = Split-Path -Parent $Path
    if ($envDir -and -not (Test-Path -LiteralPath $envDir)) {
        New-Item -ItemType Directory -Path $envDir -Force | Out-Null
    }

    $lines = [System.Collections.Generic.List[string]]::new()
    if (Test-Path -LiteralPath $Path) {
        foreach ($line in Get-Content -LiteralPath $Path) {
            [void]$lines.Add($line)
        }
    }

    $values = [ordered]@{
        ORACLE_DOCS_PORTAL_DOC_AI = $DocAIUrl.TrimEnd("/")
        ORACLE_DOCS_PORTAL_DOC_USER = $DocUserUrl.TrimEnd("/")
    }

    foreach ($key in $values.Keys) {
        $updated = $false
        for ($i = 0; $i -lt $lines.Count; $i++) {
            if ($lines[$i] -match "^\s*$([regex]::Escape($key))\s*=") {
                $lines[$i] = "$key=$($values[$key])"
                $updated = $true
                break
            }
        }
        if (-not $updated) {
            $lines.Add("$key=$($values[$key])")
        }
    }

    Set-Content -LiteralPath $Path -Value $lines -Encoding utf8
}

function ConvertTo-YamlPath {
    param([Parameter(Mandatory = $true)][string]$Path)
    return $Path -replace "'", "''"
}

$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$REPO_ROOT = Split-Path -Parent $SCRIPT_DIR
$oracleEnv = if ($OracleEnvPath) { $OracleEnvPath } else { Get-DefaultOracleEnvPath }

Write-Host ""
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "  InvoiceJet Docs Portal - Setup & Start" -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host ""

INFO "Sprawdzam Python..."
$pythonCmd = $null
foreach ($cmd in @("python", "python3", "py")) {
    try {
        $ver = & $cmd --version 2>&1
        if ($ver -match "Python (\d+)\.(\d+)") {
            $major = [int]$Matches[1]
            $minor = [int]$Matches[2]
            if ($major -ge 3 -and $minor -ge 8) {
                $pythonCmd = $cmd
                OK "Python $major.$minor ($cmd)"
                break
            }
        }
    } catch {}
}
if (-not $pythonCmd) { FAIL "Python 3.8+ nie znaleziony." }

INFO "Sprawdzam pip..."
$pipOk = $false
try {
    & $pythonCmd -m pip --version | Out-Null
    $pipOk = $true
} catch {}
if (-not $pipOk) { FAIL "pip nie znaleziony. Uruchom: $pythonCmd -m ensurepip" }
OK "pip OK"

INFO "Instaluje/aktualizuje mkdocs i pluginy..."
$packages = @(
    "mkdocs>=1.6",
    "mkdocs-material>=9.5",
    "mkdocs-awesome-pages-plugin>=2.9",
    "mkdocs-kroki-plugin>=0.8",
    "Pygments>=2.18"
)
foreach ($pkg in $packages) {
    INFO "  $pkg"
    & $pythonCmd -m pip install "$pkg" --quiet --upgrade 2>&1 | Out-Null
}
OK "Pakiety zainstalowane"

INFO "Szukam mkdocs..."
$mkdocs = $null
$scriptPath = & $pythonCmd -c "import sysconfig; print(sysconfig.get_path('scripts'))" 2>$null
$searchPatterns = @(
    $scriptPath,
    "$env:APPDATA\Python\Python3*\Scripts",
    "$env:LOCALAPPDATA\Programs\Python\Python3*\Scripts",
    "$env:USERPROFILE\AppData\Roaming\Python\Python3*\Scripts",
    "C:\Python3*\Scripts"
)
$searchPaths = $searchPatterns |
    Where-Object { $_ } |
    ForEach-Object { Resolve-Path $_ -ErrorAction SilentlyContinue } |
    Select-Object -ExpandProperty Path -ErrorAction SilentlyContinue

foreach ($dir in $searchPaths) {
    $candidate = Join-Path $dir "mkdocs.exe"
    if (Test-Path -LiteralPath $candidate) {
        $mkdocs = $candidate
        break
    }
}
if (-not $mkdocs) {
    $found = Get-Command mkdocs -ErrorAction SilentlyContinue
    if ($found) { $mkdocs = $found.Source }
}
if (-not $mkdocs) { FAIL "mkdocs nie znaleziony nawet po instalacji." }
OK "mkdocs: $mkdocs"

INFO "Ustalam sciezki dokumentacji..."
$docAICandidates = @(
    (Join-Path $REPO_ROOT "InvoiceJet\doc_AI"),
    (Join-Path $REPO_ROOT "doc_AI"),
    (Join-Path $REPO_ROOT "InvoiceJet\InvoiceJet\doc_AI")
)
$docAI = $docAICandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $docAI) { FAIL "Nie moge znalezc folderu doc_AI." }

$docUser = $docAI -replace "doc_AI$", "doc_user"
if (-not (Test-Path -LiteralPath $docUser)) { FAIL "Folder doc_user nie znaleziony obok doc_AI: $docUser" }

$aiDir = Join-Path $SCRIPT_DIR "doc-ai"
$userDir = Join-Path $SCRIPT_DIR "doc-user"
OK "doc_AI:   $docAI"
OK "doc_user: $docUser"

INFO "Finalizuje porty..."
$PortAI = Resolve-FreePort -RequestedPort $PortAI
if ($PortUser -eq $PortAI) {
    WARN "Port doc_user byl taki sam jak doc_AI. Probuje $($PortUser + 10)."
    $PortUser += 10
}
$PortUser = Resolve-FreePort -RequestedPort $PortUser
OK "Porty: doc_AI=$PortAI, doc_user=$PortUser"

$aiUrl = "http://${HostName}:$PortAI/"
$userUrl = "http://${HostName}:$PortUser/"

Update-OracleEnv -Path $oracleEnv -DocAIUrl $aiUrl -DocUserUrl $userUrl
OK "Zaktualizowano lokalny Oracle .env: $oracleEnv"

INFO "Generuje mkdocs.yml z lokalnymi sciezkami..."
$docAIYaml = ConvertTo-YamlPath -Path $docAI
$docUserYaml = ConvertTo-YamlPath -Path $docUser

$baseFeatures = @"
  features:
    - navigation.tabs
    - navigation.tabs.sticky
    - navigation.sections
    - navigation.expand
    - navigation.indexes
    - navigation.prune
    - navigation.top
    - navigation.footer
    - navigation.path
    - toc.follow
    - search.suggest
    - search.highlight
    - content.code.copy
"@

$aiYml = @"
site_name: "InvoiceJet - Dokumentacja Techniczna (AOS)"
site_description: "Agent-Oriented Specification - pelna dokumentacja techniczna"
site_url: "$aiUrl"
docs_dir: '$docAIYaml'
site_dir: "_site"
use_directory_urls: false

theme:
  name: material
  language: pl
  custom_dir: overrides
  palette:
    - scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Tryb ciemny
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Tryb jasny
  font:
    text: Inter
    code: Roboto Mono
$baseFeatures
    - content.code.annotate
    - content.tabs.link

edit_uri: ""

plugins:
  - search:
      lang: pl
      separator: '[\s\-\.]+'
  - awesome-pages
  - kroki:
      server_url: https://kroki.io
      enable_mermaid: false
      enable_block_diag: false
      enable_bpmn: false
      enable_excalidraw: false
      fence_prefix: ""
      http_method: POST
      tag_format: svg
      request_timeout: 30

markdown_extensions:
  - toc:
      permalink: true
      toc_depth: 4
  - admonition
  - pymdownx.details
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.inlinehilite
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.tasklist:
      custom_checkbox: true
  - tables
  - attr_list
  - md_in_html
  - def_list
  - footnotes
  - abbr
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg

extra:
  generator: false
  portal:
    doc_ai_url: "$aiUrl"
    doc_user_url: "$userUrl"

extra_javascript:
  - https://unpkg.com/mermaid@10/dist/mermaid.min.js
"@

$userYml = @"
site_name: "InvoiceJet - Dokumentacja Uzytkownika"
site_description: "Przewodnik uzytkownika aplikacji InvoiceJet"
site_url: "$userUrl"
docs_dir: '$docUserYaml'
site_dir: "_site"
use_directory_urls: false

theme:
  name: material
  language: pl
  custom_dir: overrides
  palette:
    - scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Tryb ciemny
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Tryb jasny
  font:
    text: Inter
    code: Roboto Mono
$baseFeatures

edit_uri: ""

plugins:
  - search:
      lang: pl
  - awesome-pages

markdown_extensions:
  - toc:
      permalink: true
      toc_depth: 3
  - admonition
  - pymdownx.details
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.tasklist:
      custom_checkbox: true
  - tables
  - attr_list
  - md_in_html
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg

extra:
  generator: false
  portal:
    doc_ai_url: "$aiUrl"
    doc_user_url: "$userUrl"

extra_javascript:
  - https://unpkg.com/mermaid@10/dist/mermaid.min.js
"@

$aiYml | Out-File (Join-Path $aiDir "mkdocs.yml") -Encoding utf8
$userYml | Out-File (Join-Path $userDir "mkdocs.yml") -Encoding utf8
OK "mkdocs.yml wygenerowane"

INFO "Uruchamiam serwery..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", `
  "Set-Location '$aiDir'; Write-Host 'doc_AI $aiUrl' -ForegroundColor Cyan; & '$mkdocs' serve --dev-addr=${HostName}:$PortAI"

Start-Sleep 3

Start-Process powershell -ArgumentList "-NoExit", "-Command", `
  "Set-Location '$userDir'; Write-Host 'doc_user $userUrl' -ForegroundColor Magenta; & '$mkdocs' serve --dev-addr=${HostName}:$PortUser"

INFO "Czekam az serwery wystartuja (~20s dla duzego doc_AI)..."
Start-Sleep 20

$r1 = try { (Invoke-WebRequest $aiUrl -TimeoutSec 10 -UseBasicParsing).StatusCode } catch { 0 }
$r2 = try { (Invoke-WebRequest $userUrl -TimeoutSec 5 -UseBasicParsing).StatusCode } catch { 0 }

Write-Host ""
Write-Host "=======================================================" -ForegroundColor Cyan
if ($r1 -eq 200) { OK "doc_AI   -> $aiUrl" } else { WARN "doc_AI   -> TIMEOUT (moze jeszcze startuje)" }
if ($r2 -eq 200) { OK "doc_user -> $userUrl" } else { WARN "doc_user -> TIMEOUT" }
Write-Host ""
Write-Host "  Edycja: zmien plik .md -> przegladarka auto-odswiezy" -ForegroundColor Gray
Write-Host "  Stop:   zamknij okna PowerShell albo uruchom stop-docs.ps1" -ForegroundColor Gray
Write-Host "=======================================================" -ForegroundColor Cyan

Start-Process $aiUrl
Start-Sleep 1
Start-Process $userUrl
