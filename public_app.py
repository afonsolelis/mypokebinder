import streamlit as st
import os
from datetime import datetime
from config import supabase, STREAMLIT_CONFIG

# Configuração da página
st.set_page_config(
    page_title="MyPublicPokeBinder",
    page_icon="🎴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Função para buscar todos os cards
def get_all_cards():
    try:
        result = supabase.table('cards').select('*').execute()
        return result.data if result.data else []
    except Exception as e:
        st.error(f"Erro ao buscar cards: {str(e)}")
        return []

# Função para buscar cards por email específico
def get_cards_by_email(user_email):
    try:
        result = supabase.table('cards').select('*').eq('user_email', user_email).execute()
        return result.data if result.data else []
    except Exception as e:
        st.error(f"Erro ao buscar cards por email: {str(e)}")
        return []

# Função para buscar usuários únicos
def get_unique_users():
    try:
        result = supabase.table('cards').select('user_email').not_.is_('user_email', 'null').execute()
        if result.data:
            # Extrair emails únicos
            emails = list(set([card['user_email'] for card in result.data if card['user_email']]))
            return sorted(emails)
        return []
    except Exception as e:
        st.error(f"Erro ao buscar usuários: {str(e)}")
        return []

# Função principal
def main():
    st.title("🎴 MyPublicPokeBinder")
    st.markdown("### 🌐 Visualizador Público de Coleções Pokémon")
    st.markdown("---")
    
    # Sidebar com filtros
    with st.sidebar:
        st.header("🔍 Filtros")
        
        # Buscar por email específico
        st.subheader("👤 Buscar por Usuário")
        search_email = st.text_input("Email do usuário", placeholder="exemplo@email.com")
        
        if st.button("🔍 Buscar Usuário", use_container_width=True):
            if search_email:
                st.session_state.search_email = search_email
                st.rerun()
        
        # Limpar busca
        if st.button("🔄 Limpar Filtros", use_container_width=True):
            if 'search_email' in st.session_state:
                del st.session_state.search_email
            st.rerun()
        
        st.divider()
        
        # Lista de usuários disponíveis
        st.subheader("👥 Usuários Disponíveis")
        users = get_unique_users()
        if users:
            for user in users[:10]:  # Mostrar apenas os primeiros 10
                if st.button(f"👤 {user}", key=f"user_{user}", use_container_width=True):
                    st.session_state.search_email = user
                    st.rerun()
            
            if len(users) > 10:
                st.caption(f"... e mais {len(users) - 10} usuários")
        else:
            st.info("Nenhum usuário encontrado")
        
        st.divider()
        
        # Estatísticas gerais
        st.subheader("📊 Estatísticas")
        all_cards = get_all_cards()
        if all_cards:
            st.metric("Total de Cards", len(all_cards))
            st.metric("Usuários Ativos", len(users))
            total_value = sum(card.get('estimated_value', 0) for card in all_cards)
            st.metric("Valor Total", f"R$ {total_value:.2f}")
    
    # Conteúdo principal
    search_email = st.session_state.get('search_email', None)
    
    if search_email:
        # Mostrar cards de um usuário específico
        st.header(f"🎴 Coleção de {search_email}")
        st.info(f"Visualizando cards do usuário: {search_email}")
        
        cards = get_cards_by_email(search_email)
        
        if not cards:
            st.warning(f"Nenhum card encontrado para {search_email}")
            st.markdown("### 🔍 Possíveis motivos:")
            st.markdown("""
            - O email não está cadastrado no sistema
            - O usuário não tem cards cadastrados
            - O usuário não compartilhou sua coleção
            """)
        else:
            # Estatísticas do usuário
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total de Cards", len(cards))
            with col2:
                total_value = sum(card.get('estimated_value', 0) for card in cards)
                st.metric("Valor Total", f"R$ {total_value:.2f}")
            with col3:
                languages = set(card.get('language', '') for card in cards)
                st.metric("Idiomas", len(languages))
            with col4:
                if cards:
                    most_valuable = max(cards, key=lambda x: x.get('estimated_value', 0))
                    st.metric("Card Mais Valioso", f"R$ {most_valuable.get('estimated_value', 0):.2f}")
            
            st.markdown("---")
            
            # Filtros para os cards do usuário
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_name = st.text_input("🔍 Filtrar por nome", key="user_filter_name")
            with col2:
                filter_language = st.selectbox("🌍 Filtrar por idioma", 
                                             ["Todos"] + list(set([card.get('language', '') for card in cards])), 
                                             key="user_filter_lang")
            with col3:
                sort_by = st.selectbox("📊 Ordenar por", 
                                     ["Nome", "Número", "Valor", "Data de Criação"], 
                                     key="user_sort")
            
            # Aplicar filtros
            filtered_cards = cards
            if filter_name:
                filtered_cards = [card for card in filtered_cards 
                                if filter_name.lower() in card.get('name', '').lower()]
            if filter_language != "Todos":
                filtered_cards = [card for card in filtered_cards 
                                if card.get('language', '') == filter_language]
            
            # Aplicar ordenação
            if sort_by == "Nome":
                filtered_cards.sort(key=lambda x: x.get('name', ''))
            elif sort_by == "Número":
                filtered_cards.sort(key=lambda x: x.get('number', ''))
            elif sort_by == "Valor":
                filtered_cards.sort(key=lambda x: x.get('estimated_value', 0), reverse=True)
            elif sort_by == "Data de Criação":
                filtered_cards.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            
            # Exibir cards
            if filtered_cards:
                st.markdown(f"**Mostrando {len(filtered_cards)} de {len(cards)} cards**")
                
                cols = st.columns(4)
                for i, card in enumerate(filtered_cards):
                    with cols[i % 4]:
                        st.image(card.get('image_url', ''), width=150, use_container_width=True)
                        st.markdown(f"**{card.get('name', '')}**")
                        st.markdown(f"📋 Nº {card.get('number', '')}")
                        st.markdown(f"💰 R$ {card.get('estimated_value', 0):.2f}")
                        st.markdown(f"🌍 {card.get('language', '')}")
            else:
                st.info("🔍 Nenhum card encontrado com os filtros aplicados.")
    
    else:
        # Mostrar todos os cards
        st.header("🎴 Todas as Coleções")
        st.info("Visualizando todos os cards de todos os usuários")
        
        all_cards = get_all_cards()
        
        if not all_cards:
            st.warning("Nenhum card encontrado no sistema")
        else:
            # Estatísticas gerais
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total de Cards", len(all_cards))
            with col2:
                total_value = sum(card.get('estimated_value', 0) for card in all_cards)
                st.metric("Valor Total", f"R$ {total_value:.2f}")
            with col3:
                languages = set(card.get('language', '') for card in all_cards)
                st.metric("Idiomas", len(languages))
            with col4:
                users = get_unique_users()
                st.metric("Usuários", len(users))
            
            st.markdown("---")
            
            # Filtros gerais
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_name = st.text_input("🔍 Filtrar por nome", key="all_filter_name")
            with col2:
                filter_language = st.selectbox("🌍 Filtrar por idioma", 
                                             ["Todos"] + list(set([card.get('language', '') for card in all_cards])), 
                                             key="all_filter_lang")
            with col3:
                sort_by = st.selectbox("📊 Ordenar por", 
                                     ["Nome", "Número", "Valor", "Data de Criação", "Usuário"], 
                                     key="all_sort")
            
            # Aplicar filtros
            filtered_cards = all_cards
            if filter_name:
                filtered_cards = [card for card in filtered_cards 
                                if filter_name.lower() in card.get('name', '').lower()]
            if filter_language != "Todos":
                filtered_cards = [card for card in filtered_cards 
                                if card.get('language', '') == filter_language]
            
            # Aplicar ordenação
            if sort_by == "Nome":
                filtered_cards.sort(key=lambda x: x.get('name', ''))
            elif sort_by == "Número":
                filtered_cards.sort(key=lambda x: x.get('number', ''))
            elif sort_by == "Valor":
                filtered_cards.sort(key=lambda x: x.get('estimated_value', 0), reverse=True)
            elif sort_by == "Data de Criação":
                filtered_cards.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            elif sort_by == "Usuário":
                filtered_cards.sort(key=lambda x: x.get('user_email', ''))
            
            # Exibir cards
            if filtered_cards:
                st.markdown(f"**Mostrando {len(filtered_cards)} de {len(all_cards)} cards**")
                
                cols = st.columns(4)
                for i, card in enumerate(filtered_cards):
                    with cols[i % 4]:
                        st.image(card.get('image_url', ''), width=150, use_container_width=True)
                        st.markdown(f"**{card.get('name', '')}**")
                        st.markdown(f"📋 Nº {card.get('number', '')}")
                        st.markdown(f"💰 R$ {card.get('estimated_value', 0):.2f}")
                        st.markdown(f"🌍 {card.get('language', '')}")
                        st.markdown(f"👤 {card.get('user_email', 'N/A')}")
            else:
                st.info("🔍 Nenhum card encontrado com os filtros aplicados.")
    
    # Footer
    st.markdown("---")
    st.markdown("### 📝 Sobre")
    st.markdown("""
    **MyPublicPokeBinder** é um visualizador público de coleções de cards Pokémon.
    
    - 🌐 **Acesso público** - Não requer login
    - 🔍 **Busca por usuário** - Encontre coleções específicas
    - 📊 **Estatísticas** - Visualize métricas das coleções
    - 🎴 **Cards detalhados** - Veja informações completas dos cards
    
    Para criar sua própria coleção, acesse: [MyPokeBinder](https://mypokebinder.streamlit.app/)
    """)

if __name__ == "__main__":
    main()
