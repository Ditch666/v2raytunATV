#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TOOLS="$ROOT/tools"
BUILD="$ROOT/build/android-tv"
APK_URL="${APK_URL:-https://github.com/DigneZzZ/v2raytun/releases/latest/download/v2RayTun_universal.apk}"
SOURCE_APK="${SOURCE_APK:-$BUILD/input/v2RayTun.apk}"
PATCHED_SOURCE="$BUILD/apktool-source"
OUTPUT_APK="$BUILD/output/v2RayTun-tv.apk"
KEYSTORE="$BUILD/debug.keystore"

mkdir -p "$BUILD/input" "$BUILD/output"

if [[ ! -f "$SOURCE_APK" ]]; then
  echo "Downloading APK from GitHub..."
  curl -fsSL "$APK_URL" -o "$SOURCE_APK"
fi

if [[ ! -f "$TOOLS/apktool.jar" ]]; then
  echo "Missing $TOOLS/apktool.jar — run setup from repository README."
  exit 1
fi

echo "Decompiling APK..."
rm -rf "$PATCHED_SOURCE"
java -jar "$TOOLS/apktool.jar" d "$SOURCE_APK" -o "$PATCHED_SOURCE" -f

echo "Applying TV-only patches..."
python3 "$ROOT/android-tv/scripts/apply-tv-patches.py" "$PATCHED_SOURCE"

echo "Building TV APK..."
java -jar "$TOOLS/apktool.jar" b "$PATCHED_SOURCE" -o "$BUILD/output/unsigned.apk"

if [[ ! -f "$KEYSTORE" ]]; then
  echo "Creating debug keystore..."
  keytool -genkeypair -v \
    -keystore "$KEYSTORE" \
    -alias v2raytun-tv \
    -keyalg RSA -keysize 2048 -validity 10000 \
    -storepass android -keypass android \
    -dname "CN=v2RayTun TV, OU=Dev, O=v2raytun, L=Unknown, S=Unknown, C=US"
fi

echo "Signing APK..."
if command -v apksigner >/dev/null 2>&1; then
  apksigner sign \
    --ks "$KEYSTORE" \
    --ks-pass pass:android \
    --key-pass pass:android \
    --out "$OUTPUT_APK" \
    "$BUILD/output/unsigned.apk"
else
  jarsigner -verbose \
    -sigalg SHA256withRSA -digestalg SHA-256 \
    -keystore "$KEYSTORE" \
    -storepass android -keypass android \
    "$BUILD/output/unsigned.apk" v2raytun-tv
  cp "$BUILD/output/unsigned.apk" "$OUTPUT_APK"
fi

echo "Done: $OUTPUT_APK"
ls -lh "$OUTPUT_APK"
