# 📋 Guia de Configuração - MyPokeBinder

Guia completo para configurar e executar o MyPokeBinder em 5 passos simples.

## 🚀 Configuração Rápida (5 Passos)

### **Passo 1: Clone e Dependências**
```bash
git clone <seu-repositorio>
cd mypokebinder
pip install -r requirements.txt
```

### **Passo 2: Configure o Cloudinary**
1. Crie conta em [cloudinary.com](https://cloudinary.com)
2. Obtenha suas credenciais no Dashboard
3. Configure no `.env`:
   ```env
   CLOUDINARY_CLOUD_NAME=seu_cloud_name
   CLOUDINARY_API_KEY=sua_api_key
   CLOUDINARY_API_SECRET=seu_api_secret
   ```

### **Passo 3: Configure o Supabase**
1. Crie projeto em [supabase.com](https://supabase.com)
2. Execute o SQL do arquivo `supabase_setup.sql`
3. Configure no `.env`:
   ```env
   SUPABASE_URL=sua_url_do_supabase
   SUPABASE_KEY=sua_chave_anonima
   ```

### **Passo 4: Execute o Script de Inicialização**
```bash
python start_windows.py  # Windows
# ou
python start.py          # Linux/Mac
```

### **Passo 5: Acesse a Aplicação**
- **Local:** http://localhost:8501
- **Produção:** https://mypokebinder.streamlit.app/

## ✅ Funcionalidades Implementadas

### **🔐 Autenticação Completa**
- ✅ Registro com confirmação de email
- ✅ Login seguro
- ✅ Sessões persistentes
- ✅ Logout

### **📱 Gestão de Cards**
- ✅ **Adicionar:** Foto, nome, número (027/182), idioma, valor, descrição
- ✅ **Editar:** Todos os campos editáveis
- ✅ **Deletar:** Remove imagem do Cloudinary + registro do banco
- ✅ **Visualizar:** Detalhes completos do card

### **🎯 Interface Avançada**
- ✅ **Grid responsivo** com 4 colunas
- ✅ **Filtros:** Por nome, idioma, ordenação
- ✅ **Navegação:** Botões sempre visíveis na sidebar
- ✅ **Feedback:** Spinners, mensagens de sucesso/erro
- ✅ **Redirecionamento:** Automático após ações

### **🌐 Páginas Públicas**
- ✅ **URLs únicas:** `https://mypokebinder.streamlit.app/?user=email@exemplo.com`
- ✅ **Acesso público:** Visualização sem login
- ✅ **Estatísticas:** Total, valor, idiomas, card mais valioso
- ✅ **Compartilhamento:** Links diretos para coleções

### **📊 Análises e Métricas**
- ✅ **Valor total** da coleção
- ✅ **Contagem** por idioma
- ✅ **Cards mais valiosos** em destaque
- ✅ **Métricas visuais** com Streamlit

## 🔧 Configuração Detalhada

### **Cloudinary Setup**
```bash
# Execute para verificar configuração
python check_cloudinary.py
```

### **Supabase Setup**
```bash
# Execute para verificar banco de dados
python fix_database.py
```

### **Teste Completo**
```bash
# Execute para testar toda a configuração
python test_setup.py
```

## 🎮 Como Usar

### **Para Usuários Finais**
1. **Acesse:** https://mypokebinder.streamlit.app/
2. **Registre-se** com email e senha
3. **Confirme** o email (verifique spam)
4. **Adicione cards** com fotos e detalhes
5. **Compartilhe** sua coleção via link público

### **Funcionalidades Principais**
- **👁️ Ver:** Visualizar detalhes do card
- **✏️ Editar:** Modificar informações do card
- **🗑️ Deletar:** Remover card da coleção
- **🔍 Filtrar:** Buscar por nome, idioma
- **📊 Ordenar:** Por nome, número, valor, data

### **Páginas Públicas**
- **URL exemplo:** `https://mypokebinder.streamlit.app/?user=seu@email.com`
- **Acesso:** Qualquer pessoa pode visualizar
- **Funcionalidades:** Filtros, ordenação, estatísticas

## 🚀 Deploy

### **Streamlit Cloud**
1. **Conecte** repositório ao Streamlit Cloud
2. **Configure** variáveis de ambiente:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `CLOUDINARY_CLOUD_NAME`
   - `CLOUDINARY_API_KEY`
   - `CLOUDINARY_API_SECRET`
3. **Deploy** automático

### **URLs de Produção**
- **Aplicação:** https://mypokebinder.streamlit.app/
- **Páginas públicas:** `https://mypokebinder.streamlit.app/?user=email@exemplo.com`

## 🔍 Solução de Problemas

### **Erro: "column cards.user_email does not exist"**
```bash
# Execute o script de correção
python fix_database.py
# Ou execute manualmente no Supabase SQL Editor:
ALTER TABLE cards ADD COLUMN IF NOT EXISTS user_email TEXT;
```

### **Erro: "Invalid cloud_name"**
- Verifique se `CLOUDINARY_CLOUD_NAME` está correto
- Execute: `python check_cloudinary.py`

### **Erro: "Could not find the function public.exec_sql"**
- Execute o SQL manualmente no Supabase SQL Editor
- Use o arquivo `supabase_setup.sql`

## 📚 Documentação Adicional

- [☁️ Cloudinary Setup](CLOUDINARY_SETUP.md)
- [🗄️ Supabase Setup](SUPABASE_SETUP.md)
- [🏗️ Estrutura do Projeto](PROJECT_STRUCTURE.md)

## 🎯 Próximos Passos

1. **Configure** todas as variáveis de ambiente
2. **Execute** os scripts de verificação
3. **Teste** a aplicação localmente
4. **Deploy** no Streamlit Cloud
5. **Compartilhe** sua coleção!

---

**🎴 MyPokeBinder** - Sua coleção de cards Pokémon organizada e compartilhável! ✨
