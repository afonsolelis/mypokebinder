#!/usr/bin/env python3
"""
Script para corrigir o banco de dados adicionando a coluna user_email
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Inicializar cliente Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def add_user_email_column():
    """Adiciona a coluna user_email na tabela cards"""
    try:
        # Tentar executar SQL diretamente via RPC
        sql = "ALTER TABLE cards ADD COLUMN IF NOT EXISTS user_email TEXT;"
        
        # Tentar executar via RPC
        try:
            result = supabase.rpc('exec_sql', {'sql': sql}).execute()
            print("✅ Coluna user_email adicionada via RPC!")
            return True
        except Exception as rpc_error:
            print(f"⚠️ RPC falhou: {str(rpc_error)}")
            print("📋 Execute manualmente no Supabase SQL Editor:")
            print("=" * 50)
            print("ALTER TABLE cards ADD COLUMN IF NOT EXISTS user_email TEXT;")
            print("CREATE INDEX IF NOT EXISTS idx_cards_user_email ON cards(user_email);")
            print("=" * 50)
            return False
            
    except Exception as e:
        print(f"❌ Erro ao adicionar coluna: {str(e)}")
        return False

def check_column_exists():
    """Verifica se a coluna user_email existe"""
    try:
        # Tentar buscar cards com user_email
        result = supabase.table('cards').select('user_email').limit(1).execute()
        print("✅ Coluna user_email existe e está funcionando!")
        return True
    except Exception as e:
        if "column cards.user_email does not exist" in str(e):
            print("❌ Coluna user_email não existe")
            return False
        else:
            print(f"⚠️ Erro ao verificar coluna: {str(e)}")
            return False

def update_existing_cards():
    """Atualiza cards existentes com o email do usuário"""
    try:
        # Buscar todos os cards que não têm user_email
        result = supabase.table('cards').select('*').is_('user_email', 'null').execute()
        
        if not result.data:
            print("✅ Todos os cards já têm user_email!")
            return True
        
        print(f"📝 Encontrados {len(result.data)} cards para atualizar...")
        print("⚠️ Para atualizar cards existentes, você precisa:")
        print("   1. Deletar e recriar os cards, ou")
        print("   2. Atualizar manualmente no Supabase")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar cards: {str(e)}")
        return False

def main():
    print("🔧 Corrigindo banco de dados...")
    print("=" * 50)
    
    # Verificar se a coluna existe
    if check_column_exists():
        print("✅ Banco de dados já está correto!")
        update_existing_cards()
    else:
        # Tentar adicionar a coluna
        if add_user_email_column():
            print("✅ Coluna adicionada com sucesso!")
            update_existing_cards()
        else:
            print("❌ Não foi possível adicionar a coluna automaticamente")
            print("\n📋 INSTRUÇÕES MANUAIS:")
            print("1. Acesse o Supabase Dashboard")
            print("2. Vá para SQL Editor")
            print("3. Execute o SQL do arquivo 'add_user_email_column.sql'")
            print("4. Ou execute diretamente:")
            print("   ALTER TABLE cards ADD COLUMN IF NOT EXISTS user_email TEXT;")
    
    print("=" * 50)
    print("✅ Verificação concluída!")

if __name__ == "__main__":
    main()
