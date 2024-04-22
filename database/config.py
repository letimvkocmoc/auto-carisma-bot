from __future__ import annotations

from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: list[str]


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(tg_bot=TgBot(
        token=env('BOT_TOKEN'),
        admin_ids=list(map(str, env.list('ADMIN_IDS'))))
    )
