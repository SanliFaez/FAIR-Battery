"""
labphew.view.general_worker
=============
A Worker Thread is a simple class that re-implements QThread in order to perform a task in a
separate thread.
This is a very simple example, that could be further expanded, but it is sufficient for
working with methods(operations) from an Operator class.
The only requisite of QThreads is to re-implement the ``run``
method.
Although it works, this may not be the optimum/correct way of doing things, as pointed out in this `blog post
<https://mayaposch.wordpress.com/2011/11/01/how-to-really-truly-use-qthreads-the-full-explanation/>`_
"""

from PyQt5 import QtCore
import traceback
from time import time, sleep

class WorkThread(QtCore.QThread):
    def __init__(self,  function, *args, **kwargs):
        super().__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs

    # def __del__(self):
    #     self.wait()

    def run(self):
        try:
            self.function(*self.args,**self.kwargs)
        except Exception as e:
            print("error in thread:", str(e))
            traceback.print_exc()

    def stop(self, timeout=2):
        """
        Convenience method to gracefully stop thread before terminating forcefully after a timeout
        """
        t0 = time()
        self.quit()
        while time() < t0+timeout:
            if self.isFinished():
                return
            sleep(0.005)
        self.terminate()

if __name__ == '__main__':
    from time import sleep
    import random

    def print_numbers(n=10):
        for i in range(n):
            sleep(random.random()*2)
            print(i)


    worker_thread = WorkThread(print_numbers, 20)
    worker_thread.finished.connect(worker_thread.deleteLater)
    worker_thread.start()
    worker_thread2 = WorkThread(print_numbers, 20)
    worker_thread2.finished.connect(worker_thread.deleteLater)
    worker_thread2.start()
    sleep(1)
    print('Starting')
    while worker_thread.isRunning() or worker_thread2.isRunning():
        sleep(1)
        print('Still Running')