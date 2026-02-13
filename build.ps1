# Build script for Cubemap Renderer Blender add-on
# Usage: .\build.ps1

param(
    [string]$OutputDir = ".\dist",
    [switch]$Clean
)

# Paths
$ManifestPath = ".\blender_manifest.toml"
$AddonDir = "."

# Read manifest
Write-Host "Reading manifest..." -ForegroundColor Cyan
if (-not (Test-Path $ManifestPath)) {
    Write-Host "Error: blender_manifest.toml not found!" -ForegroundColor Red
    exit 1
}

# Parse manifest with regex (skip schema_version)
$ManifestContent = Get-Content $ManifestPath -Raw

# Extract version (not schema_version) - must be on its own line
$VersionMatch = [regex]::Match($ManifestContent, '(?m)^version\s*=\s*"([^"]+)"')
$Version = if ($VersionMatch.Success) { $VersionMatch.Groups[1].Value } else { "1.0.0" }

# Extract addon ID
$IdMatch = [regex]::Match($ManifestContent, 'id\s*=\s*"([^"]+)"')
$AddonId = if ($IdMatch.Success) { $IdMatch.Groups[1].Value } else { "addon" }

Write-Host "Addon ID: $AddonId" -ForegroundColor White
Write-Host "Version: $Version" -ForegroundColor White

$ZipName = "$AddonId-$Version.zip"
$ZipPath = Join-Path $OutputDir $ZipName

# Clean old builds if requested
if ($Clean -and (Test-Path $OutputDir)) {
    Write-Host "Cleaning dist directory..." -ForegroundColor Yellow
    Remove-Item $OutputDir -Recurse -Force
}

# Create output directory
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
}

Write-Host "`nBuilding $ZipName..." -ForegroundColor Cyan

# Patterns to exclude
$ExcludePatterns = @(
    "\.git",
    "\.github",
    "\.idea",
    "\.venv",
    "dist",
    "build\.ps1",
    "BUILD\.md",
    "\.pyc",
    "__pycache__",
    "\.log",
    "\.DS_Store",
    "Thumbs\.db"
)

# Collect files to include
$IncludedItems = @()

Get-ChildItem -Recurse $AddonDir -File | ForEach-Object {
    $FullPath = $_.FullName
    $RelativePath = $FullPath.Substring((Get-Item $AddonDir).FullName.Length + 1)

    # Skip excluded patterns
    $Skip = $false
    foreach ($Pattern in $ExcludePatterns) {
        if ($RelativePath -match $Pattern) {
            $Skip = $true
            break
        }
    }

    if (-not $Skip) {
        $IncludedItems += $FullPath
    }
}

# Remove old ZIP if exists
if (Test-Path $ZipPath) {
    Remove-Item $ZipPath -Force
}

# Compress items with full paths
if ($IncludedItems.Count -gt 0) {
    try {
        Compress-Archive -Path $IncludedItems -DestinationPath $ZipPath -CompressionLevel Optimal
    } catch {
        Write-Host "Error compressing: $_" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Error: No files to compress!" -ForegroundColor Red
    exit 1
}

if (Test-Path $ZipPath) {
    $FileSize = (Get-Item $ZipPath).Length
    $FileSizeKB = [math]::Round($FileSize / 1KB, 2)
    $FullZipPath = (Resolve-Path $ZipPath).Path

    Write-Host "`n✓ Build complete!" -ForegroundColor Green
    Write-Host "ZIP created: $FullZipPath" -ForegroundColor Green
    Write-Host "Size: $FileSizeKB KB" -ForegroundColor Green
    Write-Host "`nTo install in Blender:" -ForegroundColor Cyan
    Write-Host "  Edit > Preferences > Add-ons > Install" -ForegroundColor White
    Write-Host "  Select: $FullZipPath" -ForegroundColor White
    Write-Host "`nOr use -Clean flag to remove old builds:" -ForegroundColor Cyan
    Write-Host "  .\build.ps1 -Clean" -ForegroundColor White
} else {
    Write-Host "Error: ZIP file was not created!" -ForegroundColor Red
    exit 1
}
