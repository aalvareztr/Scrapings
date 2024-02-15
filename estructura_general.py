from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def iniciar_chrome():
    ruta = ChromeDriverManager().install()
    
    options = Options()

    #---------------------------------
    #Opciones para ocultar el navegador
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    #---------------------------------


    user_agent = "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/121.0.0.0 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-extension")
    options.add_argument("--disable-notifications")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--ne-default-browser-check")
    options.add_argument("--no-first-run")
    options.add_argument("--no-proxy-server")
    options.add_argument("--disable-blink-features=AutomattionControlled")

    exp_opt = [
        'enable-automation',
        'ignore-certificate-errors',
        'enable-login'
    ]

    options.add_experimental_option("excludeSwitches", exp_opt)

    prefs = {
        "profile.default_content_setting_values.notifications": 2,
        "intl.accept_languages": ["es-ES", "es"],
        "credentials_enable_service": False
    }

    options.add_experimental_option("prefs", prefs)

    s = Service(ruta)
    driver = webdriver.Chrome(service=s, options=options)

    return driver



def funcion_estandar ():
    driver.get("https://zeusr.sii.cl//AUT2000/InicioAutenticacion/IngresoRutClave.html?https://misiir.sii.cl/cgi_misii/siihome.cgi")



if __name__ == "__main__":
    driver = iniciar_chrome()
    funcion_estandar()
    input('presiona enter')
    driver.quit()

