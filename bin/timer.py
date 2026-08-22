from datetime import timedelta
from time import sleep

from crazcalm.timers import Timer
from crazcalm import terminal

def main():
    timer = Timer(stop=timedelta(minutes=1))

    timer.start()
    while(timer.is_finished() == False):
        print(timer.time_left())
        sleep(0.5)
        terminal.clear()
    print("Timer is up!")
    terminal.beep()


if __name__ == "__main__":
    main()