-- Migration: 001_create_cards_table.sql
-- Descrição: Cria a tabela de cards para o MyPokeBinder

-- Criar tabela de cards
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

-- Criar índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_cards_user_id ON cards(user_id);
CREATE INDEX IF NOT EXISTS idx_cards_name ON cards(name);
CREATE INDEX IF NOT EXISTS idx_cards_language ON cards(language);
CREATE INDEX IF NOT EXISTS idx_cards_created_at ON cards(created_at);

-- Habilitar RLS (Row Level Security)
ALTER TABLE cards ENABLE ROW LEVEL SECURITY;

-- Política para usuários verem apenas seus próprios cards
CREATE POLICY IF NOT EXISTS "Users can view their own cards" ON cards
    FOR SELECT USING (auth.uid() = user_id);

-- Política para usuários inserirem seus próprios cards
CREATE POLICY IF NOT EXISTS "Users can insert their own cards" ON cards
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Política para usuários atualizarem seus próprios cards
CREATE POLICY IF NOT EXISTS "Users can update their own cards" ON cards
    FOR UPDATE USING (auth.uid() = user_id);

-- Política para usuários deletarem seus próprios cards
CREATE POLICY IF NOT EXISTS "Users can delete their own cards" ON cards
    FOR DELETE USING (auth.uid() = user_id);

-- Política para visualização pública (apenas leitura)
CREATE POLICY IF NOT EXISTS "Public can view all cards" ON cards
    FOR SELECT USING (true);

-- Função para atualizar o campo updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para atualizar updated_at automaticamente
CREATE TRIGGER IF NOT EXISTS update_cards_updated_at 
    BEFORE UPDATE ON cards 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
