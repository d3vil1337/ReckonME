param([Parameter(Mandatory = $true)][string]$Destination)
$ErrorActionPreference = 'Stop'
$projectRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
Set-Location -LiteralPath $projectRoot
$backupRoot = [IO.Path]::GetFullPath($Destination)
if ($backupRoot.TrimEnd('\') -eq $projectRoot.TrimEnd('\') -or
    $backupRoot.StartsWith($projectRoot.TrimEnd('\') + '\', [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Backup destination must be outside the working directory.'
}
function Invoke-GitChecked {
    param([string[]]$GitArgs)
    $result = & git @GitArgs
    if ($LASTEXITCODE -ne 0) { throw "git $GitArgs failed" }
    return $result
}
$dirty = Invoke-GitChecked @('status', '--porcelain')
if ($dirty) { throw 'Commit or preserve working changes before archiving.' }
$commit = Invoke-GitChecked @('rev-parse', 'HEAD')
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss-fff'
$archiveDir = Join-Path $backupRoot "$stamp-$($commit.Substring(0, 12))"
New-Item -ItemType Directory -Path $archiveDir | Out-Null
$zipPath = Join-Path $archiveDir 'source.zip'
$bundlePath = Join-Path $archiveDir 'history.bundle'
Invoke-GitChecked @('archive', '--format=zip', "--output=$zipPath", 'HEAD')
Invoke-GitChecked @('bundle', 'create', $bundlePath, '--all')
Invoke-GitChecked @('bundle', 'verify', $bundlePath)
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [IO.Compression.ZipFile]::OpenRead($zipPath)
try {
    $actual = @($zip.Entries | Where-Object { $_.Name } | ForEach-Object { $_.FullName } | Sort-Object)
    $expected = @(Invoke-GitChecked @('ls-tree', '-r', '--name-only', 'HEAD') | Sort-Object)
    if (Compare-Object $expected $actual) { throw 'Archive entries differ from HEAD.' }
} finally { $zip.Dispose() }
@("Commit: $commit", 'Scope: committed source and Git history; ignored data excluded.') |
    Set-Content -LiteralPath (Join-Path $archiveDir 'MANIFEST.txt')
Get-FileHash -Algorithm SHA256 -LiteralPath $zipPath, $bundlePath |
    ForEach-Object { "$($_.Hash)  $([IO.Path]::GetFileName($_.Path))" } |
    Set-Content -LiteralPath (Join-Path $archiveDir 'SHA256.txt')
Write-Output "Verified archive: $archiveDir"
