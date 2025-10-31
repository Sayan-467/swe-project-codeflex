# Quick start script for the Codeforces Editorial Fetcher

Write-Host "🚀 Starting Codeforces Editorial Fetcher..." -ForegroundColor Green
Write-Host ""

# Check if virtual environment exists
if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "✓ Activating virtual environment..." -ForegroundColor Cyan
    & .\.venv\Scripts\Activate.ps1
} else {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run: python -m venv .venv" -ForegroundColor Yellow
    exit 1
}

# Check if requirements are installed
Write-Host "✓ Checking dependencies..." -ForegroundColor Cyan
$packages = pip list 2>&1 | Out-String
if ($packages -notmatch "fastapi" -or $packages -notmatch "selenium") {
    Write-Host "⚠ Installing missing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  Server starting at: http://127.0.0.1:8000" -ForegroundColor White
Write-Host "  API Docs at: http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the server
uvicorn main:app --reload
