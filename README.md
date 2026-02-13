# Cubemap Renderer

Blender add-on for rendering cubemaps for UE5 and Unity.

## Requirements

- Blender 5.0+
- Current version: 1.5.0

## Install (Extensions Platform)

1. Open https://extensions.blender.org/add-ons/ and find "Cubemap Renderer".
2. Click Install in Blender or download the ZIP.
3. In Blender: Edit > Preferences > Add-ons > Install.
4. Select the ZIP and enable the add-on.

## Install (Local)

1. Copy this folder to your Blender add-ons directory.
2. In Blender: Edit > Preferences > Add-ons.
3. Enable "Cubemap Renderer".

## Build Locally

For quick testing or customization, build the add-on locally:

```powershell
.\build.ps1
```

See [BUILD.md](BUILD.md) for detailed instructions.

## Automated Builds (GitHub Actions)

On every release tag (e.g., `v1.5.0`), GitHub Actions automatically:
- Builds the ZIP archive
- Generates a changelog
- Attaches both to the GitHub Release

Check [Releases](https://github.com/Igrom4ik/Cubemap_Creator/releases) for builds.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Development

- Source: `__init__.py`, `operators.py`, `panels.py`, `properties.py`, `utils.py`
- Manifest: `blender_manifest.toml`

## License

GPL-3.0-or-later
