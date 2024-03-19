"Homework 7. Tests for async URL Fetcher"

import unittest
from unittest.mock import patch, call, AsyncMock
from io import StringIO
import asyncio
import contextlib
import warnings
import time
import json

from aioresponses import aioresponses

import urls_fetcher

warnings.filterwarnings("ignore")


class TestFetcher(unittest.IsolatedAsyncioTestCase):
    "Class with Tests"

    @patch("asyncio.create_task", autospec=True)
    @patch("asyncio.Queue", autospec=True)
    @patch("async_fetcher.fetch_worker", spec=True)
    @patch("async_fetcher.url_producer", spec=True)
    async def test_main(self, mock_producer, mock_worker, mock_que, mock_create_task):
        "Tests main coroutine"

        mock_que.return_vlaue = AsyncMock()
        mock_que_instance = mock_que.return_value

        mock_task = mock_create_task.return_value

        await async_fetcher.main(5, "test.txt")

        mock_producer.assert_awaited_once_with(mock_que_instance, "test.txt")

        self.assertEqual(mock_worker.call_count, 5)
        mock_worker.assert_called_with(mock_que_instance)

        self.assertEqual(mock_create_task.call_count, 5)

        self.assertEqual(mock_task.cancel.call_count, 5)

    @patch("asyncio.Queue", autospec=True)
    async def test_producer(self, mock_que):
        "Tests producer coroutine"

        mock_que.return_vlaue = AsyncMock()
        mock_que_instance = mock_que.return_value

        mock_file = AsyncMock()
        mock_file.__aenter__.return_value = mock_file
        mock_file.__aiter__.return_value = ["url1", "url2"]

        with patch("aiofiles.open", autospec=True, return_value=mock_file) as mock_open:
            await async_fetcher.url_producer(mock_que_instance, "test.txt")

            mock_open.assert_called_once_with("test.txt", "r")

            mock_file.__aenter__.assert_awaited_once()
            mock_file.__aiter__.assert_called_once()

            mock_que_instance.put.assert_awaited()
            self.assertEqual(mock_que_instance.put.call_count, 2)
            self.assertEqual(
                mock_que_instance.put.call_args_list,
                [call.put("url1"), call.put("url2")],
            )

    @patch("asyncio.Queue", autospec=True)
    @patch("async_fetcher.fetch_url", spec=True)
    async def test_worker(self, mock_fetch, mock_que):
        "Tests worker coroutine"

        mock_que.return_vlaue = AsyncMock()
        mock_que_instance = mock_que.return_value
        urls_emul = ["url1", "url2"]
        mock_que_instance.get.side_effect = urls_emul

        results_emul = ["result1", "result2"]
        mock_fetch.side_effect = results_emul

        with patch("sys.stdout", new=StringIO()) as mock_out:
            try:
                await async_fetcher.fetch_worker(mock_que_instance)
            except StopAsyncIteration:
                pass

            for i in range(2):
                self.assertIn(
                    f"URL: {urls_emul[i]}    Result: {results_emul[i]}",
                    mock_out.getvalue(),
                )

        mock_que_instance.get.assert_awaited()
        self.assertEqual(mock_que_instance.get.call_count, 3)

        mock_fetch.assert_awaited()
        self.assertEqual(mock_fetch.call_count, 2)

    @aioresponses()
    def test_fetch_url(self, mocked_session):
        "Tests fetch_url"

        loop = asyncio.get_event_loop()

        mocked_session.get("http://example.com", status=200, payload="mocked response")
        result = loop.run_until_complete(async_fetcher.fetch_url("http://example.com"))
        self.assertEqual(result, async_fetcher.get_top_k("mocked response"))

        mocked_session.get("http://example.com", status=404)
        result = loop.run_until_complete(async_fetcher.fetch_url("http://example.com"))
        self.assertEqual(result, "HTTP Error: 404")

    def test_get_top_k(self):
        "Tests get_top_k"

        html = "Lets pretend this is html. words Lets words words"
        expected = json.dumps({"words": 3, "Lets": 2})
        self.assertEqual(expected, async_fetcher.get_top_k(html, 2))

    async def test_workers_productivity(self):
        "Tests more workers -> faster"

        mock_file = AsyncMock()
        mock_file.__aenter__.return_value = mock_file
        mock_file.__aiter__.return_value = ["https://docs.python.org"] * 20

        with patch("aiofiles.open", autospec=True, return_value=mock_file):
            with contextlib.redirect_stdout(None):
                with contextlib.redirect_stderr(None):
                    t_start = time.perf_counter()
                    await async_fetcher.main(2, "urls.txt")
                    t_end = time.perf_counter()
                    time_few_workers = t_end - t_start

                    t_start = time.perf_counter()
                    await async_fetcher.main(10, "urls.txt")
                    t_end = time.perf_counter()
                    time_many_workers = t_end - t_start

        self.assertGreater(time_few_workers, time_many_workers)