# This file is part of GxBatteryIndicator.
# Copyright (C) 2014 Christopher Kyle Horton <christhehorton@gmail.com>

# GxBatteryIndicator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# GxBatteryIndicator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GxBatteryIndicator. If not, see <http://www.gnu.org/licenses/>.


# A battery indicator for GxSubOS.

# Some code based on a StackOverflow answer:
# http://stackoverflow.com/a/6156606

self.battery_full = pygame.image.load("indicators/default/GxBatteryIndicator/battery_full.png")
self.battery_two_thirds = pygame.image.load("indicators/default/GxBatteryIndicator/battery_two_thirds.png")
self.battery_one_third = pygame.image.load("indicators/default/GxBatteryIndicator/battery_one_third.png")
self.battery_low = pygame.image.load("indicators/default/GxBatteryIndicator/battery_low.png")
self.battery_charging = pygame.image.load("indicators/default/GxBatteryIndicator/battery_charging.png")

self.SetIcon(pygame.image.load("indicators/default/GxBatteryIndicator/battery_base.png"))

self.frame_code = """
global ctypes
import platform
import ctypes
from ctypes import wintypes

if platform.system() == 'Windows':

  class SYSTEM_POWER_STATUS(ctypes.Structure):
    _fields_ = [
      ('ACLineStatus', ctypes.wintypes.BYTE),
      ('BatteryFlag', ctypes.wintypes.BYTE),
      ('BatteryLifePercent', ctypes.wintypes.BYTE),
      ('Reserved1', ctypes.wintypes.BYTE),
      ('BatteryLifeTime', ctypes.wintypes.DWORD),
      ('BatteryFullLifeTime', ctypes.wintypes.DWORD),
    ]

  SYSTEM_POWER_STATUS_P = ctypes.POINTER(SYSTEM_POWER_STATUS)

  GetSystemPowerStatus = ctypes.windll.kernel32.GetSystemPowerStatus
  GetSystemPowerStatus.argtypes = [SYSTEM_POWER_STATUS_P]
  GetSystemPowerStatus.restype = ctypes.wintypes.BOOL

  status = SYSTEM_POWER_STATUS()
  if not GetSystemPowerStatus(ctypes.pointer(status)):
    raise ctypes.WinError()

  if status.BatteryLifePercent > 90:
    self.image = self.battery_full
  elif status.BatteryLifePercent > 66:
    self.image = self.battery_two_thirds
  elif status.BatteryLifePercent > 33:
    self.image = self.battery_one_third
  else:
    self.image = self.battery_low
else:
  self.image = self.icon
"""
