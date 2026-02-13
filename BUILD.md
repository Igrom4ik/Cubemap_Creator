# Build Script for Cubemap Renderer

## Quick Start

### Build locally:

```powershell
.\build.ps1
```

This will create a ZIP archive in the `dist/` folder ready for installation in Blender.

### Clean and rebuild:

```powershell
.\build.ps1 -Clean
```

This removes old builds and creates a fresh archive.

## What the script does:

1. Reads addon version and ID from `blender_manifest.toml`
2. Collects all addon files (excluding `.git`, `.idea`, `.venv`, etc.)
3. Compresses them into `cubemap_renderer-X.Y.Z.zip`
4. Outputs the path for easy installation

## Installation

After building, install the ZIP in Blender:

1. Open Blender
2. Edit → Preferences → Add-ons → Install
3. Select the ZIP file from `dist/cubemap_renderer-X.Y.Z.zip`
4. Enable the add-on

## GitHub Actions

Releases on tags (e.g., `v1.5.0`) automatically build and attach ZIPs.

