# 🎴 MyPokeBinder

Um aplicativo web para colecionadores de cards Pokémon criado com Streamlit e Supabase.

## 🚀 Funcionalidades

- **Autenticação de Usuários**: Sistema de login/registro com Supabase Auth
- **Gerenciamento de Cards**: Cadastro, edição e exclusão de cards
- **Upload de Imagens**: Armazenamento de fotos dos cards no Supabase Storage
- **Páginas Públicas**: Cada usuário tem uma página pública para compartilhar sua coleção
- **Filtros e Busca**: Filtros por nome, linguagem e ordenação por diferentes critérios
- **Interface Responsiva**: Design moderno e intuitivo

## 📋 Pré-requisitos

- Python 3.8+
- Conta no Supabase
- Conta no GitHub (opcional, para deploy)

## 🛠️ Configuração

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd mypokebinder
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure o Cloudinary

1. Crie uma conta em [cloudinary.com](https://cloudinary.com)
2. Obtenha suas credenciais (Cloud Name, API Key, API Secret)
3. Configure no arquivo `.env`:
   ```env
   CLOUDINARY_CLOUD_NAME=seu_cloud_name
   CLOUDINARY_API_KEY=sua_api_key
   CLOUDINARY_API_SECRET=sua_api_secret
   ```

**📖 Para mais detalhes, consulte [CLOUDINARY_SETUP.md](CLOUDINARY_SETUP.md)**

### 4. Configure o Supabase

#### 3.1 Crie um projeto no Supabase
1. Acesse [supabase.com](https://supabase.com)
2. Crie uma nova conta ou faça login
3. Crie um novo projeto
4. Anote a URL e a chave anônima do projeto

#### 3.2 Configure o banco de dados
Execute os seguintes comandos SQL no SQL Editor do Supabase:

```sql
-- Criar tabela de cards
CREATE TABLE cards (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    number VARCHAR(50) NOT NULL,
    language VARCHAR(50) NOT NULL,
    estimated_value DECIMAL(10,2) DEFAULT 0.00,
    description TEXT,
    image_url TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Criar índices para melhor performance
CREATE INDEX idx_cards_user_id ON cards(user_id);
CREATE INDEX idx_cards_name ON cards(name);
CREATE INDEX idx_cards_language ON cards(language);

-- Habilitar RLS (Row Level Security)
ALTER TABLE cards ENABLE ROW LEVEL SECURITY;

-- Política para usuários verem apenas seus próprios cards
CREATE POLICY "Users can view their own cards" ON cards
    FOR SELECT USING (auth.uid() = user_id);

-- Política para usuários inserirem seus próprios cards
CREATE POLICY "Users can insert their own cards" ON cards
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Política para usuários atualizarem seus próprios cards
CREATE POLICY "Users can update their own cards" ON cards
    FOR UPDATE USING (auth.uid() = user_id);

-- Política para usuários deletarem seus próprios cards
CREATE POLICY "Users can delete their own cards" ON cards
    FOR DELETE USING (auth.uid() = user_id);

-- Política para visualização pública (apenas leitura)
CREATE POLICY "Public can view all cards" ON cards
    FOR SELECT USING (true);
```

#### 4.3 Configure o Banco de Dados

**Nota**: Com o Cloudinary, não precisamos mais do Storage do Supabase para imagens.

### 5. Configure as variáveis de ambiente

1. **Copie o arquivo de exemplo:**
   ```bash
   cp env.example .env
   ```

2. **Edite o arquivo `.env`** e preencha com suas credenciais:
   ```env
   # Supabase
   SUPABASE_URL=sua_url_do_supabase
   SUPABASE_KEY=sua_chave_anonima_do_supabase
   
   # Cloudinary
   CLOUDINARY_CLOUD_NAME=seu_cloud_name
   CLOUDINARY_API_KEY=sua_api_key
   CLOUDINARY_API_SECRET=sua_api_secret
   ```

**📖 Para mais detalhes sobre cada variável, consulte o arquivo `env.example`**

### 6. Execute o aplicativo
```bash
streamlit run app.py
```

O aplicativo estará disponível em `http://localhost:8501`

## 📱 Como usar

### Para usuários logados:
1. **Registro/Login**: Crie uma conta ou faça login
2. **Adicionar Cards**: Use a seção "Adicionar Card" para cadastrar novos cards
3. **Gerenciar Binder**: Visualize, edite e organize seus cards na seção "Meu Binder"
4. **Página Pública**: Compartilhe sua coleção através da URL pública

### Para visitantes:
- Acesse a URL pública de qualquer usuário para ver sua coleção
- Visualize os cards em detalhes clicando neles

## 🗂️ Estrutura do Projeto

```
mypokebinder/
├── app.py              # Aplicação principal
├── config.py           # Configurações e conexão com Supabase
├── requirements.txt    # Dependências Python
├── README.md          # Este arquivo
└── .env              # Variáveis de ambiente (não versionado)
```

## 🔧 Tecnologias Utilizadas

- **Streamlit**: Framework web para Python
- **Supabase**: Backend-as-a-Service (Auth, Database)
- **PostgreSQL**: Banco de dados relacional
- **Cloudinary**: Gerenciamento e otimização de imagens
- **Pillow**: Processamento de imagens local

## 🚀 Deploy

### Deploy no Streamlit Cloud
1. Faça push do código para o GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte seu repositório
4. Configure as variáveis de ambiente no painel do Streamlit Cloud
5. Deploy!

### Deploy no Heroku
1. Crie um arquivo `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

2. Configure as variáveis de ambiente no painel do Heroku
3. Deploy usando Git

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

Se você encontrar algum problema ou tiver dúvidas:

1. Verifique se todas as configurações do Supabase estão corretas
2. Certifique-se de que as variáveis de ambiente estão configuradas
3. Verifique se o bucket de storage foi criado corretamente
4. Abra uma issue no GitHub

## 🎯 Roadmap

- [ ] Sistema de tags para cards
- [ ] Estatísticas da coleção
- [ ] Sistema de trocas entre usuários
- [ ] API para integração com outros sistemas
- [ ] App mobile (React Native)
- [ ] Sistema de notificações
- [ ] Backup automático da coleção
