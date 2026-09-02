Write-Host "Installing Python dependencies..."
python -m pip install -r requirements.txt

Write-Host ""
Write-Host "Checking Ollama..."

if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    Write-Host "Ollama is not installed."
    Write-Host "Install Ollama for Windows first."
    exit 1
}

Write-Host "Pulling Qwen3 0.6B..."
ollama pull qwen3:0.6b

Write-Host "Pulling embedding model..."
ollama pull nomic-embed-text

Write-Host ""
Write-Host "Starting Ollama server..."

Start-Process ollama -ArgumentList "serve"

Start-Sleep -Seconds 3

Write-Host ""
Write-Host "Testing Ollama..."

try {
    Invoke-RestMethod `
        -Uri "http://localhost:11434/api/tags" `
        -Method Get | Out-Null

    Write-Host "Ollama server is running."
}
catch {
    Write-Host "Ollama server could not be reached."
    exit 1
}

Write-Host ""
Write-Host "Setup completed."
Write-Host ""
Write-Host "Installed models:"
ollama list