# Bambuddy OrcaSlicer API

This app runs OrcaSlicer 2.4.2 behind a Bambuddy-compatible REST API.

1. Start the app.
2. Open `http://<HOME_ASSISTANT_IP>:3003/health` in a browser. The response
   should say `"status":"healthy"`.
3. In Bambuddy, open Settings → Workflow, select **OrcaSlicer**, enable
   **Use Slicer API**, and enter `http://<HOME_ASSISTANT_IP>:3003` as the
   sidecar URL.

The first install builds the image on the Home Assistant host and downloads
the official OrcaSlicer AppImage. This can take several minutes on a Pi 5.

The API has no authentication. Do not expose TCP port 3003 to the internet.

If the health check is unhealthy, inspect this app's logs. If OrcaSlicer is
missing or cannot run, include the full health JSON and app log when reporting
the problem.
