class Counter:
    def __init__(self, frames, callback):
        self.frames = frames
        self.count = 0
        self.callback = callback
        self.complete = False
    def update(self):
        self.count += 1
        if self.count >= self.frames:
            self.callback()
            self.complete = True

class CounterManager:
    def __init__(self):
        self.counters = []
    def add(self, counter):
        self.counters.append(counter)
    def update(self):
        for counter in self.counters:
            counter.update()
            if counter.complete:
                self.counters.remove(counter)
