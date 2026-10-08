# AeroTurbine Watchface

An aviation-inspired digital watchface for **Redmi Watch 4**: a bright metallic fan, oversized time, and a clean row of live information.

[Türkçe](README.tr.md) · [Download](https://github.com/KadirYurekturk/aeroturbine-watchface/releases) · [Compatibility and porting](docs/COMPATIBILITY.md)

<p align="center">
  <img src="docs/previews/sunny.png" width="240" alt="Sunny weather: yellow time, airplane steps icon, rocket battery icon and temperature">
  <img src="docs/previews/rainy.png" width="240" alt="Rainy weather: blue time and rain icon">
  <img src="docs/previews/cloudy.png" width="240" alt="Cloudy weather: white time and cloud icon">
</p>

## Features

- Large, stacked 24-hour time with live hours and minutes.
- Time color follows the watch's weather condition: **yellow when sunny**, **cyan for rain/storm**, **white for other conditions**.
- Live weekday and `DD/MM` date; weekday labels are Turkish.
- **Airplane → steps**. **Rocket → battery percentage**, displayed without `%`.
- Weather icon and temperature in **Celsius**, including negative temperatures.
- Static fan artwork and matching outline icons; no extra watch app, online account or API key is required by the watchface itself.

The icons are visual labels: the airplane does not show flight data, and the rocket does not show engine data or animate with battery level. Weather depends on data synchronized to the watch by the companion app. Preview values are illustrative.

## Compatibility

**The provided `.bin` is built for Redmi Watch 4 only**, at **390 × 450**, using Mi Create device type **365**.

| Device | Ready-to-install build | Notes |
| --- | --- | --- |
| Redmi Watch 4 | Yes, initial preview release | Compiler and project checks passed; latest artwork revision still needs on-watch validation |
| Xiaomi / Mi Band 8 or 9 | No | A separate 192 × 490 layout and device-specific build are needed |
| Xiaomi Band 8 Pro or 9 Pro | No | A separate 336 × 480 layout and device-specific build are needed |
| Other watches and bands | No | Check editor support, canvas dimensions and live data sources before porting |

An editor supporting several devices does not make one compiled watchface universal. Do not install this Redmi Watch 4 binary on another model. See [porting notes](docs/COMPATIBILITY.md).

## Install on Redmi Watch 4

1. Download **`AeroTurbine-RedmiWatch4-v0.1.0.bin`** from [Releases](https://github.com/KadirYurekturk/aeroturbine-watchface/releases/tag/v0.1.0).
2. Copy it to the Android phone paired with your Redmi Watch 4.
3. In your compatible Notify app, open **Update watchface / Saat yüzünü güncelle**, choose the local `.bin`, confirm the device, and follow the app's transfer instructions.
4. For weather, enable weather synchronization in the companion app and allow a sync to finish.

Menu wording varies by app version. This repository distributes a watchface, not Notify or Mi Fitness. The initial release is marked **pre-release** because the newest icon and overlay changes have not yet been verified on the physical watch. Earlier iterations of this project were installed successfully on the author's Redmi Watch 4.

## Edit in Mi Create

1. Install [Mi Create](https://github.com/ooflet/Mi-Create/releases) separately.
2. Download the editable project ZIP from Releases, or clone this repository.
3. Extract the ZIP and open **`watchfaces/redmi-watch-4/AeroTurbine.fprj`** in Mi Create.
4. Keep the **`images/` folder beside the `.fprj`**. These are the actual assets the project references.
5. Edit the layout and compile for **Redmi Watch 4**.

The `.fprj` is the editable source; the `.bin` is the installation package. The weather-colored clock uses weather image lists below transparent digit masks. Keep that layer order when moving or replacing clock widgets.

## Build and check

The checked-in `.fprj` and PNG assets can be edited directly; regenerating them is optional. For regeneration, use Windows, Python 3.10+ and Pillow:

```powershell
python -m pip install -r requirements.txt
python scripts/build_assets.py
python scripts/validate_project.py
powershell -ExecutionPolicy Bypass -File scripts/compile.ps1
```

`build_assets.py` uses locally installed Arial Bold and Arial Black. Font files are not distributed. Compilation uses the compiler from your installed Mi Create; neither Mi Create nor its third-party compiler is bundled. The build script creates the device-specific binary, editable ZIP and SHA-256 checksum file under `dist/`.

Validation checks the device, live data sources, image files, screen bounds, weather color mapping, icon alignment and signed temperature assets. Compilation success and preview renders do not replace testing on the physical watch.

## Project layout

```text
watchfaces/redmi-watch-4/  Editable project and deployment PNGs
assets/                  Fan illustration and reusable icon sources
scripts/                 Asset generation, validation and packaging
docs/                    Previews and porting notes
dist/                    Versioned installation and editing packages
licenses/                Third-party notices
```

## Credits and license

Created by **Kadir Yürektürk**. Original project layout and build scripts are published under [MIT](LICENSE). Icons are from [Tabler Icons](https://github.com/tabler/tabler-icons), also MIT; their notice is included in [licenses/](licenses/Tabler-Icons-MIT.txt).

The fan is an AI-assisted illustration developed from a GE9X front-fan visual reference; the reference photograph is not included. See [asset provenance](docs/ASSETS.md). This is an independent community project and is not affiliated with Xiaomi, Redmi, GE Aerospace, TEI or the companion app developers.

Contributions for additional devices are welcome. Include a separate device folder, an editable project, previews, compiler details and a real-device test report. Please do not label a port as tested until it has actually been installed and checked on that model.
