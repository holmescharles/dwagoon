# Set execution policy to allow script execution for all users
Try {
    Set-ExecutionPolicy RemoteSigned -Scope LocalMachine -Force
    Write-Host "Execution policy set to RemoteSigned for LocalMachine."
} Catch {
    Write-Warning "Failed to set execution policy at LocalMachine scope: $_"
}

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

# Import module into global profiles for both PowerShell versions
$profilePaths = @(
    "$env:windir\System32\WindowsPowerShell\v1.0\profile.ps1",         # Windows PowerShell 5.1
    "C:\Program Files\PowerShell\7\profile.ps1"                        # PowerShell 7+
)

foreach ($profilePath in $profilePaths) {
    if (-not (Test-Path $profilePath)) {
        New-Item -Path $profilePath -ItemType File -Force
    }
    Add-Content -Path $profilePath -Value "`nImport-Module '$moduleFile'"
}

# Fix permissions for the schemes folder
$schemesFolder = "C:\Users\Public\Documents\dwagoon\windows\winwal\colortool\schemes"
if (Test-Path $schemesFolder) {
    $schemesAcl = Get-Acl $schemesFolder
    $modifyRule = New-Object System.Security.AccessControl.FileSystemAccessRule("Users","Modify","ContainerInherit,ObjectInherit","None","Allow")
    $schemesAcl.AddAccessRule($modifyRule)
    Set-Acl $schemesFolder $schemesAcl
    Write-Host "Permissions updated for schemes folder."
} else {
    Write-Host "Schemes folder not found: $schemesFolder"
}