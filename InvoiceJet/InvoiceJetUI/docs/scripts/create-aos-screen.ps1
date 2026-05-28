#!/usr/bin/env pwsh
<#
.SYNOPSIS
Tworzy strukturę katalogów i szablony dla nowego ekranu AOS

.DESCRIPTION
Skrypt tworzy katalog E-[XX]_[nazwa] w docs/aos/frontend/ i populuje go
szablonowymi plikami Markdown (00_METADANE, 01_PRZEGLĄD, itp.)

.PARAMETER ScreenNumber
Numer ekranu (będzie sformatowany na 2 cyfry: 01, 02, itd.)

.PARAMETER ScreenName
Nazwa ekranu (będzie używana w nazwie katalogu, np. Clients → E-01_Clients)

.PARAMETER TemplateDir
Katalog zawierający szablony (domyślnie: docs/aos/templates)

.PARAMETER OutputDir
Katalog docelowy (domyślnie: docs/aos/frontend)

.EXAMPLE
.\create-aos-screen.ps1 -ScreenNumber 1 -ScreenName "Clients"
# Tworzy: docs/aos/frontend/E-01_Clients/

.EXAMPLE
.\create-aos-screen.ps1 -ScreenNumber 5 -ScreenName "InvoiceDetails" -OutputDir ".\output"
# Tworzy: .\output\E-05_InvoiceDetails/

.NOTES
Wymaga: PowerShell 5.0+
#>

param(
    [Parameter(Mandatory = $true)]
    [ValidateRange(1, 999)]
    [int]$ScreenNumber,

    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[A-Za-z0-9_-]+$')]
    [string]$ScreenName,

    [string]$TemplateDir = "docs/aos/templates",

    [string]$OutputDir = "docs/aos/frontend"
)

# ============= KONFIGURACJA =============

$ScreenId = $ScreenNumber.ToString("00")
$ScreenFolder = "E-${ScreenId}_${ScreenName}"
$ScreenPath = Join-Path $OutputDir $ScreenFolder
$DateNow = (Get-Date).ToString("yyyy-MM-dd")

# ============= WALIDACJA =============

if (-not (Test-Path $TemplateDir)) {
    Write-Error "❌ Katalog szablonów nie istnieje: $TemplateDir"
    exit 1
}

if (Test-Path $ScreenPath) {
    Write-Error "❌ Katalog już istnieje: $ScreenPath"
    exit 1
}

# ============= TWORZENIE STRUKTURY =============

Write-Host "📁 Tworzenie struktury katalogów..." -ForegroundColor Cyan

New-Item -ItemType Directory -Force -Path $ScreenPath | Out-Null
if (-not $?) {
    Write-Error "❌ Nie udało się utworzyć katalogu: $ScreenPath"
    exit 1
}

# ============= KOPIOWANIE I PERSONALIZACJA SZABLONÓW =============

Write-Host "📄 Generowanie plików szablonowych..." -ForegroundColor Cyan

$templates = @(
    "TEMPLATE_00_METADANE.md",
    "TEMPLATE_01_PRZEGLĄD.md",
    "TEMPLATE_02_DANE_I_OPERACJE.md",
    "TEMPLATE_03_LOGIKA_BIZNESOWA.md",
    "TEMPLATE_04_SCENARIUSZE_TESTOWE.md"
)

$targetNames = @(
    "00_METADANE.md",
    "01_PRZEGLĄD.md",
    "02_DANE_I_OPERACJE.md",
    "03_LOGIKA_BIZNESOWA.md",
    "04_SCENARIUSZE_TESTOWE.md"
)

for ($i = 0; $i -lt $templates.Count; $i++) {
    $templateFile = Join-Path $TemplateDir $templates[$i]
    $targetFile = Join-Path $ScreenPath $targetNames[$i]

    if (-not (Test-Path $templateFile)) {
        Write-Warning "⚠️  Szablon nie znaleziony: $templateFile (pomijam)"
        continue
    }

    # Przeczytaj szablon
    $content = Get-Content $templateFile -Raw -Encoding UTF8

    # Zamień placeholders
    $content = $content -replace '\[NAZWA_EKRANU\]', $ScreenName
    $content = $content -replace '\[YYYY-MM-DD\]', $DateNow
    $content = $content -replace '\[XX\]', $ScreenId

    # Zapisz personalizowany plik
    Set-Content -Path $targetFile -Value $content -Encoding UTF8 -Force

    Write-Host "  ✅ $targetNames[$i]"
}

# ============= TWORZENIE HISTORY =============

Write-Host "📄 Generowanie pliku historii zmian..." -ForegroundColor Cyan

$historyContent = @"
# Historia zmian dokumentu

| Wersja | Data | Autor | Opis zmian |
|---|---|---|---|
| 1.0 | $DateNow | Agent AI | Dokument inicjalny — wygenerowany automatycznie. |
"@

$historyFile = Join-Path $ScreenPath "HISTORIA_ZMIAN.md"
Set-Content -Path $historyFile -Value $historyContent -Encoding UTF8 -Force
Write-Host "  ✅ HISTORIA_ZMIAN.md"

# ============= KOMUNIKAT PODSUMOWANIA =============

Write-Host ""
Write-Host "✅ Struktura ekranu '$ScreenName' utworzona pomyślnie!" -ForegroundColor Green
Write-Host ""
Write-Host "📂 Katalog: $ScreenPath"
Write-Host "📋 Pliki:"
Write-Host "   • 00_METADANE.md — metadane i szybkie odniesienia"
Write-Host "   • 01_PRZEGLĄD.md — layout i przegląd funkcjonalności"
Write-Host "   • 02_DANE_I_OPERACJE.md — pola formularza i operacje"
Write-Host "   • 03_LOGIKA_BIZNESOWA.md — przepływy i integracje"
Write-Host "   • 04_SCENARIUSZE_TESTOWE.md — scenariusze dla QA"
Write-Host "   • HISTORIA_ZMIAN.md — wersjonowanie"
Write-Host ""
Write-Host "⚡ Następny krok: Otworzyć 00_METADANE.md i uzupełnić dane ekranu"
Write-Host ""

exit 0
