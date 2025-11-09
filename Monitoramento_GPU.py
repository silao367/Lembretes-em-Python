# Script de monitoramento simples
import GPUtil
import time

while True:
    gpus = GPUtil.getGPUs()
    gpu = gpus[0]
    
    print(f"GPU: {gpu.load*100:.1f}% | "
          f"VRAM: {gpu.memoryUsed}/{gpu.memoryTotal} MB | "
          f"Temp: {gpu.temperature}°C")
    
    time.sleep(1)