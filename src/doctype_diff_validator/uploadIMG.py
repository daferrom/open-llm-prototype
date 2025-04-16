***REMOVED***quests
import os
import sys
from confluence_service import pages_service

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.graphics import generate_graphviz

PAGE_ID = "4423681" 

def update_page_with_image(attachment_id):
    infoPage = pages_service.getContentById(PAGE_ID)
    currentVersion = infoPage["version"]["number"]

    contenidoXML = f"""<p>This is my firt Diagram upload</p><p>
                    <ac:image ac:align="center" ac:layout="full-width" ac:custom-width="true" ac:alt="{attachment_id}" >
                        <ri:attachment ri:filename="{attachment_id}" ri:version-at-save="1" />
                    </ac:image>
                    </p>"""
    updatePage = pages_service.updateContent(contenidoXML, pageId=PAGE_ID, title=infoPage["title"] ,version=currentVersion+1 )

    if updatePage.status_code == 200:
        print("Página actualizada exitosamente.")
    else:
        print(f"Error al actualizar la página: {updatePage.status_code} - {updatePage.text}")

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
    
    attachment_id = pages_service.upload_image_as_attachment(file_route)
    if attachment_id:
        update_page_with_image(file_route)