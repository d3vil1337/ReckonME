"""Foundation CLI; no network operations are implemented."""

import argparse

from reckonme import __version__


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="reckonme", description="ReckonME foundation. Recon is not yet implemented."
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.parse_args(argv)
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
