import streamlit as st
import pandas as pd
from auth import verificar_sessao, tela_login, fazer_logout
from register import QualitorAutomation
from validate_sheet import SheetValidator

st.set_page_config(
    page_title='Cadastro de Itens - Qualitor',
    layout='centered'
)


def tela_principal():
    """Renderizar tela principal do app"""

    # Barra laterial com saudacao e logout
    with st.sidebar:
        user_atual = st.session_state.get('input_user', 'Usuário')
        st.write(f'Bem-vindo(a), **{user_atual}!**')
        st.button('Logout', on_click=fazer_logout, use_container_width=True)

    st.title('Cadastro de Itens - Qualitor')
    st.write('Faça o upload da planilha contendo os itens a serem cadastrados no Qualitor. A planilha deve estar no formato Excel (.xlsx) e conter as colunas obrigatórias.')

    arquivo = st.file_uploader('Anexe a planilha (.xlsx)', type=['xlsx'])

    if arquivo is not None:
        try:
            validator = SheetValidator(arquivo)
            if not validator.validar_dados():
                st.error('Erro ao validar os dados da planilha.')
                return
            df_itens = validator.df_itens

            st.write('Pré-visualização dos dados carregados:')
            st.dataframe(df_itens.head(5))

            # Validar dados
            if validator.validar_dados():
                st.success('Planilha validada com sucesso! Tudo pronto para iniciar o cadastro dos itens.')
                # Botao para iniciar cadastro
                if st.button('Iniciar Cadastro Automático', use_container_width=True):

                    # Elementos para feedback visual
                    status_text = st.empty()
                    progress_bar = st.progress(0)
                    log_container = st.container()

                    total_itens = len(df_itens)

                    try:
                        # Realizando login qualitor
                        status_text.info('Iniciando o processo de cadastro...')
                        bot = QualitorAutomation()
                        bot.login()

                        # loop para cadastrar cada item
                        for index, linha in df_itens.iterrows():
                            item_atual = index + 1
                            status_text.info(f'Cadastrando item {item_atual} de {total_itens}: {linha["descricao_item"]}...')

                            try:
                                bot.access_item_registration_page()
                                bot.register_new_item(linha)

                                log_container.success(f'Item {item_atual} | {linha["descricao_item"]} cadastrado com sucesso!')

                            except Exception as e:
                                log_container.error(f'Erro ao cadastrar item {item_atual} | {linha["descricao_item"]}: {e}')

                            progress_bar.progress(item_atual / total_itens)

                        status_text.success('Processo de cadastro finalizado com sucesso!')

                    except Exception as e:
                        st.error(f'Erro crítico ao iniciar o navegador ou realizar login: {e}')

        except Exception as e:
            st.error(f'Erro ao processar a planilha: {e}')

if not verificar_sessao():
    tela_login()
else:
    tela_principal()
