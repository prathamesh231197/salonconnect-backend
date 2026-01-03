param (
    [Parameter(Mandatory=$true, HelpMessage="Enter a description for the migration")]
    [string]$Message
)

# Set error action to Stop to catch failures
$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  SalonConnect Database Migration Tool" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Generate Revision
Write-Host "Step 1: Generating migration revision..." -ForegroundColor Yellow
try {
    & alembic revision --autogenerate -m "$Message"
    if ($LASTEXITCODE -ne 0) { throw "Alembic revision command failed." }
}
catch {
    Write-Host "Error generating revision: $_" -ForegroundColor Red
    exit 1
}

# Step 2: Apply Migration
Write-Host "Step 2: Applying migration to local database..." -ForegroundColor Yellow
try {
    & alembic upgrade head
    if ($LASTEXITCODE -ne 0) { throw "Alembic upgrade command failed." }
}
catch {
    Write-Host "Error applying migration: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Success! Database has been updated." -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
