import time


class StopWatchHasNotStartedException(Exception):
    pass


class StopWatch:
    def __init__(self):
        self._start_time = None
        self._is_paused = False
        self._times = []

    @property
    def time(self):
        if self._start_time is None and self._times:
            return sum(self._times)
        elif self._start_time is None:
            return 0
        return sum(self._times) + (time.monotonic() - self._start_time)

    def start(self):
        self._start_time = time.monotonic()
        self._is_paused = False

    def pause(self):
        if self._start_time is None:
            raise StopWatchHasNotStartedException()
        self._times.append(self.stop())
        self._start_time = None
        self._is_paused = True
        return self.time

    def stop(self):
        result = self.time
        if self._start_time is None and not self._is_paused:
            raise StopWatchHasNotStartedException()
        elif not self._is_paused:
            end_time = time.monotonic() - self._start_time
            self._times.append(end_time)
            self._start_time = None
            result = end_time
        return result

    def reset(self):
        self._start_time = None
        self._times = []