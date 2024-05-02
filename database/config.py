# from __future__ import annotations
# from dataclasses import dataclass
# from environs import Env
#
#
# @dataclass
# class TgBot:
#     token: str
#     admin_ids: list[str]
#
#
# @dataclass
# class Config:
#     tg_bot: TgBot
#
#
# def load_config(path: str | None = None) -> Config:
#     env: Env = Env()
#     env.read_env(path)
#
#     return Config(
#         tg_bot=TgBot(
#             token="6156885677:AAH_SFmK_a2lPGKK2eLyN8mdwSj9YWgdOWQ",
#             admin_ids=["367150414"]
#         )
#     )
