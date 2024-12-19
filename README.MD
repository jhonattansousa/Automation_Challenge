# Documentação do Projeto: Automation Challenge

## Tecnologias Utilizadas

- Neste projeto é utilizado o Selenium para automatizar a navegação, com ele é possivel acessar, navegar e interagir com elementos mais facilmente. Para a extração de dados, é utilizado o BeautifulSoup, que é uma ferramenta que captura dados em HTML, deixando o processo de extração mais rápida. O uso do Pandas é para estruturar os dados extraídos e logo após salvar em um arquivo CSV. As requisições são feitas com o Requests, que é simples para baixar as faturas diretamente da web. 
- Foi adicionado uma verificação se o botão "next" da página está desabilitado, fazendo com que não fique em um loop buscando mais páginas.
- A estrutura do código foi organizada em uma classe com métodos separados, fazendo com que cada interação esteja em uma função, facilitando a análise.

## Como Configurar e Executar

1. **Pré-requisitos:**
   - Versão Python Utilizado: 3.12.7

2. **Instalação:**
   - Clone este repositório e entre na pasta do projeto.
   - Abra a pasta do Projeto no VS Code.
   - Instale as dependências com o comando:
        pip install -r requirements.txt

3. **Execução:**
   - Execute o script Python para iniciar o processo:
        python AutomationChallenge.py

4. **Resultado:**
   - Os dados serão salvos no arquivo `resultado_faturas.csv`.
   - As faturas serão baixadas na pasta `faturas/`.
