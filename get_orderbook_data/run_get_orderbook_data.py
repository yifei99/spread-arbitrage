import subprocess
import time

def run_script():
    while True:
        print("Starting the script...")
        process = subprocess.Popen(['python', 'get_orderbook_data.py'])
        
        # 等待脚本完成
        process.wait()
        
        print("Script stopped. Restarting in 5 seconds...")
        time.sleep(5)

if __name__ == "__main__":
    run_script()
