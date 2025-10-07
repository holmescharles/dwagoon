# For Auto Dark Mode to run
Import-Module $PSScriptRoot\winwal\winwal.psm1
Start-Sleep -Seconds 1  # otherwise it updates before the mode can be switched
Update-WalTheme -Backend colorz
