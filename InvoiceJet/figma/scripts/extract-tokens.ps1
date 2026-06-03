<#
.SYNOPSIS
  Skanuje pliki SCSS frontu InvoiceJet i wypisuje inwentarz kolorów (hex) z częstotliwością
  oraz lokalizacjami. Służy do utrzymania figma/design-tokens.* w zgodzie z kodem.

.OPIS
  To NIE nadpisuje tokenów automatycznie — wypisuje raport, który porównujesz ręcznie
  z design-tokens.md. Świadomie, by uniknąć cichych rozjazdów 1:1.

.PRZYKŁAD
  ./extract-tokens.ps1
  ./extract-tokens.ps1 -SrcDir "..\..\InvoiceJetUI\src" -Csv kolory.csv
#>

[CmdletBinding()]
param(
  # Katalog źródłowy frontu (domyślnie: InvoiceJetUI/src względem tego skryptu)
  [string]$SrcDir = (Join-Path $PSScriptRoot "..\..\InvoiceJetUI\src"),
  # Opcjonalna ścieżka do zapisu raportu CSV
  [string]$Csv
)

if (-not (Test-Path $SrcDir)) {
  Write-Error "Nie znaleziono katalogu źródłowego: $SrcDir"
  exit 1
}

Write-Host "Skanuję SCSS w: $SrcDir" -ForegroundColor Cyan

$hexRegex = '#[0-9a-fA-F]{3,8}\b'
$files = Get-ChildItem -Path $SrcDir -Recurse -Filter *.scss -File

$hits = foreach ($f in $files) {
  $lineNo = 0
  foreach ($line in Get-Content -LiteralPath $f.FullName) {
    $lineNo++
    foreach ($m in [regex]::Matches($line, $hexRegex)) {
      [pscustomobject]@{
        Hex   = $m.Value.ToLower()
        File  = $f.FullName.Replace($SrcDir, '').TrimStart('\','/')
        Line  = $lineNo
      }
    }
  }
}

if (-not $hits) {
  Write-Host "Nie znaleziono kolorów hex." -ForegroundColor Yellow
  exit 0
}

Write-Host "`n=== Inwentarz kolorów (wg częstotliwości) ===" -ForegroundColor Green
$summary = $hits | Group-Object Hex | Sort-Object Count -Descending | ForEach-Object {
  [pscustomobject]@{
    Hex       = $_.Name
    Wystapien = $_.Count
    Pliki     = ($_.Group | Select-Object -ExpandProperty File -Unique) -join '; '
  }
}
$summary | Format-Table -AutoSize -Wrap

Write-Host "Unikalnych kolorow: $($summary.Count) | Wszystkich trafien: $($hits.Count)" -ForegroundColor Cyan

if ($Csv) {
  $hits | Export-Csv -Path $Csv -NoTypeInformation -Encoding UTF8
  Write-Host "Zapisano szczegolowy raport: $Csv" -ForegroundColor Green
}

Write-Host "`nPorownaj wynik z figma/design-tokens.md i zaktualizuj recznie, jesli sa nowe kolory." -ForegroundColor DarkYellow
