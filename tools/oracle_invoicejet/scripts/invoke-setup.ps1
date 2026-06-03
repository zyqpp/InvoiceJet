. "$PSScriptRoot\invoke-env.ps1"

$ErrorActionPreference = "Stop"

function Invoke-OracleStep {
    param(
        [Parameter(Mandatory = $true)]
        [string[]] $Command
    )

    & $Command[0] @($Command[1..($Command.Length - 1)])
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code ${LASTEXITCODE}: $($Command -join ' ')"
    }
}

$python = Get-OraclePython
if ($python -eq "python") {
    python -m venv (Join-Path $Script:OracleToolRoot ".venv")
    $python = Get-OraclePython
}

Invoke-OracleStep @($python, "-m", "pip", "install", "--disable-pip-version-check", "--upgrade", "pip", "setuptools", "wheel")
Invoke-OracleStep @($python, "-m", "pip", "install", "--disable-pip-version-check", "-e", $Script:OracleToolRoot)

if (-not (Test-Path (Join-Path $Script:OracleToolRoot ".env"))) {
    Copy-Item (Join-Path $Script:OracleToolRoot ".env.example") (Join-Path $Script:OracleToolRoot ".env")
}

Write-Host "Oracle InvoiceJet setup complete."
