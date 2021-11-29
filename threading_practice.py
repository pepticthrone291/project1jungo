import threading
import time

people = {}


def jobs(stri, num):
    done = f"{stri} {num}"
    print(f"{done} is dancing.")
    global people
    people[num] = done
    return


threads = []
for i in range(30):
    t = threading.Thread(target=jobs, args=("indian", i))
    t.start()
    threads.append(t)
for thread in threads:
    thread.join()

people = sorted(people.items(), reverse=True)
fnl = []
for k in range(len(people)):
    element = people[k][1]
    fnl.append(element)

print(fnl)
