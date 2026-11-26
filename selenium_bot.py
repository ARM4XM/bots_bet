import selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import random
import string

# 🛠️ Configuração das opções do Chrome
chrome_options = Options()
chrome_options.add_argument("--incognito")  # Abre em modo anônimo
chrome_options.add_argument("--start-maximized")  # Abre a janela maximizada

# 🛠️ Gerenciar automaticamente o ChromeDriver
service = Service(ChromeDriverManager().install())

# 🖥️ Inicializa o navegador com as opções configuradas
driver = selenium.webdriver.Chrome(service=service, options=chrome_options)

# 📨 Função para gerar e-mails aleatórios
def gerar_email_aleatorio():
    prefixo = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))  # Gera 8 caracteres aleatórios
    dominio = random.choice(["gmail.com", "yahoo.com", "outlook.com"])  # Escolhe um domínio aleatório
    return f"{prefixo}@{dominio}"

# 🌐 Acessa o site
driver.get("https://7788bet.com")
time.sleep(5)  # Espera inicial para carregar a página

# 📲 Função para recarregar a página até que o elemento apareça
def esperar_elemento_e_clicar(xpath, timeout=30, max_tentativas=5):
    for tentativa in range(max_tentativas):  # Tentará no máximo 5 vezes recarregar a página
        try:
            # Aguarda até o elemento estar visível
            elemento = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            print("✅ Elemento encontrado, realizando clique!")
            elemento.click()
            return True
        except Exception as e:
            print(f"🔄 Tentativa {tentativa + 1}: Elemento não encontrado, recarregando a página...")
            driver.refresh()
            time.sleep(5)  # Aguarda um pouco após recarregar
    print("❌ Não foi possível encontrar o elemento após várias tentativas.")
    return False

# 📋 Campos do formulário: (nome, xpath, valor ou gerador)
XPATH_EMAIL = '/html/body/div[2]/div/div[1]/div/div/div[2]/div[2]/div/div/div[1]/div/form/div[2]/div/div/span/div/div/div[1]/input'
XPATH_SENHA = '/html/body/div[2]/div/div[1]/div/div/div[2]/div[2]/div/div/div[1]/div/form/div[4]/div/div[1]/div/div[1]/input'
XPATH_CONFIRMA_SENHA = '/html/body/div[2]/div/div[1]/div/div/div[2]/div[2]/div/div/div[1]/div/form/div[6]/div/div[1]/div/div[1]/input'
XPATH_BOTAO_CONFIRMACAO = '/html/body/div[2]/div/div[1]/div/div/div[3]/div[2]/div/button'
XPATH_BOTAO_FINAL = '/html/body/div[3]/div/div/div[2]/button[1]'

# 🔒 Senha lida de variável de ambiente (sem fallback hardcodeado)
SENHA = os.environ["BET_BOT_SENHA"]

# 🖱️ Preenche um campo com espera explícita: aguarda visibilidade, clica, digita
def preencher_campo(nome, xpath, valor, timeout=10):
    campo = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.XPATH, xpath))
    )
    campo.click()
    campo.send_keys(valor)
    print(f"✅ Campo '{nome}' preenchido com sucesso!")

# 🔘 Localiza um elemento com espera explícita e clica
def clicar_elemento(nome, xpath, timeout=10):
    elemento = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    elemento.click()
    print(f"✅ '{nome}' clicado com sucesso!")

# 🚀 Preenchimento do formulário de cadastro
try:
    email = gerar_email_aleatorio()
    print(f"📧 E-mail gerado: {email}")

    campos = [
        ("e-mail", XPATH_EMAIL, email),
        ("senha", XPATH_SENHA, SENHA),
        ("confirmação de senha", XPATH_CONFIRMA_SENHA, SENHA),
    ]
    for nome, xpath, valor in campos:
        preencher_campo(nome, xpath, valor)

    clicar_elemento("Botão de confirmação", XPATH_BOTAO_CONFIRMACAO)
    time.sleep(2)

    print("🎯 Conta criada com sucesso!")

    print("🎯 Conta criada com sucesso!")

    # 🔄 Recarregar até que o botão desejado apareça
    if esperar_elemento_e_clicar(XPATH_BOTAO_FINAL):
        print("✅ Botão final clicado com sucesso!")
    else:
        print("⚠️ Falha ao clicar no botão final após várias tentativas.")

except Exception as e:
    print(f"❌ Erro ao localizar ou preencher um dos elementos [{type(e).__name__}]: {e}")
    try:
        # 📸 Salva screenshot e um trecho do HTML em arquivos para diagnóstico
        driver.save_screenshot("erro_selenium.png")
        html = driver.page_source
        with open("erro_pagina.html", "w", encoding="utf-8") as f:
            f.write(html[:5000])  # Trunca para os primeiros 5000 caracteres
        print("📁 Screenshot salvo em erro_selenium.png e HTML (truncado) em erro_pagina.html")
    except Exception as diag_err:
        print(f"⚠️ Falha ao salvar diagnóstico: {diag_err}")

finally:
    try:
        # 🧹 Limpar cookies e fechar o navegador
        driver.delete_all_cookies()
        time.sleep(1)

        # Localiza o elemento pelo XPath
        elemento = driver.find_element(By.XPATH, '/html/body/div[1]/div/footer/div/div[1]/div/div[2]')

        # Realiza o clique no elemento
        elemento.click()

        elemento_mission = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div/header/header/div[2]/div/div[1]/div/div[2]')

        elemento_click_mission = elemento_mission.click()

        elemento_receber_criar_conta = driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div/section/div/section/div/div/div[2]/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/div/div/div')

        elemento_click_receber_criar_conta = elemento_receber_criar_conta.click()
    except Exception as e:
        print("❌ Erro durante as ações finais:", e)
    finally:
        driver.quit()
