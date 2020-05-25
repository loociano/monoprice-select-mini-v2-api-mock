"""
Copyright 2020 Luc Rubio <luc@loociano.com>
Plugin is licensed under the GNU Lesser General Public License v3.0.
"""
import random


class PrinterModel:
  """Printer Model."""

  def __init__(self):
    self.state = 'idle'
    self.hotend = 25
    self.target_hotend_temperature = 0
    self.bed = 20
    self.target_bed_temperature = 0
    self.progress = 0

  def tick(self):
    """Simulates the pass of time."""
    self.hotend = random.randint(20, 25)
    self.bed = random.randint(20, 25)

  def set_printer_state(self, state: str) -> None:
    """Allows setting printer state with a timer."""
    self.state = state

  def set_target_hotend_temperature(self,
                                    target_hotend_temperature: int) -> None:
    """Allows setting target hotend temperature with a timer."""
    self.target_hotend_temperature = target_hotend_temperature

  def set_target_bed_temperature(self, target_bed_temperature: int) -> None:
    """Allows setting target bed temperature with a timer."""
    self.target_bed_temperature = target_bed_temperature
