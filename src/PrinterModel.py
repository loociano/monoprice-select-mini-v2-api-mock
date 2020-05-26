"""
Copyright 2020 Luc Rubio <luc@loociano.com>
Plugin is licensed under the GNU Lesser General Public License v3.0.
"""
import random
from threading import Timer


class PrinterModel:
  """Printer Model."""
  ROOM_TEMPERATURE = 25
  ROOM_TEMPERATURE_FLUCTUATION = 5

  def __init__(self):
    self.state = 'idle'
    self.hotend = self.ROOM_TEMPERATURE
    self.target_hotend_temperature = 0
    self.bed = self.ROOM_TEMPERATURE
    self.target_bed_temperature = 0
    self.progress = 0

  def tick(self):
    """Simulates the pass of time."""
    self.hotend += random.randint(-1, 1)
    self.bed += random.randint(-1, 1)

  def set_printer_state(self, state: str) -> None:
    """Allows setting printer state with a timer."""
    self.state = state

  def set_target_hotend_temperature(self,
                                    target_hotend_temperature: int) -> None:
    """Allows setting target hotend temperature with a timer."""
    self.target_hotend_temperature = target_hotend_temperature
    self._simulate_hotend_preheating()

  def set_target_bed_temperature(self, target_bed_temperature: int) -> None:
    """Allows setting target bed temperature with a timer."""
    self.target_bed_temperature = target_bed_temperature
    self._simulate_bed_preheating()

  def _simulate_hotend_preheating(self):
    """Simulates reaching the target hotend temperature."""
    if self.hotend <= self.target_hotend_temperature:
      self.hotend += random.randint(0, 5)
    else:
      self.hotend += random.randint(-5, 0)
    if self.hotend < self.ROOM_TEMPERATURE - self.ROOM_TEMPERATURE_FLUCTUATION:
      self.hotend = self.ROOM_TEMPERATURE - self.ROOM_TEMPERATURE_FLUCTUATION
    Timer(0.5, self._simulate_hotend_preheating).start()

  def _simulate_bed_preheating(self):
    """Simulates reaching the target bed temperature."""
    if self.bed <= self.target_bed_temperature:
      self.bed += random.randint(0, 5)
    else:
      self.bed += random.randint(-5, 0)
    if self.bed < self.ROOM_TEMPERATURE - self.ROOM_TEMPERATURE_FLUCTUATION:
      self.bed = self.ROOM_TEMPERATURE - self.ROOM_TEMPERATURE_FLUCTUATION
    Timer(0.5, self._simulate_bed_preheating).start()
