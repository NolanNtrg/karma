import re
from enum import Enum, auto
from pathlib import Path

import pygame


class CinematicAction(Enum):
	NoneAction = auto()
	Skip = auto()
	Pause = auto()


class CinematicPlayer:
	"""Reads an image sequence at a fixed frame rate."""

	IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}

	def __init__(
		self,
		directory: Path,
		screen_size: tuple[int, int],
		fps: float = 10.0,
	) -> None:
		if not directory.is_dir():
			raise FileNotFoundError(f"Cinematic directory not found: {directory}")
		if fps <= 0:
			raise ValueError("Cinematic FPS must be positive")

		self.screen_size = screen_size
		self.frame_duration = 1000.0 / fps
		self.elapsed = 0.0
		self.current_frame = 0
		self.paused = False
		self.finished = False
		self.frame_paths = self._load_frame_paths(directory)
		self.frames: list[pygame.Surface | None] = [None] * len(self.frame_paths)
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
		if self.paused or self.finished:
			return self.finished

		self.elapsed += dt
		while self.elapsed >= self.frame_duration:
			self.elapsed -= self.frame_duration
			self.current_frame += 1
			if self.current_frame >= len(self.frames):
				self.current_frame = len(self.frames) - 1
				self.finished = True
				break
			self._ensure_frame(self.current_frame)

		return self.finished

	def draw(self, screen: pygame.Surface) -> None:
		self._ensure_frame(self.current_frame)
		frame = self.frames[self.current_frame]
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
		self.paused = not self.paused

	def pause(self) -> None:
		self.paused = True

	def resume(self) -> None:
		self.paused = False

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
		self.finished = True
