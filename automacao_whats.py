import pywhatkit
import pyautogui
import time

def automacao_simples():
    """
    Versão simples e direta
    """
    numero = "+5514988176669"  # Seu número aqui
    mensagem = "Olá! Este é um Lembrete Automático do BOT!" \
    "\nDigite Oi para ver!" 
    
    print("⚡ Enviando mensagem instantânea...")
    
    # Envia mensagem
    pywhatkit.sendwhatmsg_instantly(numero, mensagem)
    time.sleep(3)
    pyautogui.press('enter')
    
    print("✅ Mensagem enviada! Pronto para responder 'Oi', automaticamente.")
    
    # Aguarda um tempo e simula resposta
    time.sleep(25)
    
    # Resposta automática simulada
    resposta = "Lembrete rapido: \nVoce sempre Sera Vencedor!"
    pywhatkit.sendwhatmsg_instantly(numero, resposta)
    time.sleep(10)
    pyautogui.press('enter')
    
    print("✅ Resposta automática enviada!")

# Executar
automacao_simples()
