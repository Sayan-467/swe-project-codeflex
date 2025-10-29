# CodeChef Editorial Scraper - Quick Start Script
# Run this after installing requirements.txt

Write-Host "🚀 Starting CodeChef Editorial Scraper Server..." -ForegroundColor Green
Write-Host ""

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  Warning: .env file not found!" -ForegroundColor Yellow
    Write-Host "Creating .env template..." -ForegroundColor Yellow
    
    $envTemplate = @"
# AI Provider - Choose one:
GEMINI_API_KEY=your_gemini_api_key_here
# OR
# OPENAI_API_KEY=your_openai_api_key_here
"@
    
    $envTemplate | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "✓ Created .env template. Please add your API key!" -ForegroundColor Green
    Write-Host ""
    Read-Host "Press Enter after updating .env file"
}

Write-Host "Starting FastAPI server on http://localhost:8001" -ForegroundColor Cyan
Write-Host ""
Write-Host "Available endpoints:" -ForegroundColor White
Write-Host "  GET  /" -ForegroundColor Gray
Write-Host "  POST /generate/hints" -ForegroundColor Gray
Write-Host "  GET  /fetch/editorial" -ForegroundColor Gray
Write-Host "  GET  /metadata" -ForegroundColor Gray
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start uvicorn
uvicorn main:app --reload --port 8001
