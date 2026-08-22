from datetime import datetime, timedelta

from .exceptions import (
    TimerStopValueMustBeInTheFutureException,
    TimerStartTimeNotSpecifiedException,
    TimerHasAlreadyStartedException,
    TimerHasAlreadyFinishedException,
)
from .stop_watch import StopWatch


class Timer:
    def __init__(self, stop: timedelta, start: datetime | None = None):
        self.start_time = start
        self._stop = stop
        self.started = False

    @property
    def stop(self):
        return self._stop

    @stop.setter
    def stop(self, new: timedelta):
        if new <= timedelta():
            raise TimerStopValueMustBeInTheFutureException()

        self._stop = new

    @property
    def end(self):
        if self.start_time is None:
            raise TimerStartTimeNotSpecifiedException() 
        return self.start_time + self.stop

    def start(self):
        if self.start_time is None:
            self.start_time = datetime.now()

        elif self.is_finished():
            raise TimerHasAlreadyFinishedException()

        elif self.started:
            raise TimerHasAlreadyStartedException

        self.started = True

    def is_finished(self):
        return datetime.now() >= self.end

    def time_left(self):
        return self.end - datetime.now()

    def reset(self):
        self.started = False
        self.start_time = None


class PausableTimer(Timer):
    StopWatch = StopWatch
    def __init__(self, stop: timedelta, start = None):
        super().__init__(stop, start)
        self._paused = False
        self._pause_time = None
        self._time_left_cache = None
        self._stop_watch = StopWatch()

    def time_left(self):
        if self._time_left_cache:
            return self._time_left_cache
        return super().time_left()

    def pause(self):
        self._paused = True
        self._pause_time = datetime.now()
        self._time_left_cache = super().time_left()
        self._stop_watch.start()

    def resume(self):
        self._paused = False
        self._pause_time = None
        self._time_left_cache = None
        self.stop += timedelta(seconds=self._stop_watch.stop())
        self._stop_watch.reset()

    def is_finished(self):
        if self._paused:
            return self._pause_time >= self.end
        return super().is_finished()
    

    