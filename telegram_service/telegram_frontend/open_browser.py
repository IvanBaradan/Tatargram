import webbrowser
import os

# Get the absolute path to the index.html file
file_path = os.path.abspath('index.html')
file_url = f'file://{file_path}'

print(f'Opening {file_url} in your default browser...')
webbrowser.open(file_url)