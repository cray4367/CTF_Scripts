#!/usr/bin/env bash

set -e

SHARE_NAME="shared"
MOUNT_POINT="/mnt/shared"

echo "[+] Detecting package manager..."

install_pkg() {
    if command -v apt >/dev/null 2>&1; then
        sudo apt update
        sudo apt install -y "$@"
    elif command -v dnf >/dev/null 2>&1; then
        sudo dnf install -y "$@"
    elif command -v pacman >/dev/null 2>&1; then
        sudo pacman -Sy --noconfirm "$@"
    else
        echo "[-] Unsupported package manager. Make sure you have virtiofs kernel support."
    fi
}

# Ubuntu often needs extra modules for virtiofs
if command -v apt >/dev/null 2>&1; then
    echo "[+] Installing extra Linux modules (Ubuntu/Debian)..."
    install_pkg "linux-modules-extra-$(uname -r)" || true
fi

echo "[+] Loading virtiofs kernel module..."
sudo modprobe virtiofs || echo "[!] Could not load module (might already be loaded or built-in)"

echo "[+] Creating mount point at $MOUNT_POINT ..."
sudo mkdir -p "$MOUNT_POINT"

echo "[+] Mounting shared folder..."
if sudo mount -t virtiofs "$SHARE_NAME" "$MOUNT_POINT"; then
    echo "[+] Mounted successfully!"
else
    echo "[-] Mount failed. Check virt-manager config and ensure the share is named '$SHARE_NAME'."
    exit 1
fi

echo "[+] Do you want to enable auto-mount on boot? (y/n)"
read -r choice

if [[ "$choice" == "y" || "$choice" == "Y" ]]; then
    if ! grep -q "$MOUNT_POINT" /etc/fstab; then
        echo "[+] Adding to /etc/fstab..."
        # Note: Added 'nofail' to prevent boot hangs if the share is disconnected
        echo "$SHARE_NAME $MOUNT_POINT virtiofs defaults,_netdev,nofail 0 0" | sudo tee -a /etc/fstab
    else
        echo "[!] Entry already exists in fstab"
    fi
fi

echo "[+] Done! Access your shared folder at: $MOUNT_POINT"
echo "[!] Note: If you cannot read/write to the folder, you must adjust the folder permissions on your HOST machine, not the guest."
