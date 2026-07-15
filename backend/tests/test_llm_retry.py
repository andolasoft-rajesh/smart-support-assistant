import sys
from pathlib import Path
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.llm import _run_with_backoff


class RetryBackoffTests(unittest.TestCase):
    def test_retries_rate_limited_errors(self):
        attempts = {"count": 0}

        def flaky():
            attempts["count"] += 1
            if attempts["count"] < 3:
                raise RuntimeError("429 rate limit exceeded")
            return "ok"

        with patch("app.services.llm.time.sleep", return_value=None) as sleep_mock:
            result = _run_with_backoff(
                flaky,
                operation_name="test",
                max_attempts=3,
                base_delay=0.01,
            )

        self.assertEqual(result, "ok")
        self.assertEqual(attempts["count"], 3)
        self.assertEqual(sleep_mock.call_count, 2)


if __name__ == "__main__":
    unittest.main()
