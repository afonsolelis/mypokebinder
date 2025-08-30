#!/usr/bin/env python3
"""
Script para corrigir configuração do Cloudinary
"""

import os
from dotenv import load_dotenv

def show_cloudinary_guide():
    """Mostra guia detalhado para configurar Cloudinary"""
    print("🔧 GUIA PARA CONFIGURAR CLOUDINARY")
    print("=" * 50)
    print()
    print("📋 PASSO A PASSO:")
    print()
    print("1️⃣ Acesse: https://cloudinary.com/console")
    print("2️⃣ Faça login na sua conta")
    print("3️⃣ No Dashboard, você verá:")
    print("   └── Cloud Name (exemplo: dxyz12345)")
    print("   └── API Key (exemplo: 1475115867)")
    print("   └── API Secret (exemplo: abc123def456)")
    print()
    print("4️⃣ Copie esses valores")
    print("5️⃣ Abra o arquivo .env")
    print("6️⃣ Substitua as linhas do Cloudinary:")
    print()
    print("❌ ATUAL (INCORRETO):")
    print("CLOUDINARY_CLOUD_NAME=pokebinder")
    print()
    print("✅ CORRETO (exemplo):")
    print("CLOUDINARY_CLOUD_NAME=dxyz12345")
    print("CLOUDINARY_API_KEY=1475115867")
    print("CLOUDINARY_API_SECRET=abc123def456")
    print()
    print("⚠️ IMPORTANTE:")
    print("- Cloud Name NÃO é 'pokebinder'")
    print("- Cloud Name é o nome da sua conta Cloudinary")
    print("- Geralmente começa com letras/números")
    print("- Exemplo: dxyz12345, mycloud, etc.")
    print()

def check_current_config():
    """Verifica configuração atual"""
    load_dotenv()
    
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
    api_key = os.getenv("CLOUDINARY_API_KEY")
    api_secret = os.getenv("CLOUDINARY_API_SECRET")
    
    print("🔍 CONFIGURAÇÃO ATUAL:")
    print("=" * 30)
    print(f"Cloud Name: {cloud_name}")
    print(f"API Key: {api_key[:10] + '...' if api_key else 'Não configurado'}")
    print(f"API Secret: {api_secret[:10] + '...' if api_secret else 'Não configurado'}")
    print()
    
    if cloud_name == "pokebinder":
        print("❌ PROBLEMA IDENTIFICADO:")
        print("   O Cloud Name 'pokebinder' não é válido!")
        print("   Você precisa usar o Cloud Name real da sua conta.")
        print()
        return False
    else:
        print("✅ Cloud Name parece estar correto")
        return True

def test_connection():
    """Testa conexão com Cloudinary"""
    try:
        import cloudinary
        import cloudinary.api
        
        load_dotenv()
        
        cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
        api_key = os.getenv("CLOUDINARY_API_KEY")
        api_secret = os.getenv("CLOUDINARY_API_SECRET")
        
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret
        )
        
        result = cloudinary.api.ping()
        if result.get('status') == 'ok':
            print("✅ Conexão com Cloudinary: SUCESSO!")
            return True
        else:
            print("❌ Erro na conexão com Cloudinary")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar conexão: {str(e)}")
        return False

def main():
    print("🎴 MyPokeBinder - Correção do Cloudinary")
    print("=" * 50)
    print()
    
    # Verificar configuração atual
    if not check_current_config():
        show_cloudinary_guide()
        return
    
    # Testar conexão
    print("🔗 Testando conexão...")
    if test_connection():
        print("\n🎉 Cloudinary configurado corretamente!")
        print("🚀 Você pode agora usar o aplicativo!")
    else:
        print("\n❌ Ainda há problemas com a configuração")
        show_cloudinary_guide()

if __name__ == "__main__":
    main()
