import os
import sys
from multiprocessing import Process

def task():
    print(f"This is another process: {os.getpid()}", flush=True)


if __name__=='__main__':
    print(f'Main process id: {os.getpid()}')
    p = Process(target=task)
    p.start()
    p.join()
