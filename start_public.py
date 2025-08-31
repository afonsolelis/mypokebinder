#!/usr/bin/env python3
"""
Script de inicialização para MyPublicPokeBinder
Versão pública que não requer login
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário")
        print(f"   Versão atual: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")
    return True

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    try:
        import streamlit
        import supabase
        import cloudinary
        print("✅ Dependências Python OK")
        return True
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        print("📦 Execute: pip install -r requirements.txt")
        return False

def check_env_file():
    """Verifica se o arquivo .env existe"""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ Arquivo .env não encontrado")
        print("📋 Copie env.example para .env e configure suas credenciais")
        return False
    print("✅ Arquivo .env encontrado")
    return True

def check_supabase_connection():
    """Testa conexão com Supabase"""
    try:
        from config import supabase
        # Teste simples de conexão
        result = supabase.table('cards').select('id').limit(1).execute()
        print("✅ Conexão com Supabase OK")
        return True
    except Exception as e:
        print(f"❌ Erro na conexão com Supabase: {e}")
        return False

def main():
    """Função principal"""
    print("🎴 MyPublicPokeBinder - Versão Pública")
    print("=" * 50)
    
    # Verificações
    checks = [
        check_python_version(),
        check_dependencies(),
        check_env_file(),
        check_supabase_connection()
    ]
    
    if not all(checks):
        print("\n❌ Verificações falharam. Corrija os problemas acima.")
        return
    
    print("\n✅ Todas as verificações passaram!")
    print("🚀 Iniciando MyPublicPokeBinder...")
    print("=" * 50)
    
    # Iniciar aplicação
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "public_app.py",
            "--server.port", "8502",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Aplicação encerrada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar aplicação: {e}")

if __name__ == "__main__":
    main()
