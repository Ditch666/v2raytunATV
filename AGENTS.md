# AGENTS.md

## Repository overview

This repository (`v2raytunATV`) is a **README-only distribution mirror** for the **v2raytun** VPN/proxy client. It does not contain application source code, build tooling, tests, or runtime services.

- **Product**: v2raytun — cross-platform client (Android APK, Windows installer) built around the xray core.
- **Upstream releases**: https://github.com/DigneZzZ/v2raytun/releases
- **Tracked content**: `README.md` with release notes and download links.

There is nothing to `npm install`, `gradle build`, `docker compose up`, or run as a local dev server in this workspace.

## What “working” means here

Validation for this repo is about **distribution integrity**, not compiling or running the client in the VM:

1. README renders and links resolve.
2. Release asset URLs (especially the Android APK) return HTTP 200 and valid binaries.
3. Optional: compare README version notes against the latest GitHub release tag.

The v2raytun client itself runs on **Android devices/emulators** or **Windows**; it is not runnable as a native Linux server process in this cloud VM.

## Cursor Cloud specific instructions

### No install step

The VM update script is a no-op (`true`). There are no language runtimes or package managers tied to this repository.

### Lint / test / build

| Step   | Command | Notes |
|--------|---------|-------|
| Lint   | N/A     | No linters configured |
| Test   | N/A     | No test suite |
| Build  | N/A     | No build system |

### Manual verification (recommended hello-world)

From the repo root, verify README links and the primary release artifact:

```bash
python3 - <<'PY'
import re, subprocess, tempfile, urllib.request, ssl
from pathlib import Path

readme = Path("README.md").read_text()
apk_urls = [u for u in re.findall(r'https://[^\s\)\]]+', readme) if u.endswith('.apk')]
ctx = ssl.create_default_context()

for apk_url in apk_urls:
    req = urllib.request.Request(apk_url, method='HEAD', headers={'User-Agent': 'validate/1'})
    with urllib.request.urlopen(req, context=ctx) as r:
        assert r.status == 200, apk_url
    with tempfile.NamedTemporaryFile(suffix='.apk') as tmp:
        subprocess.check_call([
            'curl', '-fsSL', apk_url, '-o', tmp.name,
            '--range', '0-1048575',
        ])
        out = subprocess.check_output(['file', '-b', tmp.name], text=True)
        assert 'Android package' in out, (apk_url, out)
    print('OK:', apk_url)
PY
```

To inspect the latest release tag and assets via GitHub API:

```bash
curl -s https://api.github.com/repos/DigneZzZ/v2raytun/releases/latest | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['tag_name']); print([a['name'] for a in d['assets']])"
```

### Known README caveats

- The Windows installer link in `README.md` (`v2RayTun_Setup.exe`) may 404 when the latest GitHub release only publishes the Android APK (e.g. tag `5.23.73` at time of writing).
- `https://databridges.tech` has been observed to reset connections from some networks; other project links remain valid.

### Running the actual application

End-to-end client testing requires:

1. Install the APK on Android (or the Windows build on Windows).
2. Import a valid xray/v2ray JSON configuration.
3. Connect to a reachable proxy server.

Source code and build instructions are not in this repository; see https://docs.v2raytun.com/ and https://t.me/v2raytun for product support.
