import time


class Progress:
    # don't update more than once every 2 seconds
    MIN_REFRESH_INTERVAL = 2

    def __init__(self, stream):
        self.count = 0
        self.text = ""
        self.last_lengths = [0, 0]
        self.stream = stream
        self._last_updated = None
        self.stream.write('\n\n')

    def update(self, new_text):
        self.count += 1
        self.text = new_text
        self.refresh()

    def refresh(self):
        now = time.time()
        if self._last_updated is not None and now - self._last_updated <= self.MIN_REFRESH_INTERVAL:
            return
        self._last_updated = now
        self.stream.write("\033[F\033[F")
        for length in self.last_lengths:
            self.stream.write(" " * length)
            self.stream.write("\n")
        self.stream.write("\033[F\033[F")
        messages = [
            '%d done' % self.count,
            self.text
        ]
        for m in messages:
            self.stream.write("%s\n" % m)
        self.last_lengths = [len(x) for x in messages]