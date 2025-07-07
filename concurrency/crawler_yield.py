import queue
import requests
from codetiming import Timer

def task(name: str, work_queue: queue.Queue):
    timer = Timer(text=f"Task {name} elapsed time: {{:.2f}} seconds")
    while not work_queue.empty():
        url = work_queue.get()
        print(f"Task {name} running: url={url}")
        timer.start()
        response = requests.get(url)
        print(f"Response: {response.text}")
        timer.stop()
        yield


def main():
    work_queue = queue.Queue()
    for url in [
        "https://httpbin.org/get?name=one",
        "https://httpbin.org/get?name=two",
        "https://httpbin.org/get?name=three",
        "https://httpbin.org/get?name=four",
    ]:
        work_queue.put(url)
    
    tasks = [task("One", work_queue), task("Two", work_queue)]
    done = False
    with Timer(text=f"Total elapsed time: {{:.2f}} seconds"):
        while not done:
            for t in tasks:
                try:
                    next(t)
                except StopIteration:
                    tasks.remove(t)
            if len(tasks) == 0:
                done = True

if __name__ == "__main__":
    main()