#!/bin/bash

KLIPPER_PATH="${HOME}/klipper"
PLUGIN_PATH="${HOME}/klipper_fan_stall_detector"

set -eu
export LC_ALL=C

function preflight_checks {
    if [ "$EUID" -eq 0 ]; then
        echo "[PRE-CHECK] This script must not be run as root!"
        exit -1
    fi

    if [ "$(sudo systemctl list-units --full -all -t service --no-legend | grep -F 'klipper.service')" ]; then
        printf "[PRE-CHECK] Klipper service found! Continuing...\n\n"
    else
        echo "[ERROR] Klipper service not found, please install Klipper first!"
        exit -1
    fi
}

function check_download {
    local mydirname mybasename
    mydirname="$(dirname ${PLUGIN_PATH})"
    mybasename="$(basename ${PLUGIN_PATH})"

    if [ ! -d "${PLUGIN_PATH}" ]; then
        echo "[DOWNLOAD] Downloading Fan Stall Detector repository..."
        if git -C $mydirname clone https://github.com/rogerlz/klipper_fan_stall_detector.git $mybasename; then
            chmod +x ${PLUGIN_PATH}/install.sh
            printf "[DOWNLOAD] Download complete!\n\n"
        else
            echo "[ERROR] Download of Fan Stall Detector git repository failed!"
            exit -1
        fi
    else
        printf "[DOWNLOAD] Fan Stall Detector repository already found locally. Continuing...\n\n"
    fi
}

function link_extension {
    echo "[INSTALL] Linking extension to Klipper..."
    ln -srfn "${PLUGIN_PATH}/fan_stall_detector.py" "${KLIPPER_PATH}/klippy/extras/fan_stall_detector.py"
}

function restart_klipper {
    echo "[POST-INSTALL] Restarting Klipper..."
    sudo systemctl restart klipper
}

printf "\n======================================\n"
echo "- Fan Stall Detector install script -"
printf "======================================\n\n"

# Run steps
preflight_checks
check_download
link_extension
restart_klipper
