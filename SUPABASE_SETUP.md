# 🗄️ Configuração do Supabase - MyPokeBinder

Guia completo para configurar o Supabase para o MyPokeBinder.

## 🚀 Configuração Rápida

### **1. Criar Projeto no Supabase**
1. Acesse [supabase.com](https://supabase.com)
2. Crie uma nova conta ou faça login
3. Clique em "New Project"
4. Escolha uma organização
5. Preencha os dados do projeto:
   - **Name:** MyPokeBinder
   - **Database Password:** (escolha uma senha forte)
   - **Region:** (escolha a mais próxima)
6. Clique em "Create new project"

### **2. Obter Credenciais**
1. Vá para **Settings** → **API**
2. Copie:
   - **Project URL** (ex: `https://xyz.supabase.co`)
   - **anon public** key (chave anônima)

### **3. Configurar Banco de Dados**
Execute o SQL do arquivo `supabase_setup.sql` no **SQL Editor** do Supabase.

## 📋 Script SQL Completo

```sql
-- 🎴 MyPokeBinder - Setup Completo do Supabase

-- 1. Criar tabela de cards
CREATE TABLE IF NOT EXISTS cards (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    user_email TEXT,                    -- ✅ Nova coluna para páginas públicas
    name VARCHAR(255) NOT NULL,
    number VARCHAR(50) NOT NULL,        -- Formato: 027/182
    language VARCHAR(50) NOT NULL,
    estimated_value DECIMAL(10,2) DEFAULT 0.00,
    description TEXT,
    image_url TEXT NOT NULL,            -- URL do Cloudinary
    cloudinary_public_id VARCHAR(255),  -- ID para deletar imagem
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Criar índices para performance
CREATE INDEX IF NOT EXISTS idx_cards_user_id ON cards(user_id);
CREATE INDEX IF NOT EXISTS idx_cards_user_email ON cards(user_email);
CREATE INDEX IF NOT EXISTS idx_cards_name ON cards(name);
CREATE INDEX IF NOT EXISTS idx_cards_language ON cards(language);
CREATE INDEX IF NOT EXISTS idx_cards_created_at ON cards(created_at);

-- 3. Habilitar Row Level Security (RLS)
ALTER TABLE cards ENABLE ROW LEVEL SECURITY;

-- 4. Dropar políticas existentes (se houver)
DROP POLICY IF EXISTS "Users can view their own cards" ON cards;
DROP POLICY IF EXISTS "Users can insert their own cards" ON cards;
DROP POLICY IF EXISTS "Users can update their own cards" ON cards;
DROP POLICY IF EXISTS "Users can delete their own cards" ON cards;
DROP POLICY IF EXISTS "Public can view all cards" ON cards;

-- 5. Criar políticas de segurança
-- Usuários podem ver apenas seus próprios cards
CREATE POLICY "Users can view their own cards" ON cards
    FOR SELECT USING (auth.uid() = user_id);

-- Usuários podem inserir seus próprios cards
CREATE POLICY "Users can insert their own cards" ON cards
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Usuários podem atualizar seus próprios cards
CREATE POLICY "Users can update their own cards" ON cards
    FOR UPDATE USING (auth.uid() = user_id);

-- Usuários podem deletar seus próprios cards
CREATE POLICY "Users can delete their own cards" ON cards
    FOR DELETE USING (auth.uid() = user_id);

-- Público pode ver todos os cards (para páginas públicas)
CREATE POLICY "Public can view all cards" ON cards
    FOR SELECT USING (true);

-- 6. Função para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 7. Trigger para atualizar updated_at
DROP TRIGGER IF EXISTS update_cards_updated_at ON cards;
CREATE TRIGGER update_cards_updated_at
    BEFORE UPDATE ON cards
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 8. Verificar se tudo foi criado corretamente
SELECT 
    table_name,
    column_name,
    data_type
FROM information_schema.columns 
WHERE table_name = 'cards'
ORDER BY ordinal_position;
```

## 🔐 Configuração de Autenticação

### **1. Habilitar Email Auth**
1. Vá para **Authentication** → **Settings**
2. Em **Email Auth**, certifique-se que está habilitado
3. Configure **Site URL** para: `https://mypokebinder.streamlit.app/`
4. Configure **Redirect URLs** para: `https://mypokebinder.streamlit.app/`

### **2. Configurar Templates de Email**
1. Vá para **Authentication** → **Email Templates**
2. Personalize os templates de:
   - **Confirm signup**
   - **Reset password**
   - **Magic Link**

### **3. Configurar Políticas de Senha**
1. Vá para **Authentication** → **Settings**
2. Configure:
   - **Minimum password length:** 6
   - **Enable email confirmations:** ✅
   - **Enable phone confirmations:** ❌

## 🛡️ Segurança e Políticas

### **Row Level Security (RLS)**
```sql
-- Políticas implementadas:
✅ Usuários só veem seus próprios cards
✅ Usuários só podem modificar seus cards
✅ Páginas públicas permitem visualização
✅ Validação automática de propriedade
```

### **Índices de Performance**
```sql
-- Índices criados:
✅ idx_cards_user_id      -- Busca por usuário
✅ idx_cards_user_email   -- Busca por email (páginas públicas)
✅ idx_cards_name         -- Busca por nome
✅ idx_cards_language     -- Filtro por idioma
✅ idx_cards_created_at   -- Ordenação por data
```

## 🔧 Configuração do .env

```env
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key-here

# Exemplo:
# SUPABASE_URL=https://abcdefghijklmnop.supabase.co
# SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## ✅ Verificação da Configuração

### **1. Teste Automático**
```bash
python test_setup.py
```

### **2. Teste Manual**
1. Vá para **Table Editor** no Supabase
2. Verifique se a tabela `cards` existe
3. Verifique se as políticas RLS estão ativas
4. Teste inserir um registro manualmente

### **3. Verificar Políticas**
```sql
-- Verificar políticas ativas
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual
FROM pg_policies 
WHERE tablename = 'cards';
```

## 🚨 Solução de Problemas

### **Erro: "column cards.user_email does not exist"**
```sql
-- Execute este SQL no Supabase SQL Editor:
ALTER TABLE cards ADD COLUMN IF NOT EXISTS user_email TEXT;
CREATE INDEX IF NOT EXISTS idx_cards_user_email ON cards(user_email);
```

### **Erro: "Could not find the function public.exec_sql"**
- Execute o SQL manualmente no **SQL Editor**
- Use o arquivo `supabase_setup.sql`

### **Erro: "RLS policy violation"**
```sql
-- Verificar se RLS está habilitado
SELECT schemaname, tablename, rowsecurity 
FROM pg_tables 
WHERE tablename = 'cards';

-- Verificar políticas
SELECT * FROM pg_policies WHERE tablename = 'cards';
```

### **Erro: "Foreign key violation"**
- Verifique se a tabela `auth.users` existe
- Verifique se o `user_id` está correto

## 📊 Monitoramento

### **Logs de Auditoria**
1. Vá para **Logs** no Supabase
2. Monitore:
   - **Auth logs** (logins/registros)
   - **Database logs** (queries)
   - **API logs** (requisições)

### **Métricas de Uso**
1. Vá para **Dashboard**
2. Monitore:
   - **Database size**
   - **API requests**
   - **Auth users**

## 🔄 Backup e Restauração

### **Backup Automático**
- Supabase faz backup automático diário
- Retenção de 7 dias para projetos gratuitos
- Retenção de 30 dias para projetos pagos

### **Backup Manual**
```sql
-- Exportar dados (via SQL Editor)
SELECT * FROM cards;
```

## 📈 Escalabilidade

### **Limites Gratuitos**
- **Database:** 500MB
- **API requests:** 50,000/month
- **Auth users:** 50,000
- **File storage:** 1GB

### **Upgrade para Pagos**
- **Pro:** $25/month
- **Team:** $599/month
- **Enterprise:** Contato

## 🎯 Próximos Passos

1. **Execute** o SQL de setup
2. **Configure** as variáveis de ambiente
3. **Teste** a conexão
4. **Deploy** a aplicação
5. **Monitore** o uso

---

**🗄️ Supabase** - Backend robusto e escalável para o MyPokeBinder! ✨
