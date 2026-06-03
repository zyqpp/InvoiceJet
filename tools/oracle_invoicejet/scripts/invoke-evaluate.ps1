param(
    [ValidateSet("retrieval", "answer")]
    [string]$Mode = "retrieval",
    [int]$Limit = 0,
    [switch]$Json
)

. "$PSScriptRoot\invoke-env.ps1"

$python = Get-OraclePython
$argsList = @("-m", "oracle_invoicejet.cli_evaluate", "--mode", $Mode)
if ($Limit -gt 0) {
    $argsList += @("--limit", [string]$Limit)
}
if ($Json) {
    $argsList += "--json"
}
& $python @argsList
