#!/usr/bin/env python3
import os
import argparse

def rename_files_sorted_by_ctime(directory=".", dry_run=False):
    # 1. Get all files in the chosen directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    # 2. Sort by ctime (creation/change time)
    files.sort(key=lambda f: os.path.getctime(os.path.join(directory, f)))

    # 3. Rename them with numbers
    for i, f in enumerate(files, start=1):
        name, ext = os.path.splitext(f)
        new_name = f"{i}_{name}{ext}"

        old_path = os.path.join(directory, f)
        new_path = os.path.join(directory, new_name)

        if dry_run:
            print(f"[DRY-RUN] Would rename: {old_path} -> {new_path}")
        else:
            print(f"Renaming: {old_path} -> {new_path}")
            os.rename(old_path, new_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Rename files in a directory by adding numbers based on creation/change time."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to process (default: current directory)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without renaming files"
    )

    args = parser.parse_args()

    rename_files_sorted_by_ctime(args.directory, args.dry_run)
