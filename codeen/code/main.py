import os
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from PIL import Image
from io import BytesIO
import json

# Function to download image
def download_image(url, crop_logo):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    image_tag = soup.find('img', class_='f+2d')
    if image_tag and 'src' in image_tag.attrs:
        image_url = image_tag['src']
        print(f"Image link: {image_url}")
        image_response = requests.get(image_url)
        image_data = image_response.content
        ext = image_url.split('.')[-1].split('?')[0]
        filename = os.path.join('images', f"img_{url.split('/')[-1]}.{ext}")

        # Check if 'images' directory exists and create if it doesn't
        if not os.path.exists('images'):
            os.makedirs('images')

        with open(filename, 'wb') as file:
            file.write(image_data)
        print(f'Image saved as {filename}')

        if crop_logo:
            # Open image using PIL to crop the bottom border
            image = Image.open(BytesIO(image_data))
            width, height = image.size
            cropped_image = image.crop((0, 0, width, height - 20))

            # Save cropped image back to the same file
            cropped_image.save(filename)
            print(f'Image cropped successfully and overwritten at {filename}')
        else:
            print('Image was not cropped.')

    else:
        print('Could not find the image.')

# Function to download video
def download_video(url):
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
        print(f"Video link: {video_url}")
        filename = os.path.join('videos', f"video_{url.split('/')[-1]}.mp4")

        # Check if 'videos' directory exists and create if it doesn't
        if not os.path.exists('videos'):
            os.makedirs('videos')

        video_response = requests.get(video_url)
        with open(filename, 'wb') as file:
            file.write(video_response.content)
        print(f'Video saved as {filename}')
    else:
        print('Could not find the video.')

# Main function to determine content type and call appropriate function
def download_content(url, crop_logo):
    if 'ifunny.co/picture' in url:
        download_image(url, crop_logo)
    elif 'ifunny.co/video' in url:
        download_video(url)
    else:
        print('URL not recognized as image or video.')

# Load configuration from JSON file
def load_configuration():
    config_filename = 'config.json'
    if os.path.exists(config_filename):
        with open(config_filename, 'r') as config_file:
            config = json.load(config_file)
        crop_logo = config.get("crop_logo", True)
    else:
        # Default configuration if file does not exist
        crop_logo = True
        with open(config_filename, 'w') as config_file:
            json.dump({"crop_logo": crop_logo}, config_file)
    return crop_logo

# Prompt user for links of posts separated by comma
urls = input("Enter the links of posts (separated by comma): ").split(',')

# Load configuration
crop_logo = load_configuration()

# Call the function to download content for each provided URL
for url in urls:
    url = url.strip()  # Remove any extra whitespace
    if url:
        download_content(url, crop_logo)
