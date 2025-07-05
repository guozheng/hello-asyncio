import queue
from time import sleep

def task(name: str, work_queue: queue.Queue):
    if work_queue.empty():
        print(f"Task {name} found the queue to be empty")
    else:
        while not work_queue.empty():
            count = work_queue.get()
            total = 0
            print(f"Task {name} processing value {count} in the queue")
            for i in range(count):
                total += 1
            print(f"Task {name} total: {total}")

def main():
    work_queue = queue.Queue()
    for work in [15, 10, 5, 20]:
        work_queue.put(work)
    
    # task two never has a chance to run
    tasks = [(task, "One", work_queue), (task, "Two", work_queue)]

    for t, n, q in tasks:
        t(n, q)

if __name__ == "__main__":
    main()
    
    
        