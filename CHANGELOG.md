# Changelog

## v1.5.4 - 2026-02-13

- Fixed manifest encoding (removed BOM) so tomllib can parse it.

## v1.5.3 - 2026-02-13

- Kept Pillow controls only in Preferences; main panel shows status only.

## v1.5.1 - 2026-02-13

- Added visible popup for Pillow version check results.
- Added force reinstall option for Pillow in Preferences and main panel.
- Exposed Check Version action regardless of install state.

## v1.5.0 - 2026-02-13

- Added add-on Preferences panel for Pillow dependency (install/check in Settings).
- Moved Pillow installation out of the main UI; main panel shows status only.
- Switched engine selector to icon buttons and widened the controls.
- Updated engine logos with light backgrounds for readability on dark themes.
- Improved "Assemble Strip" icon contrast and visuals.
- Removed OpenEXR from supported formats to avoid assembly errors.
- Fixed default format selection for UE5 preset.
- Refined build and release automation to attach artifacts on tag releases.
- Fixed manifest schema for Blender 5.0+.
- Updated permissions and license entries.
- Improved icon loading and UI display.
