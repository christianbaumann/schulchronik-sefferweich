#!/usr/bin/env python3
"""Phase 1: Prepare raw scans for transcription.

Copies raw photos to Scans/ with sequential naming, updates
raw_mapping.json, moves originals to Scans/raw/done/.

Usage:
    python3 Scripts/prepare_scans.py                  # Process all new raw files
    python3 Scripts/prepare_scans.py --start-page 55  # Override start page
    python3 Scripts/prepare_scans.py --dry-run         # Preview only
"""

import argparse, glob, json, os, shutil, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(SCRIPT_DIR, "..")
SCANS_DIR = os.path.join(ROOT, "Scans")
RAW_DIR = os.path.join(SCANS_DIR, "raw")
DONE_DIR = os.path.join(RAW_DIR, "done")
MAPPING_FILE = os.path.join(SCANS_DIR, "raw_mapping.json")

def next_page_number():
    """Determine next page number from existing scans."""
    existing = glob.glob(os.path.join(SCANS_DIR, "[0-9][0-9][0-9].jpg"))
    if not existing:
        return 0
    nums = [int(os.path.basename(f)[:3]) for f in existing]
    return max(nums) + 1

def main():
    parser = argparse.ArgumentParser(description="Prepare raw scans")
    parser.add_argument("--start-page", type=int, default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    # Find new raw files (exclude done/)
    raw_files = sorted(
        f for f in glob.glob(os.path.join(RAW_DIR, "*.*"))
        if os.path.isfile(f) and not f.startswith(DONE_DIR)
           and f.lower().endswith((".jpg", ".jpeg", ".png"))
    )

    if not raw_files:
        print("No new raw files found in Scans/raw/")
        return

    page_num = args.start_page if args.start_page is not None else next_page_number()

    # Load existing mapping
    if os.path.exists(MAPPING_FILE):
        with open(MAPPING_FILE, encoding="utf-8") as f:
            mapping = json.load(f)
    else:
        mapping = {}

    os.makedirs(DONE_DIR, exist_ok=True)

    for raw_file in raw_files:
        target_name = f"{page_num:03d}.jpg"
        target_path = os.path.join(SCANS_DIR, target_name)
        raw_name = os.path.basename(raw_file)

        if args.dry_run:
            print(f"  {raw_name} -> {target_name}")
        else:
            shutil.copy2(raw_file, target_path)
            mapping[target_name] = raw_name
            shutil.move(raw_file, os.path.join(DONE_DIR, raw_name))
            print(f"  {raw_name} -> {target_name}")

        page_num += 1

    if not args.dry_run:
        with open(MAPPING_FILE, "w", encoding="utf-8") as f:
            json.dump(mapping, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"Updated {MAPPING_FILE}")
    else:
        print(f"(dry run — {len(raw_files)} files would be processed)")

if __name__ == "__main__":
    main()
