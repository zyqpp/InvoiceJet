#!/usr/bin/env pwsh
<#
.SYNOPSIS
Skanuje katalog dokumentacji AOS i generuje rejestr ekranów

.DESCRIPTION
Skrypt przeszukuje docs/aos/frontend/ i wczytuje metadane z każdego pliku
00_METADANE.md, tworząc tabelę ze statusami dokumentacji.

.PARAMETER AosDir
Katalog źródłowy dokumentacji AOS (domyślnie: docs/aos/frontend)

.PARAMETER OutputFile
Plik wyjściowy w Markdown (domyślnie: docs/REJESTR_EKRANÓW.md)

.PARAMETER ExportCsv
Jeśli True, eksportuje dodatkowo do CSV

.EXAMPLE
.\scan-aos-screens.ps1
# Skanuje docs/aos/frontend/, wyświetla na konsolę i tworzy rejestr

.EXAMPLE
.\scan-aos-screens.ps1 -OutputFile "./SCREENS.md" -ExportCsv $true
# Eksportuje do SCREENS.md i SCREENS.csv

.NOTES
Wymaga: PowerShell 5.0+
#>

param(
    [string]$AosDir = "docs/aos/frontend",
    [string]$OutputFile = "docs/REJESTR_EKRANÓW.md",
    [bool]$ExportCsv = $false
)

# ============= WALIDACJA =============

if (-not (Test-Path $AosDir)) {
    Write-Error "❌ Katalog nie istnieje: $AosDir"
    exit 1
}

# ============= SKANOWANIE =============

Write-Host "🔍 Skanowanie katalogu: $AosDir" -ForegroundColor Cyan
Write-Host ""

$screens = @()

$folders = Get-ChildItem -Path $AosDir -Directory -Filter "E-*" -ErrorAction SilentlyContinue

if ($folders.Count -eq 0) {
    Write-Warning "⚠️  Brak znalezionych ekranów (katalogów E-XX_*)"
    exit 0
}

foreach ($folder in $folders) {
    $metadataFile = Join-Path $folder.FullName "00_METADANE.md"

    if (-not (Test-Path $metadataFile)) {
        Write-Warning "⚠️  Brak pliku 00_METADANE.md w: $($folder.Name)"
        continue
    }

    Write-Host "  📂 Czytam: $($folder.Name)" -ForegroundColor Gray

    $content = Get-Content $metadataFile -Raw -Encoding UTF8

    # Ekstraktuj metadane za pomocą regex
    $screenName = if ($content -match '\| \*\*Nazwa biznesowa ekranu\*\* \| (.+?) \|') { $matches[1].Trim() } else { "N/D" }
    $screenUrl = if ($content -match '\| \*\*Ścieżka URL\*\* \| \`([^`]+)\` \|') { $matches[1].Trim() } else { "N/D" }
    $status = if ($content -match '\| \*\*Status\*\* \| \[?([^|\]]+)\]? \|') { $matches[1].Trim() } else { "Roboczy" }
    $version = if ($content -match '\| \*\*Wersja dokumentu\*\* \| ([^\|]+) \|') { $matches[1].Trim() } else { "1.0" }
    $lastUpdate = if ($content -match '\| \*\*Ostatnia aktualizacja\*\* \| ([^\|]+) \|') { $matches[1].Trim() } else { "N/D" }

    # Wyekstrahuj numer ekranu z nazwy katalogu
    if ($folder.Name -match '^E-(\d+)_(.+)$') {
        $screenId = $matches[1]
        $screenDirName = $matches[2]
    }
    else {
        $screenId = "?"
        $screenDirName = $folder.Name
    }

    $screens += [PSCustomObject]@{
        ID              = $screenId
        Name            = $screenName
        Directory       = $folder.Name
        URL             = $screenUrl
        Status          = $status
        Version         = $version
        LastUpdate      = $lastUpdate
        MetadataPath    = $metadataFile
        ScreenPath      = $folder.FullName
    }
}

# ============= SORTOWANIE =============

$screens = $screens | Sort-Object { [int]$_.ID }

# ============= WYŚWIETLENIE NA KONSOLI =============

Write-Host ""
Write-Host "📊 Znalezionych ekranów: $($screens.Count)" -ForegroundColor Green
Write-Host ""

$screens | Format-Table -AutoSize @(
    @{ Label = "ID"; Expression = { $_.ID }; Width = 3 },
    @{ Label = "Nazwa"; Expression = { $_.Name } },
    @{ Label = "URL"; Expression = { $_.URL } },
    @{ Label = "Status"; Expression = { $_.Status } },
    @{ Label = "Wersja"; Expression = { $_.Version } }
)

# ============= GENEROWANIE MARKDOWN REJESTRU =============

Write-Host "📝 Generowanie rejestru Markdown..." -ForegroundColor Cyan

$markdownContent = @"
# Rejestr Ekranów InvoiceJet

**Data wygenerowania**: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
**Łączna liczba ekranów**: $($screens.Count)

---

## Tabela ekranów

| ID | Nazwa | URL | Status | Wersja | Ostatnia aktualizacja |
|---|---|---|---|---|---|
"@

foreach ($screen in $screens) {
    $statusEmoji = switch ($screen.Status) {
        "Zatwierdzony" { "✅" }
        "Do zatwierdzenia" { "⏳" }
        "Do weryfikacji technicznej" { "🔍" }
        "Roboczy" { "📝" }
        "Wymaga aktualizacji" { "⚠️" }
        default { "❓" }
    }

    $markdownContent += "`n| $($screen.ID) | [$($screen.Name)]($($screen.ScreenPath)/01_PRZEGLĄD.md) | ``$($screen.URL)`` | $statusEmoji $($screen.Status) | $($screen.Version) | $($screen.LastUpdate) |"
}

$markdownContent += @"


---

## Statystyka

| Status | Liczba |
|---|---|
"@

$statusCounts = $screens | Group-Object -Property Status

foreach ($group in $statusCounts) {
    $markdownContent += "`n| $($group.Name) | $($group.Count) |"
}

$markdownContent += @"


---

## Katalog ekranów (hierarchia)

\`\`\`
docs/aos/frontend/
"@

foreach ($screen in $screens) {
    $markdownContent += "`n├── $($screen.Directory)"
    $markdownContent += "`n│   ├── 00_METADANE.md"
    $markdownContent += "`n│   ├── 01_PRZEGLĄD.md"
    $markdownContent += "`n│   ├── 02_DANE_I_OPERACJE.md"
    $markdownContent += "`n│   ├── 03_LOGIKA_BIZNESOWA.md"
    $markdownContent += "`n│   ├── 04_SCENARIUSZE_TESTOWE.md"
    $markdownContent += "`n│   └── HISTORIA_ZMIAN.md"
}

$markdownContent += @"

\`\`\`

---

## Legenda statusów

- **✅ Zatwierdzony** — Dokument produkcyjny, wdrożony
- **⏳ Do zatwierdzenia** — Weryfikacje skończone, czeka na sign-off
- **🔍 Do weryfikacji technicznej** — Weryfikacja analityczna ukończona
- **📝 Roboczy** — Wygenerowany, bez weryfikacji
- **⚠️ Wymaga aktualizacji** — Aplikacja się zmieniła, dokument nieaktualny

---

## Instrukcje

### Dla analityków
1. Otwórz katalog ekranu (np. \`E-01_Clients\`)
2. Zacznij od \`01_PRZEGLĄD.md\` — szybki overview
3. Czytaj \`02_DANE_I_OPERACJE.md\` dla szczegółów
4. Opisz znalezione problemy w \`03_LOGIKA_BIZNESOWA.md\`

### Dla developerów
1. Przeczytaj \`00_METADANE.md\` — szybkie odniesienia
2. Przeczytaj \`02_DANE_I_OPERACJE.md\` — pola i operacje
3. Przeczytaj \`03_LOGIKA_BIZNESOWA.md\` — logika biznesowa
4. Uzupełnij \`[WYMAGA WERYFIKACJI]\` po implementacji

### Dla testerów
1. Otwórz \`04_SCENARIUSZE_TESTOWE.md\` — kroki testowe
2. Użyj selektorów z tabeli "Tabela selektorów i lokalizatorów"
3. Testuj na różnych browserach i urządzeniach

---

## Generowanie

Ten rejestr został wygenerowany przez skrypt:
\`\`\`powershell
.\docs\scripts\scan-aos-screens.ps1
\`\`\`
"@

Set-Content -Path $OutputFile -Value $markdownContent -Encoding UTF8 -Force

Write-Host "  ✅ Rejestr zapisany: $OutputFile" -ForegroundColor Green

# ============= EXPORT CSV (OPCJONALNIE) =============

if ($ExportCsv) {
    Write-Host "📊 Eksportowanie do CSV..." -ForegroundColor Cyan

    $CsvFile = [System.IO.Path]::ChangeExtension($OutputFile, ".csv")

    $screens | Select-Object `
        @{ Name = "ID"; Expression = { $_.ID } },
    @{ Name = "Nazwa"; Expression = { $_.Name } },
    @{ Name = "URL"; Expression = { $_.URL } },
    @{ Name = "Status"; Expression = { $_.Status } },
    @{ Name = "Wersja"; Expression = { $_.Version } },
    @{ Name = "Ostatnia aktualizacja"; Expression = { $_.LastUpdate } } |
    Export-Csv -Path $CsvFile -NoTypeInformation -Encoding UTF8

    Write-Host "  ✅ CSV zapisany: $CsvFile" -ForegroundColor Green
}

Write-Host ""
Write-Host "✅ Skanowanie ukończone!" -ForegroundColor Green
Write-Host ""

exit 0
