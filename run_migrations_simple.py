#!/usr/bin/env python3
"""
Script simples para executar migrations do banco de dados
"""

import os
import sys
from config import supabase

def run_migration_directly():
    """Executa a migration diretamente no Supabase"""
    try:
        print("🗄️ Executando configuração do banco de dados...")
        
        # SQL para criar a tabela e configurações
        sql_commands = [
            # 1. Criar tabela de cards
            """
            CREATE TABLE IF NOT EXISTS cards (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
                name VARCHAR(255) NOT NULL,
                number VARCHAR(50) NOT NULL,
                language VARCHAR(50) NOT NULL,
                estimated_value DECIMAL(10,2) DEFAULT 0.00,
                description TEXT,
                image_url TEXT NOT NULL,
                cloudinary_public_id VARCHAR(255),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """,
            
            # 2. Criar índices
            """
            CREATE INDEX IF NOT EXISTS idx_cards_user_id ON cards(user_id);
            CREATE INDEX IF NOT EXISTS idx_cards_name ON cards(name);
            CREATE INDEX IF NOT EXISTS idx_cards_language ON cards(language);
            CREATE INDEX IF NOT EXISTS idx_cards_created_at ON cards(created_at);
            """,
            
            # 3. Habilitar RLS
            """
            ALTER TABLE cards ENABLE ROW LEVEL SECURITY;
            """,
            
            # 4. Dropar políticas existentes
            """
            DROP POLICY IF EXISTS "Users can view their own cards" ON cards;
            DROP POLICY IF EXISTS "Users can insert their own cards" ON cards;
            DROP POLICY IF EXISTS "Users can update their own cards" ON cards;
            DROP POLICY IF EXISTS "Users can delete their own cards" ON cards;
            DROP POLICY IF EXISTS "Public can view all cards" ON cards;
            """,
            
            # 5. Criar políticas
            """
            CREATE POLICY "Users can view their own cards" ON cards
                FOR SELECT USING (auth.uid() = user_id);
            """,
            
            """
            CREATE POLICY "Users can insert their own cards" ON cards
                FOR INSERT WITH CHECK (auth.uid() = user_id);
            """,
            
            """
            CREATE POLICY "Users can update their own cards" ON cards
                FOR UPDATE USING (auth.uid() = user_id);
            """,
            
            """
            CREATE POLICY "Users can delete their own cards" ON cards
                FOR DELETE USING (auth.uid() = user_id);
            """,
            
            """
            CREATE POLICY "Public can view all cards" ON cards
                FOR SELECT USING (true);
            """,
            
            # 6. Função para updated_at
            """
            CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = NOW();
                RETURN NEW;
            END;
            $$ language 'plpgsql';
            """,
            
            # 7. Trigger
            """
            DROP TRIGGER IF EXISTS update_cards_updated_at ON cards;
            CREATE TRIGGER update_cards_updated_at
                BEFORE UPDATE ON cards
                FOR EACH ROW
                EXECUTE FUNCTION update_updated_at_column();
            """
        ]
        
        # Executar cada comando SQL
        for i, sql in enumerate(sql_commands, 1):
            try:
                print(f"  Executando comando {i}/{len(sql_commands)}...")
                
                # Usar rpc para executar SQL
                result = supabase.rpc('exec_sql', {'sql': sql.strip()}).execute()
                
                print(f"  ✅ Comando {i} executado com sucesso")
                
            except Exception as e:
                print(f"  ⚠️ Comando {i} falhou: {str(e)}")
                print("  Continuando com os próximos comandos...")
        
        print("✅ Configuração do banco concluída!")
        return True
        
    except Exception as e:
        print(f"❌ Erro geral: {str(e)}")
        return False

def create_exec_sql_function():
    """Cria a função exec_sql se ela não existir"""
    try:
        print("🔧 Criando função exec_sql...")
        
        sql = """
        CREATE OR REPLACE FUNCTION exec_sql(sql text)
        RETURNS void
        LANGUAGE plpgsql
        SECURITY DEFINER
        AS $$
        BEGIN
            EXECUTE sql;
        END;
        $$;
        """
        
        # Tentar executar via SQL direto
        result = supabase.rpc('exec_sql', {'sql': sql}).execute()
        print("✅ Função exec_sql criada com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar função exec_sql: {str(e)}")
        return False

def main():
    """Função principal"""
    print("🎴 MyPokeBinder - Configuração do Banco de Dados")
    print("=" * 50)
    
    # Tentar criar a função exec_sql primeiro
    if not create_exec_sql_function():
        print("\n⚠️ Não foi possível criar a função exec_sql.")
        print("📋 Execute manualmente o SQL no Supabase:")
        print("   - Vá para o SQL Editor do Supabase")
        print("   - Execute o conteúdo do arquivo 'supabase_setup.sql'")
        print("   - Ou copie e cole o SQL do arquivo 'supabase_setup.sql'")
        return False
    
    # Executar as migrations
    if run_migration_directly():
        print("\n🎉 Banco de dados configurado com sucesso!")
        print("🚀 Você pode agora executar: python start.py")
        return True
    else:
        print("\n❌ Erro na configuração do banco de dados")
        return False

if __name__ == "__main__":
    main()
