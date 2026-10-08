## AeroTurbine v0.1.0

Initial public release for **Redmi Watch 4 only (390 × 450)**.

- Bright metallic fan illustration and large weather-colored digital time.
- Live Turkish weekday/date, airplane steps indicator and rocket battery indicator.
- Weather icons and Celsius temperature; earlier dash overlay removed.
- Editable Mi Create project, full source assets, English/Turkish README, build scripts and MIT notices.

### Downloads

- **`AeroTurbine-RedmiWatch4-v0.1.0.bin`** — install through a compatible Notify app on an Android phone paired with Redmi Watch 4.
- **`AeroTurbine-RedmiWatch4-v0.1.0-editable.zip`** — extract and open `watchfaces/redmi-watch-4/AeroTurbine.fprj` in Mi Create; keep `images` next to it.
- **`SHA256SUMS.txt`** — checksums for the binary and editable archive.

### Validation and limitations

Project/device/source checks, image integrity, canvas bounds, alignment and weather color validation passed. Rebuilding the project assets and compiling with Mi Create's RedmiWatch4 compiler succeeded.

On **2026-10-09**, the author confirmed that the latest revision works on the physical Redmi Watch 4. The pre-release flag has been removed. This is a basic operation report, not exhaustive coverage of every weather state or firmware version. Weather relies on companion-app synchronization. No Mi Band builds, AOD layout or animated fan are included.

The installation binary is unchanged; documentation and the editable ZIP were updated with the test result.

Mi Band and other devices require separate layouts, device settings and compilation. Read the repository's compatibility guide before creating a port.
