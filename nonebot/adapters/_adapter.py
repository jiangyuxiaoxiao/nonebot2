import abc
from typing import Any, Dict

from ._bot import Bot
from nonebot.config import Config
from nonebot.drivers import (
    Driver,
    ForwardDriver,
    ReverseDriver,
    HTTPServerSetup,
    WebSocketServerSetup,
)


class Adapter(abc.ABC):
    def __init__(self, driver: Driver, **kwargs: Any):
        self.driver: Driver = driver
        self.bots: Dict[str, Bot] = {}

    @classmethod
    @abc.abstractmethod
    def get_name(cls) -> str:
        raise NotImplementedError

    @property
    def config(self) -> Config:
        return self.driver.config

    def bot_connect(self, bot: Bot):
        self.driver._bot_connect(bot)
        self.bots[bot.self_id] = bot

    def bot_disconnect(self, bot: Bot):
        self.driver._bot_disconnect(bot)
        self.bots.pop(bot.self_id, None)

    def setup_http_server(self, setup: HTTPServerSetup):
        if not isinstance(self.driver, ReverseDriver):
            raise TypeError("Current driver does not support http server")
        self.driver.setup_http_server(setup)

    def setup_websocket_server(self, setup: WebSocketServerSetup):
        if not isinstance(self.driver, ReverseDriver):
            raise TypeError("Current driver does not support websocket server")
        self.driver.setup_websocket_server(setup)

    @abc.abstractmethod
    async def _call_api(self, api: str, **data) -> Any:
        """
        :说明:

          ``adapter`` 实际调用 api 的逻辑实现函数，实现该方法以调用 api。

        :参数:

          * ``api: str``: API 名称
          * ``**data``: API 数据
        """
        raise NotImplementedError