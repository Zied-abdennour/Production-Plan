$ErrorActionPreference = "Stop"

Write-Host "========================================"
Write-Host " Production Planner - Setup"
Write-Host "========================================"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

Write-Host ""
Write-Host "[1/7] Checking Python..."

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python was not found."
    exit 1
}

python --version

Write-Host ""
Write-Host "[2/7] Installing Python dependencies..."

if (-not (Test-Path "requirements.txt")) {
    Write-Host "requirements.txt was not found."
    exit 1
}

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

Write-Host ""
Write-Host "[3/7] Checking Ollama..."

if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    Write-Host "Ollama was not found."
    Write-Host "Install Ollama and run setup again."
    exit 1
}

ollama --version

Write-Host ""
Write-Host "[4/7] Checking Ollama server..."

$ollamaRunning = $false

try {
    $response = curl.exe -s --max-time 3 http://localhost:11434/api/tags

    if ($LASTEXITCODE -eq 0 -and $response) {
        $ollamaRunning = $true
        Write-Host "Ollama server is already running."
    }
}
catch {
    $ollamaRunning = $false
}

if (-not $ollamaRunning) {
    Write-Host "Starting Ollama server..."

    Start-Process `
        -FilePath "ollama" `
        -ArgumentList "serve" `
        -WindowStyle Hidden

    Start-Sleep -Seconds 5

    try {
        $response = curl.exe -s --max-time 5 http://localhost:11434/api/tags

        if ($LASTEXITCODE -ne 0 -or -not $response) {
            Write-Host "Could not start Ollama server."
            exit 1
        }

        Write-Host "Ollama server started successfully."
    }
    catch {
        Write-Host "Could not connect to Ollama server."
        exit 1
    }
}

Write-Host ""
Write-Host "[5/7] Pulling Qwen3 0.6B..."

ollama pull qwen3:0.6b

Write-Host ""
Write-Host "[6/7] Pulling embedding model..."

ollama pull nomic-embed-text

Write-Host ""
Write-Host "[7/7] Creating project directories..."

New-Item -ItemType Directory -Force -Path "data" | Out-Null
New-Item -ItemType Directory -Force -Path "data\chroma" | Out-Null

Write-Host ""
Write-Host "========================================"
Write-Host " Verifying Ollama"
Write-Host "========================================"

curl.exe http://localhost:11434/api/tags

Write-Host ""
Write-Host "========================================"
Write-Host " Setup completed successfully."
Write-Host "========================================"

Write-Host ""
Write-Host "Installed models:"
ollama list

Write-Host ""
Write-Host "To start the application:"
Write-Host "streamlit run app.py"

Write-Host ""
Write-Host "Ollama API:"
Write-Host "http://localhost:11434"