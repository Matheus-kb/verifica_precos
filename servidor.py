import socket
import threading
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import logging
import time

# Criar o diretório logs se não existir
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configuração do logging
logging.basicConfig(
    filename=os.path.join(log_directory, "precos_log.txt"),
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)


# Função para configurar o WebDriver com um User-Agent
def configurar_driver():
    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    )
    options.add_argument("accept-language=en-US,en;q=0.5")  # Cabeçalho de linguagem
    options.add_argument("accept-encoding=gzip, deflate, br")  # Compressão de resposta
    driver = webdriver.Chrome(options=options)
    return driver


# Função para verificar preços
def verificar_precos(driver):
    precos = {}
    
    try:
        # Nike
        driver.get(
            "https://www.nike.com.br/tenis-nike-air-max-excee-xbts-masculino-029517.html"
        )
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'span[data-testid="main-price"]')
            )
        )
        preco_nike = driver.find_element(
            By.CSS_SELECTOR, 'span[data-testid="main-price"]'
        ).text
        precos["Nike"] = preco_nike
    except Exception as e:
        logging.error(f"Erro ao acessar Nike: {str(e)}")

    try:
        # Mercado Livre
        driver.get(
            "https://produto.mercadolivre.com.br/MLB-3799415319-tnis-nike-air-max-excee-xbts-masculino-_JM"
        )
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "span.andes-money-amount__fraction")
            )
        )
        preco_mercadolivre = driver.find_element(
            By.CSS_SELECTOR, "span.andes-money-amount__fraction"
        ).text
        preco_mercadolivre = (
            f"R$ {preco_mercadolivre},00"  # Adiciona a formatação para o valor
        )
        precos["Mercado Livre"] = preco_mercadolivre
    except Exception as e:
        logging.error(f"Erro ao acessar Mercado Livre: {str(e)}")

    return precos


def handle_client(conn, addr):
    print(f"Conexão estabelecida com {addr}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                print(f"Conexão encerrada pelo cliente {addr}")
                break

            comando_cliente = data.decode()
            print(f"Cliente {addr}: {comando_cliente}")

            if comando_cliente.lower() == "verificar_precos":
                driver = configurar_driver()
                precos_encontrados = verificar_precos(driver)
                resposta_servidor = str(precos_encontrados)
                driver.quit()
            else:
                resposta_servidor = "Comando desconhecido. Use 'verificar_precos' para consultar os preços."

            conn.sendall(resposta_servidor.encode())

    except Exception as e:
        print(f"Erro ao processar a solicitação: {str(e)}")

    finally:
        conn.close()
        print(f"Conexão fechada com {addr}")


HOST = ""  # Escuta em todas as interfaces de rede disponíveis
PORT = 5000  # Porta para escutar as conexões

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()
print(f"Servidor escutando na porta {PORT}...")

while True:
    conn, addr = servidor.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    print(f"Clientes ativos: {threading.active_count() - 1}")
