# Release Script for Cubemap Renderer

Automated release script that bumps version, builds, commits, and pushes to GitHub.

## Usage

```powershell
# Bump patch version (e.g., 1.5.0 → 1.5.1) - default
.\release.ps1

# Bump minor version (e.g., 1.5.0 → 1.6.0)
.\release.ps1 -BumpType minor

# Bump major version (e.g., 1.5.0 → 2.0.0)
.\release.ps1 -BumpType major

# With release message
.\release.ps1 -BumpType patch -Message "Fix icons and Pillow detection"
```

## What it does

1. **Reads** current version from `blender_manifest.toml`
2. **Bumps** version (major/minor/patch)
3. **Updates** manifest with new version
4. **Builds** ZIP archive using `build.ps1`
5. **Commits** changes with message `Release v1.5.1`
6. **Pushes** to `main` branch
7. **Creates release tag** `v1.5.1` and pushes it
8. **GitHub Actions** automatically creates Release and uploads assets

## Output

- ✓ Updated `blender_manifest.toml` with new version
- ✓ Built `dist/cubemap_renderer-X.Y.Z.zip`
- ✓ Created git commit
- ✓ Pushed to GitHub
- ✓ Created GitHub Release with ZIP and CHANGELOG

## Example

```powershell
.\release.ps1 -BumpType minor -Message "Add Pillow preferences and fix icons"
```

This will:
- Bump 1.5.0 → 1.6.0
- Create commit: "Release v1.6.0: Add Pillow preferences and fix icons"
- Push tag v1.6.0
- GitHub Actions creates Release automatically

