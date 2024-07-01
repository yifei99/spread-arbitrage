import subprocess
import time
import os

# 定义要运行的脚本及其路径
scripts = ['get_data_aevo.py', 'get_data_apex.py', 'get_data_dydx.py']

# 运行每个脚本并捕获进程对象
processes = []
for script in scripts:
    try:
        process = subprocess.Popen(['python', script])
        processes.append((script, process))
        print(f"Started {script} with PID {process.pid}")
    except Exception as e:
        print(f"Failed to start {script}: {e}")

# 定义一个检查函数来监控进程
def check_processes(processes):
    for script, process in processes:
        if process.poll() is not None:  # 检查进程是否已经结束
            print(f"{script} terminated unexpectedly. Restarting...")
            try:
                new_process = subprocess.Popen(['python', script])
                processes.append((script, new_process))
                print(f"Restarted {script} with PID {new_process.pid}")
                processes.remove((script, process))  # 移除旧的进程对象
            except Exception as e:
                print(f"Failed to restart {script}: {e}")

try:
    # 持续监控进程
    while True:
        check_processes(processes)
        time.sleep(10)  # 每10秒检查一次
except KeyboardInterrupt:
    print("Stopping all processes...")

    # 终止所有进程
    for script, process in processes:
        process.terminate()
        print(f"Terminated {script} with PID {process.pid}")

    # 等待所有进程完全终止
    for script, process in processes:
        process.wait()
        print(f"Process {process.pid} has exited.")

    print("All processes stopped.")
