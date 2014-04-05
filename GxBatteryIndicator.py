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
self.battery_unknown = pygame.image.load("indicators/default/GxBatteryIndicator/battery_unknown.png")

self.SetIcon(self.battery_unknown)

self.frame_code = """
import platform

self.status_string = ""

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
  
  self.status_string = "Your battery is " + str(status.BatteryLifePercent) + "% charged"
  if status.ACLineStatus == 1:
    self.status_string += " and is plugged in"
  self.status_string += "."
  
elif platform.system() == 'Linux':
  
  # Ubuntu and elementary OS are supported
  
  import subprocess
  
  power_sources = []
  
  pipe = subprocess.Popen(["upower", "-e"], stdout=subprocess.PIPE).stdout
  for power_source in pipe:
    power_sources.append(power_source)
  
  percentages = []
  for power_source in power_sources:
    if "battery" in power_source:
      print "Calling upower -i " + power_source
      source_pipe = subprocess.Popen(["upower", "-i", power_source], stdout=subprocess.PIPE).stdout
      for line in source_pipe:
        if "percentage" in line:
          import re
          percentage = float((re.findall(r"\d*\.\d+|\d+", line))[0])
          percentages.append(percentage)
  if len(percentages) > 0:
    average_percentage = sum(percentages) / float(len(percentages))
    if average_percentage > 90:
      self.image = self.battery_100
    elif average_percentage > 70:
      self.image = self.battery_80
    elif average_percentage > 50:
      self.image = self.battery_60
    elif average_percentage > 30:
      self.image = self.battery_40
    elif average_percentage > 10:
      self.image = self.battery_20
    else:
      self.image = self.battery_critical
    self.status_string = "Your laptop is " + str(average_percentage) + "% charged"
  else:
    self.status_string = "No battery was found "
  
  self.status_string += " (" + str(len(power_sources)) + " power sources)"
  
  self.image = self.icon
  
else:
  self.image = self.icon
  self.status_string = "Your battery status is unknown."

self.SetClickCode('self.wm.ShowPopupMessage("Battery Status", self.status_string)')
"""
