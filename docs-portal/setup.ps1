#!/usr/bin/env pwsh
<#
.SYNOPSIS
    InvoiceJet Docs Portal — jednorazowy setup + start na nowym komputerze.

.DESCRIPTION
    Skrypt:
    1. Sprawdza Python 3.8+
    2. Instaluje mkdocs + mkdocs-material + pluginy
    3. Generuje mkdocs.yml z poprawnymi ścieżkami dla tego komputera
    4. Uruchamia oba serwery MkDocs
    5. Otwiera przeglądarke

.PARAMETER PortAI
    Port dla dokumentacji technicznej (doc_AI). Domyślnie: 8201

.PARAMETER PortUser
    Port dla dokumentacji użytkownika (doc_user). Domyślnie: 8301

.EXAMPLE
    # Domyślne porty 8201 i 8301
    .\setup.ps1

    # Własne porty
    .\setup.ps1 -PortAI 9001 -PortUser 9002

.NOTES
    Wymagania: Python 3.8+, pip, dostęp do internetu (instalacja pakietów)
    Repo: https://github.com/zyqpp/InvoiceJet
#>

param(
    [int]$PortAI   = 8201,
    [int]$PortUser = 8301
)

$ErrorActionPreference = "Stop"

# ── Kolory ──────────────────────────────────────────────────
function OK   { Write-Host "  ✅ $args" -ForegroundColor Green   }
function INFO { Write-Host "  ℹ️  $args" -ForegroundColor Cyan    }
function WARN { Write-Host "  ⚠️  $args" -ForegroundColor Yellow  }
function FAIL { Write-Host "  ❌ $args" -ForegroundColor Red; exit 1 }

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  InvoiceJet Docs Portal — Setup & Start"               -ForegroundColor Cyan
Write-Host "  doc_AI   → http://127.0.0.1:$PortAI"                  -ForegroundColor Yellow
Write-Host "  doc_user → http://127.0.0.1:$PortUser"                -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# ── 1. SPRAWDŹ PYTHON ────────────────────────────────────────
INFO "Sprawdzam Python..."
$pythonCmd = $null
foreach ($cmd in @("python", "python3", "py")) {
    try {
        $ver = & $cmd --version 2>&1
        if ($ver -match "Python (\d+)\.(\d+)") {
            $major = [int]$Matches[1]; $minor = [int]$Matches[2]
            if ($major -ge 3 -and $minor -ge 8) {
                $pythonCmd = $cmd
                OK "Python $major.$minor ($cmd)"
                break
            }
        }
    } catch {}
}
if (-not $pythonCmd) { FAIL "Python 3.8+ nie znaleziony. Zainstaluj: https://www.python.org" }

# ── 2. ZNAJDŹ pip ────────────────────────────────────────────
INFO "Sprawdzam pip..."
$pipOk = $false
try { & $pythonCmd -m pip --version | Out-Null; $pipOk = $true } catch {}
if (-not $pipOk) { FAIL "pip nie znaleziony. Uruchom: $pythonCmd -m ensurepip" }
OK "pip OK"

# ── 3. INSTALUJ PAKIETY ──────────────────────────────────────
INFO "Instaluję/aktualizuję mkdocs i pluginy..."
$packages = @("mkdocs>=1.6", "mkdocs-material>=9.5", "mkdocs-awesome-pages-plugin>=2.9", "Pygments>=2.18")
foreach ($pkg in $packages) {
    INFO "  $pkg"
    & $pythonCmd -m pip install "$pkg" --quiet --upgrade 2>&1 | Out-Null
}
OK "Pakiety zainstalowane"

# ── 4. ZNAJDŹ mkdocs.exe ─────────────────────────────────────
INFO "Szukam mkdocs.exe..."
$mkdocs = $null
$searchPaths = @(
    (& $pythonCmd -c "import sysconfig; print(sysconfig.get_path('scripts'))" 2>$null),
    "$env:APPDATA\Python\Python3*\Scripts",
    "$env:LOCALAPPDATA\Programs\Python\Python3*\Scripts",
    "C:\Python3*\Scripts",
    "$env:USERPROFILE\AppData\Roaming\Python\Python3*\Scripts"
) | ForEach-Object { Resolve-Path $_ -ErrorAction SilentlyContinue } | Select-Object -ExpandProperty Path -ErrorAction SilentlyContinue

foreach ($dir in $searchPaths) {
    $candidate = Join-Path $dir "mkdocs.exe"
    if (Test-Path $candidate) { $mkdocs = $candidate; break }
}
# Fallback: sprawdź PATH
if (-not $mkdocs) {
    $found = Get-Command mkdocs -ErrorAction SilentlyContinue
    if ($found) { $mkdocs = $found.Source }
}
if (-not $mkdocs) { FAIL "mkdocs.exe nie znaleziony nawet po instalacji. Sprawdź PATH." }
OK "mkdocs: $mkdocs"

# ── 5. USTAL ŚCIEŻKI ─────────────────────────────────────────
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$REPO_ROOT  = Split-Path -Parent $SCRIPT_DIR   # jeden poziom wyżej — katalog projektu

# Szukamy doc_AI i doc_user
$candidates = @(
    "$REPO_ROOT\InvoiceJet\doc_AI",
    "$REPO_ROOT\doc_AI",
    (Join-Path $REPO_ROOT "InvoiceJet\InvoiceJet\doc_AI")
)
$docAI = $candidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $docAI) { FAIL "Nie mogę znaleźć folderu doc_AI. Upewnij się że repozytorium jest sklonowane poprawnie." }

$docUser = $docAI -replace "doc_AI$", "doc_user"
if (-not (Test-Path $docUser)) { FAIL "Folder doc_user nie znaleziony obok doc_AI: $docUser" }

OK "doc_AI:   $docAI"
OK "doc_user: $docUser"

# ── 6. GENERUJ mkdocs.yml ────────────────────────────────────
INFO "Generuję mkdocs.yml z lokalnymi ścieżkami..."

$aiDir   = "$SCRIPT_DIR\doc-ai"
$userDir = "$SCRIPT_DIR\doc-user"

# Escape backslashes for YAML
$docAIYaml   = $docAI   -replace "\\","\\\\"
$docUserYaml = $docUser -replace "\\","\\\\"
$aiUrl   = "http://127.0.0.1:$PortAI/"
$userUrl = "http://127.0.0.1:$PortUser/"

$baseFeatures = @"
  features:
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
    - content.action.edit
    - content.code.copy
    - content.code.annotate
"@

$baseExtensions = @"
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
"@

$aiYml = @"
site_name: "InvoiceJet — Dokumentacja Techniczna (AOS)"
site_url: "$aiUrl"
docs_dir: "$docAIYaml"
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
      toggle: {icon: material/brightness-7, name: Tryb ciemny}
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle: {icon: material/brightness-4, name: Tryb jasny}
  font: {text: Inter, code: Roboto Mono}
$baseFeatures

edit_uri: ""

plugins:
  - search: {lang: pl}
  - awesome-pages

$baseExtensions

extra: {generator: false}
extra_javascript:
  - https://unpkg.com/mermaid@10/dist/mermaid.min.js
"@

$userYml = @"
site_name: "InvoiceJet — Dokumentacja Użytkownika"
site_url: "$userUrl"
docs_dir: "$docUserYaml"
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
      toggle: {icon: material/brightness-7, name: Tryb ciemny}
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle: {icon: material/brightness-4, name: Tryb jasny}
  font: {text: Inter, code: Roboto Mono}
  features:
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
    - content.action.edit
    - content.code.copy

edit_uri: ""

plugins:
  - search: {lang: pl}
  - awesome-pages

markdown_extensions:
  - toc: {permalink: true, toc_depth: 3}
  - admonition
  - pymdownx.details
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.highlight: {anchor_linenums: true}
  - pymdownx.inlinehilite
  - pymdownx.tabbed: {alternate_style: true}
  - pymdownx.tasklist: {custom_checkbox: true}
  - tables
  - attr_list
  - md_in_html
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg

extra: {generator: false}
extra_javascript:
  - https://unpkg.com/mermaid@10/dist/mermaid.min.js
"@

# Zastąp linki do portali w overrides z poprawnymi portami
function UpdateOverride($dir, $portSelf, $portOther, $selfLabel, $otherLabel) {
    $ovPath = "$dir\overrides\main.html"
    if (Test-Path $ovPath) {
        $content = Get-Content $ovPath -Raw
        $content = $content -replace "http://127\.0\.0\.1:\d+/.*class=.current", "http://127.0.0.1:$portSelf/ class=`"current`""
        Set-Content $ovPath $content -Encoding utf8
    }
}

$aiYml   | Out-File "$aiDir\mkdocs.yml"   -Encoding utf8
$userYml | Out-File "$userDir\mkdocs.yml" -Encoding utf8
OK "mkdocs.yml wygenerowane"

# ── 7. SPRAWDŹ PORTY ─────────────────────────────────────────
INFO "Sprawdzam wolne porty $PortAI i $PortUser..."
foreach ($port in @($PortAI, $PortUser)) {
    $used = netstat -ano 2>$null | Select-String ":$port\s" | Select-String "LISTENING"
    if ($used) {
        WARN "Port $port zajęty! Używam portu $($port+10) zamiast..."
        if ($port -eq $PortAI)   { $PortAI   = $PortAI   + 10 }
        else                     { $PortUser = $PortUser + 10 }
    }
}
OK "Porty: doc_AI=$PortAI, doc_user=$PortUser"

# ── 8. URUCHOM SERWERY ───────────────────────────────────────
INFO "Uruchamiam serwery..."

Start-Process powershell -ArgumentList "-NoExit","-Command", `
  "Set-Location '$aiDir'; Write-Host '📚 doc_AI http://127.0.0.1:$PortAI' -ForegroundColor Cyan; & '$mkdocs' serve --dev-addr=127.0.0.1:$PortAI"

Start-Sleep 3

Start-Process powershell -ArgumentList "-NoExit","-Command", `
  "Set-Location '$userDir'; Write-Host '👤 doc_user http://127.0.0.1:$PortUser' -ForegroundColor Magenta; & '$mkdocs' serve --dev-addr=127.0.0.1:$PortUser"

INFO "Czekam aż serwery wystartują (~20s dla dużego doc_AI)..."
Start-Sleep 20

# ── 9. WERYFIKACJA ───────────────────────────────────────────
$r1 = try { (Invoke-WebRequest "http://127.0.0.1:$PortAI"   -TimeoutSec 10 -UseBasicParsing).StatusCode } catch { 0 }
$r2 = try { (Invoke-WebRequest "http://127.0.0.1:$PortUser" -TimeoutSec 5  -UseBasicParsing).StatusCode } catch { 0 }

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
if ($r1 -eq 200) { OK "doc_AI   → http://127.0.0.1:$PortAI" } else { WARN "doc_AI   → TIMEOUT (może jeszcze startuje)" }
if ($r2 -eq 200) { OK "doc_user → http://127.0.0.1:$PortUser" } else { WARN "doc_user → TIMEOUT" }
Write-Host ""
Write-Host "  Edycja: zmień plik .md → przeglądarka auto-odświeży" -ForegroundColor Gray
Write-Host "  Stop:   zamknij okna PowerShell" -ForegroundColor Gray
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan

Start-Process "http://127.0.0.1:$PortAI"
Start-Sleep 1
Start-Process "http://127.0.0.1:$PortUser"
