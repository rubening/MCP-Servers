from __future__ import annotations

import asyncio
import inspect
from typing import Any, Awaitable, Callable


def ensure_async(func: Callable[..., Any]) -> Callable[..., Awaitable[Any]]:
    """Wrap a synchronous callable so it can be awaited."""

    if inspect.iscoroutinefunction(func):
        return func  # type: ignore[return-value]

    async def _async_wrapper(*args: Any, **kwargs: Any) -> Any:
        return await asyncio.get_event_loop().run_in_executor(None, lambda: func(*args, **kwargs))

    return _async_wrapper
