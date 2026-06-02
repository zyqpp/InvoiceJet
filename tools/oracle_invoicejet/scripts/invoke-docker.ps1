param(
    [switch]$Build
)

. "$PSScriptRoot\invoke-env.ps1"

Push-Location $Script:OracleToolRoot
try {
    if ($Build) {
        docker compose up --build
    } else {
        docker compose up
    }
} finally {
    Pop-Location
}
