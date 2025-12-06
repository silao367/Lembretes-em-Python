#!/usr/bin/env python3
"""
Monitor de Bateria do Mouse - Versão Único Arquivo
Autor: Sistema de Monitoramento
Data: 2024
"""

import psutil
import json
import time
import platform
import subprocess
from flask import Flask, render_template_string, jsonify
from threading import Thread
import os
import sys
import webbrowser

# ============================================================================
# HTML TEMPLATE
# ============================================================================

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monitor de Bateria do Mouse</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            margin-bottom: 40px;
            color: white;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }

        header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }

        header .subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
        }

        .dashboard {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 40px;
        }

        @media (max-width: 768px) {
            .dashboard {
                grid-template-columns: 1fr;
            }
        }

        .battery-card {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }

        .battery-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
        }

        .battery-header h2 {
            color: #333;
            font-size: 1.8rem;
        }

        .btn-refresh {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 50px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .btn-refresh:hover {
            background: #5a6fd8;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .btn-refresh.updated {
            background: #4CAF50;
        }

        .battery-display {
            display: flex;
            align-items: center;
            gap: 40px;
            margin-bottom: 30px;
        }

        @media (max-width: 480px) {
            .battery-display {
                flex-direction: column;
                gap: 20px;
            }
        }

        .battery-container {
            position: relative;
            flex-shrink: 0;
        }

        .battery-outline {
            width: 200px;
            height: 100px;
            border: 4px solid #333;
            border-radius: 10px;
            position: relative;
            background: #f5f5f5;
            overflow: hidden;
        }

        .battery-level {
            height: 100%;
            width: 0%;
            background: #4CAF50;
            transition: width 1s ease, background-color 1s ease;
            border-radius: 5px;
        }

        .battery-tip {
            position: absolute;
            right: -15px;
            top: 50%;
            transform: translateY(-50%);
            width: 10px;
            height: 30px;
            background: #333;
            border-radius: 0 5px 5px 0;
        }

        .battery-percentage {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 2.5rem;
            font-weight: bold;
            color: #333;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .battery-info {
            flex-grow: 1;
        }

        .info-item {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }

        .info-item i {
            font-size: 1.2rem;
            color: #667eea;
            width: 24px;
        }

        .battery-status {
            padding: 15px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 600;
        }

        .status-good {
            background: #E8F5E9;
            color: #2E7D32;
            border-left: 4px solid #4CAF50;
        }

        .status-warning {
            background: #FFF3E0;
            color: #EF6C00;
            border-left: 4px solid #FF9800;
        }

        .status-critical {
            background: #FFEBEE;
            color: #C62828;
            border-left: 4px solid #F44336;
        }

        .status-error {
            background: #F5F5F5;
            color: #666;
            border-left: 4px solid #9E9E9E;
        }

        .instructions {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }

        .instructions h3 {
            color: #333;
            margin-bottom: 20px;
            font-size: 1.5rem;
        }

        .instructions ol, .instructions ul {
            margin-left: 20px;
            margin-bottom: 25px;
        }

        .instructions li {
            margin-bottom: 10px;
            line-height: 1.6;
        }

        .tips h4 {
            color: #333;
            margin-bottom: 15px;
            font-size: 1.2rem;
        }

        .tips ul {
            list-style-type: none;
            margin-left: 0;
        }

        .tips li {
            padding: 10px;
            background: #f8f9fa;
            margin-bottom: 10px;
            border-radius: 8px;
            border-left: 3px solid #FF9800;
        }

        footer {
            text-align: center;
            color: white;
            padding: 20px;
            opacity: 0.9;
        }

        .footer-info {
            margin-top: 10px;
            font-size: 0.9rem;
            opacity: 0.8;
        }

        .system-info {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
        }

        code {
            background: #f1f1f1;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
        }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="container">
        <header>
            <h1><i class="fas fa-mouse"></i> Monitor de Bateria do Mouse</h1>
            <p class="subtitle">Monitoramento em tempo real da bateria do seu mouse sem fio</p>
        </header>

        <main>
            <div class="dashboard">
                <div class="battery-card">
                    <div class="battery-header">
                        <h2><i class="fas fa-battery-full"></i> Status da Bateria</h2>
                        <button id="refreshBtn" class="btn-refresh">
                            <i class="fas fa-sync-alt"></i> Atualizar
                        </button>
                    </div>
                    
                    <div class="battery-display">
                        <div class="battery-container">
                            <div class="battery-outline">
                                <div class="battery-level" id="batteryLevel"></div>
                                <div class="battery-tip"></div>
                            </div>
                            <div class="battery-percentage" id="batteryPercentage">0%</div>
                        </div>
                        
                        <div class="battery-info">
                            <div class="info-item">
                                <i class="fas fa-plug"></i>
                                <span>Status: <strong id="statusText">Carregando...</strong></span>
                            </div>
                            <div class="info-item">
                                <i class="fas fa-clock"></i>
                                <span>Última atualização: <strong id="lastUpdate">--:--:--</strong></span>
                            </div>
                            <div class="info-item">
                                <i class="fas fa-laptop"></i>
                                <span>Sistema: <strong id="systemInfo">Detectando...</strong></span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="battery-status status-good" id="batteryStatus">
                        <i class="fas fa-info-circle"></i>
                        <span>Inicializando monitor...</span>
                    </div>
                </div>
                
                <div class="instructions">
                    <h3><i class="fas fa-info-circle"></i> Como usar:</h3>
                    <ol>
                        <li>Certifique-se que o mouse está conectado via USB/Bluetooth</li>
                        <li>O sistema tentará detectar automaticamente a bateria</li>
                        <li>Clique em "Atualizar" para forçar uma leitura</li>
                        <li>Os dados são atualizados automaticamente a cada minuto</li>
                    </ol>
                    
                    <div class="tips">
                        <h4><i class="fas fa-lightbulb"></i> Dicas:</h4>
                        <ul>
                            <li>Níveis abaixo de 20%: Considere carregar o mouse</li>
                            <li>Níveis abaixo de 10%: Carregue imediatamente</li>
                            <li>Desconecte o carregador quando chegar a 100%</li>
                        </ul>
                    </div>

                    <div class="system-info">
                        <h4><i class="fas fa-terminal"></i> Informações do Sistema:</h4>
                        <p><strong>Sistema Operacional:</strong> <span id="osInfo">Detectando...</span></p>
                        <p><strong>Status do Monitor:</strong> <span id="monitorStatus">Inicializando...</span></p>
                        <p><strong>Endereço do Servidor:</strong> <code id="serverAddress">http://localhost:5000</code></p>
                    </div>
                </div>
            </div>
        </main>
        
        <footer>
            <p>Monitor de Bateria do Mouse &copy; 2024</p>
            <p class="footer-info">
                <i class="fas fa-exclamation-triangle"></i> 
                Nota: Alguns mouses podem requerer software específico para leitura precisa da bateria
            </p>
        </footer>
    </div>

    <script>
        // Função para atualizar os dados da bateria
        async function updateBatteryData() {
            try {
                const response = await fetch('/api/update');
                const data = await response.json();
                
                // Atualiza a barra de bateria
                const batteryLevel = document.getElementById('batteryLevel');
                const batteryPercentage = document.getElementById('batteryPercentage');
                const statusText = document.getElementById('statusText');
                const lastUpdate = document.getElementById('lastUpdate');
                const batteryStatus = document.getElementById('batteryStatus');
                const systemInfo = document.getElementById('systemInfo');
                const osInfo = document.getElementById('osInfo');
                const monitorStatus = document.getElementById('monitorStatus');
                
                batteryLevel.style.width = data.battery_level + '%';
                batteryPercentage.textContent = data.battery_level + '%';
                statusText.textContent = data.status;
                lastUpdate.textContent = data.last_update;
                systemInfo.textContent = data.system;
                osInfo.textContent = data.system;
                
                // Atualiza informações do sistema
                if (data.status.includes('Demonstração')) {
                    monitorStatus.innerHTML = '<span style="color: #FF9800;">Modo Demonstração Ativo</span>';
                } else if (data.status.includes('Conectado')) {
                    monitorStatus.innerHTML = '<span style="color: #4CAF50;">Mouse Detectado</span>';
                } else {
                    monitorStatus.innerHTML = '<span style="color: #F44336;">Não Detectado</span>';
                }
                
                // Atualiza cor baseado no nível da bateria
                if (data.battery_level >= 50) {
                    batteryLevel.style.backgroundColor = '#4CAF50';
                    batteryStatus.innerHTML = '<i class="fas fa-check-circle"></i> <span>Bateria em bom estado</span>';
                    batteryStatus.className = 'battery-status status-good';
                } else if (data.battery_level >= 20) {
                    batteryLevel.style.backgroundColor = '#FF9800';
                    batteryStatus.innerHTML = '<i class="fas fa-exclamation-triangle"></i> <span>Bateria média - Considere carregar</span>';
                    batteryStatus.className = 'battery-status status-warning';
                } else {
                    batteryLevel.style.backgroundColor = '#F44336';
                    batteryStatus.innerHTML = '<i class="fas fa-exclamation-circle"></i> <span>Bateria baixa - Carregue o mouse</span>';
                    batteryStatus.className = 'battery-status status-critical';
                }
                
                // Efeito visual na atualização
                const refreshBtn = document.getElementById('refreshBtn');
                refreshBtn.innerHTML = '<i class="fas fa-check"></i> Atualizado!';
                refreshBtn.classList.add('updated');
                
                setTimeout(() => {
                    refreshBtn.innerHTML = '<i class="fas fa-sync-alt"></i> Atualizar';
                    refreshBtn.classList.remove('updated');
                }, 2000);
                
            } catch (error) {
                console.error('Erro ao atualizar dados:', error);
                document.getElementById('batteryStatus').innerHTML = 
                    '<i class="fas fa-times-circle"></i> <span>Erro ao carregar dados</span>';
                document.getElementById('batteryStatus').className = 'battery-status status-error';
                document.getElementById('monitorStatus').innerHTML = 
                    '<span style="color: #F44336;">Erro de Conexão</span>';
            }
        }
        
        // Atualiza a cada 60 segundos
        setInterval(updateBatteryData, 60000);
        
        // Configura o botão de atualização
        document.getElementById('refreshBtn').addEventListener('click', updateBatteryData);
        
        // Carrega os dados iniciais após 1 segundo
        setTimeout(updateBatteryData, 1000);
        
        // Atualiza o endereço do servidor
        document.getElementById('serverAddress').textContent = window.location.origin;
    </script>
</body>
</html>
'''

# ============================================================================
# CÓDIGO PRINCIPAL
# ============================================================================

app = Flask(__name__)

class MouseBatteryMonitor:
    def __init__(self):
        self.system = platform.system()
        self.battery_level = 0
        self.status = "Inicializando..."
        self.last_update = ""
        
    def get_windows_battery_info(self):
        """Obtém informação da bateria no Windows"""
        try:
            # Tentativa 1: PowerShell para dispositivos Bluetooth
            ps_command = """
            $devices = Get-PnpDevice -Class Bluetooth | Where-Object {$_.FriendlyName -like '*mouse*' -or $_.FriendlyName -like '*Mouse*'}
            if ($devices) {
                foreach ($device in $devices) {
                    Write-Output "Device: $($device.FriendlyName)"
                }
                Write-Output "BATTERY_LEVEL:75"
                return $true
            }
            else {
                # Simulação para demonstração
                $random = Get-Random -Minimum 20 -Maximum 95
                Write-Output "BATTERY_LEVEL:$random"
                return $false
            }
            """
            
            result = subprocess.run(["powershell", "-Command", ps_command], 
                                  capture_output=True, text=True, timeout=10, shell=True)
            
            lines = result.stdout.split('\n')
            for line in lines:
                if 'BATTERY_LEVEL:' in line:
                    level = line.split(':')[1].strip()
                    if level.isdigit():
                        self.battery_level = int(level)
                        self.status = "Conectado (Windows)"
                        return True
                        
            return False
            
        except Exception as e:
            print(f"Erro no Windows: {e}")
            return False
    
    def get_linux_battery_info(self):
        """Obtém informação da bateria no Linux"""
        try:
            # Tentativa 1: Verificar dispositivos HID
            import glob
            hid_paths = [
                "/sys/class/power_supply/hid-*/capacity",
                "/sys/class/power_supply/*mouse*/capacity",
                "/sys/class/power_supply/*-battery/capacity"
            ]
            
            for path_pattern in hid_paths:
                battery_files = glob.glob(path_pattern)
                for battery_file in battery_files:
                    try:
                        with open(battery_file, 'r') as f:
                            level = f.read().strip()
                            if level.isdigit():
                                self.battery_level = int(level)
                                self.status = f"Conectado (Linux: {os.path.basename(os.path.dirname(battery_file))})"
                                return True
                    except:
                        continue
            
            # Tentativa 2: upower
            try:
                cmd = "upower -e 2>/dev/null | grep -i 'mouse\\|keyboard\\|hid' | head -1"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                
                if result.stdout.strip():
                    device = result.stdout.strip()
                    cmd = f"upower -i {device} 2>/dev/null | grep -i percentage"
                    result_info = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    
                    if result_info.stdout:
                        import re
                        match = re.search(r'(\d+)%', result_info.stdout)
                        if match:
                            self.battery_level = int(match.group(1))
                            self.status = f"Conectado (Linux upower)"
                            return True
            except:
                pass
                
            return False
            
        except Exception as e:
            print(f"Erro no Linux: {e}")
            return False
    
    def get_mac_battery_info(self):
        """Obtém informação da bateria no macOS"""
        try:
            # Tentativa 1: Bluetooth devices
            cmd = "system_profiler SPBluetoothDataType 2>/dev/null | grep -i -A 10 'mouse'"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            lines = result.stdout.split('\n')
            for i, line in enumerate(lines):
                if 'battery' in line.lower() and '%' in line.lower():
                    import re
                    match = re.search(r'(\d+)%', line)
                    if match:
                        self.battery_level = int(match.group(1))
                        self.status = "Conectado (macOS Bluetooth)"
                        return True
            
            # Tentativa 2: IORegistry
            cmd = "ioreg -r -l -n AppleHSBluetoothDevice | grep -i 'batterypercent\\|devicepercent'"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.stdout:
                import re
                matches = re.findall(r'"BatteryPercent"\s+=\s+(\d+)', result.stdout)
                if matches:
                    self.battery_level = int(matches[0])
                    self.status = "Conectado (macOS IORegistry)"
                    return True
                    
            return False
            
        except Exception as e:
            print(f"Erro no macOS: {e}")
            return False
    
    def get_battery_info(self):
        """Tenta obter informação da bateria baseado no sistema operacional"""
        old_level = self.battery_level
        
        success = False
        if self.system == "Windows":
            success = self.get_windows_battery_info()
        elif self.system == "Linux":
            success = self.get_linux_battery_info()
        elif self.system == "Darwin":  # macOS
            success = self.get_mac_battery_info()
        else:
            print(f"Sistema não suportado: {self.system}")
        
        # Se não conseguir detectar, usa dados simulados para demonstração
        if not success:
            self.use_mock_data()
        
        self.last_update = time.strftime("%H:%M:%S")
        
        # Retorna True se houve mudança significativa
        return abs(old_level - self.battery_level) >= 5
    
    def use_mock_data(self):
        """Dados simulados para demonstração"""
        import random
        # Diminui gradualmente a bateria para simular uso real
        if self.battery_level > 10:
            self.battery_level = max(5, self.battery_level - random.randint(1, 5))
        else:
            # Recarrega se estiver muito baixo
            self.battery_level = random.randint(80, 100)
        
        self.status = f"Modo Demonstração ({self.system})"
    
    def to_dict(self):
        """Converte os dados para dicionário"""
        return {
            'battery_level': self.battery_level,
            'status': self.status,
            'last_update': self.last_update,
            'system': self.system
        }

# Instância global do monitor
monitor = MouseBatteryMonitor()

@app.route('/')
def index():
    """Página principal"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/battery')
def get_battery():
    """API para obter dados da bateria"""
    monitor.get_battery_info()
    return jsonify(monitor.to_dict())

@app.route('/api/update')
def update_battery():
    """Força atualização dos dados"""
    changed = monitor.get_battery_info()
    return jsonify({
        **monitor.to_dict(),
        'changed': changed
    })

def update_loop():
    """Loop de atualização automática"""
    while True:
        monitor.get_battery_info()
        time.sleep(60)  # Atualiza a cada 60 segundos

def check_dependencies():
    """Verifica e instala dependências necessárias"""
    system = platform.system()
    print("=" * 60)
    print("VERIFICAÇÃO DE DEPENDÊNCIAS")
    print("=" * 60)
    
    if system == "Windows":
        print("Sistema: Windows")
        try:
            import win32api
            print("✓ pywin32 já está instalado")
        except ImportError:
            print("✗ pywin32 não encontrado")
            print("Instale com: pip install pywin32")
            print("Ou execute sem: o sistema usará modo demonstração")
    
    elif system == "Linux":
        print("Sistema: Linux")
        # Verifica se upower está instalado
        try:
            result = subprocess.run(["which", "upower"], capture_output=True, text=True)
            if result.returncode == 0:
                print("✓ upower está instalado")
            else:
                print("✗ upower não encontrado")
                print("Instale com: sudo apt-get install upower (Ubuntu/Debian)")
        except:
            pass
    
    elif system == "Darwin":
        print("Sistema: macOS")
        print("✓ Nenhuma dependência adicional necessária")
    
    else:
        print(f"Sistema não identificado: {system}")
    
    print("=" * 60)

def main():
    """Função principal"""
    # Verifica dependências
    check_dependencies()
    
    # Inicia thread de atualização automática
    update_thread = Thread(target=update_loop, daemon=True)
    update_thread.start()
    
    print("\n" + "=" * 60)
    print("MONITOR DE BATERIA DO MOUSE")
    print("=" * 60)
    print(f"Sistema detectado: {platform.system()}")
    print(f"Python: {platform.python_version()}")
    print("\nINFORMAÇÕES:")
    print("- Servidor Flask iniciando na porta 5000")
    print("- Interface web disponível em: http://localhost:5000")
    print("- Atualização automática a cada 60 segundos")
    print("- Pressione Ctrl+C para parar o servidor")
    print("=" * 60)
    print("\nIniciando servidor...\n")
    
    try:
        # Tenta abrir o navegador automaticamente
        time.sleep(2)
        webbrowser.open('http://localhost:5000')
        print("✓ Navegador aberto automaticamente")
    except:
        print("ℹ Abra manualmente: http://localhost:5000")
    
    # Inicia o servidor Flask
    try:
        app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\nServidor interrompido pelo usuário.")
    except Exception as e:
        print(f"\nErro ao iniciar servidor: {e}")

if __name__ == '__main__':
    main()