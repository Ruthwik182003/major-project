import psutil

def forensic_analysis():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        print(f"Process: {proc.info}")