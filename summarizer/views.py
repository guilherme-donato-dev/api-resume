# summarizer/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Libs do Django e Scraper
import requests
from bs4 import BeautifulSoup
from django.conf import settings # Para pegar a API Key

# Libs da OpenAI
from openai import OpenAI
from openai import OpenAIError # Para tratar erros da OpenAI

class SummarizeView(APIView):
    """
    Recebe uma URL, raspa o conteúdo e retorna um resumo da OpenAI.
    """
    def post(self, request, format=None):
        url = request.data.get('url', None)

        if not url:
            return Response(
                {"error": "URL não fornecida."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # --- FASE 1: O SCRAPER (Já funciona) ---
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            page = requests.get(url, headers=headers, timeout=5)
            page.raise_for_status()

            soup = BeautifulSoup(page.text, 'html.parser')
            textos = soup.find_all('p')
            conteudo_raspado = "\n".join([p.get_text() for p in textos])

            if not conteudo_raspado:
                conteudo_raspado = soup.get_text(separator='\n', strip=True)
            
            if not conteudo_raspado:
                 return Response(
                    {"error": "Não foi possível extrair conteúdo desta URL."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Erro ao acessar a URL: {e}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # --- FASE 2: A MÁGICA DA IA (Novo!) ---
        try:
            # 1. Pega a chave das configurações do Django
            api_key = settings.OPENAI_API_KEY
            if not api_key:
                raise ValueError("Chave da OpenAI não encontrada nas configurações.")

            # 2. Inicializa o cliente da OpenAI
            client = OpenAI(api_key=api_key)

            # 3. Define o prompt
            # (Limitamos o conteúdo raspado para não estourar o limite de tokens)
            max_length = 22000 # ~5000 tokens
            prompt_texto = conteudo_raspado[:max_length]

            # 4. Chama a API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um assistente que resume textos de forma concisa em português do Brasil."
                    },
                    {
                        "role": "user",
                        "content": f"Resuma o seguinte texto em até 2 parágrafos: \n\n{prompt_texto}"
                    }
                ],
                temperature=0.4, # Baixa temperatura para resumos mais "diretos"
            )

            # 5. Pega o resumo da resposta
            resumo = response.choices[0].message.content

            # 6. Devolve o resumo!
            return Response(
                {"summary": resumo.strip()},
                status=status.HTTP_200_OK
            )

        except OpenAIError as e:
            # Erro específico da OpenAI (chave errada, sem créditos, etc.)
            return Response(
                {"error": f"Erro na API da OpenAI: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            # Pega qualquer outro erro (como a chave não estar no .env)
             return Response(
                {"error": f"Ocorreu um erro inesperado: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )