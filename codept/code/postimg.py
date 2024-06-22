import os
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from PIL import Image
from io import BytesIO

# Gera um cabeçalho de usuário falso
ua = UserAgent()
headers = {
    'User-Agent': ua.random
}

# URL da página que contém a imagem
url = input("Digite o link do post com imagem: ")

# Variável para definir se deve cortar a logomarca
cortar_logomarca = True  # Defina como False se não quiser cortar a logomarca

# Nome do diretório onde as imagens serão salvas
diretorio = 'images'

# Verifica se o diretório existe e cria se não existir
if not os.path.exists(diretorio):
    os.makedirs(diretorio)
    print(f'Diretório "{diretorio}" criado com sucesso.')

# Faça a requisição para obter o HTML da página
response = requests.get(url, headers=headers)
html = response.text

# Analise o HTML usando BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Encontre a tag <img> correta
image_tag = soup.find('img', class_='f+2d')
if image_tag and 'src' in image_tag.attrs:
    image_url = image_tag['src']
    print(f"Link da imagem: {image_url}")

    # Baixe a imagem
    image_response = requests.get(image_url)
    image_data = image_response.content

    # Obtenha a extensão da imagem original
    ext = image_url.split('.')[-1].split('?')[0]  # Extrai a extensão da URL da imagem

    # Nome do arquivo local com a extensão original
    filename = os.path.join(diretorio, f"img_{url.split('/')[-1]}.{ext}")

    with open(filename, 'wb') as file:
        file.write(image_data)
    print(f'Imagem salva com sucesso como {filename}')

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
