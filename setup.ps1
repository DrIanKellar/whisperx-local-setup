# WhisperX setup for Windows + NVIDIA GPU
# Run from PowerShell in this folder:  .\setup.ps1
# If you get an execution policy error first run:
#   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

$ErrorActionPreference = "Stop"

Write-Host "=== WhisperX setup ===" -ForegroundColor Cyan

# Helper: does a command exist on PATH?
function Test-Cmd($name) {
    return [bool](Get-Command $name -ErrorAction SilentlyContinue)
}

# 1. Check Python
if (-not (Test-Cmd python)) {
    Write-Host "Python not found on PATH. Install Python 3.11 from python.org and tick 'Add to PATH'." -ForegroundColor Red
    exit 1
}
$pyVersion = (& python --version 2>&1 | Out-String).Trim()
Write-Host "Python: $pyVersion"
if ($pyVersion -notmatch "3\.(10|11)\.") {
    Write-Host "Warning: WhisperX is tested on Python 3.10/3.11. You have $pyVersion. Continuing anyway." -ForegroundColor Yellow
}

# 2. Check ffmpeg (just check it exists; -version pipe trick fights with $ErrorActionPreference=Stop)
if (-not (Test-Cmd ffmpeg)) {
    Write-Host "ffmpeg not found on PATH. Install with:  winget install Gyan.FFmpeg" -ForegroundColor Red
    exit 1
}
Write-Host "ffmpeg: OK"

# 3. Check NVIDIA driver
if (-not (Test-Cmd nvidia-smi)) {
    Write-Host "nvidia-smi not found. Install NVIDIA driver before continuing." -ForegroundColor Red
    exit 1
}
$nvidia = (& nvidia-smi --query-gpu=name,driver_version --format=csv,noheader | Out-String).Trim()
Write-Host "GPU: $nvidia"

# 4. Create venv if missing
if (-not (Test-Path ".\venv")) {
    Write-Host "Creating venv..." -ForegroundColor Cyan
    & python -m venv venv
}

# 5. Activate venv
$activate = ".\venv\Scripts\Activate.ps1"
if (-not (Test-Path $activate)) {
    Write-Host "venv activation script missing. Delete the venv folder and rerun." -ForegroundColor Red
    exit 1
}
. $activate

# 6. Upgrade pip
& python -m pip install --upgrade pip wheel setuptools

# 7. Install WhisperX + dependencies (pulls in CPU torch 2.8.0 as a transitive dep)
Write-Host "Installing WhisperX..." -ForegroundColor Cyan
& pip install --upgrade --no-cache-dir -r requirements.txt

# 8. Force-replace the CPU torch with the CUDA build (matching version 2.8.0)
# WhisperX 3.8.x pins torch~=2.8.0; cu124 wheels available on the PyTorch index.
Write-Host "Replacing CPU torch with CUDA-enabled build..." -ForegroundColor Cyan
& pip install --upgrade --force-reinstall --no-deps `
    torch==2.8.0 torchaudio==2.8.0 torchvision==0.23.0 `
    --index-url https://download.pytorch.org/whl/cu124

# 9. Diagnostic
Write-Host "`n=== Diagnostic ===" -ForegroundColor Cyan
& python -c @"
import torch
print(f'torch:       {torch.__version__}')
print(f'cuda avail:  {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'device:      {torch.cuda.get_device_name(0)}')
    print(f'cuda ver:    {torch.version.cuda}')
import whisperx
print(f'whisperx:    {whisperx.__version__ if hasattr(whisperx, \"__version__\") else \"installed\"}')
"@

Write-Host "`nSetup complete." -ForegroundColor Green
Write-Host "Next: copy .env.example to .env and add your Hugging Face token, then:"
Write-Host "    .\venv\Scripts\Activate.ps1"
Write-Host "    python transcribe.py path\to\audio.mp3"
