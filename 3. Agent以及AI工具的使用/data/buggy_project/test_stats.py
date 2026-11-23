"""stats.py 的测试。运行：python3 -m unittest test_stats"""
import os
import tempfile
import unittest

from stats import best_loss

LOG = """[INFO] epoch=1 loss=12.4
[WARN] gpu_memory_high
[INFO] epoch=2 loss=9.75
[INFO] epoch=3 loss=8.1
"""


class TestBestLoss(unittest.TestCase):
    def test_best_loss(self):
        with tempfile.NamedTemporaryFile("w", suffix=".log", delete=False, encoding="utf-8") as f:
            f.write(LOG)
        try:
            self.assertEqual(best_loss(f.name), 8.1)
        finally:
            os.unlink(f.name)


if __name__ == "__main__":
    unittest.main()
