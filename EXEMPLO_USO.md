# 📖 Exemplos de Uso - MyPokeBinder

Este arquivo contém exemplos práticos de como usar o MyPokeBinder.

## 🚀 Iniciando o Aplicativo

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar o aplicativo
streamlit run app.py
```

O aplicativo estará disponível em: `http://localhost:8501`

## 👤 Fluxo de Usuário

### 1. Primeiro Acesso

1. **Acesse o aplicativo**: `http://localhost:8501`
2. **Crie uma conta**:
   - Clique na aba "Registro"
   - Preencha email e senha
   - Confirme a senha
   - Clique em "Registrar"
   - Verifique seu email para confirmar a conta

3. **Faça login**:
   - Clique na aba "Login"
   - Digite seu email e senha
   - Clique em "Entrar"

### 2. Adicionando Cards

1. **Navegue para "Adicionar Card"**
2. **Preencha os dados**:
   - Nome do Card: "Pikachu"
   - Número: "025"
   - Linguagem: "Português"
   - Valor Estimado: 50.00
   - Descrição: "Meu primeiro Pikachu, muito especial!"
   - Foto: Faça upload de uma imagem do card

3. **Clique em "Cadastrar Card"**

### 3. Gerenciando seu Binder

1. **Vá para "Meu Binder"**
2. **Use os filtros**:
   - Filtrar por nome: Digite "Pikachu"
   - Filtrar por linguagem: Selecione "Português"
   - Ordenar por: "Valor" (mais valiosos primeiro)

3. **Visualize um card**:
   - Clique em "Ver" em qualquer card
   - Veja todos os detalhes
   - Clique em "Voltar" para retornar

4. **Edite um card**:
   - Clique em "Editar" em qualquer card
   - Modifique os dados
   - Faça upload de uma nova foto (opcional)
   - Clique em "Atualizar Card"

### 4. Compartilhando sua Coleção

1. **Vá para "Minha Página Pública"**
2. **Copie a URL** mostrada
3. **Compartilhe** com amigos ou nas redes sociais

## 🌐 Páginas Públicas

### Como Acessar

Para ver a coleção de outro usuário, use a URL:
```
http://localhost:8501?user=email@exemplo.com
```

### O que os Visitantes Veem

- Lista de todos os cards do usuário
- Miniaturas das imagens
- Nome, número e valor dos cards
- Possibilidade de clicar para ver detalhes
- **NÃO podem editar ou deletar cards**

## 📱 Funcionalidades Avançadas

### Filtros e Busca

- **Busca por nome**: Digite parte do nome do card
- **Filtro por linguagem**: Selecione um idioma específico
- **Ordenação**: Por nome, número, valor ou data de criação

### Estatísticas

O sistema calcula automaticamente:
- Total de cards na coleção
- Valor total estimado
- Valor médio por card
- Número de idiomas diferentes

### Upload de Imagens

- **Formatos suportados**: PNG, JPG, JPEG
- **Tamanho máximo**: 5MB
- **Processamento**: As imagens são redimensionadas automaticamente
- **Armazenamento**: No Supabase Storage

## 🔧 Configurações

### Personalização

Você pode personalizar o aplicativo editando:

1. **Tema**: `.streamlit/config.toml`
2. **Configurações**: `config.py`
3. **Utilitários**: `utils.py`

### Variáveis de Ambiente

Configure no arquivo `.env`:
```env
SUPABASE_URL=sua_url_do_supabase
SUPABASE_KEY=sua_chave_anonima_do_supabase
```

## 🚨 Solução de Problemas

### Erro de Login
- Verifique se o email foi confirmado
- Verifique se as credenciais estão corretas
- Tente criar uma nova conta

### Erro ao Fazer Upload
- Verifique se a imagem não excede 5MB
- Use formatos PNG, JPG ou JPEG
- Verifique a conexão com a internet

### Erro ao Salvar Card
- Verifique se todos os campos obrigatórios estão preenchidos
- Verifique se a imagem foi selecionada
- Verifique a conexão com o Supabase

### Página Pública Não Carrega
- Verifique se o email está correto na URL
- Verifique se o usuário existe
- Verifique se o usuário tem cards cadastrados

## 💡 Dicas de Uso

### Organização da Coleção
1. **Use nomes consistentes**: "Pikachu" em vez de "Pikachu #25"
2. **Numeração padronizada**: Use sempre o mesmo formato (ex: "025")
3. **Descrições úteis**: Adicione informações sobre raridade, condição, etc.
4. **Fotos de qualidade**: Tire fotos bem iluminadas dos cards

### Compartilhamento
1. **URLs amigáveis**: Compartilhe URLs diretas para cards específicos
2. **Redes sociais**: Use as imagens dos cards em posts
3. **Comunidade**: Conecte-se com outros colecionadores

### Backup
1. **Exporte dados**: Use as APIs do Supabase para backup
2. **Fotos**: Mantenha cópias das imagens originais
3. **Documentação**: Mantenha um registro offline da coleção

## 🎯 Próximos Passos

Após dominar o uso básico, você pode:

1. **Automatizar**: Criar scripts para importar cards em lote
2. **Integrar**: Conectar com APIs de preços de cards
3. **Expandir**: Adicionar mais campos (raridade, condição, etc.)
4. **Compartilhar**: Contribuir com melhorias no código

## 📞 Suporte

Se precisar de ajuda:

1. **Documentação**: Leia o README.md
2. **Configuração**: Consulte SUPABASE_SETUP.md
3. **Issues**: Abra uma issue no GitHub
4. **Comunidade**: Participe de fóruns de colecionadores
