param(
    [string]$Compiler = (Join-Path $env:LOCALAPPDATA 'Programs\Mi Create\compiler\compile.exe')
)
$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path $PSScriptRoot -Parent
$projectPath = Join-Path $repoRoot 'watchfaces\redmi-watch-4\AeroTurbine.fprj'
$buildPath = Join-Path $repoRoot '.build'
if (-not (Test-Path -LiteralPath $Compiler)) {
    throw 'Install Mi Create or pass -Compiler with the path to its compile.exe.'
}
New-Item -ItemType Directory -Force -Path $buildPath | Out-Null
# The compiler writes its .info metadata beside the project regardless of -b output.
New-Item -ItemType Directory -Force -Path (Join-Path (Split-Path $projectPath -Parent) 'output') | Out-Null
$ErrorActionPreference = 'Continue'
$compilerLog = & $Compiler -b $projectPath $buildPath 'AeroTurbine.face' 1461256429 2>&1
$compilerExit = $LASTEXITCODE
$ErrorActionPreference = 'Stop'
$compilerLog | Write-Output
if (($compilerExit -ne 0) -or (($compilerLog -join "`n") -notmatch 'No Errors')) {
    throw 'Compilation failed; release files were not packaged.'
}
python (Join-Path $PSScriptRoot 'package_release.py')
if ($LASTEXITCODE -ne 0) { throw 'Release packaging failed.' }
