-- 🎴 MyPokeBinder - Fix User Email Column
-- Execute este SQL no Supabase SQL Editor

-- 1. Adicionar a coluna user_email se ela não existir
ALTER TABLE cards 
ADD COLUMN IF NOT EXISTS user_email TEXT;

-- 2. Criar índice para melhorar performance
CREATE INDEX IF NOT EXISTS idx_cards_user_email ON cards(user_email);

-- 3. Atualizar cards existentes com o email do usuário
-- (Isso só funciona se você tiver acesso aos dados dos usuários)
UPDATE cards 
SET user_email = (
    SELECT email 
    FROM auth.users 
    WHERE auth.users.id = cards.user_id
)
WHERE user_email IS NULL;

-- 4. Verificar se a coluna foi criada
SELECT 
    column_name, 
    data_type, 
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'cards' 
AND column_name = 'user_email';

-- 5. Verificar quantos cards têm user_email
SELECT 
    COUNT(*) as total_cards,
    COUNT(user_email) as cards_with_email,
    COUNT(*) - COUNT(user_email) as cards_without_email
FROM cards;

-- 6. Mostrar alguns exemplos de cards
SELECT 
    id,
    name,
    user_id,
    user_email,
    created_at
FROM cards 
LIMIT 5;
