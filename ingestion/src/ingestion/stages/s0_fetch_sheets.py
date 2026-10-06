import os
import pathlib

from ingestion.config import Config


def run(ctx: object, cfg: Config) -> list[str]:
    basepath = str(pathlib.Path(__file__).parent.absolute() / "data/sheets/")
    return [sheet for sheet in os.listdir(basepath) if sheet.split(".")[-1] in ["xls", "xlsx"]]
