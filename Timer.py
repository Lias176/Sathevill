from __future__ import annotations

class Timer:
    timers: list[Timer] = []

    def __init__(self, time: int, onEllapsed: callable):
        self.isRunning: bool = False
        self.time: int = time
        self.onEllapsed: callable = onEllapsed
        self.timers.append(self)
    
    def update(self, time: int):
        if(not self.isRunning):
            return
        self.time -= time
        if(self.time <= 0):
            self.onEllapsed()
            self.isRunning = False
            self.timers.remove(self)
    
    def start(self):
        self.isRunning = True
    
    def stop(self):
        self.isRunning = False