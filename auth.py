import streamlit as st

def inicializar_sessao():
    """Iniciar funcao para permanencia de dados na sessao (memoria)"""
    if 'logado' not in st.session_state:
        st.session_state['logado'] = False

def verificar_credenciais():
    """validar o user e senha informada"""
    user = st.session_state.get('input_user', '')
    senha = st.session_state.get('input_senha', '')

    # credenciais temporaria
    if user == '' and senha == '':
        st.session_state['logado'] = True
    else:
        st.session_state['logado'] = False
        st.error('Usuário ou senha inválidos. Tente novamente.')

def fazer_logout():
    """Funcao para fazer logout"""
    st.session_state['logado'] = False
    st.session_state['input_user'] = ''
    st.session_state['input_senha'] = ''
    st.success('Logout realizado com sucesso!')

def tela_login():
    """Tela de login"""
    st.title('Realizar Login')
    st.markdown('**Desenvolvido pelo Guilherme Costa Barbosa (GETCH STUDIO) - Automação Qualitor**')

    with st.form('form_login'):
        st.text_input('Usuário (CPF)', key='input_user')
        st.text_input('Senha', type='password', key='input_senha')
        st.form_submit_button('Login', on_click=verificar_credenciais)

def verificar_sessao():
    """Retornar se user esta logado ou nao"""
    inicializar_sessao()
    return st.session_state['logado']
    
