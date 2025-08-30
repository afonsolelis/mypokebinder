import streamlit as st
from PIL import Image
import io
from datetime import datetime
from config import supabase

def format_currency(value):
    """Formata valor monetário"""
    return f"R$ {value:.2f}"

def format_date(date_string):
    """Formata data para exibição"""
    try:
        date_obj = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return date_obj.strftime('%d/%m/%Y %H:%M')
    except:
        return date_string

def validate_image_file(image_file):
    """Valida arquivo de imagem"""
    if image_file is None:
        return False, "Nenhuma imagem selecionada"
    
    # Verificar tipo de arquivo
    allowed_types = ['image/png', 'image/jpeg', 'image/jpg']
    if image_file.type not in allowed_types:
        return False, "Tipo de arquivo não suportado. Use PNG, JPG ou JPEG"
    
    # Verificar tamanho (máximo 5MB)
    if image_file.size > 5 * 1024 * 1024:
        return False, "Arquivo muito grande. Máximo 5MB"
    
    return True, "OK"

def resize_image(image, max_size=(800, 800)):
    """Redimensiona imagem mantendo proporção"""
    image.thumbnail(max_size, Image.Resampling.LANCZOS)
    return image

def get_user_by_email(email):
    """Busca usuário pelo email"""
    try:
        result = supabase.auth.admin.list_users()
        for user in result.users:
            if user.email == email:
                return user
        return None
    except Exception as e:
        st.error(f"Erro ao buscar usuário: {str(e)}")
        return None

def get_user_stats(user_id):
    """Retorna estatísticas do usuário"""
    try:
        cards = supabase.table('cards').select('*').eq('user_id', user_id).execute()
        
        if not cards.data:
            return {
                'total_cards': 0,
                'total_value': 0,
                'languages': [],
                'avg_value': 0
            }
        
        total_cards = len(cards.data)
        total_value = sum(card['estimated_value'] for card in cards.data)
        languages = list(set(card['language'] for card in cards.data))
        avg_value = total_value / total_cards if total_cards > 0 else 0
        
        return {
            'total_cards': total_cards,
            'total_value': total_value,
            'languages': languages,
            'avg_value': avg_value
        }
    except Exception as e:
        st.error(f"Erro ao buscar estatísticas: {str(e)}")
        return None

def display_card_grid(cards, columns=4, show_actions=True, user_id=None):
    """Exibe grid de cards"""
    if not cards:
        st.info("Nenhum card encontrado.")
        return
    
    cols = st.columns(columns)
    for i, card in enumerate(cards):
        with cols[i % columns]:
            # Container para o card
            with st.container():
                st.image(card['image_url'], width=150, use_container_width=True)
                st.write(f"**{card['name']}**")
                st.write(f"Nº {card['number']}")
                st.write(f"{format_currency(card['estimated_value'])}")
                st.write(f"🌍 {card['language']}")
                
                if show_actions:
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Ver", key=f"view_{card['id']}"):
                            st.session_state.viewing_card = card['id']
                            st.rerun()
                    with col2:
                        if user_id and card['user_id'] == user_id:
                            if st.button("Editar", key=f"edit_{card['id']}"):
                                st.session_state.editing_card = card['id']
                                st.rerun()

def display_user_stats(stats):
    """Exibe estatísticas do usuário"""
    if not stats:
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Cards", stats['total_cards'])
    
    with col2:
        st.metric("Valor Total", format_currency(stats['total_value']))
    
    with col3:
        st.metric("Valor Médio", format_currency(stats['avg_value']))
    
    with col4:
        st.metric("Idiomas", len(stats['languages']))

def create_public_url(user_email):
    """Cria URL pública para o usuário"""
    base_url = st.get_option("server.baseUrlPath") or "http://localhost:8501"
    return f"{base_url}?user={user_email}"

def show_error_message(error):
    """Exibe mensagem de erro formatada"""
    st.error(f"❌ Erro: {error}")

def show_success_message(message):
    """Exibe mensagem de sucesso formatada"""
    st.success(f"✅ {message}")

def show_info_message(message):
    """Exibe mensagem informativa formatada"""
    st.info(f"ℹ️ {message}")
