param(
    [Parameter(Mandatory=$true)]
    [string]$Question,
    [string]$Scope = "full"
)

. "$PSScriptRoot\invoke-env.ps1"

$python = Get-OraclePython
& $python -m oracle_invoicejet.cli_query --scope $Scope $Question

