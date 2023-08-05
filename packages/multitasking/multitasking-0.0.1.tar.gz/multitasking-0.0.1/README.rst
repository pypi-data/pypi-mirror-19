multitasking: Simple async w/o async
=================================================


**multitasking** offers a simple method to convert Python methods
into asynchronous / non-blocking methods by using decorators.

Example
--------------------
.. code:: python

    import multitasking
    import time
    import random

    import signal

    # kill all tasks on ctrl-c
    signal.signal(signal.SIGINT, multitasking.killall)

    # to wait for task to finish, use:
    # signal.signal(signal.SIGINT, multitasking.wait_for_tasks)

    @multitasking.task
    def hello(count):
        sleep = random.randint(1,10)/2
        print("Hello %s (sleeping for %ss)" % (count, sleep))
        time.sleep(sleep)
        print("Goodbye %s (after for %ss)" % (count, sleep))


    if __name__ == "__main__":
        for i in range(0, 10):
            hello(i+1)


Installation
============

Install multitasking using ``pip``:

.. code:: bash

    $ pip install multitasking --upgrade --no-cache-dir


Legal Stuff
===========

multitasking is distributed under the **GNU Lesser General Public License v3.0**. See the `LICENSE.txt <./LICENSE.txt>`_ file in the release for details.
multitasking is not a product of Interactive Brokers, nor is it affiliated with Interactive Brokers.
