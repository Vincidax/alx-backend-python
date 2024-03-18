#!/usr/bin/env python3
'''Task 4's module.
'''
import asyncio
from typing import List


task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    '''Executes the task_wait_random coroutine n times with
    the specified max_delay.

    Args:
        n (int): The number of times to execute the coroutine.
        max_delay (int): The upper limit of the random delay in seconds.

    Returns:
        List[float]: A list of the random delay times in ascending order.
    '''
    wait_times = await asyncio.gather(
        *(task_wait_random(max_delay) for _ in range(n))
    )
    return sorted(wait_times)
