#!/usr/bin/env python3
"""
Script para verificar e corrigir configurações do Cloudinary
"""

import os
from dotenv import load_dotenv

def check_cloudinary_config():
    """Verifica a configuração do Cloudinary"""
    print("🔍 Verificando configuração do Cloudinary...")
    print("=" * 50)
    
    # Carrega as variáveis de ambiente
    load_dotenv()
    
    # Verifica as variáveis
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
    api_key = os.getenv("CLOUDINARY_API_KEY")
    api_secret = os.getenv("CLOUDINARY_API_SECRET")
    
    print(f"📋 Cloud Name: {cloud_name}")
    print(f"📋 API Key: {api_key[:10] + '...' if api_key else 'Não configurado'}")
    print(f"📋 API Secret: {api_secret[:10] + '...' if api_secret else 'Não configurado'}")
    print()
    
    # Validações
    issues = []
    
    if not cloud_name:
        issues.append("❌ CLOUDINARY_CLOUD_NAME não configurado")
    elif cloud_name == "your-cloud-name" or cloud_name == "placeholder":
        issues.append("❌ CLOUDINARY_CLOUD_NAME ainda com valor padrão")
    else:
        print("✅ CLOUDINARY_CLOUD_NAME configurado")
    
    if not api_key:
        issues.append("❌ CLOUDINARY_API_KEY não configurado")
    elif api_key == "your-api-key" or api_key == "placeholder":
        issues.append("❌ CLOUDINARY_API_KEY ainda com valor padrão")
    else:
        print("✅ CLOUDINARY_API_KEY configurado")
    
    if not api_secret:
        issues.append("❌ CLOUDINARY_API_SECRET não configurado")
    elif api_secret == "your-api-secret" or api_secret == "placeholder":
        issues.append("❌ CLOUDINARY_API_SECRET ainda com valor padrão")
    else:
        print("✅ CLOUDINARY_API_SECRET configurado")
    
    if issues:
        print("\n🚨 PROBLEMAS ENCONTRADOS:")
        for issue in issues:
            print(f"   {issue}")
        
        print("\n🔧 SOLUÇÃO:")
        print("1. Acesse https://cloudinary.com/console")
        print("2. Faça login na sua conta")
        print("3. Vá em 'Dashboard'")
        print("4. Copie as credenciais:")
        print("   - Cloud Name")
        print("   - API Key")
        print("   - API Secret")
        print("5. Atualize o arquivo .env com os valores corretos")
        
        return False
    else:
        print("\n✅ Todas as configurações estão corretas!")
        
        # Testa a conexão
        try:
            import cloudinary
            import cloudinary.api
            
            cloudinary.config(
                cloud_name=cloud_name,
                api_key=api_key,
                api_secret=api_secret
            )
            
            result = cloudinary.api.ping()
            if result.get('status') == 'ok':
                print("✅ Conexão com Cloudinary: OK")
                return True
            else:
                print("❌ Erro na conexão com Cloudinary")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao testar conexão: {str(e)}")
            return False

def show_env_example():
    """Mostra exemplo do arquivo .env"""
    print("\n📝 EXEMPLO DO ARQUIVO .env:")
    print("=" * 50)
    print("""
# Cloudinary
CLOUDINARY_CLOUD_NAME=seu_cloud_name_real
CLOUDINARY_API_KEY=sua_api_key_real
CLOUDINARY_API_SECRET=sua_api_secret_real

# Supabase
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua_anon_key
""")

if __name__ == "__main__":
    print("🎴 MyPokeBinder - Verificação do Cloudinary")
    print("=" * 50)
    
    if check_cloudinary_config():
        print("\n🎉 Cloudinary configurado corretamente!")
    else:
        show_env_example()
