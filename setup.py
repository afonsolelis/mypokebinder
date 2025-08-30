#!/usr/bin/env python3
"""
Script de setup para o MyPokeBinder
"""

import os
import sys
import subprocess

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 ou superior é necessário")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")

def install_dependencies():
    """Instala as dependências do projeto"""
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso")
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências")
        sys.exit(1)

def create_env_file():
    """Cria arquivo .env se não existir"""
    if not os.path.exists(".env"):
        print("🔧 Criando arquivo .env...")
        with open(".env", "w") as f:
            f.write("# Configure suas credenciais do Supabase aqui\n")
            f.write("SUPABASE_URL=your_supabase_url_here\n")
            f.write("SUPABASE_KEY=your_supabase_anon_key_here\n")
        print("✅ Arquivo .env criado")
        print("⚠️  Lembre-se de configurar suas credenciais do Supabase no arquivo .env")
    else:
        print("✅ Arquivo .env já existe")

def check_env_config():
    """Verifica se as variáveis de ambiente estão configuradas"""
    print("🔍 Verificando configuração do ambiente...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or supabase_url == "your_supabase_url_here":
            print("⚠️  SUPABASE_URL não configurada no arquivo .env")
        else:
            print("✅ SUPABASE_URL configurada")
            
        if not supabase_key or supabase_key == "your_supabase_anon_key_here":
            print("⚠️  SUPABASE_KEY não configurada no arquivo .env")
        else:
            print("✅ SUPABASE_KEY configurada")
            
    except ImportError:
        print("❌ python-dotenv não instalado")

def main():
    """Função principal"""
    print("🎴 MyPokeBinder - Setup")
    print("=" * 40)
    
    # Verificar versão do Python
    check_python_version()
    
    # Instalar dependências
    install_dependencies()
    
    # Criar arquivo .env
    create_env_file()
    
    # Verificar configuração
    check_env_config()
    
    print("\n" + "=" * 40)
    print("🎉 Setup concluído!")
    print("\n📋 Próximos passos:")
    print("1. Configure suas credenciais do Supabase no arquivo .env")
    print("2. Configure o banco de dados no Supabase (veja o README.md)")
    print("3. Execute: streamlit run app.py")
    print("\n📖 Para mais informações, consulte o README.md")

if __name__ == "__main__":
    main()
