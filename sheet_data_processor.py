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

# instanciar a classe de automação
robo = QualitorAutomation()
robo.login()

for index, linha in df_itens.iterrows():
    robo.access_item_registration_page()
    robo.register_new_item(linha)
    print(f"Item {index + 1} | {linha['descricao_item']} foi registrado com sucesso!")

print("Todos os itens foram registrados com sucesso!")
# robo.close_browser()