# 🚀 Guia Rápido de Configuração - MyPokeBinder

## ⚡ Configuração em 5 Passos

### 1. **Configure o Cloudinary**
1. Crie conta em [cloudinary.com](https://cloudinary.com)
2. Obtenha suas credenciais (Cloud Name, API Key, API Secret)
3. Configure no arquivo `.env`

### 2. **Configure o Supabase**
1. Crie conta em [supabase.com](https://supabase.com)
2. Crie um novo projeto
3. Obtenha suas credenciais (URL e anon key)
4. Configure no arquivo `.env`

### 3. **Configure o Banco de Dados**
**Opção A - Automática (Recomendada):**
```bash
python run_migrations_simple.py
```

**Opção B - Manual:**
1. Vá para o **SQL Editor** do Supabase
2. Execute o conteúdo do arquivo `supabase_setup.sql`

### 4. **Teste a Configuração**
```bash
python test_setup.py
```

### 5. **Inicie o Aplicativo**
```bash
python start.py
```

## 📋 Configuração Manual do Banco (Se necessário)

Se o script automático não funcionar, execute este SQL no **SQL Editor** do Supabase:

```sql
-- 🎴 MyPokeBinder - Configuração Manual

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

-- 2. Criar índices
CREATE INDEX IF NOT EXISTS idx_cards_user_id ON cards(user_id);
CREATE INDEX IF NOT EXISTS idx_cards_name ON cards(name);
CREATE INDEX IF NOT EXISTS idx_cards_language ON cards(language);
CREATE INDEX IF NOT EXISTS idx_cards_created_at ON cards(created_at);

-- 3. Habilitar RLS
ALTER TABLE cards ENABLE ROW LEVEL SECURITY;

-- 4. Dropar políticas existentes
DROP POLICY IF EXISTS "Users can view their own cards" ON cards;
DROP POLICY IF EXISTS "Users can insert their own cards" ON cards;
DROP POLICY IF EXISTS "Users can update their own cards" ON cards;
DROP POLICY IF EXISTS "Users can delete their own cards" ON cards;
DROP POLICY IF EXISTS "Public can view all cards" ON cards;

-- 5. Criar políticas
CREATE POLICY "Users can view their own cards" ON cards
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own cards" ON cards
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own cards" ON cards
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own cards" ON cards
    FOR DELETE USING (auth.uid() = user_id);

CREATE POLICY "Public can view all cards" ON cards
    FOR SELECT USING (true);

-- 6. Função para updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 7. Trigger
DROP TRIGGER IF EXISTS update_cards_updated_at ON cards;
CREATE TRIGGER update_cards_updated_at
    BEFORE UPDATE ON cards
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

## 🔧 Configuração do .env

Copie o arquivo `env.example` para `.env` e preencha:

```env
# Supabase
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key-here

# Cloudinary
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

## ✅ Verificação

Após a configuração, execute:

```bash
python test_setup.py
```

Você deve ver:
- ✅ Variáveis de ambiente: Configuradas
- ✅ Dependências: OK
- ✅ Cloudinary: OK
- ✅ Supabase: OK

## 🚀 Iniciar

```bash
python start.py
```

O aplicativo estará disponível em: `http://localhost:8501`

## 🆘 Problemas Comuns

### Erro de Conexão com Supabase
- Verifique se as credenciais estão corretas
- Verifique se o projeto está ativo

### Erro de Conexão com Cloudinary
- Verifique se as credenciais estão corretas
- Verifique se a conta está ativa

### Erro de Banco de Dados
- Execute o SQL manualmente no Supabase
- Verifique se as políticas RLS foram criadas

## 📞 Suporte

- **Documentação**: README.md
- **Cloudinary**: CLOUDINARY_SETUP.md
- **Supabase**: SUPABASE_SETUP.md
