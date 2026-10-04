# Bambuddy OrcaSlicer API for Home Assistant

This Home Assistant app packages the Bambuddy-compatible REST wrapper with
OrcaSlicer 2.4.2. It supports `aarch64` (Raspberry Pi 5) and `amd64`.
Home Assistant builds the image locally during installation; no separate
Docker installation is needed.

After starting the app, check `http://<HA-IP>:3003/health`. A healthy response
must include `"status":"healthy"` and report OrcaSlicer as available.
In Bambuddy, select OrcaSlicer, enable Slicer API, and set the sidecar URL to
`http://<HA-IP>:3003`.

The service has no authentication. Keep port 3003 on a trusted LAN and do not
forward it to the internet.

The wrapper is derived from
[maziggy/orca-slicer-api](https://github.com/maziggy/orca-slicer-api/tree/bambuddy/profile-resolver)
and remains under AGPL-3.0-or-later. OrcaSlicer is downloaded at build time
from its official v2.4.2 GitHub release; its SHA-256 digest is checked.

This package has been source-checked and Node-compiled on Windows. A full
Raspberry Pi 5 container build and an STL-to-3MF slice must be verified on
the target Home Assistant host before relying on it for printing.
