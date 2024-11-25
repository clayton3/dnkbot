import unittest
from strategies.moving_average import moving_average_strategy
import pandas as pd

class TestStrategies(unittest.TestCase):
    def test_moving_average_strategy(self):
        # Mock data
        data = pd.DataFrame({
            'close': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        })
        result = moving_average_strategy(data, short_window=2, long_window=3)
        self.assertTrue('signal' in result.columns)

if __name__ == "__main__":
    unittest.main()