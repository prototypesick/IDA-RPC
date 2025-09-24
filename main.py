import time
import psutil
from pypresence import Presence
import os
import sys
import subprocess

DISCORD_CLIENT_ID = '1420489154625798205'

IDA_PROCESS_NAMES = [
    "ida64",
    "ida",
    "idaq",
    "idaq64"
]

def get_binary_from_ida_window():
    try:
        window_ids = subprocess.check_output(['xdotool', 'search', '--name', 'IDA'])
        window_ids = window_ids.decode().splitlines()
        for wid in window_ids:
            try:
                name = subprocess.check_output(['xdotool', 'getwindowname', wid])
                title = name.decode().strip()
                if title.startswith("IDA - ") and ' - ' in title:
                    parts = title.split(' - ', 1)
                    if len(parts) > 1:
                        full_path = parts[1].strip()
                        return os.path.basename(full_path)
            except subprocess.CalledProcessError:
                continue
    except subprocess.CalledProcessError:
        pass
    return None

def is_ida_running():
    for proc in psutil.process_iter(attrs=['name']):
        try:
            name = proc.info['name'].lower()
            if any(ida_name in name for ida_name in IDA_PROCESS_NAMES):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

def main():
    rpc = Presence(DISCORD_CLIENT_ID)
    connected = False
    # binary_name = get_binary_from_ida_window() or "Unknown Binary"  cannot use this as this does not refresh for me
    start_time = None
    while True:
        try:
            ida_running = is_ida_running()
            if ida_running and not connected:
                try:
                    rpc.connect()
                    connected = True
                    start_time = time.time()
                    print("Connected to Discord RPC.")
                    rpc.update(
                        state=f"Disassembling {get_binary_from_ida_window() or "Unknown Binary"}",
                        details="Using IDA Pro",
                        large_image="ida_icon",
                        large_text="IDA Pro",
                        start=start_time
                    )
                except Exception as e:
                    print(f"Failed to connect or update RPC: {e}")
                    connected = False

            elif connected and ida_running:
                print(f"updating RPC with binary of {get_binary_from_ida_window() or "Unknown Binary"}")
                rpc.update(
                        state=f"Disassembling {get_binary_from_ida_window() or "Unknown Binary"}",
                        details="Using IDA Pro",
                        large_image="ida_icon",
                        large_text="IDA Pro",
                        start=start_time
                    )
                
            elif not ida_running and connected:
                try:
                    rpc.clear()
                    rpc.close()
                    connected = False
                    print("IDA not running. RPC cleared.")
                except Exception as e:
                    print(f"Failed to clear RPC: {e}")

        except KeyboardInterrupt:
            if connected:
                rpc.clear()
                rpc.close()
            print("Exiting.")
            sys.exit(0)

        time.sleep(30)

if __name__ == "__main__":
    main()
