import os
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from PIL import Image
from io import BytesIO
import json

# Função para baixar imagem
def baixar_imagem(url, cortar_logomarca):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    image_tag = soup.find('img', class_='f+2d')
    if image_tag and 'src' in image_tag.attrs:
        image_url = image_tag['src']
        print(f"Link da imagem: {image_url}")
        image_response = requests.get(image_url)
        image_data = image_response.content
        ext = image_url.split('.')[-1].split('?')[0]
        filename = os.path.join('images', f"img_{url.split('/')[-1]}.{ext}")

        # Verifica se o diretório 'images' existe e cria se não existir
        if not os.path.exists('images'):
            os.makedirs('images')

        with open(filename, 'wb') as file:
            file.write(image_data)
        print(f'Imagem salva como {filename}')

        if cortar_logomarca:
            # Abrir a imagem com PIL para cortar a borda de baixo
            image = Image.open(BytesIO(image_data))
            width, height = image.size
            cropped_image = image.crop((0, 0, width, height - 20))

            # Salvar a imagem cortada de volta no mesmo arquivo
            cropped_image.save(filename)
            print(f'Imagem cortada com sucesso e sobrescrita em {filename}')
        else:
            print('Imagem não foi cortada.')

    else:
        print('Não foi possível encontrar a imagem.')

# Função para baixar vídeo
def baixar_video(url):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    video_url = None
    for meta_tag in soup.find_all('meta'):
        if 'property' in meta_tag.attrs and meta_tag.attrs['property'] == 'og:video:url':
            video_url = meta_tag.attrs['content']
            break
    if video_url:
        print(f"Link do vídeo: {video_url}")
        filename = os.path.join('videos', f"video_{url.split('/')[-1]}.mp4")

        # Verifica se o diretório 'videos' existe e cria se não existir
        if not os.path.exists('videos'):
            os.makedirs('videos')

        video_response = requests.get(video_url)
        with open(filename, 'wb') as file:
            file.write(video_response.content)
        print(f'Vídeo salvo como {filename}')
    else:
        print('Não foi possível encontrar o vídeo.')

# Função principal para determinar o tipo de conteúdo e chamar a função apropriada
def baixar_conteudo(url, cortar_logomarca):
    if 'ifunny.co/picture' in url:
        baixar_imagem(url, cortar_logomarca)
    elif 'ifunny.co/video' in url:
        baixar_video(url)
    else:
        print('URL não reconhecida como imagem ou vídeo.')

# Carregar configurações do arquivo JSON
def carregar_configuracao():
    config_filename = 'config.json'
    if os.path.exists(config_filename):
        with open(config_filename, 'r') as config_file:
            config = json.load(config_file)
        cortar_logomarca = config.get("cortar_logomarca", True)
    else:
        # Configuração padrão se o arquivo não existir
        cortar_logomarca = True
        with open(config_filename, 'w') as config_file:
            json.dump({"cortar_logomarca": cortar_logomarca}, config_file)
    return cortar_logomarca

# Solicita ao usuário os links dos posts separados por vírgula
urls = input("Digite os links dos posts (separados por vírgula): ").split(',')

# Carrega a configuração
cortar_logomarca = carregar_configuracao()

# Chama a função para baixar o conteúdo para cada URL fornecida
for url in urls:
    url = url.strip()  # Remove espaços em branco extras
    if url:
        baixar_conteudo(url, cortar_logomarca)
