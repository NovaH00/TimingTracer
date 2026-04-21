from __future__ import annotations
import time
from typing import Optional

class TimeTracer:
    """A simple time tracer for measuring code execution time.

    Usage::

        # Method 1: start/end
        tt = TimeTracer("MyModule")
        tt.start("fetch data")
        # ... code to measure ...
        tt.end()

        # Method 2: context manager (recommended)
        with TimeTracer("MyModule", "fetch data"):
            # ... code to measure ...
            pass

        # Or with method chaining
        with TimeTracer("MyModule").operation("fetch data"):
            # ... code to measure ...
            pass
    """

    def __init__(self, tracer: str = "TimeTracer"):
        """Initialize the TimeTracer.

        Args:
            tracer: Name of the module/component (shown in brackets).
            operation: Name of the operation being measured (for context manager).
        """
        self._tracer = tracer
        self._operation: str 
        self._start_time: float
        self._elapsed: float

    def start(self, operation_name: str = "Operation") -> None:
        """Start the timer with an operation name.

        Args:
            operation: Name describing the block being measured.
        """
        self._operation = operation_name 
        self._start_time = time.perf_counter()

    def end(self) -> float:
        """Stop the timer and print the elapsed time.

        Returns:
            The elapsed time in seconds.
        """
        if self._start_time is None:
            raise RuntimeError("start() must be called before end()")

        self._elapsed = time.perf_counter() - self._start_time
        self._print_elapsed()
        return self._elapsed

    def _print_elapsed(self) -> None:
        """Print a formatted elapsed time."""
        dt = self._elapsed
        if dt < 1e-3:
            fmt = f"{dt * 1e6:.1f}µs"
        elif dt < 1:
            fmt = f"{dt * 1e3:.2f}ms"
        else:
            fmt = f"{dt:.3f}s"

        print(f"[{self._tracer}] - {self._operation} took {fmt}")

    @property
    def elapsed(self) -> Optional[float]:
        """Return the elapsed time after end() has been called."""
        return self._elapsed

    def __enter__(self) -> "TimeTracer":
        """Context manager entry — starts the timer."""
        if self._operation is None:
            raise RuntimeError("Operation name required for context manager")
        self._start_time = time.perf_counter()
        return self

    def __exit__(self, _exc_type, _exc, _tb) -> None:
        """Context manager exit — stops the timer and prints elapsed time."""
        self.end()
