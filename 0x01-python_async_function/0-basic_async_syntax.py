#!/usr/bin/env python3
''' an asynchronous coroutine that takes in an integer argument'''

import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    '''An asynchronous coroutine that waits for a random delay
        between 0 and max_delay seconds.

    Args:
        max_delay (float): The upper limit of the random delay in seconds.
                            Defaults to 10.

    Returns:
        float: The random delay time.
    '''
    delay = random.random() * max_delay
    await asyncio.sleep(delay)
    return delay
