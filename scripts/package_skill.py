#!/usr/bin/env python3
"""
Package a skill folder into a .skill file (zip archive).

Usage:
    python scripts/package_skill.py skills/dev/repo-reconciler
    python scripts/package_skill.py skills/dev/repo-reconciler --output dist/
"""

import argparse
import zipfile
import os
import sys
from pathlib import Path


def package_skill(skill_path: str, output_dir: str = "dist") -> Path:
    skill_dir = Path(skill_path).resolve()

    if not skill_dir.is_dir():
        print(f"Error: '{skill_path}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        print(f"Error: No SKILL.md found in '{skill_path}'.", file=sys.stderr)
        sys.exit(1)

    skill_name = skill_dir.name
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    output_path = out_dir / f"{skill_name}.skill"

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in skill_dir.rglob("*"):
            if file.is_file():
                arcname = Path(skill_name) / file.relative_to(skill_dir)
                zf.write(file, arcname)
                print(f"  + {arcname}")

    print(f"\n✅ Packaged: {output_path}")
    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Package a skill into a .skill file.")
    parser.add_argument("skill_path", help="Path to the skill folder")
    parser.add_argument("--output", default="dist", help="Output directory (default: dist/)")
    args = parser.parse_args()

    package_skill(args.skill_path, args.output)
