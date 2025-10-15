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
    # Path to image to set as background, if not set current wallpaper is used
    [Parameter(Mandatory = $true)][string]$Image
  )

  # Trigger update of wallpaper
  # modified from https://www.joseespitia.com/2017/09/15/set-wallpaper-powershell-function/
  Add-Type -TypeDefinition @"
  using System;
  using System.Runtime.InteropServices;

  public class PInvoke
  {
    [DllImport("User32.dll",CharSet=CharSet.Unicode)] 
    public static extern int SystemParametersInfo(UInt32 action, UInt32 iParam, String sParam, UInt32 winIniFlags);
  }
"@

  # Setting the wallpaper requires an absolute path, so pass image into resolve-path
  [PInvoke]::SystemParametersInfo(0x0014, 0, $($Image | Resolve-Path), 0x0003) | out-null
}

function RandomWallpaper() {
  $file = Get-ChildItem -Path $WALLPAPER_FOLDER -File | Get-Random
  SetWallpaper -Image $file.FullName
}

function Rice() {
  RandomWallpaper
  Update-WalTheme -Backend colorz
}
