from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import random
import json



class Parser:
    def __init__(self, url: str) -> None:
        self.url = url
    
    def create_driver(self):  # Настройка драйвера Chrome
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def scroll_page(self):
        SCROLL_PAUSE_TIME = 2

        last_height = self.driver.execute_script("return document.body.scrollHeight")  # Получение высоты страницы

        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Прокрутка до низа страницы

            time.sleep(SCROLL_PAUSE_TIME)  # Ожидание загрузки новой части страницы

            new_height = self.driver.execute_script("return document.body.scrollHeight")  # Получение новой высоты страницы и сравнение с последней
            if new_height == last_height:
                break
            last_height = new_height


    def get_links(self) -> None:
        """
        получаем ссылки на объявления. не все объявления подгружаются сразу, поэтому
        для начала нужно прокрутить вниз до конца
        """
        self.create_driver()

        self.driver.get(url)
        if "Доступ ограничен" in self.driver.title:
            time.sleep(10)
            raise Exception("Перезапуск из-за блокировки IP")


        cookies = [{"name":"_gcl_au","value":"1.1.888010305.1718655129"},{"name":"__upin","value":"OFcLXolGK+W6pbOT/jOv8A"},{"name":"uxs_uid","value":"e1d5c1b0-2ce5-11ef-a1f5-8b2fa9d0fc72"},{"name":"f","value":"5.0c4f4b6d233fb90636b4dd61b04726f11eccd97b390632d8c20a33b8e4f349ed58be5175b053b08bc372824dc536c237968e6fdb7397767447389c084fe43167aecb54a12f32f4101eccd97b390632d871d48616ed55cd7e0df103df0c26013a20f3d16ad0b1c5460df103df0c26013a0df103df0c26013adc5322845a0cba1af0a83522d52421ff11fcdaf91a1879904288c41a710a38fe1b79bc6b7defe3bbc6cdbaacc305c8451a2a574992f83a92d50b96489ab264ed3de19da9ed218fe2c772035eab81f5e1d50b96489ab264edf88859c11ff008953de19da9ed218fe23de19da9ed218fe23de19da9ed218fe23de19da9ed218fe2e992ad2cc54b8aa8d69b45fdf9045113f1cc8f457244b1a81ac794a8d120d7dc3f5a2844b590ac6f4bb552479cac81675d3d12014bda85a4c3b5d00afc8c01be98f19217d016aee229aa4cecca288d6b67225fc8b2e8e8015cb420629a7bed1f46b8ae4e81acb9fa46b8ae4e81acb9fa02c68186b443a7aced9c64720c11e7010e93f61101a51c122da10fb74cac1eab2da10fb74cac1eab25037f810d2d41a8134ecdeb26beb8b5db1614ea79b06f8db841da6c7dc79d0b"},{"name":"ft","value":"\"OxmjKY56gXG1FsvVtYMAlBNWdMF6w5/MYdU9u4LhmVJxhBtavio/ntYW9MRSxg7cixoMYHrhZqaQ23V8AL3I66WC4RjbfdOk3SOPraBjmkTZ2xn5F034fYXyNDVZhUE/wLLZmsiasA95n/+auVlxgjdSqpbiMtUIGKdaHa/49xFC4SzWcpnwom0Kdo5GHdti\""},{"name":"_buzz_fpc","value":"JTdCJTIydmFsdWUlMjIlM0ElN0IlMjJ1ZnAlMjIlM0ElMjJlOGEyOGEyMzRkZTJiN2NkM2RmZjU2MTcxNjlhY2Y1YiUyMiUyQyUyMmJyb3dzZXJWZXJzaW9uJTIyJTNBJTIyMTI0LjAlMjIlMkMlMjJ0c0NyZWF0ZWQlMjIlM0ExNzE4NjU1MTM2MjM0JTdEJTJDJTIycGF0aCUyMiUzQSUyMiUyRiUyMiUyQyUyMmRvbWFpbiUyMiUzQSUyMi53d3cuYXZpdG8ucnUlMjIlMkMlMjJleHBpcmVzJTIyJTNBJTIyVHVlJTJDJTIwMTclMjBKdW4lMjAyMDI1JTIwMjAlM0ExMiUzQTE3JTIwR01UJTIyJTJDJTIyU2FtZVNpdGUlMjIlM0ElMjJMYXglMjIlN0Q"},{"name":"_buzz_aidata","value":"JTdCJTIydmFsdWUlMjIlM0ElN0IlMjJ1ZnAlMjIlM0ElMjJPRmNMWG9sR0slMkJXNnBiT1QlMkZqT3Y4QSUyMiUyQyUyMmJyb3dzZXJWZXJzaW9uJTIyJTNBJTIyMTI0LjAlMjIlMkMlMjJ0c0NyZWF0ZWQlMjIlM0ExNzE4NjU1MTM2NDE4JTdEJTJDJTIycGF0aCUyMiUzQSUyMiUyRiUyMiUyQyUyMmRvbWFpbiUyMiUzQSUyMi53d3cuYXZpdG8ucnUlMjIlMkMlMjJleHBpcmVzJTIyJTNBJTIyVHVlJTJDJTIwMTclMjBKdW4lMjAyMDI1JTIwMjAlM0ExMiUzQTE3JTIwR01UJTIyJTJDJTIyU2FtZVNpdGUlMjIlM0ElMjJMYXglMjIlN0Q"},{"name":"AMP_MKTG_07c61c6ea8","value":"JTdCJTdE"},{"name":"AMP_07c61c6ea8","value":"JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJmMGZlMWEyOC0yOTQ0LTQ0YjctYWYwMi01ODk2ZDRmNjk2MWIlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzE4NjYzMDE2NTk1JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcxODY2MzA0MDIyMiUyQyUyMmxhc3RFdmVudElkJTIyJTNBNCU3RA"},{"name":"__zzatw-avito","value":"MDA0dBA"},{"name":"__zzatw-avito","value":"MDA0dBA"},{"name":"cfidsw-avito","value":"HYM805RhafbbVgg5n5ytwd7Q28+vJVNArfSUuSBgd3madvkzxMdGSv42mdIyvdTty673vTZxjOMogote2RQk+k7pMaBVD5HStuZTy02lLoe+NOKc1tpXhmgB83X1cgUmX0ytlMuWkBwlJ6eJs2k0boZlDR6HDLMlx4P5"},{"name":"cfidsw-avito","value":"HYM805RhafbbVgg5n5ytwd7Q28+vJVNArfSUuSBgd3madvkzxMdGSv42mdIyvdTty673vTZxjOMogote2RQk+k7pMaBVD5HStuZTy02lLoe+NOKc1tpXhmgB83X1cgUmX0ytlMuWkBwlJ6eJs2k0boZlDR6HDLMlx4P5"},{"name":"cfidsw-avito","value":"ijwNA2V4UiD94qTU9ySfdFChMyXpSBluvqhRUVoN7g1brkjziHPFvK6dvghUQVBgsM2gKRkatWQLFkdfHiBImZx6OEn0G40rtFMIyKQMzP7rx6Kxb9CvH4EQ3DkxIDJ4n5BfX5twWtQ8P3xydRQF2lwuDEhUgIKA+OdV"}]
        for cookie in cookies:
            self.driver.add_cookie({
                'name': cookie['name'],
                'value': cookie['value'],
            })

        self.scroll_page()

        html_code = self.driver.page_source

        soup = BeautifulSoup(html_code, 'html.parser')
        links = soup.find_all('a', class_='styles-module-root-YeOVk styles-module-root_noVisited-MpiGq')

        self.urls = [link.get('href') for link in links]
        self.urls.reverse()
        
    def get_all_data(self):
        """
        Проходиться по всем ссылкам и передает случайное значение для time.sleep().
        """
        for idx, link in enumerate(self.urls[self.id:]):
            sleep_time = random.uniform(3, 7)
            print(self.get_data('https://avito.ru' + link, sleep_time))
            self.data['id'] = idx
            self.set_context()

    def get_data(self, url, sleep_time):
        self.driver.get(url)

        original_window = self.driver.current_window_handle
        self.driver.switch_to.new_window('tab')
        self.driver.switch_to.window(original_window)

        html_code = self.driver.page_source
        self.scroll_page()
        time.sleep(sleep_time)

        soup = BeautifulSoup(html_code, 'html.parser')

        data = {
            'photos': [],
            'title': '',
            'price': '',
            'description': ''
        }
        try:
            imgs = soup.find_all('img', class_='desktop-1i6k59z')
            data['photos'] = [img.get('src') for img in imgs]
            data['title'] = soup.find('h1', class_="styles-module-root-GKtmM styles-module-root-YczkZ styles-module-size_xxxl-MrhiK styles-module-size_xxxl-c1c6_ stylesMarningNormal-module-root-S7NIr stylesMarningNormal-module-header-3xl-scwbO").get_text()
            data['price'] = soup.find('span', class_='styles-module-size_xxxl-MrhiK').get_text()
            data['description'] = soup.find('div', class_="style-item-description-html-qCwUL").get_text()
        except:
            print('вполне возможно что авито распознал парсинг')

        return data

    def get_context(self):  # Открытие и чтение JSON файла
        with open('context.json', 'r') as file:
            self.data = json.load(file)

        if self.data['url'] == self.url:
            self.id = self.data['id']

        else:
            self.id = 0
            self.data['url'] = self.url

    def set_context(self):
        with open('context.json', 'w') as file:
            json.dump(self.data, file, indent=4)
 


if __name__ == "__main__":
    url = "https://www.avito.ru/brands/cf402d1455964d3c18a5b408e2ab33cc/items/all/avtomobili?sellerId=cf402d1455964d3c18a5b408e2ab33cc"
    pars = Parser(url)        
    pars.get_context()
    pars.get_links()
    pars.get_all_data()