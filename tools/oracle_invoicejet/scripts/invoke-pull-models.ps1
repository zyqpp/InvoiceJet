param(
    [string[]]$Models = @()
)

. "$PSScriptRoot\invoke-env.ps1"

$python = Get-OraclePython
if ($Models.Count -gt 0) {
    & $python -m oracle_invoicejet.cli_pull_models @Models
} else {
    & $python -m oracle_invoicejet.cli_pull_models
}

