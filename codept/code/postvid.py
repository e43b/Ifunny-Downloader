import os
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# Função para processar cada URL e baixar o vídeo
def processar_url_video(url):
    # Gera um cabeçalho de usuário falso
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }

    # Faça a requisição para obter o HTML da página
    response = requests.get(url, headers=headers)
    html = response.text

    # Analise o HTML usando BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Encontre a tag meta correta que contém a URL do vídeo
    video_url = None
    for meta_tag in soup.find_all('meta'):
        if 'property' in meta_tag.attrs and meta_tag.attrs['property'] == 'og:video:url':
            video_url = meta_tag.attrs['content']
            break

    if video_url:
        print(f"Link do vídeo: {video_url}")

        # Cria a pasta 'videos' se não existir
        if not os.path.exists('videos'):
            os.makedirs('videos')

        # Baixe o vídeo
        video_response = requests.get(video_url)
        video_data = video_response.content

        # Nome do arquivo local
        filename = os.path.join('videos', f"video_{url.split('/')[-1]}.mp4")

        with open(filename, 'wb') as file:
            file.write(video_data)
        print(f'Vídeo salvo com sucesso como {filename}')
    else:
        print('Não foi possível encontrar a URL do vídeo.')

# Solicita ao usuário os links dos posts com vídeos (separados por vírgula)
urls = input("Digite os links dos posts com vídeos (separados por vírgula): ").split(',')

# Processa cada URL fornecida
for url in urls:
    url = url.strip()  # Remover espaços em branco extras
    if url:
        processar_url_video(url)
