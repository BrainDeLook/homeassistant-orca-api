"""Exercise the HTTP boundary and the Orca CLI with a tiny printable cube."""

from pathlib import Path
import urllib.error
import urllib.request


vertices = [
    (0, 0, 0), (10, 0, 0), (10, 10, 0), (0, 10, 0),
    (0, 0, 10), (10, 0, 10), (10, 10, 10), (0, 10, 10),
]
faces = [
    (0, 2, 1), (0, 3, 2), (4, 5, 6), (4, 6, 7),
    (0, 1, 5), (0, 5, 4), (1, 2, 6), (1, 6, 5),
    (2, 3, 7), (2, 7, 6), (3, 0, 4), (3, 4, 7),
]
stl = ["solid cube\n"]
for a, b, c in faces:
    stl.append("facet normal 0 0 0\n outer loop\n")
    for index in (a, b, c):
        stl.append("vertex %s %s %s\n" % vertices[index])
    stl.append("endloop\nendfacet\n")
stl.append("endsolid cube\n")

profiles = Path("smoke-profiles")
boundary = "orca-api-smoke-boundary"
parts = [
    ("file", "cube.stl", "".join(stl).encode("ascii"), "model/stl"),
    ("printerProfile", "printer.json", (profiles / "printer.json").read_bytes(), "application/json"),
    ("presetProfile", "process.json", (profiles / "process.json").read_bytes(), "application/json"),
    ("filamentProfile", "filament.json", (profiles / "filament.json").read_bytes(), "application/json"),
]
body = bytearray()
for name, filename, data, mime in parts:
    body.extend(
        f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"; '
        f'filename="{filename}"\r\nContent-Type: {mime}\r\n\r\n'.encode()
    )
    body.extend(data)
    body.extend(b"\r\n")
body.extend(f'--{boundary}\r\nContent-Disposition: form-data; name="exportType"\r\n\r\n3mf\r\n'.encode())
body.extend(f"--{boundary}--\r\n".encode())

request = urllib.request.Request(
    "http://127.0.0.1:3003/slice",
    data=bytes(body),
    headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    method="POST",
)
try:
    with urllib.request.urlopen(request, timeout=240) as response:
        result = response.read()
        assert response.status == 200
        assert result.startswith(b"PK"), "3MF must be a ZIP archive"
        assert len(result) > 1000, "3MF output is unexpectedly small"
        print(f"Slice passed: HTTP {response.status}, {len(result)} bytes")
except urllib.error.HTTPError as error:
    print(error.read().decode(errors="replace")[:5000])
    raise
