import os
from multiprocessing import Pool

def task(number):
    print(f'This print number {number} from another process: {os.getpid()}', flush=True)


if __name__=='__main__':
    with Pool() as pool:
        some_numbers = [i for i in range(20)]
        async_processes = []
        for i in range(10):
            async_processes.append(pool.apply_async(task, args=[i]))
        for pr in async_processes:
            pr.wait() # если убрать, то программа раньше завершится, чем async процессы, и принтов не будет
            if pr.ready():
                print(f'{pr} is finished')
        
        # pool.map(task, some_numbers)
