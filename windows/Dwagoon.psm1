Import-Module $PSScriptRoot\winwal\winwal.psm1

$WALLPAPER_FOLDER = "$HOME\Downloads\reddit"

function wal {
  [CmdletBinding(DefaultParameterSetName = "Run")]
  param (
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
  )
  $exe = Get-Command wal -CommandType Application
  & $exe.Path '--cols16' @Args
}

function SetWallpaper() {
  param(
    [Parameter(Mandatory = $true)][string]$Image
  )
  python -c "import pywal; pywal.wallpaper.change(r'$Image')"
}

function RandomWallpaper() {
  $file = Get-ChildItem -Path $WALLPAPER_FOLDER -File | Get-Random
  SetWallpaper -Image $file.FullName
}

function Rice() {
  RandomWallpaper
  Update-WalTheme -Backend colorz
}
