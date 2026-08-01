import pandas as pd
from register import QualitorAutomation

# Carregar os dados
df_itens = pd.read_excel('./data/itens_qualitor.xlsx')

df_itens = df_itens.fillna('').astype(str)

df_exemplo_dois_itens = pd.DataFrame({
    'hub': ['HUB SOROCABA', 'HUB SOROCABA'],
    'unidade': ['HOSPITAL CRISTAO DE SOROCABA (350001)', 'HOSPITAL CRISTAO DE SOROCABA (350001)'],
    'deve_estender': ['Sim', 'Sim'],
    'unidade_estender': ['HUB SOROCABA-ONCO CLINICAS ESPECIALIZADAS (351001)', 'HUB SOROCABA-ONCO CLINICAS ESPECIALIZADAS (351001)'],
    'tipo_produto': ['Nutrição', 'Nutrição'],
    'item_imobilizado': ['Não', 'Não'],
    'descricao_item': ['Suco natural', 'Baguete'],
    'referencia_material': ['', ''],
    'ca_epi': ['', ''],
    'registro_anvisa': ['', ''],
    'unidade_medida_consumo': ['Litros', 'Unidade'],
    'unidade_medida_compra': ['Litros', 'Unidade'],
    'conversao_unidade': ['', ''],
    'ressuprimento': ['Não', 'Não'],
    'lote': ['Não', 'Não'],
    'material_etiqueta': ['Não', 'Não'],
    'atividade': ['Gêneros Alimenticios', 'Gêneros Alimenticios'],
    'simpro': ['', ''],
    'brasindice': ['', ''],
    'descricao_observacao': ['', ''],
    'caminho_arquivo': ['', '']
    })

def validar_dados(dados):
    # Verificar se planilha esta vazia
    if dados.empty:
        print('Erro: a planilha anexada está vázia.')
        return False

    # Verificar se existe colunas obrigatorias
    col_obrigatorias = ['hub', 'unidade', 'deve_estender', 'unidade_estender', 'tipo_produto', 'item_imobilizado', 'descricao_item', 'unidade_medida_consumo', 'unidade_medida_compra', 'ressuprimento', 'lote', 'material_etiqueta', 'atividade']
    for col in col_obrigatorias:
        if col not in dados.columns:
            print(f'Erro: no arquivo anexado não contem a coluna obrigatória ({col}).')
            return False

    # Verificar se tem campos em branco nas colunas obrigatórias
    for index, linha in dados.iterrows():
        num_linha = index + 2
        for col in col_obrigatorias:
            valor = str(linha[col]).strip()
            if not valor or valor.lower() in ['nan', 'none', 'null']:
                print(f'Erro na lina {num_linha}: O campo obrigatório "{col}" está em branco')
                return False
            
    return True

if validar_dados(df_itens):
    # instanciar a classe de automação
    robo = QualitorAutomation()
    robo.login()

    for index, linha in df_itens.iterrows():
        robo.access_item_registration_page()
        robo.register_new_item(linha)
        print(f"Item {index + 1} | {linha['descricao_item']} foi registrado com sucesso!")

    print("Todos os itens foram registrados com sucesso!")
else:
    print("Automação cancelada. Por favor, corrija os erros na planilha.")
    
# robo.close_browser()
