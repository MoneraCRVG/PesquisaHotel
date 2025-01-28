from selenium import webdriver #pip install selenium
from selenium.webdriver.common.by import By # Biblioteca pra gente poder extrair os elementos
import time
from datetime import datetime, timedelta

#URL da plataforma
def main():
    start_date = datetime.now().strftime("%Y-%m-%d")
    end_date = datetime.now() + timedelta(days=1)
    end_date = end_date.strftime("%Y-%m-%d")
    pagina = f"https://www.booking.com/searchresults.en-gb.html?ss=Ponta+Por%C3%A3%2C+Mato+Grosso+do+Sul%2C+Brazil&efdco=1&label=gen173nr-1BCAEoggI46AdIM1gEaCCIAQGYAQm4ARnIAQzYAQHoAQGIAgGoAgO4Aqf447wGwAIB0gIkYTVkZGJkZTgtYWFhZS00YWZkLThhMWQtNzY5OTg0MWM3NmFl2AIF4AIB&sid=0f70e48eda27c09361538e14d83967f8&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=index&dest_id=-663177&dest_type=city&place_id=city%2F-663177&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=f3a36f13c0480611&ac_meta=GhBkZDk4NzA2NjlkZjYwNGQ2IAAoATICZW46C1BvbnRhIFBvcsOjQABKAFAA&checkin={start_date}&checkout={end_date}&group_adults=2&no_rooms=1&group_children=0"

    driver = webdriver.Chrome()

    driver.get(pagina)

    titulo_hoteis = driver.find_elements(By.CLASS_NAME, 'a15b38c233')

    precos_hoteis = driver.find_elements(By.CLASS_NAME, 'e84eb96b1f')

    for hotel, preco in zip(titulo_hoteis, precos_hoteis):
        print(f"Hotel: {hotel.text}")
        print(f"\tPreço: {preco.text}")
        print('\n')  # Adding a separator for clarity

if __name__ == '__main__':
    main()