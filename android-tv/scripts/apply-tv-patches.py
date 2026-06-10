#!/usr/bin/env python3
"""Apply TV-only patches to apktool-decompiled v2RayTun source."""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

PATCHES = Path(__file__).resolve().parent.parent / "patches"


def patch_manifest(manifest: Path) -> None:
    text = manifest.read_text(encoding="utf-8")
    text = text.replace(
        '<uses-feature android:name="android.software.leanback" android:required="false"/>',
        '<uses-feature android:name="android.software.leanback" android:required="true"/>',
    )
    text = text.replace(
        "<category android:name=\"android.intent.category.LAUNCHER\"/>\n",
        "",
    )
    manifest.write_text(text, encoding="utf-8")


def patch_strings(strings_xml: Path) -> None:
    text = strings_xml.read_text(encoding="utf-8")
    text = text.replace(
        '<string name="app_name">v2RayTun</string>',
        '<string name="app_name">v2RayTun TV</string>',
    )
    strings_xml.write_text(text, encoding="utf-8")


def patch_is_tv_smali(smali: Path) -> None:
    """Force isTv() / F(Context) to always return true."""
    text = smali.read_text(encoding="utf-8")
    replacement = """.method public static F(Landroid/content/Context;)Z
    .locals 1

    const-string v0, "context"

    invoke-static {p0, v0}, Lkotlin/jvm/internal/Intrinsics;->checkNotNullParameter(Ljava/lang/Object;Ljava/lang/String;)V

    const/4 p0, 0x1

    return p0
.end method"""
    text, count = re.subn(
        r"\.method public static F\(Landroid/content/Context;\)Z.*?\.end method",
        replacement,
        text,
        count=1,
        flags=re.DOTALL,
    )
    if count != 1:
        raise RuntimeError(f"Failed to patch isTv method in {smali}")
    smali.write_text(text, encoding="utf-8")


def copy_tv_layouts(source_root: Path) -> None:
    tv_layout = source_root / "res" / "layout-television"
    layout = source_root / "res" / "layout"
    if not tv_layout.is_dir():
        raise RuntimeError(f"Missing {tv_layout}")
    for xml in tv_layout.glob("*.xml"):
        shutil.copy2(xml, layout / xml.name)


def copy_patch_drawables(source_root: Path) -> None:
    drawable = source_root / "res" / "drawable"
    for patch in (PATCHES / "drawable").glob("*.xml"):
        shutil.copy2(patch, drawable / patch.name)


def patch_navbar_colors(navbar_xml: Path) -> None:
  text = navbar_xml.read_text(encoding="utf-8")
  if "state_focused" in text:
    return
  insert = (
    '    <item android:state_focused="true" android:color="@color/color_fab_active" />\n'
  )
  text = text.replace("<selector\n", "<selector\n", 1)
  text = text.replace(
    "  xmlns:android=\"http://schemas.android.com/apk/res/android\">",
    "  xmlns:android=\"http://schemas.android.com/apk/res/android\">\n" + insert,
    1,
  )
  navbar_xml.write_text(text, encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <apktool-source-dir>", file=sys.stderr)
        return 1

    root = Path(sys.argv[1]).resolve()
    patch_manifest(root / "AndroidManifest.xml")
    patch_strings(root / "res" / "values" / "strings.xml")
    patch_is_tv_smali(root / "smali_classes2" / "w" / "A.smali")
    copy_tv_layouts(root)
    copy_patch_drawables(root)
    patch_navbar_colors(root / "res" / "drawable" / "navbar_item_color.xml")
    print(f"TV patches applied to {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
