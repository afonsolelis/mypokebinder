-- Script para adicionar a coluna user_email na tabela cards
-- Execute este SQL diretamente no Supabase SQL Editor

-- Adicionar a coluna user_email se ela não existir
ALTER TABLE cards 
ADD COLUMN IF NOT EXISTS user_email TEXT;

-- Criar um índice para melhorar a performance das consultas por email
CREATE INDEX IF NOT EXISTS idx_cards_user_email ON cards(user_email);

-- Verificar se a coluna foi criada
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'cards' AND column_name = 'user_email';
