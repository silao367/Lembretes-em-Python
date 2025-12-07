# sono_simples.py - Versão que funciona SEM OpenCV inicialmente
import sys
import time

print("=" * 50)
print("INSTALADOR DE DETECTOR DE SONOLÊNCIA")
print("=" * 50)

# Verificar instalações
def check_installation():
    print("\n1. Verificando instalações...")
    
    # Verificar Python
    print(f"Python: {sys.version}")
    
    # Tentar importar OpenCV
    try:
        import cv2
        print("✅ OpenCV já está instalado!")
        return True
    except ImportError:
        print("❌ OpenCV não está instalado")
        return False

# Instalar OpenCV se necessário
def install_opencv():
    print("\n2. Instalando OpenCV...")
    print("Execute estes comandos no PowerShell:")
    print("\nComando 1:")
    print("python -m pip install --upgrade pip")
    print("\nComando 2:")
    print("pip install opencv-python")
    print("\nComando 3 (se necessário):")
    print("pip install --user opencv-python")
    
    input("\nPressione Enter após instalar o OpenCV...")

# Programa principal simplificado
def main_program():
    print("\n" + "=" * 50)
    print("DETECTOR DE SONOLÊNCIA SIMPLIFICADO")
    print("=" * 50)
    
    try:
        import cv2
        
        print("\n✅ OpenCV carregado com sucesso!")
        print("Versão:", cv2.__version__)
        
        # Testar câmera
        print("\nTestando câmera...")
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Não foi possível acessar a câmera.")
            print("Possíveis soluções:")
            print("1. Verifique se a câmera está conectada")
            print("2. Feche outros programas que usam câmera")
            print("3. Tente outro índice (0, 1, 2)...")
            return
        
        print("✅ Câmera acessada com sucesso!")
        
        # Mostrar câmera funcionando
        print("\nCâmera ativa. Pressione 'q' para sair do teste...")
        
        for i in range(100):  # Mostrar por 100 frames
            ret, frame = cap.read()
            if ret:
                cv2.putText(frame, "Camera OK! Pressione 'q'", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.imshow('Teste Camera', frame)
                
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        print("\n✅ Teste concluído com sucesso!")
        print("\nAgora você pode executar o detector completo.")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")

# Menu principal
if __name__ == "__main__":
    print("\nSelecione uma opção:")
    print("1. Verificar instalação")
    print("2. Instalar OpenCV")
    print("3. Testar câmera")
    print("4. Executar detector simples")
    
    choice = input("\nDigite sua opção (1-4): ")
    
    if choice == "1":
        check_installation()
    elif choice == "2":
        install_opencv()
    elif choice == "3":
        main_program()
    elif choice == "4":
        # Aqui vai o detector real depois que OpenCV estiver instalado
        print("\nPrimeiro instale o OpenCV (opção 2) e teste a câmera (opção 3)")
    else:
        print("Opção inválida!")
    
    input("\nPressione Enter para sair...")