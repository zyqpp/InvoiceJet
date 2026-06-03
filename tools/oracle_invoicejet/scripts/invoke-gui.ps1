param(
    [int]$Port = 8502
)

. "$PSScriptRoot\invoke-env.ps1"

$python = Get-OraclePython
& $python -m oracle_invoicejet.cli_serve --port $Port

