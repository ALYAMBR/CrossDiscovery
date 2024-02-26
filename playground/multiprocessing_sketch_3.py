from multiprocessing import Process, Queue
import os
import time

def download_batches(queue):
    for i in range(5):  # Example: Download 5 batches
        print(f"Downloading batch {i}", flush=True)
        time.sleep(1)  # Simulate time taken to download
        queue.put(f"Batch {i}")
    queue.put(None)  # Sentinel value to indicate completion

def process_batch(queue):
    while True:
        batch = queue.get()
        if batch is None:  # Check for sentinel value
            queue.put(None)  # Put it back for other processes
            break
        print(f"Processing {batch}", flush=True)
        time.sleep(5)  # Simulate processing time

if __name__ == "__main__":
    # Create a Queue
    queue = Queue()

    # Start the batch downloading process
    downloader = Process(target=download_batches, args=(queue,))
    downloader.start()

    # Create and start worker processes
    num_workers = 2  # Adjust as needed
    workers = []
    for _ in range(num_workers):
        worker = Process(target=process_batch, args=(queue,))
        worker.start()
        workers.append(worker)

    # Wait for the downloader process to finish
    downloader.join()

    # Wait for all worker processes to finish
    for worker in workers:
        worker.join()