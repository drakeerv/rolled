import os
from dataclasses import dataclass
from typing import Literal, Self


class ConfigError(RuntimeError):
    """Raised when there is a configuration error."""


def _require(name: str) -> str:
    value = os.getenv(name)
    if value is None or value == "":
        raise ConfigError(f"missing required environment variable: {name}")
    return value


@dataclass(frozen=True)
class PostgresConfig:
    host: str
    port: int
    username: str
    password: str
    database: str

    @classmethod
    def from_env(cls) -> Self:
        return cls(
            host=_require("ING_POSTGRES_HOST"),
            port=int(_require("ING_POSTGRES_PORT")),
            username=_require("ING_POSTGRES_USERNAME"),
            password=_require("ING_POSTGRES_PASSWORD"),
            database=_require("ING_POSTGRES_DATABASE"),
        )


@dataclass(frozen=True)
class TypesenseNode:
    host: str
    port: int
    protocol: Literal["http", "https"]

    @classmethod
    def from_env(cls) -> Self:
        protocol = _require("ING_TYPESENSE_PROTO")
        if protocol not in ("http", "https"):
            raise ConfigError(f"ING_TYPESENSE_PROTO must be http or https, got {protocol!r}")
        return cls(
            host=_require("ING_TYPESENSE_HOST"),
            port=int(_require("ING_TYPESENSE_PORT")),
            protocol=protocol,  # type narrowed to the Literal
        )


@dataclass(frozen=True)
class Config:
    postgres: PostgresConfig
    typesense_node: TypesenseNode
    typesense_apikey: str
    typesense_searchkey: str

    @classmethod
    def from_env(cls) -> Self:
        return cls(
            postgres=PostgresConfig.from_env(),
            typesense_node=TypesenseNode.from_env(),
            typesense_apikey=_require("ING_TYPESENSE_BOOTSTRAP_API_KEY"),
            typesense_searchkey=_require("ING_TYPESENSE_SEARCH_API_KEY"),
        )
