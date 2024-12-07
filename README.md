
### Arquivos

- `cliente.py`: Implementa o cliente que se conecta ao servidor, envia comandos e recebe respostas.
- `servidor.py`: Implementa o servidor que escuta conexões de clientes, processa comandos e verifica preços em sites.

## Como Executar

### Pré-requisitos

- Python 3.x
- Selenium
- WebDriver para o navegador desejado (ex: ChromeDriver para Google Chrome)

### Instalação

1. Clone o repositório:

    ```sh
    git clone https://github.com/Matheus-kb/verifica_precos.git
    ```

2. Instale as dependências:

    ```sh
    pip install selenium
    ```

3. Baixe o WebDriver correspondente ao seu navegador e adicione-o ao PATH do sistema.

### Executando o Servidor

1. Inicie o servidor:

    ```sh
    python servidor.py
    ```

2. O servidor estará escutando na porta 5000.

### Executando o Cliente

1. Em outro terminal, inicie o cliente:

    ```sh
    python cliente.py
    ```

2. O cliente se conectará ao servidor e permitirá que você envie comandos.

### Comandos Disponíveis

- `verificar_precos`: Solicita ao servidor a verificação dos preços nos sites configurados.
- `sair`: Encerra a conexão com o servidor.

## Logs

Os logs das verificações de preços são armazenados no arquivo `logs/precos_log.txt`.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).