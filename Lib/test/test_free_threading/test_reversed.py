import unittest
from threading import Thread
from test.support import threading_helper


@threading_helper.reap_threads
@threading_helper.requires_working_threading()
class TestReversed(unittest.TestCase):
    def test_reversed_threading(self):
        # Test reading out the iterator with multiple threads cannot corrupt
        # the reversed iterator state.
        # The reversed iterator is not guaranteed to be thread safe

        number_of_threads = 10
        size = 4_000

        def work(r):
            while True:
                try:
                     l = r.__length_hint__()
                     next(r)
                except StopIteration:
                    break
                assert 0 <= l <= size
        x = tuple(range(size))
        r = reversed(x)
        worker_threads = []
        for ii in range(number_of_threads):
            worker_threads.append(Thread(target=work, args=[r]))
        for t in worker_threads:
            t.start()
        for t in worker_threads:
            t.join()

if __name__ == "__main__":
    unittest.main()
