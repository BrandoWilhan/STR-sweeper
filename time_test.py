import time
from timeMed import TimeMed

time_meditions = []

for i in range(10):
    t1 = time.time()
    for x in range(1, 10):
        print(x)
    t2 = time.time()
    td = (t2 - t1)*10**3 #time in miliseconds
    time_medition = TimeMed(td, "time_test", i)
    time_meditions.append(time_medition)

for timing in time_meditions:
    print(f"{timing.time} {timing.index}")