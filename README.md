# Klipper Fan Stall Detector

![console.png](https://github.com/rogerlz/klipper_fan_stall_detector/blob/main/imgs/console.png?raw=true)

## Context
Klipper plugin to work with Timmit fan stall pcb, to pause the print (or do other operations) if the hotend fan is not running.
The hw can be found here https://github.com/timmit99/Fan_Stall_Detector.

## Install

```bash
wget -O - https://raw.githubusercontent.com/rogerlz/klipper_fan_stall_detector/main/install.sh | bash
```

Then, add the following to your `moonraker.conf` to enable automatic updates:

```ini
[update_manager klipper_fan_stall_detector]
type: git_repo
channel: dev
path: ~/klipper_fan_stall_detector
origin: https://github.com/rogerlz/klipper_fan_stall_detector.git
managed_services: klipper
primary_branch: main
install_script: install.sh
```

## Configuration

```ini
[fan_stall_detector hef]
pin: !gpio22
threshold: 5
gcode_ok:
    M118 The HEF is OK now
gcode_fail:
    M118 The HEF has FAILED
gcode_failing:
    M118 The HEF FAN is FAILING
```

## Uninstall
