# Update-TerminalWithCols16.ps1
# Injects pywal16's colors.json into Windows Terminal as "cols16" theme
$colorsPath = "$HOME/.cache/wal/colors.json"
if (!(Test-Path -Path $colorsPath)) {
  Write-Host "colors.json not found. Run pywal16 first." -ForegroundColor Yellow
  return
}
$wal = Get-Content $colorsPath -Raw | ConvertFrom-Json

$theme = [PSCustomObject]@{
  name         = "cols16"
  foreground   = $wal.special.foreground
  background   = $wal.special.background
  cursorColor  = $wal.special.cursor
  black        = $wal.colors.color0
  red          = $wal.colors.color1
  green        = $wal.colors.color2
  yellow       = $wal.colors.color3
  blue         = $wal.colors.color4
  purple       = $wal.colors.color5
  cyan         = $wal.colors.color6
  white        = $wal.colors.color7
  brightBlack  = $wal.colors.color8
  brightRed    = $wal.colors.color9
  brightGreen  = $wal.colors.color10
  brightYellow = $wal.colors.color11
  brightBlue   = $wal.colors.color12
  brightPurple = $wal.colors.color13
  brightCyan   = $wal.colors.color14
  brightWhite  = $wal.colors.color15
}

$terminalPaths = @(
  "$HOME/AppData/Local/Packages/Microsoft.WindowsTerminal_8wekyb3d8bbwe/LocalState/settings.json",
  "$HOME/AppData/Local/Packages/Microsoft.WindowsTerminalPreview_8wekyb3d8bbwe/LocalState/settings.json"
)

foreach ($path in $terminalPaths) {
  if (!(Test-Path $path)) { continue }
  
  $config = Get-Content $path -Raw | ConvertFrom-Json
  
  # Remove old cols16 and add new one
  $config.schemes = @($config.schemes | Where-Object { $_.name -ne "cols16" }) + $theme
  
  # Set as default color scheme
  if (-not $config.profiles.defaults) {
    $config.profiles.defaults = [PSCustomObject]@{}
  }
  $config.profiles.defaults.colorScheme = "cols16"
  
  $config | ConvertTo-Json -Depth 32 | Set-Content $path
  Write-Host "Updated: $path" -ForegroundColor Green
}