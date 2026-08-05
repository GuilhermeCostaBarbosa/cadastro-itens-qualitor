import pandas as pd

class SheetValidator:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df_itens = pd.read_excel(file_path)
        self.df_itens = self.df_itens.fillna('').astype(str)

    def validar_dados(self):
        # Verificar se planilha esta vazia
        if self.df_itens.empty:
            print('Erro: a planilha anexada está vázia.')
            return False

        # Verificar se existe colunas obrigatorias
        col_obrigatorias = ['hub', 'unidade', 'deve_estender', 'unidade_estender', 'tipo_produto', 'item_imobilizado', 'descricao_item', 'unidade_medida_consumo', 'unidade_medida_compra', 'ressuprimento', 'lote', 'material_etiqueta', 'atividade']
        for col in col_obrigatorias:
            if col not in self.df_itens.columns:
                print(f'Erro: no arquivo anexado não contem a coluna obrigatória ({col}).')
                return False

        # Verificar se tem campos em branco nas colunas obrigatórias
        for index, linha in self.df_itens.iterrows():
            num_linha = index + 2
            for col in col_obrigatorias:
                valor = str(linha[col]).strip()
                if not valor or valor.lower() in ['nan', 'none', 'null']:
                    print(f'Erro na lina {num_linha}: O campo obrigatório "{col}" está em branco')
                    return False
                
        return True
