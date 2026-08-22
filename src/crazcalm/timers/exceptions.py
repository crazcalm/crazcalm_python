class TimerException(Exception):
    pass

class TimerStopValueMustBeInTheFutureException(TimerException):
    pass

class TimerStartTimeNotSpecifiedException(TimerException):
    pass

class TimerHasAlreadyStartedException(TimerException):
    pass

class TimerHasAlreadyFinishedException(TimerException):
    pass