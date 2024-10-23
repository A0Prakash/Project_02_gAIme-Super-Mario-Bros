import numpy as np

class FrameStackWrapper:
    def __init__(self, num_stack):
        self.num_stack = num_stack
        self.frames = []

    def reset(self):
        self.frames = []

    def step(self, frame):
        self.frames.append(frame)
        if len(self.frames) > self.num_stack:
            self.frames.pop(0)
        return np.concatenate(self.frames, axis=0)  # Assuming frames are numpy arrays

class SkipFrameWrapper:
    def __init__(self, skip_frames):
        self.skip_frames = skip_frames
        self.count = 0

    def reset(self):
        self.count = 0

    def step(self, frame):
        self.count += 1
        if self.count % self.skip_frames == 0:
            self.count = 0
            return frame
        return None