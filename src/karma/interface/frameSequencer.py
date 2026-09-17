class FrameSequencer:
    # Avance un index de frame à intervalle fixe jusqu'à la dernière frame

    def __init__(self, frame_count: int, fps: float) -> None:
        if frame_count <= 0:
            raise ValueError("frame_count must be positive")
        if fps <= 0:
            raise ValueError("fps must be positive")

        self.frame_count: int = frame_count
        self.frame_duration: float = 1000.0 / fps
        self.elapsed: float = 0.0
        self.current_frame: int = 0
        self.paused: bool = False
        self.finished: bool = False

    def update(self, dt: float) -> bool:
        if self.paused or self.finished:
            return self.finished

        # compteur de frames avance avec dt jusqu'à la dernière frame, puis s'arrête
        self.elapsed += dt
        while self.elapsed >= self.frame_duration:
            self.elapsed -= self.frame_duration
            self.current_frame += 1
            if self.current_frame >= self.frame_count:
                self.current_frame = self.frame_count - 1
                self.finished = True
                break

        return self.finished

    def toggle_pause(self) -> None:
        self.paused = not self.paused

    def pause(self) -> None:
        self.paused = True

    def resume(self) -> None:
        self.paused = False

    def skip(self) -> None:
        self.finished = True
