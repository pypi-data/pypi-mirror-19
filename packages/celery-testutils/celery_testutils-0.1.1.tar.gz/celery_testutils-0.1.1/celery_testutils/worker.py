import threading
import socket
from datetime import datetime
from celery import signals, states

class CeleryWorkerThread(threading.Thread):
    '''
    Thread that runs a celery worker while monitoring its state.

    Useful for testing purposes. Use the idle and active signals
    to wait for tasks to complete.
    '''
    def __init__(self, app):
        super(CeleryWorkerThread, self).__init__()

        self.app = app
        self.workers = []
        self.consumers = []
        self.monitor = CeleryMonitorThread(app)
        signals.after_task_publish.connect(self.monitor.task_begin)
        signals.task_postrun.connect(self.monitor.task_finished)

        self.ready = threading.Event()
        self.active = self.monitor.active
        self.idle = self.monitor.idle

    def on_worker_init(self, sender=None, **kwargs):
        self.workers.append(sender)

    def on_worker_ready(self, sender=None, **kwargs):
        if not self.ready.is_set():
            self.ready.set()

        self.consumers.append(sender)
        
    def run(self):
        signals.worker_init.connect(self.on_worker_init)
        signals.worker_ready.connect(self.on_worker_ready)

        self.monitor.daemon = self.daemon
        self.monitor.start()

        worker = self.app.Worker()
        if hasattr(worker, 'start'):
            worker.start()
        elif hasattr(worker, 'run'):
            worker.run()
        else:
            raise Exception("Don't know how to start worker. Incompatible Celery?")

    def stop(self):
        self.monitor.stop()

        for c in self.consumers:
            c.stop()
        
        for w in self.workers:
            w.terminate()
        
        signals.worker_init.disconnect(self.on_worker_init)
        signals.worker_ready.disconnect(self.on_worker_ready)

    def join(self, *args, **kwargs):
        self.monitor.join(*args, **kwargs)
        super(CeleryWorkerThread, self).join(*args, **kwargs)


class CeleryMonitorThread(threading.Thread):
    '''
    Monitors a Celery app. Keeps track of pending tasks.
    Exposes idle and active events.
    '''
    
    def __init__(self, app):
        super(CeleryMonitorThread, self).__init__()

        self.app = app
        self.state = app.events.State()
        self.stop_requested = False

        self.pending = 0
        self.pending_lock = threading.Lock()
        self.idle = threading.Event()
        self.idle.set()
        self.active = threading.Event()


    def task_begin(self, *args, **kwargs):
        with self.pending_lock:
            self.pending += 1
            self.idle.clear()
            self.active.set()

    def task_finished(self, *args, **kwargs):
        with self.pending_lock:
            self.pending -= 1
            if self.pending <= 0:
                self.active.clear()
                self.idle.set()

    def on_event(self, event):
        # maintain state
        self.state.event(event)

    @property
    def pending_tasks(self):
        tasks = self.state.tasks.values()
        return [t for t in tasks if t.state in states.UNREADY_STATES]

    @property
    def immediate_pending_tasks(self):
        now = datetime.utcnow().isoformat()
        return [t for t in self.pending_tasks if not t.eta or t.eta < now]

    def run(self):
        with self.app.connection() as connection:
            recv = self.app.events.Receiver(connection, handlers={
                '*': self.on_event,
            })

            # we want to be able to stop from outside
            while not self.stop_requested:
                try:
                    # use timeout so we can monitor if we should stop
                    recv.capture(limit=None, timeout=.5, wakeup=False)
                except socket.timeout:
                    pass

    def stop(self):
        self.stop_requested = True