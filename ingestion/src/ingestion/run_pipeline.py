"""Run the ordered ingestion stages."""

from __future__ import annotations

import importlib
import logging
import os
import pathlib
from typing import Protocol, cast

from ingestion.config import Config

log = logging.getLogger(__name__)

STAGE_DIR = pathlib.Path(__file__).resolve().parent / "stages"
STAGES_PACKAGE = f"{__package__}.stages"


def setup_logging() -> None:
    logging.basicConfig(
        level=os.getenv("ING_LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


class Stage(Protocol):
    def run(self, ctx: object, cfg: Config) -> object:
        """Run the stage with the given context and configuration."""
        ...


def discover_and_load_stages() -> list[tuple[str, Stage]]:
    """Return fully-qualified module names for `s<n>_*.py`, ordered by n."""
    stages: list[tuple[int, str]] = []
    for path in STAGE_DIR.glob("s[0-9]*_*.py"):
        digits, _, _ = path.stem[1:].partition("_")
        if digits.isdigit():
            stages.append((int(digits), f"{STAGES_PACKAGE}.{path.stem}"))
    stage_names: list[str] = [name for _, name in sorted(stages)]
    loaded_stages: list[tuple[str, Stage]] = []
    for name in stage_names:
        module = importlib.import_module(name)
        if not hasattr(module, "run"):
            log.warning("module %s does not have a 'run' function", name)
        else:
            module = cast(Stage, module)
            loaded_stages.append((name, module))
    return loaded_stages


def main() -> int:
    setup_logging()
    log.info("running pipeline")

    cfg = Config.from_env()
    ctx: object = None
    stages = discover_and_load_stages()

    if not stages:
        log.warning("no stages found in %s", STAGE_DIR)
        return 1

    for module_name, module in stages:
        log.info("running stage %s", module_name)
        try:
            ctx = module.run(ctx, cfg)
        except Exception as e:
            log.error("error running stage %s: %s", module_name, e)
            return 1

    log.info("pipeline complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
