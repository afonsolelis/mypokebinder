import cloudinary
import cloudinary.uploader
import cloudinary.api
from PIL import Image
import io
import streamlit as st
from datetime import datetime
from cloudinary_config import cloudinary, DEFAULT_UPLOAD_CONFIG, IMAGE_TRANSFORMATIONS

def upload_image_to_cloudinary(image_file, user_id, folder=None):
    """
    Faz upload de uma imagem para o Cloudinary
    
    Args:
        image_file: Arquivo de imagem do Streamlit
        user_id: ID do usuário para organizar as imagens
        folder: Pasta no Cloudinary (padrão: pokebinder)
    
    Returns:
        dict: Dicionário com 'url' e 'public_id' da imagem
    """
    try:
        # Usa pasta padrão se não especificada
        if folder is None:
            folder = DEFAULT_UPLOAD_CONFIG['folder']
        
        # Lê a imagem
        image = Image.open(image_file)
        
        # Redimensiona se necessário
        max_width, max_height = DEFAULT_UPLOAD_CONFIG['max_dimensions']
        if image.size[0] > max_width or image.size[1] > max_height:
            image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        
        # Converte para bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG', optimize=True)
        img_byte_arr.seek(0)
        
        # Nome único para o arquivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        public_id = f"{folder}/{user_id}/{timestamp}"
        
        # Upload para o Cloudinary
        result = cloudinary.uploader.upload(
            img_byte_arr,
            public_id=public_id,
            folder=folder,
            resource_type=DEFAULT_UPLOAD_CONFIG['resource_type'],
            transformation=[
                {"width": max_width, "height": max_height, "crop": "limit"},
                {"quality": DEFAULT_UPLOAD_CONFIG['quality'], 
                 "fetch_format": DEFAULT_UPLOAD_CONFIG['fetch_format']}
            ]
        )
        
        return {
            'url': result['secure_url'],
            'public_id': result['public_id']
        }
        
    except Exception as e:
        st.error(f"Erro ao fazer upload da imagem: {str(e)}")
        return None

def delete_image_from_cloudinary(public_id):
    """
    Deleta uma imagem do Cloudinary
    
    Args:
        public_id: ID público da imagem no Cloudinary
    
    Returns:
        bool: True se deletado com sucesso, False caso contrário
    """
    try:
        result = cloudinary.uploader.destroy(public_id)
        return result.get('result') == 'ok'
    except Exception as e:
        st.error(f"Erro ao deletar imagem: {str(e)}")
        return False

def get_optimized_image_url(public_id, width=300, height=300, crop="fill"):
    """
    Gera URL otimizada da imagem do Cloudinary
    
    Args:
        public_id: ID público da imagem
        width: Largura desejada
        height: Altura desejada
        crop: Tipo de crop (fill, limit, scale, etc.)
    
    Returns:
        str: URL otimizada da imagem
    """
    try:
        return cloudinary.CloudinaryImage(public_id).build_url(
            width=width,
            height=height,
            crop=crop,
            quality="auto",
            fetch_format="auto"
        )
    except Exception as e:
        st.error(f"Erro ao gerar URL da imagem: {str(e)}")
        return None

def validate_image_file(image_file):
    """
    Valida arquivo de imagem
    
    Args:
        image_file: Arquivo de imagem do Streamlit
    
    Returns:
        tuple: (bool, str) - (é_válido, mensagem)
    """
    if image_file is None:
        return False, "Nenhuma imagem selecionada"
    
    # Verificar tipo de arquivo
    allowed_types = [f'image/{fmt}' for fmt in DEFAULT_UPLOAD_CONFIG['allowed_formats']]
    if image_file.type not in allowed_types:
        return False, f"Tipo de arquivo não suportado. Use: {', '.join(DEFAULT_UPLOAD_CONFIG['allowed_formats'])}"
    
    # Verificar tamanho
    max_size = DEFAULT_UPLOAD_CONFIG['max_file_size']
    if image_file.size > max_size:
        max_size_mb = max_size / (1024 * 1024)
        return False, f"Arquivo muito grande. Máximo {max_size_mb}MB"
    
    return True, "OK"

def get_image_info(public_id):
    """
    Obtém informações da imagem no Cloudinary
    
    Args:
        public_id: ID público da imagem
    
    Returns:
        dict: Informações da imagem
    """
    try:
        result = cloudinary.api.resource(public_id)
        return {
            'url': result['secure_url'],
            'width': result['width'],
            'height': result['height'],
            'format': result['format'],
            'size': result['bytes'],
            'created_at': result['created_at']
        }
    except Exception as e:
        st.error(f"Erro ao obter informações da imagem: {str(e)}")
        return None
