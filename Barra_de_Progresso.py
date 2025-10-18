from tqdm import tqdm
import time

#Numero de iteracoes no loop
total_iterations = 100

#Usando tqdm para criar uma barra de progresso
for i in tqdm(range(total_iterations)):
    #Simulando algum trabalho com um pequeno atraso
    time.sleep(0.1)

print('Sucesso!\U0001F680')    