# Compatibility and porting

## Current target

AeroTurbine v0.1.0 is compiled for Redmi Watch 4: 390 × 450 pixels, FPRJ device type 365. Its latest design has passed local asset/layout checks and the Mi Create compiler. On 2026-10-09, the author reported that the latest revision works on the physical Redmi Watch 4. Firmware and companion-app versions were not recorded; this confirms basic operation, not an exhaustive weather-state or firmware test matrix.

The project keeps live source identifiers for hours (`0811`), minutes (`1011`), weekday (`2012`), day (`1812`), month (`1012`), steps (`0821`), battery (`0841`), Celsius temperature (`2031`) and weather condition (`3031`). Identifiers must be checked against the target device's editor definition when porting.

## Why the same binary does not work everywhere

The package contains device-specific metadata, image dimensions and widget positions. Mi Create's device definitions for v1.1.1 list these example canvases:

| Model | Canvas | Consequence |
| --- | --- | --- |
| Redmi Watch 4 | 390 × 450 | Current layout |
| Xiaomi Band 8 / 9 | 192 × 490 | Much narrower; use a new vertical composition |
| Xiaomi Band 8 Pro / 9 Pro | 336 × 480 | Rebalance widths, spacing and fan crop |

Source: [Mi Create device definitions](https://github.com/ooflet/Mi-Create/blob/v1.1.1/src/data/devices.json). These dimensions are layout references, not a guarantee that a compiled port will work on every firmware.

## Recommended port workflow

1. Create a new `.fprj` with the exact target model; give the port its own project ID.
2. Keep a separate `watchfaces/<device>/` directory and release filename.
3. Recompose the clock and information row for that canvas. On narrow bands, place the metrics vertically rather than simply shrinking all text.
4. Resize/crop the fan asset, regenerate masks and digits, and use the target thumbnail dimensions.
5. Map live sources, check weather indexes and visibility flags, and preserve the weather-color/mask layer order.
6. Compile with the correct device selected, inspect previews at native size, and check negative temperatures, leading zeros and maximum values.
7. Install on the actual target device and record model, firmware, companion app and test results before marking it supported.

Do not rename the Redmi Watch 4 `.bin` and treat it as a port. Always publish a separately compiled build. This release does not include an always-on-display layout, fan animation or ports to other devices.

## Weather notes

The 42 weather states follow [EasyFace's published weather table](https://github.com/m0tral/EasyFace/wiki/WeatherTableIT). Validity behavior still depends on the watch's firmware and synchronized data. The dash overlay from an earlier version was removed because it could appear above a valid temperature on the user's watch. This release hides weather widgets through their validity source without adding a separate dash.
