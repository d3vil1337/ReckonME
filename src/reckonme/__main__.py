"""Foundation CLI; no network operations are implemented."""

import argparse
import sys

from reckonme import __version__
from reckonme.config import ConfigError, load_config
from reckonme.scope import ScopeError
from reckonme.targets import TargetError


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="reckonme", description="ReckonME offline scope validation. Recon is not yet implemented."
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    commands = parser.add_subparsers(dest="command")
    validate = commands.add_parser("validate-config", help="Validate a TOML configuration offline")
    validate.add_argument("--config", required=True)
    check = commands.add_parser("check-scope", help="Validate and check one target offline")
    check.add_argument("--config", required=True)
    check.add_argument("target")
    args = parser.parse_args(argv)
    if args.command:
        try:
            config = load_config(args.config)
            if args.command == "validate-config":
                print("Configuration valid.")
            else:
                target = config.scope.require_allowed(args.target)
                print(f"Allowed: {target.normalized}")
            return 0
        except ScopeError as exc:
            print(f"Out of scope: {exc}", file=sys.stderr)
            return 1
        except (ConfigError, TargetError) as exc:
            parser.error(str(exc))
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
