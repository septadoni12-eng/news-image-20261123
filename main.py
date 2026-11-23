#!/usr/bin/env python3
"""news-image-20261123 entrypoint.

The front-page image is the entry, and it already ships in this
repository as entry.png. This program only delivers it: it places an
exact copy of that file into the directory the grader points at, then
proves the delivery is byte-for-byte identical before reporting success.
Nothing is drawn, altered, downloaded, or generated here.
"""

import hashlib
import os
import shutil
import sys


def sha256_of(path):
    """Hex digest of a file, read in 1 MiB chunks."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def deliver(source_name="entry.png"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(script_dir, source_name)
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, source_name)

    if not os.path.isfile(source):
        print(f"missing source image: {source}", file=sys.stderr)
        return 2

    with open(source, "rb") as handle:
        magic = handle.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        print(f"not a PNG file, refusing to deliver: {source}", file=sys.stderr)
        return 2

    shutil.copyfile(source, target)

    source_bytes = os.path.getsize(source)
    target_bytes = os.path.getsize(target)
    if source_bytes != target_bytes:
        print(
            f"size mismatch after copy: source {source_bytes} bytes, "
            f"target {target_bytes} bytes",
            file=sys.stderr,
        )
        return 1
    if sha256_of(source) != sha256_of(target):
        print("sha256 mismatch after copy", file=sys.stderr)
        return 1

    print(f"wrote {target} ({target_bytes} bytes, sha256 verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(deliver())
