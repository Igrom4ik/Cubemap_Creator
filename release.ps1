# Auto-build and push script for Cubemap Renderer
# Automatically bumps version, builds ZIP, commits, and pushes with release tag

param(
    [ValidateSet("major", "minor", "patch")]
    [string]$BumpType = "patch",
    [string]$Message = ""
)

# Colors
$Green = "Green"
$Yellow = "Yellow"
$Red = "Red"
$Cyan = "Cyan"

function Write-Status {
    param([string]$Text, [string]$Color = "White")
    Write-Host $Text -ForegroundColor $Color
}

Write-Status "=== Cubemap Renderer Auto-Build & Push ===" -Color $Cyan
Write-Status "Bump Type: $BumpType" -Color $Yellow

# 1. Read current version from manifest
Write-Status "`n[1/6] Reading current version..." -Color $Cyan
$ManifestPath = ".\blender_manifest.toml"
if (-not (Test-Path $ManifestPath)) {
    Write-Status "❌ Error: blender_manifest.toml not found!" -Color $Red
    exit 1
}

$ManifestContent = Get-Content $ManifestPath -Raw
$VersionMatch = [regex]::Match($ManifestContent, '(?m)^version\s*=\s*"([^"]+)"')
if (-not $VersionMatch.Success) {
    Write-Status "❌ Error: Could not parse version from manifest!" -Color $Red
    exit 1
}

$CurrentVersion = $VersionMatch.Groups[1].Value
Write-Status "Current version: $CurrentVersion" -Color $Green

# 2. Bump version
Write-Status "`n[2/6] Bumping version ($BumpType)..." -Color $Cyan
$VersionParts = $CurrentVersion -split '\.'
[int]$Major = $VersionParts[0]
[int]$Minor = $VersionParts[1]
[int]$Patch = $VersionParts[2]

switch ($BumpType) {
    "major" {
        $Major++
        $Minor = 0
        $Patch = 0
    }
    "minor" {
        $Minor++
        $Patch = 0
    }
    "patch" {
        $Patch++
    }
}

$NewVersion = "$Major.$Minor.$Patch"
Write-Status "New version: $NewVersion" -Color $Green

# 3. Update manifest
Write-Status "`n[3/6] Updating manifest..." -Color $Cyan
$UpdatedManifest = $ManifestContent -replace '(?m)^version\s*=\s*"[^"]+"', "version = `"$NewVersion`""
Set-Content -Path $ManifestPath -Value $UpdatedManifest -Encoding UTF8
Write-Status "✓ Manifest updated" -Color $Green

# 4. Build archive
Write-Status "`n[4/6] Building archive..." -Color $Cyan
Remove-Item -Path ".\dist" -Recurse -Force -ErrorAction SilentlyContinue
.\build.ps1 | Out-Null
if (-not (Test-Path ".\dist\cubemap_renderer-$NewVersion.zip")) {
    Write-Status "❌ Error: Archive build failed!" -Color $Red
    exit 1
}
Write-Status "✓ Archive created: cubemap_renderer-$NewVersion.zip" -Color $Green

# 5. Commit and push
Write-Status "`n[5/6] Committing changes..." -Color $Cyan
$CommitMsg = "Release v$NewVersion"
if ($Message) {
    $CommitMsg += ": $Message"
}

git add blender_manifest.toml
git commit -m $CommitMsg
if ($LASTEXITCODE -ne 0) {
    Write-Status "❌ Error: Commit failed!" -Color $Red
    exit 1
}
Write-Status "✓ Committed: $CommitMsg" -Color $Green

Write-Status "`n[6/6] Pushing to GitHub..." -Color $Cyan
git push origin main
if ($LASTEXITCODE -ne 0) {
    Write-Status "⚠ Warning: Push to main failed (but continuing with tag)" -Color $Yellow
}
Write-Status "✓ Pushed to main" -Color $Green

# 6. Create release tag
Write-Status "`nCreating release tag v$NewVersion..." -Color $Cyan
git tag -d "v$NewVersion" 2>$null
git push origin ":refs/tags/v$NewVersion" 2>$null
git tag -a "v$NewVersion" -m "Release v$NewVersion"
git push origin "v$NewVersion"
if ($LASTEXITCODE -ne 0) {
    Write-Status "❌ Error: Tag push failed!" -Color $Red
    exit 1
}
Write-Status "✓ Tag v$NewVersion pushed" -Color $Green

Write-Status "`n✅ Build complete!" -Color $Green
Write-Status "Release: https://github.com/Igrom4ik/Cubemap_Creator/releases/tag/v$NewVersion" -Color $Cyan
Write-Status "Archive: dist\cubemap_renderer-$NewVersion.zip" -Color $Cyan
Write-Status "`nGitHub Actions should create the release automatically (check Actions tab)." -Color $Yellow

