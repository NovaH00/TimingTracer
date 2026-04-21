from __future__ import annotations
import time
from dataclasses import dataclass
from typing import TypeAlias

TraceName: TypeAlias = str
TimeStamp: TypeAlias = float
DeltaTime: TypeAlias = float

@dataclass
class _TracerState:
    name: str
    traces: list[tuple[TraceName, DeltaTime]]
    last_timestamp: TimeStamp

class TimeTracer:
    """A time tracer that allows measuring and printing deltas between operations.

    Usage::

        with TimeTracer().build().start() as tracer:
            tracer.mark("first operation")
            tracer.mark("second operation")
            tracer.end()
    """

    def __init__(self, name: str = "Time Tracer"):
        """Initialize the TimeTracer with a display name.

        Args:
            name: The name shown in trace output.
        """
        self._name = name

    def build(self) -> IdleTracer:
        """Build and return an IdleTracer ready for use.

        Returns:
            An IdleTracer instance configured with this tracer's name.
        """
        return IdleTracer(_TracerState(self._name, [], 0.0))

class IdleTracer:
    """An idle tracer that can only be started.

    Represents a tracer in its initial, idle state. It does not yet
    record any data — the first action is to call start() (or use
    it as a context manager) to transition into StartedTracer.
    """

    def __init__(self, state: _TracerState):
        """Initialize the idle tracer with the given internal state.

        Args:
            state: The shared _TracerState object used by all tracer variants.
        """
        self._state = state

    def start(self) -> StartedTracer:
        """Start tracing.

        Records the current timestamp and clears any previous traces,
        transitioning this idle tracer into a started state.

        Returns:
            A StartedTracer instance for marking, resetting, and ending.
        """
        self._state.last_timestamp = time.perf_counter()
        self._state.traces.clear()
        return StartedTracer(self._state)

    def __enter__(self) -> StartedTracer:
        """Context manager entry — starts tracing.

        Returns:
            A StartedTracer instance.
        """
        return self.start()

    def __exit__(self, exc_type, exc, tb) -> None:
        """Context manager exit — no-op (tracing continues until explicitly ended)."""
        pass

class StartedTracer:
    """A tracer that has been started and can be used to mark operations.

    Provides methods to record timing marks, reset the timer, end tracing,
    and use as a context manager.
    """
    def __init__(self, state: _TracerState):
        self._state = state
        """Initialize with the tracer's internal state."""

    def _print_trace(self, name: TraceName, dt: DeltaTime) -> None:
        """Print a formatted trace line showing the operation name and elapsed time."""
        if dt < 1e-3:
            fmt = f"{dt * 1e6:.1f}µs"
        elif dt < 1:
            fmt = f"{dt * 1e3:.2f}ms"
        else:
            fmt = f"{dt:.3f}s"

        print(f"[{self._state.name}] - {name} took {fmt}")

    def mark(self, operation: str = "Operation") -> None:
        """Record a timing mark for the given operation name.

        Records the elapsed time since the last mark (or since start) and
        updates the internal timestamp so subsequent marks are measured from now.
        """
        now = time.perf_counter()
        delta = now - self._state.last_timestamp
        self._state.traces.append((operation, delta))
        self._state.last_timestamp = now

    def reset(self) -> None:
        """Reset the internal timestamp so the next mark measures from this point."""

    def end(self) -> None:
        """Print all recorded trace entries and stop tracing."""
        for name, dt in self._state.traces:
            self._print_trace(name, dt)

    def __enter__(self) -> StartedTracer:
        """Return self for use as a context manager."""
        return self

    def __exit__(self, _exc_type, _exc, _tb) -> None:
        """Context manager exit — ends tracing by printing all recorded traces."""
        self.end()
