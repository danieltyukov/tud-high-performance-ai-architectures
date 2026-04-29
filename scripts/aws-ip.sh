#!/usr/bin/env bash
# Update the HostName for the cese5040 SSH alias when AWS rotates the IP.
# Usage: ./scripts/aws-ip.sh <new-ip>
#
# Run after `$start` whenever `$info` shows a different IP than the one
# currently in ~/.ssh/config.

set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "usage: $0 <new-ip>" >&2
    exit 1
fi

new_ip="$1"
config="$HOME/.ssh/config"

if ! grep -q "^Host cese5040$" "$config"; then
    echo "error: no 'Host cese5040' block in $config" >&2
    exit 1
fi

# Replace the HostName line within the cese5040 block only.
awk -v ip="$new_ip" '
    /^Host cese5040$/ { in_block = 1; print; next }
    in_block && /^Host / && !/^Host cese5040$/ { in_block = 0 }
    in_block && /^[[:space:]]*HostName / { sub(/HostName .*/, "HostName " ip); print; next }
    { print }
' "$config" > "$config.tmp" && mv "$config.tmp" "$config"
chmod 600 "$config"

# Drop any stale host key for the old IP so the new one auto-accepts.
ssh-keygen -R cese5040 -f "$HOME/.ssh/known_hosts_cese5040" >/dev/null 2>&1 || true

echo "updated cese5040 -> $new_ip"
echo "test: ssh cese5040 'hostname && python3 --version'"
