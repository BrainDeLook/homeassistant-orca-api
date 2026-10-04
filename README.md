# Bambuddy OrcaSlicer API — Home Assistant repository

Home Assistant app for server-side slicing with OrcaSlicer 2.4.2. Supports
Raspberry Pi 5 (`aarch64`) and x86-64. The app builds locally in Home Assistant.

## Install from GitHub

Add this repository URL in Home Assistant under Settings → Apps → App Store
→ ⋮ → Repositories:

`https://github.com/BrainDeLook/homeassistant-orca-api`

Install **Bambuddy OrcaSlicer API**, start it, then open
`http://<HA-IP>:3003/health`. Enter `http://<HA-IP>:3003` as the OrcaSlicer
sidecar URL in Bambuddy's Workflow settings.

The API is reachable without a password. Use it only on your trusted LAN.

## Source and license

The REST wrapper in `orca_api/src` is derived from
[maziggy/orca-slicer-api](https://github.com/maziggy/orca-slicer-api/tree/bambuddy/profile-resolver)
(AGPL-3.0-or-later). `orca_api/LICENSE` contains its license. OrcaSlicer is
downloaded from the official 2.4.2 release at build time.

## Verification status

The source compiles on Windows. The HA container build and runtime slicing
need verification on the Pi 5 host.
