# 🎴 MyPokeBinder

Uma aplicação web completa para colecionadores de cards Pokémon, desenvolvida com **Streamlit**, **Supabase** e **Cloudinary**.

## ✨ Funcionalidades

### 🔐 **Autenticação**
- ✅ Registro e login com Supabase Auth
- ✅ Confirmação de email
- ✅ Sessões seguras

### 📱 **Gestão de Cards**
- ✅ **Adicionar cards** com foto, nome, número, idioma, valor e descrição
- ✅ **Editar cards** existentes (todos os campos)
- ✅ **Deletar cards** (remove imagem do Cloudinary e registro do banco)
- ✅ **Visualizar cards** em detalhes
- ✅ **Validação de número** do card (formato 027/182 com campos separados)
- ✅ **Upload de imagens** otimizado via Cloudinary

### 🎯 **Interface Intuitiva**
- ✅ **Grid responsivo** de cards
- ✅ **Filtros** por nome, idioma e ordenação
- ✅ **Navegação** com botões sempre visíveis
- ✅ **Feedback visual** (spinners, mensagens de sucesso/erro)
- ✅ **Redirecionamento automático** após ações

### 🌐 **Páginas Públicas**
- ✅ **Compartilhamento** de coleções via URL
- ✅ **Visualização pública** para não logados
- ✅ **Estatísticas** da coleção (total, valor, idiomas)
- ✅ **Cards mais valiosos** em destaque
- ✅ **Filtros e ordenação** nas páginas públicas

### 📊 **Estatísticas e Análises**
- ✅ **Valor total** da coleção
- ✅ **Contagem** de cards por idioma
- ✅ **Card mais valioso** identificado
- ✅ **Métricas visuais** com Streamlit

## 🚀 Tecnologias

- **Frontend:** Streamlit (Python)
- **Backend:** Supabase (PostgreSQL + Auth)
- **Storage:** Cloudinary (imagens)
- **Deploy:** Streamlit Cloud

## 📋 Pré-requisitos

- Python 3.8+
- Conta no Supabase
- Conta no Cloudinary
- Git

## 🛠️ Instalação

### 1. **Clone o repositório**
```bash
git clone <seu-repositorio>
cd mypokebinder
```

### 2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

### 3. **Configure as variáveis de ambiente**
```bash
cp env.example .env
```

Edite o arquivo `.env` com suas credenciais:
```env
# Supabase
SUPABASE_URL=sua_url_do_supabase
SUPABASE_KEY=sua_chave_do_supabase

# Cloudinary
CLOUDINARY_CLOUD_NAME=seu_cloud_name
CLOUDINARY_API_KEY=sua_api_key
CLOUDINARY_API_SECRET=seu_api_secret
```

### 4. **Configure o Supabase**
Execute o SQL do arquivo `supabase_setup.sql` no SQL Editor do Supabase.

### 5. **Execute o script de inicialização**
```bash
python start_windows.py  # Para Windows
# ou
python start.py          # Para Linux/Mac
```

## 📚 Estrutura do Projeto

```
mypokebinder/
├── app.py                 # Aplicação principal
├── config.py             # Configurações do Supabase
├── cloudinary_config.py  # Configurações do Cloudinary
├── cloudinary_utils.py   # Utilitários do Cloudinary
├── requirements.txt      # Dependências Python
├── .streamlit/          # Configurações do Streamlit
├── migrations/          # Scripts de migração
├── docs/               # Documentação
└── scripts/            # Scripts auxiliares
```

## 🎮 Como Usar

### **Para Usuários**
1. **Acesse:** https://mypokebinder.streamlit.app/
2. **Registre-se** ou faça login
3. **Adicione cards** com fotos e detalhes
4. **Compartilhe** sua coleção via link público
5. **Gerencie** seus cards (editar/deletar)

### **Para Desenvolvedores**
1. Clone e configure o projeto
2. Execute `python start_windows.py`
3. Acesse `http://localhost:8501`

## 🔧 Funcionalidades Técnicas

### **Gestão de Cards**
- **CRUD completo** (Create, Read, Update, Delete)
- **Validação de entrada** (números, imagens)
- **Upload otimizado** de imagens
- **Limpeza automática** do storage

### **Páginas Públicas**
- **URLs únicas** por usuário
- **Acesso sem login** para visualização
- **Filtros e ordenação** públicos
- **Estatísticas em tempo real**

### **Segurança**
- **Row Level Security** (RLS) no Supabase
- **Autenticação** via Supabase Auth
- **Validação** de propriedade dos cards
- **Sanitização** de inputs

## 📖 Documentação Adicional

- [📋 Guia de Configuração](SETUP_GUIDE.md)
- [☁️ Configuração do Cloudinary](CLOUDINARY_SETUP.md)
- [🗄️ Configuração do Supabase](SUPABASE_SETUP.md)
- [🏗️ Estrutura do Projeto](PROJECT_STRUCTURE.md)

## 🚀 Deploy

### **Streamlit Cloud**
1. Conecte seu repositório ao Streamlit Cloud
2. Configure as variáveis de ambiente
3. Deploy automático

### **URL de Produção**
- **Aplicação:** https://mypokebinder.streamlit.app/
- **Páginas públicas:** `https://mypokebinder.streamlit.app/?user=email@exemplo.com`

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

- **Issues:** Abra uma issue no GitHub
- **Documentação:** Consulte os arquivos `.md` na pasta `docs/`
- **Configuração:** Siga o [Guia de Configuração](SETUP_GUIDE.md)

---

**🎴 MyPokeBinder** - Organize, compartilhe e gerencie sua coleção de cards Pokémon! ✨
