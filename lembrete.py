import time 

from plyer import notification

def lembrete():
    notification.notify(
        title="Ja se Hidratou Hoje Estrupicio?",
        message="Hora de beber agua 💧",
        timeout=10
    )

while True:
    lembrete()
    time.sleep(1000)    