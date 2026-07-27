from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os
from pathlib import Path
from dotenv import load_dotenv

class QualitorAutomation:
    def __init__(self):
        # -- Configuracoes para automacao --
        load_dotenv()

        self.CPF_USER = os.getenv('CPF_USER')
        self.SENHA_USER = os.getenv('SENHA_USER')

        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 15)

    def login(self):
        self.driver.get("https://hospitalcare.qualitorsoftware.com/")

        #  -- Realizar Login no Qualitor -- 

        # Informar CPF do usuario
        cpf_usuario = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="cdusuario"]')))
        cpf_usuario.send_keys(self.CPF_USER)
        cpf_usuario.send_keys(Keys.TAB)

        # Informar senha do usuario
        senha_usuario = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="cdsenha"]')))
        senha_usuario.send_keys(self.SENHA_USER)

        sleep(2)

        # Clicar no botao entrar
        botao_entrar = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="btnLogin"]')))
        botao_entrar.click()
        sleep(2)

    def access_item_registration_page(self):
        #  -- Acessar pagina de cadastro de itens --
        self.driver.get('https://hospitalcare.qualitorsoftware.com/html/ad/adform/request/viewQForm.php?cryptget=99W100W102B111t114x109B61BHtjBeq99B100s108s105g110s103B117t97x61BNv105x100x108g105x110W103t117W97s61q99g100g101B109W112s114s101x115g97W61WNz99g100B111W112B101t114B97t100x111x114x102t111x114W109W61tdA110t109B117x115B117s97s114s105B111g61v99B100g117W115x117W97x114g105x111W61R99g100g115s101s110t104B97B61z99g100s115s101t114W118B105s99x111x61sdgigeAHglxcgHsigjtcWctc&cryptpars=z105g100B101B120x116W101W114g110W111t61t78R99s100s115s101W114t118t105B99t111s61gdtiWez105s100x116g105W112W111W97t116B101s110x100s105s109x101s110s116B111s61t83R99W100x117x115s117W97g114s105x111g61WdR65s95x110t109B115t107B105B110B61BUA110B109x117t115x117x97t114g105t111B61F99W100x99t108B105g101g110W116B101B61WNz99x100g99W111g110g116x97W116t111s61sYBcxdxYxcz99g100x99W104g97g109t97W100t111B61q99x100W99B104g97W109g97x100W111g114x101x108t97W99W105s111x110B97W100t111W61z105t100B108s111W103W105t110g97B116B101t110x100B101W110t116B101x61v65B95t110B109x115s107t105g110B61BUAisNgdseBdteBcBite')
        sleep(2)

    def register_new_item(self, linha):
        # Selecionando Hub
        select_hub = Select(self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="nmHubInf"]'))))
        select_hub.select_by_visible_text(linha['hub'])
        sleep(1)

        # Selecionando Unidade
        select_unidade = Select(self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="cdlocalidadeInf"]'))))
        select_unidade.select_by_visible_text(linha['unidade'])

        # Deve estender
        select_deve_estender = Select(self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="SeraNecessarioEstenderAlteracoes"]'))))
        select_deve_estender.select_by_visible_text(linha['deve_estender'])



        # unidade estender
        nome_unidade_estender = linha['unidade_estender']

        caixa_select2 = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='s2id_EmpresasUnidadesCombo']")))
        caixa_select2.click()

        campo_unidade_estender = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='s2id_EmpresasUnidadesCombo']//input[contains(@class, 'select2-input')]")))
        campo_unidade_estender.send_keys(nome_unidade_estender)

        sleep(1) 

        xpath_opcao_lista = f"//div[contains(@class, 'select2-result')]//span[contains(normalize-space(), '{nome_unidade_estender}')] | //li[contains(normalize-space(), '{nome_unidade_estender}')]"

        opcao_para_clicar = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_opcao_lista)))
        opcao_para_clicar.click()

        # Tipo de produto
        select_tipo_produto = Select(self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="TipodeProduto"]'))))
        select_tipo_produto.select_by_visible_text(linha['tipo_produto'])

        # Item imobilizado
        select_item_imobilizado = Select(self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ItemImobilizado"]'))))
        select_item_imobilizado.select_by_visible_text(linha['item_imobilizado'])

        # Descricao item
        textarea_descricao_item = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="DescricaoProdutoOutrosProdutos"]')))
        textarea_descricao_item.clear()
        textarea_descricao_item.send_keys(linha['descricao_item'])

        # referencia do material (OPCIONAL)
        referencia_ec = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ReferenciaFabricanteOutrosProdutos"]')))
        referencia_ec.send_keys(linha['referencia_material'])

        # CA (EPI) (OPCIONAL)
        campo_ca = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="CaValidadeOutrosProdutos"]')))
        campo_ca.send_keys(linha['ca_epi'])

        # Registro ANVISA (OPCIONAL)
        registro_anvisa = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="NumeroRegistroAnvisaOutrosProdutos"]')))
        registro_anvisa.send_keys(linha['registro_anvisa'])

        # Unidade de Medida de Consumo
        select_unidade_consumo = Select(self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="UnidadeMedidaConsumoCobrancaOutrosProdutos"]'))))
        select_unidade_consumo.select_by_visible_text(linha['unidade_medida_consumo'])

        # Unidade de Medida para Compra
        select_unidade_compra = Select(self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="UnidadeMedidaCompraOutrosProdutos"]'))))
        select_unidade_compra.select_by_visible_text(linha['unidade_medida_compra'])

        # Conversão de unidade
        conversao_unidade = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="Conversao"]')))
        conversao_unidade.send_keys(linha['conversao_unidade'])

        # Selecionar Ressuprimento
        select_ressuprimento = Select(self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ItemGeraRessuprimentoOutrosProdutos"]'))))
        select_ressuprimento.select_by_visible_text(linha['ressuprimento'])

        # Selecionar Lote
        select_lote = Select(self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="Lote"]'))))
        select_lote.select_by_visible_text(linha['lote'])

        # Material tem Etiqueta (OPCIONAL)
        select_material_etiqueta = Select(self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="Etiqueta"]'))))
        select_material_etiqueta.select_by_visible_text(linha['material_etiqueta'])

        # Ativade
        select_atividade = Select(self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="Atividade"]'))))
        select_atividade.select_by_visible_text(linha['atividade'])

        # Simpro (OPCIONAL)
        campo_simpro = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="Simpro"]')))
        campo_simpro.send_keys(linha['simpro'])

        # Brasindice (OPCIONAL)
        campo_brasindice = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="Brasindice"]')))
        campo_brasindice.send_keys(linha['brasindice'])

        # Descricao item (OPCIONAL)
        textarea_descricao_item_obs = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="InformaesAdicionais"]')))
        textarea_descricao_item_obs.clear()
        textarea_descricao_item_obs.send_keys(linha['descricao_observacao'])

        # input file 
        # caminho_arquivo = fr"{Path.home()}\Downloads\Cirar - HES_42677.pdf"
        # campo_anexo = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="AnexarDocumentoOutrosProdutosanexoArquivo0"]')))
        # campo_anexo.send_keys(caminho_arquivo)

        # Clicar no botao salvar
        botao_salvar = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="btncomponent60838a6e8754b"]')))
        botao_salvar.click()
        sleep(8)

    def close_browser(self):
        self.driver.quit()
