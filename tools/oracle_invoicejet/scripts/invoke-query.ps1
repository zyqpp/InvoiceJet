param(
    [Parameter(Mandatory=$true)]
    [string]$Question,
    [string]$Scope = "full",
    [string]$RagProfile = "",
    [string]$PromptProfile = ""
)

. "$PSScriptRoot\invoke-env.ps1"

$python = Get-OraclePython
$argsList = @("-m", "oracle_invoicejet.cli_query", "--scope", $Scope)
if ($RagProfile) {
    $argsList += @("--rag-profile", $RagProfile)
}
if ($PromptProfile) {
    $argsList += @("--prompt-profile", $PromptProfile)
}
$argsList += $Question
& $python @argsList
