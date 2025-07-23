import threading
from queue import Queue
import datetime as dt
from rich.live import Live
from rich.table import Table
import keyboard
import time


def gen_table(changeColor):
    duration = dt.datetime.now() - startTime
    hours = int(duration.seconds / 3600)
    minutes = int((duration.seconds % 3600) / 60)
    seconds = int((duration.seconds % 60))

    caption = (
        (f"{hours:02d}:" if hours > 0 else "") + f"{minutes:02d}:" + f"{seconds:02d}"
    )
    table = Table(
        title="Test table oooo spooky", caption=caption, caption_justify="left"
    )

    table.add_column("Now, I guess")
    table.add_row(
        f"{"[purple]" if changeColor else ""}{dt.datetime.now().strftime("%b_%d_%Y %H:%M:%S")}"
    )

    return table


def live_output(q, stop):
    colorChanged = False

    with Live(gen_table(colorChanged), refresh_per_second=4) as l:

        while not stop.is_set():
            time.sleep(0.2)

            if not q.empty():
                if q.get() == True:
                    colorChanged = not colorChanged

            l.update(gen_table(colorChanged))


def live_input(q, stop):
    while not stop.is_set():
        time.sleep(0.2)
        key = keyboard.read_key()
        # print(f"key: {key}")
        if key == "f":
            q.put(True)


startTime = dt.datetime.now()
q = Queue(10)
stopEvent = threading.Event()


try:
    ti = threading.Thread(target=live_input, args=(q, stopEvent))
    to = threading.Thread(target=live_output, args=(q, stopEvent))
    to.start()
    ti.start()
    # ti.run()

    while True:
        time.sleep(1)


except KeyboardInterrupt:
    print("Ok stopping...")
    stopEvent.set()
    ti.join(timeout=2)
    to.join(timeout=2)
    print("Done")
