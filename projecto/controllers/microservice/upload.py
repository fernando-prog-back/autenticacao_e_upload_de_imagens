from projecto import UPLOAD_FOLDER 
from werkzeug.utils import secure_filename # Importar secure_filename para garantir que o nome do arquivo seja seguro
import os

# Função para lidar com o upload de arquivos
def upload(file):
    filename = None
    if file:
        # Garantir que o nome do arquivo seja seguro para evitar vulnerabilidades
        filename = secure_filename(file.filename)
        # Criar o caminho completo para salvar o arquivo
        path = os.path.join(UPLOAD_FOLDER, filename)
        # Salvar o arquivo no caminho especificado
        file.save(path)
    # Retornar o nome do arquivo salvo para referência futura
    return filename    