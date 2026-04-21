from timingtracer import TimeTracer
import time
tracer = TimeTracer("test")
tracer.start("Sleep 2")
time.sleep(2)
tracer.end()
