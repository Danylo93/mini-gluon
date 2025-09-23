#!/usr/bin/env python3
"""
Servidor simples para o Dashboard de Workflows
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

PORT = 8080

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def serve_dashboard():
    """Inicia o servidor do dashboard"""
    
    # Mudar para o diretório do projeto
    os.chdir(Path(__file__).parent)
    
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"🚀 Dashboard de Workflows rodando em:")
        print(f"   📍 http://localhost:{PORT}/workflow-dashboard.html")
        print(f"   📍 http://localhost:{PORT}/workflow-dashboard.html")
        print()
        print("🎯 Funcionalidades do Dashboard:")
        print("   ✅ Visualização em tempo real dos 5 workflows")
        print("   ✅ Status de execução (Executando, Sucesso, Falha)")
        print("   ✅ Logs streaming em tempo real")
        print("   ✅ Métricas de performance")
        print("   ✅ Simulação de workflows")
        print()
        print("🔄 Pressione Ctrl+C para parar o servidor")
        print()
        
        # Abrir o dashboard automaticamente no navegador
        try:
            webbrowser.open(f'http://localhost:{PORT}/workflow-dashboard.html')
        except:
            pass
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Servidor parado pelo usuário")
            httpd.shutdown()

if __name__ == "__main__":
    serve_dashboard()
