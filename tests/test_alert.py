import json
import unittest
from unittest.mock import AsyncMock, Mock, patch

import requests

from func.alert import Alert


def response(payload, content_type=None):
    result = requests.Response()
    result.status_code = 200
    result._content = json.dumps(payload).encode()
    if content_type is not None:
        result.headers["Content-Type"] = content_type
    return result


class AlertTests(unittest.IsolatedAsyncioTestCase):
    async def test_missing_content_type_skips_poll(self):
        alert = Alert(Mock(), "dev")
        with patch("func.alert.requests.get", return_value=response({})) as get:
            await Alert.notice_alert.coro(alert)
        get.assert_called_once_with(alert.status_api_url, params={"game_code": "ps2", "name": "SolTech (Asia)"})
        alert.bot.get_guild.assert_not_called()

    async def test_non_json_content_type_skips_poll(self):
        alert = Alert(Mock(), "dev")
        with patch("func.alert.requests.get", return_value=response({}, "text/html")) as get:
            await Alert.notice_alert.coro(alert)
        self.assertEqual(get.call_count, 1)
        alert.bot.get_guild.assert_not_called()

    async def test_json_response_sends_population_chart(self):
        channel = Mock(purge=AsyncMock(), send=AsyncMock())
        bot = Mock()
        bot.get_guild.return_value.get_channel.return_value = channel
        alert = Alert(bot, "dev")
        status = response(
            {"game_server_status_list": [{"last_reported_state": "up"}]}, "application/json; charset=utf-8"
        )
        population = response({"result": [{"vs": 10, "nc": 20, "tr": 30, "ns": 5, "timestamp": 1700000000}]})
        with patch("func.alert.requests.get", side_effect=[status, population]):
            await Alert.notice_alert.coro(alert)
        channel.purge.assert_awaited_once_with(limit=1)
        channel.send.assert_awaited_once()
        sent = channel.send.await_args.kwargs
        self.assertIn("UP", sent["embed"].description)
        self.assertEqual(sent["file"].filename, "image.png")


if __name__ == "__main__":
    unittest.main()
