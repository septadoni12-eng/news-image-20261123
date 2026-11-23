#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261123.

The submitted image is a broadsheet drawn in-session with Python/PIL
(see ../render23.py) from verified Monday 23 November 2026 reporting:
Democrats clinch 258 House seats, the world reacts to the COP31
collapse, Asia's tech rout, plus 45 more stories across 7 regions,
with a date-check box, a UTC timeline and a day-in-numbers strip.

This program does the rules-blessed simple thing: it copies the
committed entry.png to the output directory. No clock, no randomness,
no network, so two runs write identical bytes.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # Guard against a truncated copy: the output must be the committed
    # file byte for byte, so the sizes have to agree.
    if os.path.getsize(dst) != os.path.getsize(src):
        print(f"size mismatch: {src} vs {dst}", file=sys.stderr)
        return 1
    print(f"wrote {dst} ({os.path.getsize(dst)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
