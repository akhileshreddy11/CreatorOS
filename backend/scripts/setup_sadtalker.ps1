$ErrorActionPreference = 'Stop'

$backend = Split-Path -Parent $PSScriptRoot
$root = Split-Path -Parent $backend
$tools = Join-Path $root 'tools'
$sadtalker = Join-Path $tools 'SadTalker'
$venv = Join-Path $sadtalker '.venv'

New-Item -ItemType Directory -Force -Path $tools | Out-Null

if (-not (Test-Path $sadtalker)) {
    git clone https://github.com/OpenTalker/SadTalker.git $sadtalker
}

if (-not (Test-Path (Join-Path $venv 'Scripts/python.exe'))) {
    py -3.10 -m venv $venv
}

$python = Join-Path $venv 'Scripts/python.exe'
& $python -m pip install --upgrade pip
& $python -m pip install -r (Join-Path $sadtalker 'requirements.txt')

Write-Host ''
Write-Host 'SadTalker code and Python environment are ready.'
Write-Host 'Model checkpoints are required before the first generation.'
Write-Host 'Use the SadTalker README/download script to install the checkpoints into SadTalker/checkpoints.'
Write-Host "Expected Python: $python"
Write-Host "Expected presenter: $(Join-Path $root 'assets/creatoros_presenter.png')"
