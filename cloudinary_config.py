import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Carrega as variáveis de ambiente
load_dotenv()

# Configurações do Cloudinary
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

# Valida se as variáveis estão configuradas
if not all([CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET]):
    raise ValueError("""
    Configurações do Cloudinary não encontradas!
    
    Certifique-se de que o arquivo .env contém:
    CLOUDINARY_CLOUD_NAME=seu_cloud_name
    CLOUDINARY_API_KEY=sua_api_key
    CLOUDINARY_API_SECRET=sua_api_secret
    """)

# Configura o Cloudinary
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

# Configurações padrão para uploads
DEFAULT_UPLOAD_CONFIG = {
    'folder': 'pokebinder',
    'resource_type': 'image',
    'allowed_formats': ['png', 'jpg', 'jpeg', 'gif', 'webp'],
    'max_file_size': 10 * 1024 * 1024,  # 10MB
    'max_dimensions': (800, 800),
    'quality': 'auto',
    'fetch_format': 'auto'
}

# Transformações padrão para diferentes tamanhos
IMAGE_TRANSFORMATIONS = {
    'thumbnail': {'width': 150, 'height': 150, 'crop': 'fill'},
    'medium': {'width': 300, 'height': 300, 'crop': 'fill'},
    'large': {'width': 600, 'height': 600, 'crop': 'limit'},
    'original': {'width': 800, 'height': 800, 'crop': 'limit'}
}

def get_cloudinary_config():
    """Retorna a configuração atual do Cloudinary"""
    return {
        'cloud_name': CLOUDINARY_CLOUD_NAME,
        'api_key': CLOUDINARY_API_KEY,
        'folder': DEFAULT_UPLOAD_CONFIG['folder']
    }

def validate_cloudinary_connection():
    """Valida se a conexão com o Cloudinary está funcionando"""
    try:
        # Tenta fazer uma operação simples
        result = cloudinary.api.ping()
        return result.get('status') == 'ok'
    except Exception as e:
        return False, str(e)
