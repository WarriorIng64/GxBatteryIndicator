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

self.battery_100 = pygame.image.load("indicators/default/GxBatteryIndicator/battery_100.png")
self.battery_80 = pygame.image.load("indicators/default/GxBatteryIndicator/battery_80.png")
self.battery_60 = pygame.image.load("indicators/default/GxBatteryIndicator/battery_60.png")
self.battery_40 = pygame.image.load("indicators/default/GxBatteryIndicator/battery_40.png")
self.battery_20 = pygame.image.load("indicators/default/GxBatteryIndicator/battery_20.png")
self.battery_critical = pygame.image.load("indicators/default/GxBatteryIndicator/battery_critical.png")
self.battery_charging = pygame.image.load("indicators/default/GxBatteryIndicator/battery_charging.png")

self.SetIcon(pygame.image.load("indicators/default/GxBatteryIndicator/battery_base.png"))

self.frame_code = """
import platform

if platform.system() == 'Windows':
  
  global ctypes
  import ctypes
  from ctypes import wintypes

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

  if status.ACLineStatus == 1:
    self.image = self.battery_charging
  elif status.BatteryLifePercent > 90:
    self.image = self.battery_100
  elif status.BatteryLifePercent > 70:
    self.image = self.battery_80
  elif status.BatteryLifePercent > 50:
    self.image = self.battery_60
  elif status.BatteryLifePercent > 30:
    self.image = self.battery_40
  elif status.BatteryLifePercent > 10:
    self.image = self.battery_20
  else:
    self.image = self.battery_critical
else:
  self.image = self.icon
"""
