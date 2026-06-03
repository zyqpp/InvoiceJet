param(
    [switch]$ForceRebuild
)

. "$PSScriptRoot\invoke-env.ps1"

$python = Get-OraclePython
if ($ForceRebuild) {
    & $python -m oracle_invoicejet.cli_ingest --force-rebuild
} else {
    & $python -m oracle_invoicejet.cli_ingest
}
