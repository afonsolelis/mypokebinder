import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Carrega as variáveis de ambiente
load_dotenv()

# Configurações do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Inicializa o cliente Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configurações do Streamlit para versão pública
STREAMLIT_CONFIG = {
    "page_title": "MyPublicPokeBinder",
    "page_icon": "🎴",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Configurações específicas da versão pública
PUBLIC_CONFIG = {
    "app_name": "MyPublicPokeBinder",
    "description": "Visualizador Público de Coleções Pokémon",
    "main_app_url": "https://mypokebinder.streamlit.app/",
    "max_users_display": 10,  # Máximo de usuários mostrados na sidebar
    "cards_per_row": 4,       # Cards por linha no grid
    "image_width": 150,       # Largura das imagens
}
