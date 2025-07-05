import queue
from codetiming import Timer
from time import sleep


def task(name: str, work_queue: queue.Queue):
    # notice the double curly braces here, it is used for escaping the braces, 
    # so that the format string is not evaluated by the Timer class
    timer = Timer(text=f"Task {name} elapsed time: {{:.2f}} seconds")
    if work_queue.empty():
        print(f"Task {name} found the queue to be empty")
    else:
        while not work_queue.empty():
            timer.start()
            delay_sec = work_queue.get()
            print(f"Task {name} sleeping for {delay_sec} seconds")
            sleep(delay_sec)
            timer.stop()
            yield # yield control back to the scheduler

def main():
    work_queue = queue.Queue()
    for work in [1, 2, 3, 4]:
        work_queue.put(work)
    
    # each task is a generator now
    tasks = [task("One", work_queue), task("Two", work_queue)]

    done = False
    with Timer(text=f"Total elapsed time: {{:.2f}} seconds"):
        while not done:
            for t in tasks:
                try:
                    next(t) # gives control back to the task
                except StopIteration:
                    tasks.remove(t) # this task is done
            if len(tasks) == 0:
                done = True

if __name__ == "__main__":
    main()