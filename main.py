from email.mime.multipart import MIMEMultipart # importa de dentro da biblioteca email um módulo que está relacionado ao tipo do corpo do email ('plain', 'html', etc)
from email.mime.text import MIMEText # mesma proposta
import smtplib # é a biblioteca que irá fazer a conexão do email
from selenium import webdriver # importa da biblioteca selenium o webdriver, que é um navegador embutido que é controlado pelo python e responde a comandos
from selenium.webdriver.common.by import By # Biblioteca do selenium pra gente poder extrair os elementos
from datetime import datetime, timedelta  # datetime é a biblioteca responsável por conseguir a data de hoje, e timedelta serve para fazer operações com datas ou horários
from dotenv import load_dotenv # biblioteca para carregar as configurações da aplicação, que irá armazenar senhas de bancos de dados e no nosso caso, do email
import os # essa biblioteca permite com que nosso código se comunique com o sistema, para conseguirmos os valores do arquivo .env 

#inicializar o dotenv
load_dotenv()
def enviar_email(lista_hoteis):

    # extrair as credenciais
    destinatario = os.getenv("GERENTE_EMAIL")
    remetente = os.getenv("SMTP_USER")
    senha = os.getenv("SMTP_PASSWORD")
    servidor = os.getenv("SMTP_SERVER")
    porta = os.getenv("SMTP_PORT")

    # define o assunto do email
    titulo = "Comparativo de preços dos hotéis em Ponta Porã"

    #esse é o corpo
    corpo = f'''<p>Bom dia, Geraldo.</p><br /><p>Segue a lista de valores dos hotéis da região para data de hoje.</p><div>{lista_hoteis}</div>'''

    # 
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = titulo
    msg.attach(MIMEText(corpo, 'html'))

    server = None

    try:
        #tenta conectar com o servidor
        server = smtplib.SMTP(servidor, porta)
        #processo de segurança (criptografia)
        server.starttls()
        #faz login
        server.login(remetente, senha)
        # manda email
        server.sendmail(remetente, destinatario, msg.as_string())
    except Exception as e:
        print("Erro ao enviar: ", e)
    finally:
        #finalmente, se houve sucesso na conexão e no envio, encerra a conexão.
        if server:
            server.quit()


def main():
    check_in = datetime.now().strftime("%Y-%m-%d") # define como a data de checkin o dia de hoje. a função strftime pega o valor da hora atual e transforma em texto. pode ser do jeito que a gente quiser
    check_out = datetime.now() + timedelta(days=1) # faz a operação matemática para adicionar um dia 
    check_out = check_out.strftime("%Y-%m-%d") # transformar o número do resultado em texto

    #aqui definimos o site em que vamos extrair as informações. esse f no começo do valor diz pro python inserir variáveis que definirmos no texto.    
    pagina = f"https://www.booking.com/searchresults.en-gb.html?ss=Ponta+Por%C3%A3%2C+Mato+Grosso+do+Sul%2C+Brazil&efdco=1&label=gen173nr-1BCAEoggI46AdIM1gEaCCIAQGYAQm4ARnIAQzYAQHoAQGIAgGoAgO4Aqf447wGwAIB0gIkYTVkZGJkZTgtYWFhZS00YWZkLThhMWQtNzY5OTg0MWM3NmFl2AIF4AIB&sid=0f70e48eda27c09361538e14d83967f8&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=index&dest_id=-663177&dest_type=city&place_id=city%2F-663177&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=f3a36f13c0480611&ac_meta=GhBkZDk4NzA2NjlkZjYwNGQ2IAAoATICZW46C1BvbnRhIFBvcsOjQABKAFAA&checkin={check_in}&checkout={check_out}&group_adults=2&no_rooms=1&group_children=0"

    driver = webdriver.Chrome() # abrir o navegador embutido

    driver.get(pagina) # acessar a página que definimos

    titulo_hoteis = driver.find_elements(By.CLASS_NAME, 'a15b38c233') # procuramos todos os elementos de hoteis. eles tem em comum esse nome de classe

    precos_hoteis = driver.find_elements(By.CLASS_NAME, 'e84eb96b1f') # procuramos todos os elementos de preço. assim como os hoteis, eles tem esse mesmo nome da classe

    hoteis = '' # inicializamos uma variavel string (texto) vazio. nela iremos inserir mais texto que irá ser no final o nosso email
    for hotel, preco in zip(titulo_hoteis, precos_hoteis): # agrupamos as listas dos hoteis e dos preços e desse grupo extraimos o titulo do hotel e o preço
        # pra cada hotel e preço na lista agrupada, iremos inserir na variavel hoteis
        hoteis += f'<h1 style="font-family: fantasy ; background-color: aquamarine; border-radius: 4px;">{hotel.text}</h1><h2>{preco.text}</h2>'

    enviar_email(hoteis) # executa a função de enviar email com o texto pronto
if __name__ == '__main__':
    main()