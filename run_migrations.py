#!/usr/bin/env python3
"""
Script para executar migrations do banco de dados
"""

import os
import sys
from config import supabase

def run_migration(migration_file):
    """Executa um arquivo de migration"""
    try:
        with open(migration_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        print(f"Executando migration: {migration_file}")
        
        # Executar o SQL
        result = supabase.rpc('exec_sql', {'sql': sql_content}).execute()
        
        print(f"✅ Migration {migration_file} executada com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao executar migration {migration_file}: {str(e)}")
        return False

def run_all_migrations():
    """Executa todas as migrations na ordem"""
    migrations_dir = "migrations"
    
    if not os.path.exists(migrations_dir):
        print(f"❌ Diretório {migrations_dir} não encontrado")
        return False
    
    # Listar arquivos de migration em ordem
    migration_files = []
    for file in os.listdir(migrations_dir):
        if file.endswith('.sql'):
            migration_files.append(os.path.join(migrations_dir, file))
    
    migration_files.sort()  # Ordenar por nome
    
    if not migration_files:
        print("❌ Nenhum arquivo de migration encontrado")
        return False
    
    print(f"🎴 MyPokeBinder - Executando Migrations")
    print("=" * 50)
    
    success_count = 0
    total_count = len(migration_files)
    
    for migration_file in migration_files:
        if run_migration(migration_file):
            success_count += 1
        else:
            print(f"⚠️  Parando execução devido a erro na migration {migration_file}")
            break
    
    print("=" * 50)
    print(f"📊 Resultado: {success_count}/{total_count} migrations executadas com sucesso")
    
    if success_count == total_count:
        print("🎉 Todas as migrations foram executadas com sucesso!")
        return True
    else:
        print("❌ Algumas migrations falharam")
        return False

def main():
    """Função principal"""
    if len(sys.argv) > 1:
        # Executar migration específica
        migration_file = sys.argv[1]
        if os.path.exists(migration_file):
            run_migration(migration_file)
        else:
            print(f"❌ Arquivo de migration não encontrado: {migration_file}")
    else:
        # Executar todas as migrations
        run_all_migrations()

if __name__ == "__main__":
    main()
