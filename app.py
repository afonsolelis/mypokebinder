import streamlit as st
import os
from PIL import Image
import io
import base64
from datetime import datetime
from config import supabase, STREAMLIT_CONFIG
from cloudinary_utils import upload_image_to_cloudinary, delete_image_from_cloudinary, validate_image_file, get_optimized_image_url

# Configuração da página
st.set_page_config(**STREAMLIT_CONFIG)

# Função para verificar se o usuário está logado
def is_user_logged_in():
    return 'user' in st.session_state and st.session_state.user is not None

# Função para fazer upload de imagem (usando Cloudinary)
def upload_image_to_cloudinary_wrapper(image_file, user_id):
    """
    Wrapper para upload de imagem usando Cloudinary
    """
    # Validar arquivo primeiro
    is_valid, message = validate_image_file(image_file)
    if not is_valid:
        st.error(message)
        return None
    
    # Fazer upload para o Cloudinary
    result = upload_image_to_cloudinary(image_file, user_id)
    return result

# Função para cadastrar um novo card
def add_card(user_id, card_data, image_file):
    try:
        # Upload da imagem para o Cloudinary
        upload_result = upload_image_to_cloudinary_wrapper(image_file, user_id)
        if not upload_result:
            return False
        
        # Dados do card
        card_data['user_id'] = user_id
        card_data['user_email'] = st.session_state.user.email  # Adicionar email do usuário
        card_data['image_url'] = upload_result['url']
        card_data['cloudinary_public_id'] = upload_result['public_id']
        card_data['created_at'] = datetime.now().isoformat()
        
        # Inserir no banco de dados
        result = supabase.table('cards').insert(card_data).execute()
        
        if result.data:
            return True
        else:
            return False
            
    except Exception as e:
        st.error(f"Erro ao cadastrar card: {str(e)}")
        return False

# Função para buscar cards de um usuário
def get_user_cards(user_id):
    try:
        result = supabase.table('cards').select('*').eq('user_id', user_id).execute()
        return result.data
    except Exception as e:
        st.error(f"Erro ao buscar cards: {str(e)}")
        return []

# Função para buscar cards por email (para páginas públicas)
def get_cards_by_email(user_email):
    try:
        # Buscar cards pelo email do usuário
        result = supabase.table('cards').select('*').eq('user_email', user_email).execute()
        
        if not result.data:
            return [], "Usuário não encontrado ou sem cards cadastrados"
        
        return result.data, None
        
    except Exception as e:
        return None, f"Erro ao buscar cards por email: {str(e)}"

# Função para buscar cards públicos (todos os cards disponíveis)
def get_public_cards():
    try:
        result = supabase.table('cards').select('*').execute()
        return result.data if result.data else []
    except Exception as e:
        st.error(f"Erro ao buscar cards públicos: {str(e)}")
        return []

# Função para buscar um card específico
def get_card_by_id(card_id):
    try:
        result = supabase.table('cards').select('*').eq('id', card_id).single().execute()
        return result.data
    except Exception as e:
        st.error(f"Erro ao buscar card: {str(e)}")
        return None

# Função para atualizar um card
def update_card(card_id, card_data, image_file=None):
    try:
        if image_file:
            # Upload da nova imagem para o Cloudinary
            upload_result = upload_image_to_cloudinary_wrapper(image_file, card_data['user_id'])
            if upload_result:
                card_data['image_url'] = upload_result['url']
                card_data['cloudinary_public_id'] = upload_result['public_id']
        
        # Adicionar email do usuário se não estiver presente
        if 'user_email' not in card_data:
            card_data['user_email'] = st.session_state.user.email
        
        card_data['updated_at'] = datetime.now().isoformat()
        
        result = supabase.table('cards').update(card_data).eq('id', card_id).execute()
        
        if result.data:
            st.success("Card atualizado com sucesso!")
            return True
        else:
            st.error("Erro ao atualizar o card")
            return False
            
    except Exception as e:
        st.error(f"Erro ao atualizar card: {str(e)}")
        return False

# Função para deletar um card
def delete_card(card_id):
    try:
        # Primeiro, buscar o card para obter o public_id do Cloudinary
        card = get_card_by_id(card_id)
        if card and card.get('cloudinary_public_id'):
            # Deletar imagem do Cloudinary
            delete_image_from_cloudinary(card['cloudinary_public_id'])
        
        # Deletar do banco de dados
        result = supabase.table('cards').delete().eq('id', card_id).execute()
        
        if result.data:
            st.success("Card deletado com sucesso!")
            return True
        else:
            st.error("Erro ao deletar o card")
            return False
            
    except Exception as e:
        st.error(f"Erro ao deletar card: {str(e)}")
        return False

# Página de login/registro
def auth_page():
    st.title("🎴 MyPokeBinder - Autenticação")
    
    tab1, tab2 = st.tabs(["Login", "Registro"])
    
    with tab1:
        st.header("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Senha", type="password", key="login_password")
        
        if st.button("Entrar"):
            try:
                response = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
                
                if response.user:
                    st.session_state.user = response.user
                    st.success("Login realizado com sucesso!")
                    st.rerun()
                else:
                    st.error("Credenciais inválidas")
                    
            except Exception as e:
                st.error(f"Erro no login: {str(e)}")
    
    with tab2:
        st.header("Registro")
        email = st.text_input("Email", key="register_email")
        password = st.text_input("Senha", type="password", key="register_password")
        confirm_password = st.text_input("Confirmar Senha", type="password", key="confirm_password")
        
        if st.button("Registrar"):
            if password != confirm_password:
                st.error("As senhas não coincidem")
            else:
                try:
                    response = supabase.auth.sign_up({
                        "email": email,
                        "password": password
                    })
                    
                    if response.user:
                        st.success("Registro realizado com sucesso! Verifique seu email para confirmar a conta.")
                    else:
                        st.error("Erro no registro")
                        
                except Exception as e:
                    st.error(f"Erro no registro: {str(e)}")

# Página principal do usuário logado
def main_page():
    st.title("🎴 MyPokeBinder")
    
    # Indicador da página atual no topo
    current_page = st.session_state.get('current_page', 'Meu Binder')
    st.markdown(f"### 📍 {current_page}")
    st.divider()
    
    # Sidebar com informações do usuário
    with st.sidebar:
        st.header(f"Bem-vindo, {st.session_state.user.email}!")
        
        if st.button("Sair"):
            supabase.auth.sign_out()
            del st.session_state.user
            st.rerun()
        
        st.divider()
        
        # Menu de navegação sempre visível
        st.subheader("📚 Navegação")
        
        current_page = st.session_state.get('current_page', 'Meu Binder')
        
        # Botões de navegação com destaque para página atual
        if current_page == "Meu Binder":
            st.success("🏠 Meu Binder")
        else:
            if st.button("🏠 Meu Binder", use_container_width=True):
                st.session_state.current_page = "Meu Binder"
                st.rerun()
        
        if current_page == "Adicionar Card":
            st.success("➕ Adicionar Card")
        else:
            if st.button("➕ Adicionar Card", use_container_width=True):
                st.session_state.current_page = "Adicionar Card"
                st.rerun()
        
        if current_page == "Minha Página Pública":
            st.success("🌐 Minha Página Pública")
        else:
            if st.button("🌐 Minha Página Pública", use_container_width=True):
                st.session_state.current_page = "Minha Página Pública"
                st.rerun()
    
    # Exibir a página selecionada
    current_page = st.session_state.get('current_page', 'Meu Binder')
    
    # Conteúdo da página
    if current_page == "Meu Binder":
        show_my_binder()
    elif current_page == "Adicionar Card":
        add_card_page()
    elif current_page == "Minha Página Pública":
        show_public_page()

# Página para adicionar novo card
def add_card_page():
    # Título já está no topo da página principal
    
    with st.form("add_card_form"):
        card_name = st.text_input("Nome do Card")
        
        # Número do card em duas partes
        st.write("**Número do Card:**")
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            card_number_part1 = st.text_input("Número", placeholder="027", key="card_num_1", max_chars=3)
        with col2:
            st.write("**/**")
        with col3:
            card_number_part2 = st.text_input("Total", placeholder="182", key="card_num_2", max_chars=3)
        
        # Validar e formatar número
        card_number = ""
        if card_number_part1 and card_number_part2:
            # Permitir apenas números
            num1 = ''.join(filter(str.isdigit, card_number_part1))
            num2 = ''.join(filter(str.isdigit, card_number_part2))
            if num1 and num2:
                card_number = f"{num1.zfill(3)}/{num2.zfill(3)}"
                st.success(f"Número formatado: {card_number}")
            else:
                st.error("Digite apenas números no número do card")
        elif card_number_part1 or card_number_part2:
            st.warning("Preencha ambos os campos do número")
        
        language = st.selectbox("Linguagem", ["Português", "Inglês", "Japonês", "Espanhol", "Francês", "Alemão", "Italiano"])
        estimated_value = st.number_input("Valor Estimado (R$)", min_value=0.0, value=0.0, step=0.01)
        description = st.text_area("Descrição/Resumo do Card (opcional)")
        image_file = st.file_uploader("Foto do Card", type=['png', 'jpg', 'jpeg'])
        
        submitted = st.form_submit_button("Cadastrar Card")
        
        if submitted and image_file and card_number and card_name.strip():
            # Mostrar indicador de carregamento
            with st.spinner("🔄 Cadastrando card..."):
                card_data = {
                    'name': card_name,
                    'number': card_number,
                    'language': language,
                    'estimated_value': estimated_value,
                    'description': description
                }
                
                if add_card(st.session_state.user.id, card_data, image_file):
                    # Sucesso - redirecionar para Meu Binder
                    st.success("✅ Card cadastrado com sucesso!")
                    st.info("🔄 Redirecionando para Meu Binder...")
                    
                    # Aguardar um pouco para mostrar a mensagem
                    import time
                    time.sleep(2)
                    
                    # Redirecionar para Meu Binder
                    st.session_state.current_page = "Meu Binder"
                    st.rerun()
                else:
                    st.error("❌ Erro ao cadastrar o card. Tente novamente.")
        elif submitted and not card_number:
            st.error("❌ Preencha corretamente o número do card")
        elif submitted and not image_file:
            st.error("❌ Selecione uma imagem para o card")
        elif submitted and not card_name:
            st.error("❌ Digite o nome do card")

# Página para visualizar o binder do usuário
def show_my_binder():
    # Título já está no topo da página principal
    
    cards = get_user_cards(st.session_state.user.id)
    
    if not cards:
        st.markdown("---")
        st.markdown("### 📭 Nenhum card encontrado")
        st.info("🎴 Você ainda não tem cards cadastrados. Adicione seu primeiro card!")
        
        # Botão para ir para Adicionar Card
        if st.button("➕ Adicionar Primeiro Card", use_container_width=True):
            st.session_state.current_page = "Adicionar Card"
            st.rerun()
        return
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_name = st.text_input("Filtrar por nome")
    with col2:
        filter_language = st.selectbox("Filtrar por linguagem", ["Todas"] + list(set([card['language'] for card in cards])))
    with col3:
        sort_by = st.selectbox("Ordenar por", ["Nome", "Número", "Valor", "Data de Criação"])
    
    # Aplicar filtros
    filtered_cards = cards
    if filter_name:
        filtered_cards = [card for card in filtered_cards if filter_name.lower() in card['name'].lower()]
    if filter_language != "Todas":
        filtered_cards = [card for card in filtered_cards if card['language'] == filter_language]
    
    # Aplicar ordenação
    if sort_by == "Nome":
        filtered_cards.sort(key=lambda x: x['name'])
    elif sort_by == "Número":
        filtered_cards.sort(key=lambda x: x['number'])
    elif sort_by == "Valor":
        filtered_cards.sort(key=lambda x: x['estimated_value'], reverse=True)
    elif sort_by == "Data de Criação":
        filtered_cards.sort(key=lambda x: x['created_at'], reverse=True)
    
    # Exibir cards em grid
    cols = st.columns(4)
    for i, card in enumerate(filtered_cards):
        with cols[i % 4]:
            st.image(card['image_url'], width=150)
            st.write(f"**{card['name']}**")
            st.write(f"Nº {card['number']}")
            st.write(f"R$ {card['estimated_value']:.2f}")
            
            # Botões de ação
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("👁️ Ver", key=f"view_{card['id']}"):
                    st.session_state.viewing_card = card['id']
                    st.rerun()
            with col2:
                if st.button("✏️ Editar", key=f"edit_{card['id']}"):
                    st.session_state.editing_card = card['id']
                    st.rerun()
            with col3:
                if st.button("🗑️ Deletar", key=f"delete_{card['id']}"):
                    with st.spinner("🗑️ Deletando card..."):
                        if delete_card(card['id']):
                            st.success("✅ Card deletado com sucesso!")
                            st.info("🔄 Redirecionando...")
                            
                            # Aguardar um pouco para mostrar a mensagem
                            import time
                            time.sleep(2)
                            
                            st.rerun()
                        else:
                            st.error("❌ Erro ao deletar o card")

# Página para visualizar um card específico
def show_card_detail(card_id):
    card = get_card_by_id(card_id)
    
    if not card:
        st.error("Card não encontrado")
        return
    
    st.header(f"Card: {card['name']}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(card['image_url'], width=300)
    
    with col2:
        st.write(f"**Nome:** {card['name']}")
        st.write(f"**Número:** {card['number']}")
        st.write(f"**Linguagem:** {card['language']}")
        st.write(f"**Valor Estimado:** R$ {card['estimated_value']:.2f}")
        
        if card.get('description'):
            st.write(f"**Descrição:** {card['description']}")
        
        st.write(f"**Data de Criação:** {card['created_at'][:10]}")
        
        # Botões de ação (apenas para o dono do card)
        if is_user_logged_in() and card['user_id'] == st.session_state.user.id:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Editar Card"):
                    st.session_state.editing_card = card['id']
                    st.rerun()
            with col2:
                if st.button("🗑️ Deletar Card"):
                    with st.spinner("🗑️ Deletando card..."):
                        if delete_card(card['id']):
                            st.success("✅ Card deletado com sucesso!")
                            st.info("🔄 Redirecionando...")
                            
                            # Aguardar um pouco para mostrar a mensagem
                            import time
                            time.sleep(2)
                            
                            st.rerun()
                        else:
                            st.error("❌ Erro ao deletar o card")
    
    if st.button("Voltar"):
        if 'viewing_card' in st.session_state:
            del st.session_state.viewing_card
        if 'editing_card' in st.session_state:
            del st.session_state.editing_card
        st.rerun()

# Página para editar um card
def edit_card_page(card_id):
    card = get_card_by_id(card_id)
    
    if not card:
        st.error("Card não encontrado")
        return
    
    st.header(f"Editar Card: {card['name']}")
    
    with st.form("edit_card_form"):
        card_name = st.text_input("Nome do Card", value=card['name'])
        
        # Número do card em duas partes
        st.write("**Número do Card:**")
        
        # Separar o número atual em duas partes
        current_number = card['number']
        if '/' in current_number:
            parts = current_number.split('/')
            current_part1 = parts[0].lstrip('0') if parts[0] != '000' else '0'
            current_part2 = parts[1].lstrip('0') if parts[1] != '000' else '0'
        else:
            current_part1 = current_part2 = ""
        
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            card_number_part1 = st.text_input("Número", value=current_part1, key="edit_card_num_1", max_chars=3)
        with col2:
            st.write("**/**")
        with col3:
            card_number_part2 = st.text_input("Total", value=current_part2, key="edit_card_num_2", max_chars=3)
        
        # Validar e formatar número
        card_number = ""
        if card_number_part1 and card_number_part2:
            # Permitir apenas números
            num1 = ''.join(filter(str.isdigit, card_number_part1))
            num2 = ''.join(filter(str.isdigit, card_number_part2))
            if num1 and num2:
                card_number = f"{num1.zfill(3)}/{num2.zfill(3)}"
                st.success(f"Número formatado: {card_number}")
            else:
                st.error("Digite apenas números no número do card")
        elif card_number_part1 or card_number_part2:
            st.warning("Preencha ambos os campos do número")
        
        language = st.selectbox("Linguagem", ["Português", "Inglês", "Japonês", "Espanhol", "Francês", "Alemão", "Italiano"], index=["Português", "Inglês", "Japonês", "Espanhol", "Francês", "Alemão", "Italiano"].index(card['language']))
        estimated_value = st.number_input("Valor Estimado (R$)", min_value=0.0, value=float(card['estimated_value']), step=0.01)
        description = st.text_area("Descrição/Resumo do Card (opcional)", value=card.get('description', ''))
        image_file = st.file_uploader("Nova Foto do Card (opcional)", type=['png', 'jpg', 'jpeg'])
        
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("Atualizar Card")
        with col2:
            if st.form_submit_button("Cancelar"):
                del st.session_state.editing_card
                st.rerun()
        
        if submitted and card_number and card_name.strip():
            # Mostrar indicador de carregamento
            with st.spinner("🔄 Atualizando card..."):
                card_data = {
                    'name': card_name,
                    'number': card_number,
                    'language': language,
                    'estimated_value': estimated_value,
                    'description': description,
                    'user_id': card['user_id']
                }
                
                if update_card(card_id, card_data, image_file):
                    st.success("✅ Card atualizado com sucesso!")
                    st.info("🔄 Redirecionando...")
                    
                    # Aguardar um pouco para mostrar a mensagem
                    import time
                    time.sleep(2)
                    
                    del st.session_state.editing_card
                    st.rerun()
                else:
                    st.error("❌ Erro ao atualizar o card. Tente novamente.")
        elif submitted and not card_number:
            st.error("❌ Preencha corretamente o número do card")
        elif submitted and not card_name.strip():
            st.error("❌ Digite o nome do card")

# Página pública do usuário
def show_public_page():
    # Título já está no topo da página principal
    
    # Gerar URL da página pública
    public_url = f"https://mypokebinder.streamlit.app/?user={st.session_state.user.email}"
    
    # Container para o link público
    with st.container():
        st.markdown("### 🌐 Sua Página Pública")
        st.markdown(f"**Link:** `{public_url}`")
        
        # Botão de compartilhamento
        if st.button("🔗 Compartilhar", use_container_width=True):
            st.info("📤 Compartilhe este link:")
            st.code(public_url)
            st.success("✅ Coleção compartilhada!")
    
    st.markdown("---")
    
    # Estatísticas da coleção
    cards = get_user_cards(st.session_state.user.id)
    
    if not cards:
        st.markdown("---")
        st.markdown("### 📭 Nenhum card encontrado")
        st.info("🎴 Você ainda não tem cards cadastrados. Adicione cards para criar sua página pública!")
        
        # Botão para ir para Adicionar Card
        if st.button("➕ Adicionar Primeiro Card", use_container_width=True):
            st.session_state.current_page = "Adicionar Card"
            st.rerun()
        return
    
    # Estatísticas da coleção
    st.markdown("---")
    st.markdown("### 📊 Estatísticas da Coleção")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de Cards", len(cards))
    with col2:
        total_value = sum(card['estimated_value'] for card in cards)
        st.metric("Valor Total", f"R$ {total_value:.2f}")
    with col3:
        languages = set(card['language'] for card in cards)
        st.metric("Idiomas", len(languages))
        # Mostrar idiomas disponíveis
        if languages:
            st.caption(f"({', '.join(languages)})")
    with col4:
        most_valuable = max(cards, key=lambda x: x['estimated_value'])
        st.metric("Card Mais Valioso", f"R$ {most_valuable['estimated_value']:.2f}")
    
    st.markdown("---")
    
    # Cards mais valiosos
    if len(cards) > 1:
        st.markdown("### 💎 Cards Mais Valiosos")
        valuable_cards = sorted(cards, key=lambda x: x['estimated_value'], reverse=True)[:3]
        
        cols = st.columns(3)
        for i, card in enumerate(valuable_cards):
            with cols[i]:
                st.image(card['image_url'], width=120, use_container_width=True)
                st.markdown(f"**{card['name']}**")
                st.markdown(f"💰 R$ {card['estimated_value']:.2f}")
                st.markdown(f"📋 Nº {card['number']}")
    
    st.markdown("---")
    st.markdown("### 🎴 Sua Coleção Completa")
    
    # Filtros para a página pública
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_name = st.text_input("🔍 Filtrar por nome", key="public_filter_name")
    with col2:
        filter_language = st.selectbox("🌍 Filtrar por idioma", ["Todos"] + list(set([card['language'] for card in cards])), key="public_filter_lang")
    with col3:
        sort_by = st.selectbox("📊 Ordenar por", ["Nome", "Número", "Valor", "Data de Criação"], key="public_sort")
    
    # Aplicar filtros
    filtered_cards = cards
    if filter_name:
        filtered_cards = [card for card in filtered_cards if filter_name.lower() in card['name'].lower()]
    if filter_language != "Todos":
        filtered_cards = [card for card in filtered_cards if card['language'] == filter_language]
    
    # Aplicar ordenação
    if sort_by == "Nome":
        filtered_cards.sort(key=lambda x: x['name'])
    elif sort_by == "Número":
        filtered_cards.sort(key=lambda x: x['number'])
    elif sort_by == "Valor":
        filtered_cards.sort(key=lambda x: x['estimated_value'], reverse=True)
    elif sort_by == "Data de Criação":
        filtered_cards.sort(key=lambda x: x['created_at'], reverse=True)
    
    # Exibir cards em grid responsivo
    if filtered_cards:
        st.markdown(f"**Mostrando {len(filtered_cards)} de {len(cards)} cards**")
        
        # Grid responsivo
        cols = st.columns(4)
        for i, card in enumerate(filtered_cards):
            with cols[i % 4]:
                # Container para cada card
                with st.container():
                    st.image(card['image_url'], width=150, use_container_width=True)
                    st.markdown(f"**{card['name']}**")
                    st.markdown(f"📋 Nº {card['number']}")
                    st.markdown(f"💰 R$ {card['estimated_value']:.2f}")
                    st.markdown(f"🌍 {card['language']}")
                    
                    # Botão para ver detalhes
                    if st.button(f"👁️ Ver {card['name']}", key=f"public_view_{card['id']}"):
                        st.session_state.viewing_card = card['id']
                        st.rerun()
    else:
        st.info("🔍 Nenhum card encontrado com os filtros aplicados.")

# Página pública de outro usuário
def show_user_public_page(user_email):
    st.title(f"🎴 Binder de {user_email}")
    st.markdown("---")
    
    # Verificar se o usuário atual está logado e é o mesmo da URL
    current_user_logged_in = is_user_logged_in()
    is_own_page = current_user_logged_in and st.session_state.user.email == user_email
    
    if is_own_page:
        # Se é a própria página do usuário logado, mostrar sua coleção
        st.success("✅ Visualizando sua própria coleção pública")
        cards = get_user_cards(st.session_state.user.id)
    else:
        # Para outros usuários, buscar cards específicos do usuário
        st.info("🔍 Visualizando coleção pública")
        st.markdown("### 📋 Coleção Pública")
        st.markdown(f"**Proprietário:** {user_email}")
        
        # Informações para usuários não logados
        if not current_user_logged_in:
            st.markdown("---")
            st.info("👋 **Visitante!** Você está visualizando uma coleção pública.")
            st.markdown("💡 **Dica:** Faça login para criar sua própria coleção de cards!")
        
        # Buscar cards específicos do usuário
        cards, error_message = get_cards_by_email(user_email)
        
        # Se não encontrou cards, mostrar erro
        if cards is None:
            st.error(f"❌ {error_message}")
            st.markdown("---")
            st.markdown("### 🔍 Possíveis motivos:")
            st.markdown("""
            - O email não está cadastrado no sistema
            - O usuário não tem cards cadastrados
            - O usuário não compartilhou sua coleção pública
            """)
            
            # Botão para login se não estiver logado
            if not current_user_logged_in:
                st.markdown("---")
                st.markdown("### 🔐 Quer criar sua própria coleção?")
                if st.button("🚀 Fazer Login / Registro", use_container_width=True):
                    # Limpar parâmetros da URL para ir para a página de login
                    st.query_params.clear()
                    st.rerun()
            return
    
    if not cards:
        st.markdown("---")
        st.markdown("### 📭 Nenhum card encontrado")
        if is_own_page:
            st.info("🎴 Você ainda não tem cards cadastrados. Adicione cards para criar sua coleção pública!")
        else:
            st.info("🎴 Este usuário ainda não tem cards cadastrados em sua coleção.")
        
        # Botão para login se não estiver logado
        if not current_user_logged_in:
            st.markdown("---")
            st.markdown("### 🔐 Quer criar sua própria coleção?")
            if st.button("🚀 Fazer Login / Registro", use_container_width=True):
                # Limpar parâmetros da URL para ir para a página de login
                st.query_params.clear()
                st.rerun()
        return
        
        # Estatísticas da coleção
        st.markdown("### 📊 Estatísticas da Coleção")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total de Cards", len(cards))
        with col2:
            total_value = sum(card['estimated_value'] for card in cards)
            st.metric("Valor Total", f"R$ {total_value:.2f}")
        with col3:
            languages = set(card['language'] for card in cards)
            st.metric("Idiomas", len(languages))
        with col4:
            most_valuable = max(cards, key=lambda x: x['estimated_value'])
            st.metric("Card Mais Valioso", f"R$ {most_valuable['estimated_value']:.2f}")
        
        st.markdown("---")
        st.markdown("### 🎴 Coleção")
        
        # Filtros para visualização
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_name = st.text_input("🔍 Filtrar por nome", key="view_filter_name")
        with col2:
            filter_language = st.selectbox("🌍 Filtrar por idioma", ["Todos"] + list(set([card['language'] for card in cards])), key="view_filter_lang")
        with col3:
            sort_by = st.selectbox("📊 Ordenar por", ["Nome", "Número", "Valor", "Data de Criação"], key="view_sort")
        
        # Aplicar filtros
        filtered_cards = cards
        if filter_name:
            filtered_cards = [card for card in filtered_cards if filter_name.lower() in card['name'].lower()]
        if filter_language != "Todos":
            filtered_cards = [card for card in filtered_cards if card['language'] == filter_language]
        
        # Aplicar ordenação
        if sort_by == "Nome":
            filtered_cards.sort(key=lambda x: x['name'])
        elif sort_by == "Número":
            filtered_cards.sort(key=lambda x: x['number'])
        elif sort_by == "Valor":
            filtered_cards.sort(key=lambda x: x['estimated_value'], reverse=True)
        elif sort_by == "Data de Criação":
            filtered_cards.sort(key=lambda x: x['created_at'], reverse=True)
        
        # Exibir cards em grid responsivo
        if filtered_cards:
            st.markdown(f"**Mostrando {len(filtered_cards)} de {len(cards)} cards**")
            
            # Grid responsivo
            cols = st.columns(4)
            for i, card in enumerate(filtered_cards):
                with cols[i % 4]:
                    # Container para cada card
                    with st.container():
                        st.image(card['image_url'], width=150, use_container_width=True)
                        st.markdown(f"**{card['name']}**")
                        st.markdown(f"📋 Nº {card['number']}")
                        st.markdown(f"💰 R$ {card['estimated_value']:.2f}")
                        st.markdown(f"🌍 {card['language']}")
                        
                        # Botão para ver detalhes
                        if st.button(f"👁️ Ver {card['name']}", key=f"view_public_{card['id']}"):
                            st.session_state.viewing_card = card['id']
                            st.rerun()
        else:
            st.info("🔍 Nenhum card encontrado com os filtros aplicados.")
        
        # Botão para voltar ao início
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🏠 Voltar ao Início", use_container_width=True):
                # Limpar parâmetros da URL
                st.query_params.clear()
                st.rerun()
        
        # Botão de login para usuários não logados
        if not current_user_logged_in:
            with col2:
                if st.button("🔐 Fazer Login", use_container_width=True):
                    # Limpar parâmetros da URL para ir para a página de login
                    st.query_params.clear()
                    st.rerun()

# Função principal
def main():
    # Verificar se há um card sendo visualizado
    if 'viewing_card' in st.session_state:
        show_card_detail(st.session_state.viewing_card)
        return
    
    # Verificar se há um card sendo editado
    if 'editing_card' in st.session_state:
        edit_card_page(st.session_state.editing_card)
        return
    
    # Verificar se é uma página pública de usuário
    if 'user' in st.query_params:
        user_email = st.query_params['user']
        show_user_public_page(user_email)
        return
    
    # Verificar se o usuário está logado
    if is_user_logged_in():
        main_page()
    else:
        auth_page()

if __name__ == "__main__":
    main()
