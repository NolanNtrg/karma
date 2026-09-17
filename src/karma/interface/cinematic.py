import re
from enum import Enum, auto
from pathlib import Path

import pygame

from karma.interface.frameSequencer import FrameSequencer


class CinematicAction(Enum):
    NoneAction = auto()
    Skip = auto()
    Pause = auto()


class CinematicPlayer:
    # Reads an image sequence at a fixed frame rate.

    IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}

    def __init__(
        self,
        directory: Path,
        screen_size: tuple[int, int],
        fps: float = 10.0,
    ) -> None:
        if not directory.is_dir():
            raise FileNotFoundError(f"Cinematic directory not found: {directory}")

        self.screen_size: tuple[int, int] = screen_size
        self.frame_paths = self._load_frame_paths(directory)
        self.frames: list[pygame.Surface | None] = [None] * len(self.frame_paths)
        self.sequencer = FrameSequencer(len(self.frame_paths), fps)
        self._ensure_frame(0)

    def _load_frame_paths(self, directory: Path) -> list[Path]:
        paths = [
            path
            for path in directory.iterdir()
            if path.is_file() and path.suffix.lower() in self.IMAGE_EXTENSIONS
        ]
        paths.sort(key=self._frame_sort_key)

        if not paths:
            raise ValueError(f"No image found in cinematic directory: {directory}")

        return paths

    def _ensure_frame(self, frame_index: int) -> None:
        if self.frames[frame_index] is None:
            self.frames[frame_index] = pygame.image.load(self.frame_paths[frame_index]).convert()

    @staticmethod
    def _frame_sort_key(path: Path) -> tuple[int, str]:
        match = re.search(r"(\d+)(?=\.[^.]+$)", path.name)
        return (int(match.group(1)) if match else -1, path.name)

    def update(self, dt: float) -> bool:
        finished = self.sequencer.update(dt)
        self._ensure_frame(self.sequencer.current_frame)
        return finished

    def draw(self, screen: pygame.Surface) -> None:
        self._ensure_frame(self.sequencer.current_frame)
        frame = self.frames[self.sequencer.current_frame]
        assert frame is not None
        frame_ratio = frame.get_width() / frame.get_height()
        screen_ratio = self.screen_size[0] / self.screen_size[1]

        if frame_ratio > screen_ratio:
            size = (self.screen_size[0], round(self.screen_size[0] / frame_ratio))
        else:
            size = (round(self.screen_size[1] * frame_ratio), self.screen_size[1])

        scaled_frame = pygame.transform.scale(frame, size)
        screen.fill((0, 0, 0))
        position = (
            (self.screen_size[0] - size[0]) // 2,
            (self.screen_size[1] - size[1]) // 2,
        )
        screen.blit(scaled_frame, position)

    def toggle_pause(self) -> None:
        self.sequencer.toggle_pause()

    def pause(self) -> None:
        self.sequencer.pause()

    def resume(self) -> None:
        self.sequencer.resume()

    def handle_event(self, event: pygame.event.Event) -> CinematicAction:
        if event.type != pygame.KEYDOWN:
            return CinematicAction.NoneAction
        if event.key == pygame.K_SPACE:
            self.skip()
            return CinematicAction.Skip
        if event.key == pygame.K_ESCAPE:
            self.toggle_pause()
            return CinematicAction.Pause
        return CinematicAction.NoneAction

    def skip(self) -> None:
        self.sequencer.skip()
