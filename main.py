"""Entry point for the AURMARA poster (make.fun bounty).

Copies the pre-rendered poster.png (drawn at build time by
draw_poster.py) to the harness output directory as entry.png.
Standard library only: no network, no extra dependencies.
"""
import os
import shutil
from pathlib import Path

MAX_BYTES = 1_048_576

HERE = Path(__file__).resolve().parent
SRC = HERE / "poster.png"


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    if not SRC.is_file():
        raise SystemExit("poster.png missing next to main.py")
    if SRC.stat().st_size > MAX_BYTES:
        raise SystemExit("poster.png exceeds the 1 MiB limit")
    dest = out_dir / "entry.png"
    shutil.copyfile(SRC, dest)
    # sanity: the copied file must be a real PNG within the size limit
    with open(dest, "rb") as fh:
        if fh.read(8) != b"\x89PNG\r\n\x1a\n":
            raise SystemExit("entry.png is not a valid PNG")
    print(f"wrote {dest} ({dest.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
