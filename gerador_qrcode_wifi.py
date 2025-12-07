import qrcode

# Formato padrão para QR Code de WiFi
# WIFI:S:<SSID>;T:<WPA/WEP>;P:<senha>;;
wifi_config = "WIFI:S:clcoding;T:WPA;P:cl@2014;;"

# Gerar QR Code
qr = qrcode.make(wifi_config)

# Salvar imagem
qr.save("wifi_qr_code.png")
print("QR Code gerado com sucesso: wifi_qr_code.png")

# Para mostrar o QR Code (opcional)
qr.show()