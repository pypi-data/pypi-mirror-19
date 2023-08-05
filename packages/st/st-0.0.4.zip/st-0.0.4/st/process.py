import threading
import multiprocessing


def process(target, args=(), finished=None):
    p = multiprocessing.Process(target=target, args=args)
    p.start()

    def check_finished():
        p.join()
        finished()

    threading.Thread(target=check_finished).start()
