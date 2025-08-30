# 🗄️ Configuração do Supabase - MyPokeBinder

Este guia detalha como configurar o Supabase para o MyPokeBinder.

## 🚀 Configuração Inicial

### 1. Criar Projeto no Supabase

1. Acesse [supabase.com](https://supabase.com)
2. Faça login ou crie uma conta
3. Clique em "New Project"
4. Escolha sua organização
5. Dê um nome ao projeto (ex: "mypokebinder")
6. Escolha uma senha forte para o banco de dados
7. Escolha a região mais próxima
8. Clique em "Create new project"

### 2. Obter Credenciais

1. No painel do projeto, vá para **Settings** → **API**
2. Copie as seguintes informações:
   - **Project URL** → Use como `SUPABASE_URL`
   - **anon public** → Use como `SUPABASE_KEY`

### 3. Configurar Banco de Dados

Execute o seguinte SQL no **SQL Editor** do Supabase:

```sql
-- 🎴 MyPokeBinder - Configuração do Banco de Dados

-- 1. Criar tabela de cards
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

-- 2. Criar índices para performance
CREATE INDEX IF NOT EXISTS idx_cards_user_id ON cards(user_id);
CREATE INDEX IF NOT EXISTS idx_cards_name ON cards(name);
CREATE INDEX IF NOT EXISTS idx_cards_language ON cards(language);
CREATE INDEX IF NOT EXISTS idx_cards_created_at ON cards(created_at);

-- 3. Habilitar RLS (Row Level Security)
ALTER TABLE cards ENABLE ROW LEVEL SECURITY;

-- 4. Políticas de segurança
-- Usuários veem apenas seus próprios cards
CREATE POLICY "Users can view their own cards" ON cards
    FOR SELECT USING (auth.uid() = user_id);

-- Usuários inserem apenas seus próprios cards
CREATE POLICY "Users can insert their own cards" ON cards
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Usuários atualizam apenas seus próprios cards
CREATE POLICY "Users can update their own cards" ON cards
    FOR UPDATE USING (auth.uid() = user_id);

-- Usuários deletam apenas seus próprios cards
CREATE POLICY "Users can delete their own cards" ON cards
    FOR DELETE USING (auth.uid() = user_id);

-- Visualização pública (apenas leitura para visitantes)
CREATE POLICY "Public can view all cards" ON cards
    FOR SELECT USING (true);

-- 5. Função para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 6. Trigger para atualizar updated_at automaticamente
-- Primeiro, dropar o trigger se existir
DROP TRIGGER IF EXISTS update_cards_updated_at ON cards;

-- Depois, criar o trigger
CREATE TRIGGER update_cards_updated_at
    BEFORE UPDATE ON cards
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

### 4. Configurar Autenticação

1. No painel do Supabase, vá para **Authentication** → **Settings**
2. Configure as seguintes opções:
   - **Site URL**: `http://localhost:8501` (para desenvolvimento)
   - **Redirect URLs**: Adicione `http://localhost:8501`
   - **Enable email confirmations**: ✅ Ativado
   - **Enable email change confirmations**: ✅ Ativado

### 5. Configurar Email (Opcional)

1. **Authentication** → **Email Templates**
2. Personalize os templates de confirmação de email
3. Ou mantenha os templates padrão do Supabase

## 🔐 Como o RLS (Row Level Security) Funciona

### Para Usuários Logados:
- ✅ Veem apenas seus próprios cards
- ✅ Podem inserir novos cards
- ✅ Podem editar seus cards
- ✅ Podem deletar seus cards

### Para Visitantes (não logados):
- ✅ Veem todos os cards (somente leitura)
- ❌ Não podem inserir/editar/deletar

## 📊 Estrutura da Tabela

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | UUID | Identificador único |
| `user_id` | UUID | Referência ao usuário |
| `name` | VARCHAR(255) | Nome do card |
| `number` | VARCHAR(50) | Número do card |
| `language` | VARCHAR(50) | Idioma |
| `estimated_value` | DECIMAL(10,2) | Valor estimado |
| `description` | TEXT | Descrição opcional |
| `image_url` | TEXT | URL da imagem no Cloudinary |
| `cloudinary_public_id` | VARCHAR(255) | ID da imagem no Cloudinary |
| `created_at` | TIMESTAMP | Data de criação |
| `updated_at` | TIMESTAMP | Data de atualização |

## 🚀 Próximos Passos

1. **Execute o SQL** no Supabase SQL Editor
2. **Configure as variáveis** no arquivo `.env`
3. **Teste a configuração**: `python test_setup.py`
4. **Execute as migrations**: `python run_migrations.py`
5. **Inicie o aplicativo**: `python start.py`

## ⚠️ Importante

- **Não precisa criar Storage buckets** (usamos Cloudinary)
- **RLS é obrigatório** para segurança
- **As políticas garantem** que usuários só vejam seus dados
- **O sistema funciona** mesmo sem email configurado

## 🆘 Troubleshooting

### Erro de Sintaxe no Trigger
Se você encontrar erro de sintaxe no trigger, use esta versão alternativa:

```sql
-- Versão alternativa para o trigger
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'update_cards_updated_at') THEN
        CREATE TRIGGER update_cards_updated_at
            BEFORE UPDATE ON cards
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
    END IF;
END $$;
```

### Erro de Política Já Existente
Se as políticas já existirem, você pode dropar e recriar:

```sql
-- Dropar políticas existentes (se necessário)
DROP POLICY IF EXISTS "Users can view their own cards" ON cards;
DROP POLICY IF EXISTS "Users can insert their own cards" ON cards;
DROP POLICY IF EXISTS "Users can update their own cards" ON cards;
DROP POLICY IF EXISTS "Users can delete their own cards" ON cards;
DROP POLICY IF EXISTS "Public can view all cards" ON cards;
```

## 📞 Suporte

- **Documentação oficial**: [supabase.com/docs](https://supabase.com/docs)
- **Comunidade**: [github.com/supabase/supabase](https://github.com/supabase/supabase)
- **Discord**: [discord.supabase.com](https://discord.supabase.com)
