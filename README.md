# TimeTracer

A simple utility class for timing and tracing code execution. Mark operations and print elapsed times between them.

## Installation

Using uv-astral (recommended)
```bash
uv add timingtracer
```

Using pip
```bash
pip install timingtracer 
```

## Usage

### Basic usage

```python
from timingtracer import TimeTracer 

def calculate(iteration: int) -> int:
    sum = 0
    for i in range(iteration):
        sum += i

    return sum

tracer = TimeTracer("Plain Tracer")
tracer.start()

calculate(10**2)
tracer.mark("Short Operation")

calculate(10**4)
tracer.mark("Medium Operation")

tracer.end()
```

Output
```bash
[Plain Tracer] - Short Operation took 3.8µs
[Plain Tracer] - Medium Operation took 157.0µs
```

### Context manager

```python
from timetracer import TimeTracer

def calculate(iteration: int) -> int:
    sum = 0
    for i in range(iteration):
        sum += i

    return sum

sum1_limit = 10**6
sum2_limit = 10**8
with TimeTracer("Context Manager Tracer") as t:
    sum1 = calculate(sum1_limit) 
    sum2 = calculate(sum2_limit) 
    
    print("sum1", sum1)
    print("sum2", sum2)

    t.mark(f"calculate({sum1_limit}), calculate({sum2_limit}) and print results")```

Output
```bash
sum1 = 499999500000
sum2 = 4999999950000000
[Context Manager Tracer] - calculate(1000000), calculate(100000000) and print results took 1.881s
```

### Disable mode (debugging / production)

```python
from timetracer import TimeTracer

# All methods become no-ops when disabled
tracer = TimeTracer("My Tracer", disable=True)
tracer.start()
tracer.mark("Step 1")
tracer.end()  # does nothing
```
