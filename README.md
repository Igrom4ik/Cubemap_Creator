# Cubemap Renderer

Blender add-on for rendering cubemaps for UE5 and Unity.

## Requirements

- Blender 4.2+

## Install (Extensions Platform)

1. Open https://extensions.blender.org/add-ons/ and find "Cubemap Renderer".
2. Click Install in Blender or download the ZIP.
3. In Blender: Edit > Preferences > Add-ons > Install.
4. Select the ZIP and enable the add-on.

## Install (Local)

1. Copy this folder to your Blender add-ons directory.
2. In Blender: Edit > Preferences > Add-ons.
3. Enable "Cubemap Renderer".

## Build (GitHub Actions)

On every push, GitHub Actions builds a ZIP artifact and a generated `CHANGELOG.md` based on git history.

## Development

- Source: `__init__.py`, `operators.py`, `panels.py`, `properties.py`, `utils.py`
- Manifest: `blender_manifest.toml`

## License

GPL-3.0 (confirm if you want a different license).
