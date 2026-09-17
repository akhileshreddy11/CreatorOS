$ErrorActionPreference = 'Stop'

$backend = Split-Path -Parent $PSScriptRoot
$root = Split-Path -Parent $backend
$tools = Join-Path $root 'tools'
sadtalker = Join-Path $tools 'SadTalker'
$venv = Join-Path $sadtalker '.venv'
$checkpoints = Join-Path $sadtalker 'checkpoints'

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
& $python -m pip install huggingface_hub

New-Item -ItemType Directory -Force -Path $checkpoints | Out-Null

Write-Host ''
Write-Host 'Downloading SadTalker checkpoints from Hugging Face...'
Write-Host 'This is a one-time download and can take several minutes.'

$downloadScript = @"
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id='vinthony/SadTalker',
    local_dir=r'$($checkpoints.Replace("'", "''"))',
    local_dir_use_symlinks=False,
)
print('SadTalker checkpoints downloaded successfully.')
"@

& $python -c $downloadScript

$presenter = Join-Path $root 'assets/creatoros_presenter.jpg'
if (-not (Test-Path $presenter)) {
    Write-Warning "Presenter image is missing: $presenter"
    Write-Warning 'Copy the CreatorOS presenter image there before running a Reel.'
} else {
    Write-Host "Presenter image found: $presenter"
}

Write-Host ''
Write-Host 'SadTalker setup is complete.'
Write-Host "Python: $python"
Write-Host "Checkpoints: $checkpoints"
Write-Host "Presenter: $presenter"
