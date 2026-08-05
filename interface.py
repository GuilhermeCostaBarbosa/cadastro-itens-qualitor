import streamlit as st
import pandas as pd
from register import QualitorAutomation

# --- Configuração da Página ---
st.set_page_config(
    page_title="Automação Qualitor | GTECH STUDIO", 
    page_icon="🤖", 
    layout="centered"
)

def validar_dados_streamlit(dados):
    """Função de validação adaptada para dar feedback na tela do Streamlit"""
    if dados.empty:
        st.error('Erro: a planilha anexada está vazia.')
        return False

    dados.columns = dados.columns.astype(str).str.strip().str.lower()
    col_obrigatorias = [
        'hub', 'unidade', 'deve_estender', 'unidade_estender', 
        'tipo_produto', 'item_imobilizado', 'descricao_item', 
        'unidade_medida_consumo', 'unidade_medida_compra', 
        'ressuprimento', 'lote', 'material_etiqueta', 'atividade'
    ]
    
    erros = []
    
    for col in col_obrigatorias:
        if col not in dados.columns:
            erros.append(f"Falta a coluna obrigatória: '{col}'")

    if not erros:
        for index, linha in dados.iterrows():
            num_linha = index + 2
            for col in col_obrigatorias:
                valor = str(linha[col]).strip()
                if not valor or valor.lower() in ['nan', 'none', 'null']:
                    erros.append(f"Linha {num_linha}: O campo '{col}' está em branco.")

    if erros:
        st.error("⚠️ Encontramos problemas na planilha:")
        for erro in erros:
            st.warning(erro)
        return False

    return True

# --- Interface Gráfica ---
st.title("Cadastro de Itens - Qualitor")
st.markdown("**Desenvolvido por Guilherme Costa Barbsa - GTECH STUDIO**")
st.write("Faça o upload da planilha padronizada para iniciar os cadastros automaticamente.")

# Upload do Arquivo
arquivo_upload = st.file_uploader("Anexe a planilha (.xlsx)", type=["xlsx"])

if arquivo_upload is not None:
    # Ler e tratar os dados
    df_itens = pd.read_excel(arquivo_upload)
    df_itens = df_itens.fillna('').astype(str)
    
    st.write("### Pré-visualização dos Dados")
    st.dataframe(df_itens.head(3)) # Mostra as 3 primeiras linhas para conferência

    # Validação
    if validar_dados_streamlit(df_itens):
        st.success("✅ Planilha validada com sucesso! Tudo pronto para iniciar.")
        
        # Botão de Iniciar
        if st.button("🚀 Iniciar Automação", use_container_width=True):
            
            # Elementos visuais de progresso
            status_texto = st.empty()
            barra_progresso = st.progress(0)
            log_container = st.container()
            
            total_itens = len(df_itens)
            
            try:
                status_texto.info("Abrindo o navegador e fazendo login...")
                robo = QualitorAutomation()
                robo.login()
                
                # Loop de cadastro com atualização da interface
                for index, linha in df_itens.iterrows():
                    item_atual = index + 1
                    status_texto.info(f"Cadastrando item {item_atual} de {total_itens}: {linha['descricao_item']}...")
                    
                    try:
                        robo.access_item_registration_page()
                        robo.register_new_item(linha)
                        log_container.success(f"✔️ Item {item_atual} | {linha['descricao_item']} - Sucesso!")
                    except Exception as e:
                        log_container.error(f"❌ Item {item_atual} | {linha['descricao_item']} - Falhou: {e}")
                    
                    # Atualiza a barra de progresso
                    barra_progresso.progress(item_atual / total_itens)
                
                status_texto.success("🎉 Processo de automação finalizado!")
                
            except Exception as e:
                st.error(f"Erro crítico ao iniciar o navegador: {e}")