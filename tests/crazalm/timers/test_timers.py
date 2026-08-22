import unittest
from datetime import datetime, timedelta
from time import sleep

from crazcalm.timers import (
    Timer,
    PausableTimer,
    TimerStopValueMustBeInTheFutureException,
    TimerStartTimeNotSpecifiedException,
    TimerHasAlreadyStartedException,
    TimerHasAlreadyFinishedException,
)


class TestPausableTimer(unittest.TestCase):
    def setUp(self):
        self.start = datetime(year=2026, month=12, day=25, hour=22)
        self.stop = timedelta(minutes=30)

    def test_is_finished(self):
        timer = PausableTimer(timedelta(seconds=3))
        timer.start()
        sleep(1)
        timer.pause()
        sleep(3)
        self.assertFalse(timer.is_finished())
        timer.resume()
        sleep(3)
        self.assertTrue(timer.is_finished())


    def test_pause_resume_stop(self):
        timer = PausableTimer(self.stop)
        timer.start()
        sleep(2)
        timer.pause()
        time_1 = timer.time_left()
        sleep(1)
        time_2 = timer.time_left()
        timer.resume()
        sleep(1.4)
        time_3 = timer.time_left()
        new_stop = timer.stop

        self.assertEqual(time_1, time_2)
        self.assertLess(time_3, time_2)
        self.assertGreater(new_stop, self.stop)
        


class TestTimer(unittest.TestCase):
    def setUp(self):
        self.start = datetime(year=2026, month=12, day=25, hour=22)
        self.stop = timedelta(minutes=30)

    def test_stop_property(self):
        expected_end = datetime(year=2026, month=12, day=25, hour=22, minute=30)

        timer = Timer(start=self.start, stop=self.stop)
        self.assertEqual(timer.end, expected_end)

        with self.assertRaises(TimerStopValueMustBeInTheFutureException):
            timer.stop = timedelta(minutes=-10)

    def test_end_proerty_error(self):
        timer = Timer(stop=self.stop)

        with self.assertRaises(TimerStartTimeNotSpecifiedException):
            timer.end


    def test_is_finished(self):
        future_timer = Timer(start=datetime.now(), stop=self.stop)
        past_timer = Timer(start=datetime.now() - timedelta(hours=1), stop=self.stop)

        self.assertTrue(past_timer.is_finished())
        self.assertFalse(future_timer.is_finished())

    def test_start(self):

        timer = Timer(stop=timedelta(seconds=2))
        timer.start()
        self.assertTrue(timer.started)
        self.assertFalse(timer.is_finished())

        with self.assertRaises(TimerHasAlreadyStartedException):
            timer.start()

        sleep(3)

        with self.assertRaises(TimerHasAlreadyFinishedException):
            timer.start()

        self.assertTrue(timer.is_finished())



if __name__ == "__main__":
    unittest.main()