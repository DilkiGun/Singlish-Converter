$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$Python = Join-Path $Root ".venv\Scripts\python.exe"
$PyInstaller = Join-Path $Root ".venv\Scripts\pyinstaller.exe"

Write-Host "==> 1. Running test suite..." -ForegroundColor Cyan
& $Python -m pytest -v
if ($LASTEXITCODE -ne 0) { throw "Tests failed." }

Write-Host "==> 2. Generating icons and installer assets..." -ForegroundColor Cyan
& $Python scripts\generate_assets.py
if ($LASTEXITCODE -ne 0) { throw "Asset generation failed." }

Write-Host "==> 3. Building executable bundle with PyInstaller..." -ForegroundColor Cyan
& $PyInstaller --noconfirm --clean SinglishStudio.spec
if ($LASTEXITCODE -ne 0) { throw "PyInstaller build failed." }

Write-Host "==> 4. Locating Inno Setup compiler (ISCC.exe)..." -ForegroundColor Cyan
$IsccCandidates = @(
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
    "C:\Program Files\Inno Setup 6\ISCC.exe",
    "C:\Program Files (x86)\Inno Setup 7\ISCC.exe",
    "C:\Program Files\Inno Setup 7\ISCC.exe",
    "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe",
    "$env:LOCALAPPDATA\Programs\Inno Setup 7\ISCC.exe"
)
$Iscc = $IsccCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $Iscc) {
    $Cmd = Get-Command iscc -ErrorAction SilentlyContinue
    if ($Cmd) { $Iscc = $Cmd.Source }
}
if (-not $Iscc) {
    throw "Inno Setup compiler (ISCC.exe) not found. Install Inno Setup 6/7 first."
}

Write-Host "==> 5. Compiling Windows Installer using $Iscc..." -ForegroundColor Cyan
& $Iscc "installer\singlish_studio.iss"
if ($LASTEXITCODE -ne 0) { throw "Inno Setup compilation failed." }

Write-Host "==> Build complete!" -ForegroundColor Green
Get-ChildItem "dist\installer" | Format-Table Name, Length, LastWriteTime
