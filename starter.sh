# Uncomment PYTHON_SCRIPT IDA_EXECUTABLE PYTHON_VM and change it to their path so it can detect them automatically
#!/bin/bash

#IDA_EXECUTABLE="/home/username/ida-pro-pc-9.2/ida"
#PYTHON_SCRIPT="main.py"
#PYTHON_VM="/IDA-RPC/bin/activate"

check_interval=10  # seconds

is_exact_app_running() {
    for pid in $(pgrep -f "$(basename "$IDA_EXECUTABLE")"); do
        exe_path=$(readlink -f /proc/$pid/exe 2>/dev/null)
        if [[ "$exe_path" == "$IDA_EXECUTABLE" ]]; then
            echo "Found: $exe_path is running (PID $pid)"
            return 0
        fi
    done
    return 1
}

echo "Watching for $IDA_EXECUTABLE"

while true; do
    if is_exact_app_running; then
        echo "IDA is running. Launching Python script: $python_script"
        
        (
            source "$PYTHON_VM"
            python3 "$PYTHON_SCRIPT"
        )

    else
        echo "IDA not running. Checking again in $check_interval seconds..."
        sleep "$check_interval"
    fi
done
