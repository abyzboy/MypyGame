import sched
import time

sch = sched.scheduler(time.time, time.sleep)
def fwa():
    for i in range(10):
        print(i)

print("hellow")
def ddw():
    sch.enter(10,1, fwa)
    sch.run()
ddw()
print("hellow")