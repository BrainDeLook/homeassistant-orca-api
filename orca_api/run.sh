#!/bin/sh
set -eu

if [ -d /opt/orca/resources/profiles/BBL ]; then
  export BUNDLED_PROFILES_PATH=/opt/orca/resources/profiles/BBL
else
  profiles_dir="$(find /opt/orca -type d -path '*/resources/profiles/BBL' -print -quit)"
  if [ -n "$profiles_dir" ]; then
    export BUNDLED_PROFILES_PATH="$profiles_dir"
  fi
fi

exec node /app/dist/src/index.js
