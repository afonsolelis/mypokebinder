#!/usr/bin/env python3
"""
Script de inicialização do MyPokeBinder - Versão Windows
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Exibe o banner do MyPokeBinder"""
    print("=" * 50)
    print("MyPokeBinder - Sistema de Colecao de Cards")
    print("=" * 50)
    print()

def check_python_version():
    """Verifica a versão do Python"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 ou superior é necessário")
        print(f"   Versão atual: {sys.version_info.major}.{sys.version_info.minor}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")
    return True

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    print("📦 Verificando dependências...")
    
    try:
        import streamlit
        import supabase
        import cloudinary
        import PIL
        import dotenv
        print("✅ Todas as dependências estão instaladas")
        return True
    except ImportError as e:
        print(f"❌ Dependência não encontrada: {e}")
        print("   Execute: pip install -r requirements.txt")
        return False

def check_env_file():
    """Verifica se o arquivo .env existe e está configurado"""
    print("🔧 Verificando configuração do ambiente...")
    
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ Arquivo .env não encontrado")
        print("   Copie env.example para .env e configure suas credenciais")
        return False
    
    # Carrega as variáveis
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        'SUPABASE_URL',
        'SUPABASE_KEY', 
        'CLOUDINARY_CLOUD_NAME',
        'CLOUDINARY_API_KEY',
        'CLOUDINARY_API_SECRET'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value or value.startswith('your_') or value.startswith('placeholder'):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variáveis não configuradas: {', '.join(missing_vars)}")
        print("   Configure todas as variáveis no arquivo .env")
        return False
    
    print("✅ Arquivo .env configurado corretamente")
    return True

def test_connections():
    """Testa as conexões com Cloudinary e Supabase"""
    print("🔗 Testando conexões...")
    
    try:
        # Testar Cloudinary
        from cloudinary_config import validate_cloudinary_connection
        cloudinary_ok = validate_cloudinary_connection()
        
        if cloudinary_ok:
            print("✅ Conexão com Cloudinary: OK")
        else:
            print("❌ Conexão com Cloudinary: Falhou")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar Cloudinary: {e}")
        return False
    
    try:
        # Testar Supabase
        from config import supabase
        # Tenta uma operação simples
        result = supabase.auth.get_user()
        print("✅ Conexão com Supabase: OK")
    except Exception as e:
        print(f"❌ Erro ao testar Supabase: {e}")
        return False
    
    return True

def check_database():
    """Verifica se o banco de dados está configurado"""
    print("🗄️ Verificando banco de dados...")
    
    try:
        from config import supabase
        
        # Tenta buscar a tabela cards
        result = supabase.table('cards').select('id').limit(1).execute()
        print("✅ Tabela 'cards' encontrada")
        return True
        
    except Exception as e:
        print("❌ Tabela 'cards' não encontrada")
        print("   Execute o SQL no Supabase SQL Editor:")
        print("   - Vá para o SQL Editor do Supabase")
        print("   - Execute o conteúdo do arquivo 'supabase_setup.sql'")
        return False

def start_app():
    """Inicia o aplicativo Streamlit"""
    print("🚀 Iniciando o aplicativo...")
    print()
    print("📱 O aplicativo estará disponível em: http://localhost:8501")
    print("🔄 Para parar, pressione Ctrl+C")
    print()
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Aplicativo encerrado pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar aplicativo: {e}")

def main():
    """Função principal"""
    print_banner()
    
    # Verificações
    checks = [
        ("Versão do Python", check_python_version),
        ("Dependências", check_dependencies),
        ("Configuração do ambiente", check_env_file),
        ("Conexões", test_connections),
        ("Banco de dados", check_database)
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        print(f"\n🔍 {check_name}...")
        if not check_func():
            all_passed = False
            break
    
    if all_passed:
        print("\n🎉 Todas as verificações passaram!")
        print("🚀 Iniciando o MyPokeBinder...")
        start_app()
    else:
        print("\n⚠️ Algumas verificações falharam.")
        print("📖 Consulte a documentação para resolver os problemas:")
        print("   - README.md")
        print("   - SETUP_GUIDE.md")
        sys.exit(1)

if __name__ == "__main__":
    main()
