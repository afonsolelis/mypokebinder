#!/usr/bin/env python3
"""
Script para atualizar o banco de dados e adicionar a coluna user_email
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
        # SQL para adicionar a coluna user_email
        sql = """
        ALTER TABLE cards 
        ADD COLUMN IF NOT EXISTS user_email TEXT;
        """
        
        # Executar via RPC
        result = supabase.rpc('exec_sql', {'sql': sql}).execute()
        print("✅ Coluna user_email adicionada com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao adicionar coluna: {str(e)}")
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
        
        # Para cada card, tentar buscar o email do usuário
        updated_count = 0
        for card in result.data:
            try:
                # Buscar informações do usuário pelo user_id
                # Como não temos acesso direto aos usuários, vamos pular por enquanto
                # Em uma implementação futura, poderíamos usar a API de admin
                print(f"⚠️ Card {card['id']} precisa de email do usuário {card['user_id']}")
                
            except Exception as e:
                print(f"❌ Erro ao atualizar card {card['id']}: {str(e)}")
        
        print(f"📊 {updated_count} cards atualizados")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao atualizar cards: {str(e)}")
        return False

def main():
    print("🔧 Atualizando banco de dados...")
    print("=" * 50)
    
    # Adicionar coluna user_email
    if add_user_email_column():
        # Atualizar cards existentes
        update_existing_cards()
    
    print("=" * 50)
    print("✅ Atualização concluída!")
    print("\n📋 Próximos passos:")
    print("1. Os novos cards terão o email automaticamente")
    print("2. Para cards existentes, você pode:")
    print("   - Deletar e recriar os cards")
    print("   - Ou atualizar manualmente no Supabase")
    print("3. Teste a funcionalidade de páginas públicas!")

if __name__ == "__main__":
    main()
