"""Entry point for the news-image submission.

Copies the rendered front page (news.png, produced by render.py in this
same directory and committed alongside it) into the grader output
directory as entry.png. Standard library only; never writes into the
repository itself.
"""

import os
import shutil
import sys


def _source_path():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "news.png")


def _target_path():
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out:
        raise SystemExit("MAKEFUN_OUTPUT_DIR is not set")
    return os.path.join(out, "entry.png")


def main():
    src = _source_path()
    dst = _target_path()
    if not os.path.isfile(src):
        raise SystemExit("missing input: %s" % src)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)
    print("copied %s -> %s (%d bytes)" % (src, dst, os.path.getsize(dst)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
