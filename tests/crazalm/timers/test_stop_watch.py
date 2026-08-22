import unittest
import time

from crazcalm.timers import StopWatch, StopWatchHasNotStartedException


class TestStopWatch(unittest.TestCase):
    def test_stop(self):
        watch = StopWatch()

        with self.assertRaises(StopWatchHasNotStartedException):
            watch.stop()

        watch.start()
        time.sleep(2.3)
        result = watch.stop()
        self.assertGreater(result, 0)
        self.assertEqual(result, watch.time)

    def test_pause(self):
        watch = StopWatch()

        with self.assertRaises(StopWatchHasNotStartedException):
            watch.pause()

        watch.start()
        time.sleep(1.5)
        time_1 = watch.time
        time.sleep(1.2)
        pause_1 = watch.pause()
        time.sleep(0.5)
        time_2 = watch.time
        watch.start()
        time.sleep(1.6)
        pause_2 = watch.pause()
        stop_time = watch.stop()

        self.assertGreater(pause_1, time_1)
        self.assertEqual(pause_1, time_2)
        self.assertGreater(pause_2, pause_1)
        self.assertEqual(pause_2, stop_time)

    def test_reset(self):
        watch = StopWatch()
        time_1 = watch.time
        watch.start()
        time.sleep(1.2)
        time_2 = watch.stop()
        watch.reset()
        time_3 = watch.time

        self.assertEqual(time_1, 0)
        self.assertGreater(time_2, time_1)
        self.assertEqual(time_3, time_1)
        


if __name__ == "__main__":
    unittest.main()