-- 🎴 MyPokeBinder - Configuração do Banco de Dados
-- Execute este SQL no SQL Editor do Supabase

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

-- 4. Dropar políticas existentes (se houver)
DROP POLICY IF EXISTS "Users can view their own cards" ON cards;
DROP POLICY IF EXISTS "Users can insert their own cards" ON cards;
DROP POLICY IF EXISTS "Users can update their own cards" ON cards;
DROP POLICY IF EXISTS "Users can delete their own cards" ON cards;
DROP POLICY IF EXISTS "Public can view all cards" ON cards;

-- 5. Criar políticas de segurança
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

-- 6. Função para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 7. Dropar trigger existente (se houver)
DROP TRIGGER IF EXISTS update_cards_updated_at ON cards;

-- 8. Criar trigger para atualizar updated_at automaticamente
CREATE TRIGGER update_cards_updated_at
    BEFORE UPDATE ON cards
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ✅ Configuração concluída!
-- Agora você pode usar o MyPokeBinder com o Supabase
