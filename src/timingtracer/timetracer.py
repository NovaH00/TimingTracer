from __future__ import annotations
from typing import Self
import time

type TraceName = str
type TimeStamp = int | float
type DeltaTime = int | float

class TimeTracer:
    """A utility class for timing and tracing code execution.

    Provides methods to start a timer, mark operations, and print
    elapsed times. Supports usage as a context manager.
    """

    def __init__(self, name: str = "Time Tracer", *, disable: bool = False):
        """Initialize the TimeTracer.

        Args:
            name: Display name shown in trace output. Defaults to "Time Tracer".
            disable: If True, disables all methods rendering them as no-op. This is particularly useful for two scenarios:
                1. *Debugging* — toggle on/off verbose tracing without removing calls.
                2. *Production* — disable logging entirely to avoid overhead in performance-sensitive environments.
        """

        if disable:
            for name in dir(self):
                if name.startswith("_"):
                    continue

                attr = getattr(self, name)
                noop = lambda *_arg, **_kwargs: None
                if callable(attr):
                    setattr(self, name, noop)

        self._tracer_name = name
        self._is_inside_ctx_manager = False

    def _print_trace(self, name: TraceName, exec_time_second: DeltaTime) -> None:
        """Print a formatted trace message with the operation name and elapsed time."""
        fmt = f"{exec_time_second:.3f}s"  
        if exec_time_second < 1e-3:
            fmt = f"{exec_time_second*1e6:.1f}µs"
        elif exec_time_second < 1:
            fmt =  f"{exec_time_second*1e3:.2f}ms"

        print(f"[{self._tracer_name}] - {name} took {fmt}") 

    def start(self) -> None:
        """Start the timer and clear any previous traces.

        Call this before marking operations. Resets the internal trace list
        and records the start timestamp.
        """
        if self._is_inside_ctx_manager:
            print("WARNING: Calling .start() inside a context manager may produce unexpected timing. Use .mark() instead.")

        self._start_timestamp = time.perf_counter()
        self._traces: list[tuple[TraceName, TimeStamp]] = []

    def mark(self, operation: str = "Operation"):
        """Record a timestamp for the given operation name.

        Only records if the tracer has been started. If not yet started,
        prints a warning instead.

        Args:
            operation_name: Label for this trace point.
        """
        if hasattr(self, "_traces"): 
            self._traces.append((operation, time.perf_counter()))
        else:
            print("WARNING: Calling .mark() before starting the tracer — trace will not be recorded. Use .start() first.")

    def end(self) -> None:
        """Print all recorded traces and compute elapsed times.

        Iterates through the stored trace points, calculates the delta
        from each point to the previous one (including the initial start),
        and prints a formatted summary. Resets nothing — call ``start()``
        again to begin a fresh trace session.
        """
        if self._is_inside_ctx_manager:
            print("WARNING: Calling .end() inside a context manager may produce unexpected timing results")

        if not hasattr(self, "_traces"): 
            return

        # __start__ trace
        prev_trace_timestamp = self._start_timestamp 
         
        for trace in self._traces:
            curr_trace_name, curr_trace_timestamp = trace
            delta_time = curr_trace_timestamp - prev_trace_timestamp
            self._print_trace(curr_trace_name, delta_time)

            prev_trace_timestamp = curr_trace_timestamp

    def __enter__(self) -> Self:
        """Enter the context manager: start the timer."""
        self.start()
        self._is_inside_ctx_manager = True

        return self

    def __exit__(self, _exc_type, _exc_value, _traceback):
        """Exit the context manager: stop timing and print traces."""
        self._is_inside_ctx_manager = False
        self.end()
        return True 
