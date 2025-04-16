***REMOVED***quests
import os
import sys
from confluence_service import pages_service

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.graphics import generate_graphviz

# Configuración de la API de Confluence
CONFLUENCE_URL = CONFLUENCE_SPACE_KEY = os.getenv("CONFLUENCE_URL")
PAGE_ID = "4423681"  # ID de la página donde se adjuntará la imagen
USERNAME = "jascencio@nisum.com"
API_TOKEN = "***REMOVED***"
IMAGE_PATH = "architecture_diagram.png"

def upload_image_as_attachment(fileName):
    unique_filename = fileName
    unique_image_path = os.path.join(os.path.dirname(IMAGE_PATH), unique_filename)
    UPLOAD_URL = f"{CONFLUENCE_URL}/wiki/rest/api/content/{PAGE_ID}/child/attachment"
    auth = (USERNAME, API_TOKEN)

    with open(unique_image_path, "rb") as image_file:
        image_data = image_file.read()

    headers = {
        "X-Atlassian-Token": "no-check",  
    }

    files = {
        "file": (unique_filename, image_data),
    }
    response = requests.post(
        UPLOAD_URL,
        headers=headers,
        auth=auth,
        files=files,
    )

    if response.status_code == 200:
        print("Imagen cargada exitosamente.")
        attachment_data = response.json()
        attachment_id = attachment_data["results"][0]["id"]
        return attachment_id
    else:
        print(f"Error al cargar la imagen: {response.status_code} - {response.text}")
        return None

def update_page_with_image(attachment_id):
    infoPage = pages_service.getContentById(PAGE_ID)
    currentVersion = infoPage["version"]["number"]
    UPDATE_PAGE_URL = f"{CONFLUENCE_URL}/wiki/rest/api/content/{PAGE_ID}"

    updatePage = pages_service.updateContent()
    page_data = {
        "type": "page",
        "title": "User Docs",
        "version": {
            "number": currentVersion+1
        },
        "body": {
            "storage": {
                "value": f"""<p>This is my firt Diagram upload</p><p>
                    <ac:image ac:align="center" ac:layout="full-width" ac:custom-width="true" ac:alt="{attachment_id}" >
                        <ri:attachment ri:filename="{attachment_id}" ri:version-at-save="1" />
                    </ac:image>
                    </p>""",
                "representation": "storage",
            }
        },
    }

    response = requests.put(
        UPDATE_PAGE_URL,
        headers={"Content-Type": "application/json"},
        auth=(USERNAME, API_TOKEN),
        json=page_data,
    )

    if response.status_code == 200:
        print("Página actualizada exitosamente.")
    else:
        print(f"Error al actualizar la página: {response.status_code} - {response.text}")

if __name__ == "__main__":
    file_route = f"""{generate_graphviz.exe_file_generation()}.png"""
    import time

    max_wait = 15  # segundos
    waited = 0

    while not os.path.exists(file_route) and waited < max_wait:
        time.sleep(1)
        waited += 1

    if not os.path.exists(file_route):
        raise FileNotFoundError(f"No se encontró el archivo generado: {file_route}")
    

    attachment_id = upload_image_as_attachment(file_route)
    print(attachment_id)
    if attachment_id:
        update_page_with_image(file_route)