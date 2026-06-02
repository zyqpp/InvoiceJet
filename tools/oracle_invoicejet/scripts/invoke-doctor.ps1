param(
    [switch]$TestEmbedding
)

. "$PSScriptRoot\invoke-env.ps1"

$python = Get-OraclePython
if ($TestEmbedding) {
    & $python -m oracle_invoicejet.cli_doctor --test-embedding
} else {
    & $python -m oracle_invoicejet.cli_doctor
}
