FROM node:22-bookworm AS api-build

WORKDIR /build
COPY package.json package-lock.json ./
RUN npm ci
COPY tsconfig.json ./
COPY src ./src
RUN npm run build && npm prune --omit=dev

FROM ubuntu:24.04 AS slicer-build
ARG BUILD_ARCH
ARG ORCA_VERSION=2.4.2
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /opt
RUN set -eu; \
    case "$BUILD_ARCH" in \
      aarch64) ASSET="OrcaSlicer_Linux_AppImage_Ubuntu2404_aarch64_V${ORCA_VERSION}.AppImage"; \
               SHA256="e1a07275a25f176626c55a5df39e91bc4476d8c28ee4a3192ff758e29dd5c3ba" ;; \
      amd64) ASSET="OrcaSlicer_Linux_AppImage_Ubuntu2404_V${ORCA_VERSION}.AppImage"; \
             SHA256="d12fb8c8eac1aecd2dfb6377acd48f994f8fa439ed5292fa532dd82880f029fd" ;; \
      *) echo "Unsupported BUILD_ARCH: $BUILD_ARCH" >&2; exit 1 ;; \
    esac; \
    curl -fL --retry 3 -o /tmp/orca.AppImage \
      "https://github.com/OrcaSlicer/OrcaSlicer/releases/download/v${ORCA_VERSION}/${ASSET}"; \
    echo "${SHA256}  /tmp/orca.AppImage" | sha256sum -c -; \
    chmod +x /tmp/orca.AppImage; \
    /tmp/orca.AppImage --appimage-extract; \
    test -x /opt/squashfs-root/AppRun; \
    rm /tmp/orca.AppImage

FROM ubuntu:24.04
ARG BUILD_VERSION
ARG BUILD_ARCH
LABEL io.hass.version="${BUILD_VERSION}" \
      io.hass.type="app" \
      io.hass.arch="${BUILD_ARCH}" \
      org.opencontainers.image.source="https://github.com/BrainDeLook/homeassistant-orca-api"

ENV DEBIAN_FRONTEND=noninteractive \
    NODE_ENV=production \
    PORT=3000 \
    DATA_PATH=/data \
    ORCASLICER_PATH=/opt/orca/AppRun

RUN apt-get update && apt-get install -y --no-install-recommends \
      ca-certificates libgl1 libgl1-mesa-dri libegl1 libopengl0 libglu1-mesa \
      libsm6 libice6 libmspack0 libgtk-3-0t64 \
      libgstreamer1.0-0 libgstreamer-plugins-base1.0-0 \
      libwebkit2gtk-4.1-0 fonts-dejavu-core findutils \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /app /data

COPY --from=api-build /usr/local/bin/node /usr/local/bin/node
COPY --from=api-build /build/dist /app/dist
COPY --from=api-build /build/node_modules /app/node_modules
COPY --from=api-build /build/package.json /app/package.json
COPY --from=slicer-build /opt/squashfs-root /opt/orca
COPY run.sh /usr/local/bin/run-orca-api
RUN chmod +x /usr/local/bin/run-orca-api \
    && node --version \
    && test -x /opt/orca/AppRun \
    && test -f /app/dist/src/index.js

WORKDIR /app
EXPOSE 3000
CMD ["/usr/local/bin/run-orca-api"]
