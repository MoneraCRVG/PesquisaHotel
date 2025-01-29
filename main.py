from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from selenium import webdriver # importa a biblioteca selenium
from selenium.webdriver.common.by import By # Biblioteca do selenium pra gente poder extrair os elementos
from datetime import datetime, timedelta 
from dotenv import load_dotenv
import os
import time
load_dotenv()
def enviar_email(lista_hoteis):
    destinatario = os.getenv("GERENTE_EMAIL")
    remetente = os.getenv("SMTP_USER")
    senha = os.getenv("SMTP_PASSWORD")
    servidor = os.getenv("SMTP_SERVER")
    porta = os.getenv("SMTP_PORT")
    titulo = "Comparativo de preços dos hotéis em Ponta Porã"

    corpo = f'''<p>Bom dia, Geraldo.</p><br /><p>Segue a lista de valores dos hotéis da região para data de hoje.</p><div>{lista_hoteis}</div>'''

    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = titulo
    msg.attach(MIMEText(corpo, 'html'))

    server = None

    try:
        server = smtplib.SMTP(servidor, porta)
        server.starttls()
        server.login(remetente, senha)
        server.sendmail(remetente, destinatario, msg.as_string())
    except Exception as e:
        print("Erro ao enviar: ", e)
    finally:
        if server:
            server.quit()


def main():
    check_in = datetime.now().strftime("%Y-%m-%d")
    check_out = datetime.now() + timedelta(days=1)
    check_out = check_out.strftime("%Y-%m-%d")
    pagina = f"https://www.booking.com/searchresults.en-gb.html?ss=Ponta+Por%C3%A3%2C+Mato+Grosso+do+Sul%2C+Brazil&efdco=1&label=gen173nr-1BCAEoggI46AdIM1gEaCCIAQGYAQm4ARnIAQzYAQHoAQGIAgGoAgO4Aqf447wGwAIB0gIkYTVkZGJkZTgtYWFhZS00YWZkLThhMWQtNzY5OTg0MWM3NmFl2AIF4AIB&sid=0f70e48eda27c09361538e14d83967f8&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=index&dest_id=-663177&dest_type=city&place_id=city%2F-663177&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=f3a36f13c0480611&ac_meta=GhBkZDk4NzA2NjlkZjYwNGQ2IAAoATICZW46C1BvbnRhIFBvcsOjQABKAFAA&checkin={check_in}&checkout={check_out}&group_adults=2&no_rooms=1&group_children=0"

    driver = webdriver.Chrome()

    driver.get(pagina)

    titulo_hoteis = driver.find_elements(By.CLASS_NAME, 'a15b38c233')

    precos_hoteis = driver.find_elements(By.CLASS_NAME, 'e84eb96b1f')

    hoteis = ''
    for hotel, preco in zip(titulo_hoteis, precos_hoteis):
        hoteis += f'<h1 style="font-family: fantasy ; background-color: aquamarine; border-radius: 4px;">{hotel.text}</h1><h2>{preco.text}</h2>'

    enviar_email(hoteis)
if __name__ == '__main__':
    main()