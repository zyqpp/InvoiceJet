#!/usr/bin/env pwsh
# start-docs.ps1 - uruchamia oba portale MkDocs InvoiceJet.
#
# UWAGA: live-reload dziala tylko dla doc_AI/ i doc_user/ (pliki .md).
# Zmiany w overrides/ wymagaja restartu tego skryptu.

param(
  [Alias("Host")]
  [string]$HostName = "127.0.0.1",
  [int]$PortAI = 8001,
  [int]$PortUser = 8002,
  [int]$EditorPort = 8010,
  [switch]$NoEditor,
  [switch]$EnableKroki,
  [string]$Editor = "",
  [string]$OracleEnvPath
)

$ErrorActionPreference = "Stop"

$ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
$AI_DIR = Join-Path $ROOT "doc-ai"
$USER_DIR = Join-Path $ROOT "doc-user"
$EDITOR_SCRIPT = Join-Path $ROOT "start-editor.ps1"

$MKDOCS = "C:\Users\kamil\AppData\Roaming\Python\Python314\Scripts\mkdocs.exe"
if (-not (Test-Path -LiteralPath $MKDOCS)) {
  $mkdocsCmd = Get-Command mkdocs -ErrorAction SilentlyContinue
  if ($mkdocsCmd) {
    $MKDOCS = $mkdocsCmd.Source
  }
}

if (-not (Test-Path -LiteralPath $MKDOCS)) {
  Write-Host "Nie znaleziono mkdocs. Uruchom setup.ps1 albo dodaj mkdocs do PATH." -ForegroundColor Red
  exit 1
}

function Get-DefaultOracleEnvPath {
  $repoRoot = Split-Path -Parent $ROOT
  return Join-Path $repoRoot "tools\oracle_invoicejet\.env"
}

function Write-Utf8NoBom {
  param(
    [Parameter(Mandatory = $true)][string]$Path,
    [Parameter(Mandatory = $true)]$Lines
  )

  $targetPath = if (Test-Path -LiteralPath $Path) {
    (Resolve-Path -LiteralPath $Path).Path
  } else {
    [System.IO.Path]::GetFullPath($Path)
  }
  $content = [string]::Join([Environment]::NewLine, [string[]]$Lines)
  if ($content.Length -gt 0) {
    $content += [Environment]::NewLine
  }
  [System.IO.File]::WriteAllText($targetPath, $content, [System.Text.UTF8Encoding]::new($false))
}

function Convert-ToPortalPath {
  param([Parameter(Mandatory = $true)][string]$Path)
  return ((Resolve-Path -LiteralPath $Path).Path -replace "\\", "/")
}

function Resolve-DocsSourcePath {
  param([Parameter(Mandatory = $true)][string]$FolderName)

  $repoRoot = Split-Path -Parent $ROOT
  $candidates = @(
    (Join-Path $repoRoot "InvoiceJet\$FolderName"),
    (Join-Path $repoRoot $FolderName),
    (Join-Path $repoRoot "InvoiceJet\InvoiceJet\$FolderName")
  )
  foreach ($candidate in $candidates) {
    if (Test-Path -LiteralPath $candidate) {
      return (Convert-ToPortalPath -Path $candidate)
    }
  }
  Write-Host "Nie znaleziono folderu $FolderName dla przycisku edycji." -ForegroundColor Yellow
  return ""
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
    foreach ($line in Get-Content -LiteralPath $Path -Encoding utf8) {
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

  Write-Utf8NoBom -Path $Path -Lines $lines
}

function Set-YamlValue {
  param(
    [Parameter(Mandatory = $true)]$Lines,
    [Parameter(Mandatory = $true)][string]$Pattern,
    [Parameter(Mandatory = $true)][string]$Value
  )

  for ($i = 0; $i -lt $Lines.Count; $i++) {
    if ($Lines[$i] -match $Pattern) {
      $Lines[$i] = $Value
      return $true
    }
  }
  return $false
}

function Update-MkDocsPortalConfig {
  param(
    [Parameter(Mandatory = $true)][string]$Path,
    [Parameter(Mandatory = $true)][string]$SiteUrl,
    [Parameter(Mandatory = $true)][string]$DocAIUrl,
    [Parameter(Mandatory = $true)][string]$DocUserUrl,
    [Parameter(Mandatory = $true)][string]$EditorUrl,
    [Parameter(Mandatory = $true)][string]$SourceDir
  )

  if (-not (Test-Path -LiteralPath $Path)) {
    Write-Host "Nie znaleziono mkdocs.yml: $Path" -ForegroundColor Red
    exit 1
  }

  $lines = [System.Collections.Generic.List[string]]::new()
  foreach ($line in Get-Content -LiteralPath $Path -Encoding utf8) {
    [void]$lines.Add($line)
  }
  [void](Set-YamlValue -Lines $lines -Pattern '^\s*site_url:\s*' -Value "site_url: `"$SiteUrl`"")
  $hasEditorUrl = Set-YamlValue -Lines $lines -Pattern '^\s*editor_url:\s*' -Value "  editor_url: `"$EditorUrl`""
  $hasSourceDir = Set-YamlValue -Lines $lines -Pattern '^\s*source_dir:\s*' -Value "  source_dir: `"$SourceDir`""
  $hasDocAIUrl = Set-YamlValue -Lines $lines -Pattern '^\s*doc_ai_url:\s*' -Value "    doc_ai_url: `"$DocAIUrl`""
  $hasDocUserUrl = Set-YamlValue -Lines $lines -Pattern '^\s*doc_user_url:\s*' -Value "    doc_user_url: `"$DocUserUrl`""

  if (-not ($hasEditorUrl -and $hasSourceDir)) {
    $extraIndexForEditor = -1
    for ($i = 0; $i -lt $lines.Count; $i++) {
      if ($lines[$i] -match '^extra:\s*$') {
        $extraIndexForEditor = $i
        break
      }
    }
    if ($extraIndexForEditor -ge 0) {
      $insertAt = $extraIndexForEditor + 1
      if (-not $hasSourceDir) {
        $lines.Insert($insertAt, "  source_dir: `"$SourceDir`"")
      }
      if (-not $hasEditorUrl) {
        $lines.Insert($insertAt, "  editor_url: `"$EditorUrl`"")
      }
    } else {
      $lines.Add("")
      $lines.Add("extra:")
      if (-not $hasEditorUrl) { $lines.Add("  editor_url: `"$EditorUrl`"") }
      if (-not $hasSourceDir) { $lines.Add("  source_dir: `"$SourceDir`"") }
    }
  }

  if (-not ($hasDocAIUrl -and $hasDocUserUrl)) {
    $extraIndex = -1
    for ($i = 0; $i -lt $lines.Count; $i++) {
      if ($lines[$i] -match '^extra:\s*$') {
        $extraIndex = $i
        break
      }
    }

    if ($extraIndex -ge 0) {
      $insertIndex = $extraIndex + 1
      while ($insertIndex -lt $lines.Count -and $lines[$insertIndex] -match '^\s{2,}\S') {
        $insertIndex++
      }
      $lines.Insert($insertIndex, "  portal:")
      $lines.Insert($insertIndex + 1, "    doc_ai_url: `"$DocAIUrl`"")
      $lines.Insert($insertIndex + 2, "    doc_user_url: `"$DocUserUrl`"")
    } else {
      $lines.Add("")
      $lines.Add("extra:")
      $lines.Add("  portal:")
      $lines.Add("    doc_ai_url: `"$DocAIUrl`"")
      $lines.Add("    doc_user_url: `"$DocUserUrl`"")
    }
  }

  Write-Utf8NoBom -Path $Path -Lines $lines
}

$oracleEnv = if ($OracleEnvPath) { $OracleEnvPath } else { Get-DefaultOracleEnvPath }
$docAIUrl = "http://${HostName}:$PortAI/"
$docUserUrl = "http://${HostName}:$PortUser/"
$editorUrl = "http://127.0.0.1:$EditorPort"
$docAISourceDir = Resolve-DocsSourcePath -FolderName "doc_AI"
$docUserSourceDir = Resolve-DocsSourcePath -FolderName "doc_user"
$krokiEnvCommand = if ($EnableKroki) {
  '$env:INVOICEJET_MKDOCS_KROKI="true"; '
} else {
  '$env:INVOICEJET_MKDOCS_KROKI="false"; '
}

Write-Host "================================================" -ForegroundColor Cyan
Write-Host " InvoiceJet Docs Portal" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

foreach ($port in @($PortAI, $PortUser)) {
  $used = netstat -ano | Select-String ":$port\s" | Select-String "LISTENING"
  if ($used) {
    Write-Host "Port $port zajety. Uruchom stop-docs.ps1 najpierw albo wybierz inny port." -ForegroundColor Red
    exit 1
  }
}

if (-not $NoEditor) {
  $editorUsed = netstat -ano | Select-String ":$EditorPort\s" | Select-String "LISTENING"
  if ($editorUsed) {
    Write-Host "Edytor MkDocs juz dziala na http://127.0.0.1:$EditorPort" -ForegroundColor Gray
  } else {
    if (-not (Test-Path -LiteralPath $EDITOR_SCRIPT)) {
      Write-Host "Nie znaleziono start-editor.ps1, pomijam edytor." -ForegroundColor Yellow
    } else {
      $editorArgs = @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "`"$EDITOR_SCRIPT`"", "-Port", "$EditorPort")
      if ($Editor) {
        $editorArgs += @("-Editor", "`"$Editor`"")
      }
      Start-Process powershell -WindowStyle Hidden -ArgumentList $editorArgs
      Write-Host "Uruchomiono edytor MkDocs: http://127.0.0.1:$EditorPort" -ForegroundColor Gray
    }
  }
}

Update-OracleEnv -Path $oracleEnv -DocAIUrl $docAIUrl -DocUserUrl $docUserUrl
Write-Host "Zaktualizowano lokalny Oracle .env: $oracleEnv" -ForegroundColor Gray

Update-MkDocsPortalConfig -Path (Join-Path $AI_DIR "mkdocs.yml") -SiteUrl $docAIUrl -DocAIUrl $docAIUrl -DocUserUrl $docUserUrl -EditorUrl $editorUrl -SourceDir $docAISourceDir
Update-MkDocsPortalConfig -Path (Join-Path $USER_DIR "mkdocs.yml") -SiteUrl $docUserUrl -DocAIUrl $docAIUrl -DocUserUrl $docUserUrl -EditorUrl $editorUrl -SourceDir $docUserSourceDir
Write-Host "Zaktualizowano mkdocs.yml dla portali." -ForegroundColor Gray

Write-Host ""
Write-Host "doc_AI   -> $docAIUrl" -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", `
  "$krokiEnvCommand Set-Location '$AI_DIR'; Write-Host 'doc_AI $docAIUrl' -ForegroundColor Cyan; & '$MKDOCS' serve --dev-addr=${HostName}:$PortAI"

Start-Sleep 3

Write-Host "doc_user -> $docUserUrl" -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", `
  "Set-Location '$USER_DIR'; Write-Host 'doc_user $docUserUrl' -ForegroundColor Magenta; & '$MKDOCS' serve --dev-addr=${HostName}:$PortUser"

Write-Host ""
Write-Host "Czekam az serwery wystartuja (~15s dla doc_AI)..." -ForegroundColor Yellow
Start-Sleep 15

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host " GOTOWE! Otworz w przegladarce:" -ForegroundColor Green
Write-Host ""
Write-Host "  Dokumentacja Techniczna : $docAIUrl" -ForegroundColor Yellow
Write-Host "  Dokumentacja Uzytkownika: $docUserUrl" -ForegroundColor Yellow
if (-not $NoEditor) {
  Write-Host "  Edytor dokumentow       : http://127.0.0.1:$EditorPort" -ForegroundColor Yellow
}
Write-Host ""
Write-Host "  Edycja: kliknij 'Edytuj' w portalu MkDocs." -ForegroundColor Gray
Write-Host "  Stop:   uruchom stop-docs.ps1" -ForegroundColor Gray
Write-Host "================================================" -ForegroundColor Green

Start-Process $docAIUrl
Start-Sleep 1
Start-Process $docUserUrl
