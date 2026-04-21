# TimeTracer

A simple utility for timing code execution.

## Installation

Using uv (recommended)
```bash
uv add timingtracer
```

Using pip
```bash
pip install timingtracer
```

## Usage

### start/end

```python
from timingtracer import TimeTracer

tt = TimeTracer("MyModule")
tt.start("fetch data")
# ... code to measure ...
tt.end()
```

Output: `[MyModule] - fetch data took 10.5ms`

### Context manager

```python
from timingtracer import TimeTracer

with TimeTracer("MyModule", "fetch data"):
    # ... code to measure ...
    pass
```

Or with method chaining:
```python
with TimeTracer("MyModule").operation("fetch data"):
    # ... code to measure ...
    pass
```

Output: `[MyModule] - fetch data took 10.5ms`

### Get elapsed time

```python
tt = TimeTracer("MyModule")
tt.start("fetch data")
# ... code to measure ...
elapsed = tt.end()

print(f"It took {elapsed:.3f}s")
```

## API

- `TimeTracer(tracer="TimeTracer")` - Create a tracer with a name for your module
- `tt.start(operation_name)` - Start timing an operation
- `tt.end()` - Stop timing and print elapsed time
- `tt.elapsed` - Get elapsed time in seconds (after calling end())
- `tt.operation(name)` - Set operation name for context manager chaining