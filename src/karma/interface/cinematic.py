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
		self.frames = self._load_frames(directory)

	def _load_frames(self, directory: Path) -> list[pygame.Surface]:
		paths = [
			path
			for path in directory.iterdir()
			if path.is_file() and path.suffix.lower() in self.IMAGE_EXTENSIONS
		]
		paths.sort(key=self._frame_sort_key)

		if not paths:
			raise ValueError(f"No image found in cinematic directory: {directory}")

		return [pygame.image.load(path).convert() for path in paths]

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

		return self.finished

	def draw(self, screen: pygame.Surface) -> None:
		frame = self.frames[self.current_frame]
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
