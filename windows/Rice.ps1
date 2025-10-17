
param(
    [string]$WallpaperFolder = "$env:USERPROFILE\Downloads\Wallpapers",
    [string[]]$ExtraArgs = @()
)

$walArgs = @('-i', $WallpaperFolder, '--cols16', '--backend', 'colorz') + $ExtraArgs
& wal @walArgs

if ($LASTEXITCODE -eq 0) {
    & "$PSScriptRoot\UpdateTerminal.ps1"
}