"""Ordered ingestion stages.

Each ``s<n>_<name>.py`` module exposes ``run(ctx, cfg)`` and is executed in
numeric order by :mod:`ingestion.run_pipeline`.
"""
