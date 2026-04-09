param(
    [string]$TargetRoot = "$HOME\.claude\skills"
)

$source = Join-Path $PSScriptRoot "..\anti-distill"
$source = (Resolve-Path $source).Path
$target = Join-Path $TargetRoot "anti-distill"

New-Item -ItemType Directory -Force $TargetRoot | Out-Null
if (Test-Path $target) {
    Remove-Item -LiteralPath $target -Recurse -Force
}

Copy-Item -LiteralPath $source -Destination $target -Recurse -Force
Write-Host "Installed anti-distill to $target"
