# 🤖 API de Resumo de Artigos (Back-End)

Este é o back-end do projeto Resumidor de Artigos. É uma API RESTful construída com **Django** e **Django Rest Framework** que recebe uma URL, extrai o conteúdo principal da página e utiliza a **API da OpenAI (GPT)** para gerar um resumo conciso.

Este projeto foi construído como parte de um portfólio de desenvolvimento, demonstrando habilidades em:
* Criação de APIs RESTful.
* Web Scraping com `requests` e `BeautifulSoup`.
* Integração com serviços de IA de terceiros (OpenAI).
* Gerenciamento de chaves de API e variáveis de ambiente (`.env`).

---

## 🚀 Tecnologias Utilizadas

* **Python**
* **Django**
* **Django Rest Framework (DRF)**
* **OpenAI**
* **Requests** (para requisições HTTP)
* **BeautifulSoup4** (para web scraping)
* **python-dotenv** (para gerenciar segredos)

---

## ⚙️ Como Rodar Localmente

1.  **Clone este repositório** (ou navegue até a pasta `api-resumo`).

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # (ou .\venv\Scripts\activate no Windows)
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure suas variáveis de ambiente:**
    * Crie um arquivo `.env` na raiz do projeto (ao lado do `manage.py`).
    * Adicione sua chave da OpenAI dentro dele:
    ```ini
    OPENAI_API_KEY="sk-..."
    ```

5.  **Rode as migrações do Django:**
    ```bash
    python manage.py migrate
    ```

6.  **Inicie o servidor de desenvolvimento:**
    ```bash
    python manage.py runserver
    ```
    O servidor estará disponível em `http://127.0.0.1:8000/`.

---

## 🔌 Endpoint da API

### `POST /api/summarize/`

Este é o único endpoint da API. Ele aceita uma URL e retorna um resumo.

**Requisição (Request Body):**
```json
{
    "url": "[https://pt.wikipedia.org/wiki/Python_(linguagem_de_programação](https://pt.wikipedia.org/wiki/Python_(linguagem_de_programação))"
}
