import subprocess
import time

def run_program(file_choice):
    if file_choice == "1":
        process = subprocess.Popen(["python", "place_order_btc.py"])
    elif file_choice == "2":
        process = subprocess.Popen(["python", "place_order_eth.py"])
    elif file_choice == "3":
        process = subprocess.Popen(["python", "place_order_link.py"])
    elif file_choice == "4":
        process = subprocess.Popen(["python", "place_order_ltc.py"])
    elif file_choice == "5":
        process = subprocess.Popen(["python", "place_order_avax.py"])
    elif file_choice == "6":
        process = subprocess.Popen(["python", "place_order_atom.py"])
    elif file_choice == "7":
        process = subprocess.Popen(["python", "place_order_doge.py"])
    elif file_choice == "8":
        process = subprocess.Popen(["python", "place_order_bch.py"])
    elif file_choice == "9":
        process = subprocess.Popen(["python", "place_order_matic.py"])
    elif file_choice == "10":
        process = subprocess.Popen(["python", "place_order_sol.py"])
    elif file_choice == "11":
        process = subprocess.Popen(["python", "place_order_all.py"])
    else:
        print("无效的选择")
        return None
    return process

if __name__ == "__main__":
    choice = input("请输入要运行的文件(1-btc,2-eth,3-link,4-ltc,5-avax,6-atom,7-doge,8-bch,9-matic,10-sol,11-all ):")
    while True:
        program = run_program(choice)
        if program:
            while program.poll() is None:
                time.sleep(5)
            print("程序已终止，重新启动中...")
            time.sleep(1)