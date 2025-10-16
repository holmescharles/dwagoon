# Use the folder where this script is located
$moduleFolder = $PSScriptRoot
$moduleFile = Join-Path $moduleFolder "Dwagoon.psm1"

# Remove deny rule from folder
$folderAcl = Get-Acl $moduleFolder
$denyRule = New-Object System.Security.AccessControl.FileSystemAccessRule("Everyone","DeleteSubdirectoriesAndFiles","ContainerInherit,ObjectInherit","None","Deny")
$folderAcl.RemoveAccessRule($denyRule)

# Add allow rule to folder
$allowFolderRule = New-Object System.Security.AccessControl.FileSystemAccessRule("Users","ReadAndExecute","ContainerInherit,ObjectInherit","None","Allow")
$folderAcl.AddAccessRule($allowFolderRule)
Set-Acl $moduleFolder $folderAcl

# Add allow rule to module file
$fileAcl = Get-Acl $moduleFile
$allowFileRule = New-Object System.Security.AccessControl.FileSystemAccessRule("Users","ReadAndExecute","Allow")
$fileAcl.SetAccessRule($allowFileRule)
Set-Acl $moduleFile $fileAcl

# Unblock the module file
Unblock-File -Path $moduleFile

# Optional: Add import to global profile (requires admin)
$profilePath = "$env:windir\System32\WindowsPowerShell\v1.0\profile.ps1"
if (-not (Test-Path $profilePath)) {
    New-Item -Path $profilePath -ItemType File -Force
    }
    Add-Content -Path $profilePath -Value "`nImport-Module '$moduleFile'"
