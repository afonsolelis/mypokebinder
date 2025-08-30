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

# Configurações do Streamlit
STREAMLIT_CONFIG = {
    "page_title": "MyPokeBinder",
    "page_icon": "🎴",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}
