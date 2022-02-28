from __future__ import annotations

import asyncio


__all__ = ('multiplex_lifespan',)


def multiplex_lifespan(funcs):
    """
    Performs the whole algorithm to multiplex the lifespan protocol

    Takes the list of functions to multiplex, returns an ASGI app.

    This is safe for apps that don't implement lifespan.
    """
    if not funcs:
        raise Exception("Nothing implementing lifespan, bye!")

    async def _(scope, receive, send):
        if scope['type'] == 'lifespan':
            wrappers = [LifespanWrapper(f, scope) for f in funcs]

            try:
                while True:
                    msg = await receive()
                    replies = await asyncio.gather(
                        *(lw.send(msg) for lw in wrappers)
                    )
                    replies = filter(None, replies)
                    errors = [
                        r
                        for r in replies
                        if r['type'].endswith('.failed')
                    ]
                    if errors:
                        await send({
                            'type': msg['type']+'.failed',
                            'message': '\n'.join(e['message'] for e in errors)
                        })
                    else:
                        await send({
                            'type': msg['type']+'.complete',
                        })
                    if msg['type'] == 'lifespan.shutdown':
                        return
            finally:
                for lw in wrappers:
                    lw.cancel()
    return _


class LifespanWrapper:
    """
    Helps juggle the buffering, waiting, and exception handling.

    This only works with lifespan's single send/single recv pattern. If the
    sends and receives are not paired, deadlocks will happen.
    """
    def __init__(self, func, scope):
        self._o2i_queue = asyncio.Queue(1)  # Outter to inner
        self._i2o_queue = asyncio.Queue(1)  # Inner to outter
        self._task = asyncio.create_task(
            func(scope, self._o2i_queue.get, self._i2o_queue.put)
        )
        self._task_finished = asyncio.Event()

    async def _finished(self):
        """
        Blocks until the inner task finishes
        """
        if not self._task.done():
            # For some reason, this just blocks forever if the task is already finished
            await self._task
        return ...

    def cancel(self):
        try:
            self._task.cancel()
        except Exception:
            pass

    async def send(self, msg):
        """
        Send a message and wait for a reply.

        Returns None if the task exits without replying
        """
        r = await _race(self._o2i_queue.put(msg), self._finished())
        if r is ...:
            return
        r = await _race(self._i2o_queue.get(), self._finished())
        if r is ...:
            return
        return r


async def _race(*aws, timeout=None):
    """
    Waits for several awaitables in parallel, returning the results of the first
    to complete and cancelling the others.

    If several tasks are already completed, one will be returned.

    If several tasks complete at once, only one is returned.
    """
    aws = list(map(asyncio.ensure_future, aws))

    done, pending = await asyncio.wait(
        aws,
        return_when=asyncio.FIRST_COMPLETED,
        timeout=timeout,
    )

    for p in pending:
        p.cancel()

    # This is so that if multiple tasks finished at once, they're returned in
    # argument order
    for t in aws:
        if t in done:
            return t.result()
