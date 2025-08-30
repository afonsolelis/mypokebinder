# ☁️ Configuração do Cloudinary - MyPokeBinder

Este guia detalha como configurar o Cloudinary para o MyPokeBinder.

## 📋 Por que Cloudinary?

O Cloudinary oferece várias vantagens para o MyPokeBinder:

- **Otimização automática** de imagens
- **Transformações em tempo real** (redimensionamento, crop, etc.)
- **CDN global** para melhor performance
- **Interface amigável** para gerenciamento
- **Planos gratuitos** generosos (25GB de storage, 25GB de bandwidth/mês)
- **API robusta** para Python

## 🚀 Configuração

### 1. Criar Conta no Cloudinary

1. Acesse [cloudinary.com](https://cloudinary.com)
2. Clique em "Sign Up For Free"
3. Preencha seus dados
4. Verifique seu email

### 2. Obter Credenciais

1. Faça login no painel do Cloudinary
2. Vá para **Dashboard**
3. Copie as seguintes informações:
   - **Cloud Name**
   - **API Key**
   - **API Secret**

### 3. Configurar Variáveis de Ambiente

No seu arquivo `.env`, adicione:

```env
CLOUDINARY_CLOUD_NAME=seu_cloud_name
CLOUDINARY_API_KEY=sua_api_key
CLOUDINARY_API_SECRET=sua_api_secret
```

### 4. Configurações Padrão

O sistema usa as seguintes configurações padrão:

```python
DEFAULT_UPLOAD_CONFIG = {
    'folder': 'pokebinder',           # Pasta no Cloudinary
    'resource_type': 'image',         # Tipo de recurso
    'allowed_formats': ['png', 'jpg', 'jpeg', 'gif', 'webp'],
    'max_file_size': 10 * 1024 * 1024,  # 10MB
    'max_dimensions': (800, 800),     # Dimensões máximas
    'quality': 'auto',                # Qualidade automática
    'fetch_format': 'auto'            # Formato automático
}
```

## 📁 Estrutura de Pastas

As imagens são organizadas no Cloudinary da seguinte forma:

```
pokebinder/
├── user_id_1/
│   ├── 20241201_143022.png
│   ├── 20241201_143156.jpg
│   └── ...
├── user_id_2/
│   ├── 20241201_144500.png
│   └── ...
└── ...
```

## 🔧 Funcionalidades

### Upload de Imagens

```python
from cloudinary_utils import upload_image_to_cloudinary

# Upload básico
result = upload_image_to_cloudinary(image_file, user_id)

# Upload com pasta personalizada
result = upload_image_to_cloudinary(image_file, user_id, folder="minha_colecao")
```

### Transformações de Imagem

O sistema aplica automaticamente:

- **Redimensionamento**: Máximo 800x800 pixels
- **Otimização**: Qualidade automática
- **Formato**: Conversão automática para melhor performance

### URLs Otimizadas

```python
from cloudinary_utils import get_optimized_image_url

# Thumbnail (150x150)
thumbnail_url = get_optimized_image_url(public_id, 150, 150, "fill")

# Imagem média (300x300)
medium_url = get_optimized_image_url(public_id, 300, 300, "fill")

# Imagem grande (600x600)
large_url = get_optimized_image_url(public_id, 600, 600, "limit")
```

## 🗑️ Gerenciamento de Imagens

### Deletar Imagem

```python
from cloudinary_utils import delete_image_from_cloudinary

# Deletar por public_id
success = delete_image_from_cloudinary(public_id)
```

### Informações da Imagem

```python
from cloudinary_utils import get_image_info

# Obter informações detalhadas
info = get_image_info(public_id)
# Retorna: URL, dimensões, formato, tamanho, data de criação
```

## 📊 Monitoramento

### Dashboard do Cloudinary

1. **Usage**: Acompanhe o uso de storage e bandwidth
2. **Media Library**: Visualize todas as imagens
3. **Analytics**: Estatísticas de performance

### Logs de Upload

O sistema registra:
- Sucesso/falha de uploads
- Tamanho e formato das imagens
- Erros de validação

## 🚨 Troubleshooting

### Erro de Upload

**Problema**: "Invalid signature"
**Solução**: Verifique se as credenciais estão corretas

**Problema**: "File too large"
**Solução**: Verifique se o arquivo não excede 10MB

**Problema**: "Invalid file type"
**Solução**: Use apenas formatos suportados (PNG, JPG, JPEG, GIF, WebP)

### Erro de Conexão

**Problema**: "Connection timeout"
**Solução**: Verifique sua conexão com a internet

**Problema**: "API rate limit exceeded"
**Solução**: Aguarde alguns minutos ou verifique seu plano

## 💡 Dicas de Uso

### Otimização de Performance

1. **Use formatos WebP** quando possível
2. **Redimensione** antes do upload se necessário
3. **Comprima** imagens grandes

### Organização

1. **Use pastas** para organizar por usuário
2. **Nomes descritivos** para facilitar busca
3. **Tags** para categorização (opcional)

### Backup

1. **Mantenha cópias** das imagens originais
2. **Use a API** para exportar em lote
3. **Monitore** o uso de storage

## 🔒 Segurança

### Políticas de Acesso

- **Upload**: Apenas usuários autenticados
- **Visualização**: Pública (para páginas públicas)
- **Deleção**: Apenas o dono da imagem

### Validação

- **Tipo de arquivo**: Apenas imagens
- **Tamanho**: Máximo 10MB
- **Dimensões**: Máximo 800x800 pixels

## 📈 Escalabilidade

### Planos Gratuitos

- **Storage**: 25GB
- **Bandwidth**: 25GB/mês
- **Transformações**: Ilimitadas

### Planos Pagos

- **Pro**: $89/mês (100GB storage, 100GB bandwidth)
- **Advanced**: $224/mês (225GB storage, 225GB bandwidth)

## 📞 Suporte

### Recursos

1. **Documentação oficial**: [docs.cloudinary.com](https://docs.cloudinary.com)
2. **Comunidade**: [community.cloudinary.com](https://community.cloudinary.com)
3. **Suporte técnico**: Disponível em planos pagos

### Contato

- **Email**: support@cloudinary.com
- **Chat**: Disponível no painel
- **GitHub**: [github.com/cloudinary](https://github.com/cloudinary)
