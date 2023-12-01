import config
import requests
import os

def search_freesound(query, api_key, num_results=5):
    base_url = 'https://freesound.org/apiv2/search/text/'
    params = {
        'query': query,
        'token': api_key,
        'fields': 'id,name,previews',
        'format': 'json',
        'page_size': num_results,
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        results = response.json()['results']
        return results
    else:
        print(f"Error: {response.status_code}")
        return None

def download_sound(sound_id, api_key, download_folder):
    base_url = f'https://freesound.org/apiv2/sounds/{sound_id}/'
    params = {
        'token': api_key,
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        sound_info = response.json()
        preview_url = sound_info['previews']['preview-hq-mp3']
        download_url = sound_info['previews']['preview-hq-mp3']

        # Create the download folder if it doesn't exist
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        sound_data = requests.get(download_url).content
        file_path = os.path.join(download_folder, f'{sound_id}.mp3')

        with open(file_path, 'wb') as f:
            f.write(sound_data)
        
        print(f"Downloaded {sound_info['name']} ({sound_id}) to {file_path}")
    else:
        print(f"Error: {response.status_code}")


def run_crawl():
    api_key = config.api_key
    query = config.query
    num_results = config.results
    results = search_freesound(query, api_key, num_results)

    if results:
        for result in results:
            sound_id = result['id']
            folder = config.folder
            download_sound(sound_id, api_key,folder)

# run_crawl()