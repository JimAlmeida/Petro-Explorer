from multiprocessing import Queue, Process
from PySide2.QtCore import QObject, Signal
from threading import Thread


class HandlerThread(Thread, QObject):
    hasProgressed = Signal(int) #signal to update gui's progress bar
    hasFinished = Signal(bool) #signal to tell gui that calculation has finished
    messageSent = Signal(str)

    def __init__(self, ntfy_progress=False):
        Thread.__init__(self)
        QObject.__init__(self)
        self.notify_progress = ntfy_progress
        self.func = None
        self.args = None
        self.results = None

    def run(self):
        self.messageSent.emit('Os cálculos/operações estão em andamento! Aguarde.')
        q = Queue()
        self.args.append(q)
        self.args = tuple(self.args)
        p = Process(target=self.func, args=self.args)
        p.start()
        if self.notify_progress:
            while True:
                r = q.get()
                if r == -1:
                    break
                else:
                    self.hasProgressed(r)
        self.results = q.get()  #results will be packed in a dictionary or list of lists, needs to come after -1 factor in the pipeline
        p.join()
        self.messageSent.emit('Os cálculos/operações estão terminados!')
        self.hasFinished.emit(True)

    def loadParameters(self, f, _args: list):
        self.func = f
        self.args = _args