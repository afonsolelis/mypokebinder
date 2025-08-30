#!/usr/bin/env python3
"""
Script de teste para verificar se a configuração está funcionando
"""

import os
import sys
from dotenv import load_dotenv

def test_env_variables():
    """Testa se as variáveis de ambiente estão configuradas"""
    print("🔍 Testando variáveis de ambiente...")
    
    load_dotenv()
    
    required_vars = {
        'SUPABASE_URL': os.getenv("SUPABASE_URL"),
        'SUPABASE_KEY': os.getenv("SUPABASE_KEY"),
        'CLOUDINARY_CLOUD_NAME': os.getenv("CLOUDINARY_CLOUD_NAME"),
        'CLOUDINARY_API_KEY': os.getenv("CLOUDINARY_API_KEY"),
        'CLOUDINARY_API_SECRET': os.getenv("CLOUDINARY_API_SECRET")
    }
    
    all_good = True
    for var_name, var_value in required_vars.items():
        if var_value and var_value not in ['your_', 'placeholder']:
            print(f"✅ {var_name}: Configurada")
        else:
            print(f"❌ {var_name}: Não configurada ou valor padrão")
            all_good = False
    
    return all_good

def test_dependencies():
    """Testa se as dependências estão instaladas"""
    print("\n📦 Testando dependências...")
    
    dependencies = [
        'streamlit',
        'supabase',
        'cloudinary',
        'PIL',
        'dotenv'
    ]
    
    all_good = True
    for dep in dependencies:
        try:
            if dep == 'PIL':
                import PIL
                print(f"✅ {dep}: OK")
            elif dep == 'dotenv':
                import dotenv
                print(f"✅ {dep}: OK")
            else:
                __import__(dep)
                print(f"✅ {dep}: OK")
        except ImportError:
            print(f"❌ {dep}: Não instalado")
            all_good = False
    
    return all_good

def test_cloudinary_connection():
    """Testa a conexão com o Cloudinary"""
    print("\n☁️ Testando conexão com Cloudinary...")
    
    try:
        from cloudinary_config import validate_cloudinary_connection
        result = validate_cloudinary_connection()
        
        if result:
            print("✅ Conexão com Cloudinary: OK")
            return True
        else:
            print("❌ Conexão com Cloudinary: Falhou")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar Cloudinary: {str(e)}")
        return False

def test_supabase_connection():
    """Testa a conexão com o Supabase"""
    print("\n🗄️ Testando conexão com Supabase...")
    
    try:
        from config import supabase
        
        # Tenta fazer uma operação simples
        result = supabase.auth.get_user()
        print("✅ Conexão com Supabase: OK")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar Supabase: {str(e)}")
        return False

def main():
    """Função principal"""
    print("🎴 MyPokeBinder - Teste de Configuração")
    print("=" * 50)
    
    # Testar variáveis de ambiente
    env_ok = test_env_variables()
    
    # Testar dependências
    deps_ok = test_dependencies()
    
    # Testar conexões (apenas se as dependências estiverem OK)
    cloudinary_ok = False
    supabase_ok = False
    
    if deps_ok:
        cloudinary_ok = test_cloudinary_connection()
        supabase_ok = test_supabase_connection()
    
    # Resumo
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES:")
    print(f"Variáveis de ambiente: {'✅' if env_ok else '❌'}")
    print(f"Dependências: {'✅' if deps_ok else '❌'}")
    print(f"Cloudinary: {'✅' if cloudinary_ok else '❌'}")
    print(f"Supabase: {'✅' if supabase_ok else '❌'}")
    
    if all([env_ok, deps_ok, cloudinary_ok, supabase_ok]):
        print("\n🎉 Todos os testes passaram! O sistema está configurado corretamente.")
        print("\n📋 Próximos passos:")
        print("1. Execute as migrations: python run_migrations.py")
        print("2. Execute o aplicativo: streamlit run app.py")
    else:
        print("\n⚠️ Alguns testes falharam. Verifique a configuração antes de continuar.")
        
        if not env_ok:
            print("- Configure as variáveis no arquivo .env")
        if not deps_ok:
            print("- Instale as dependências: pip install -r requirements.txt")
        if not cloudinary_ok:
            print("- Verifique as credenciais do Cloudinary")
        if not supabase_ok:
            print("- Verifique as credenciais do Supabase")

if __name__ == "__main__":
    main()
