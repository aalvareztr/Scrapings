"""
Scraping que trae los siguientes datos del cliente:
{
    rut
    razon_social
    direccion
    email
    giro
}
A partir del "rut" y "password"
"""

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os


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


def traer_datos (rut,password):
    driver.get("https://zeusr.sii.cl//AUT2000/InicioAutenticacion/IngresoRutClave.html?https://misiir.sii.cl/cgi_misii/siihome.cgi")
    try:
        #input del rut
        ruter_input =  driver.find_element(By.ID, "rutcntr")
        ruter_input.send_keys(rut)

        #input de la contra
        pass_input = driver.find_element(By.ID, "clave")
        pass_input.send_keys(password)

        #boton login 
        btn_ingreso = driver.find_element(By.ID, "bt_ingresar")
        btn_ingreso.click()

        #quitar primera alerta
        try:
            alert = driver.switch_to.alert
            alert.dismiss()
        except:
            pass
        

        #quitar segunda alerta
        try:
            alert = driver.switch_to.alert
            alert.dismiss()
        except:
            pass
        
        #evaluar si el ruto o contra es valido
        try:
            #si encuentra el titulo no se pudo hacer login
            driver.find_element(By.ID, "titulo")
            print("login fallido!!!")
            return {"rut": rut,"password": password,"failed":True,"message":"loginn fallido"}

        except NoSuchElementException:
            #si no lo encuentra el login es exitoso
            try:
                boton_siguiente = driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div/p[2]/a[1]')
                boton_siguiente.click()
                
            except:
                pass
            
            #swicheando alertas
            try:
                alert = driver.switch_to.alert
                alert.dismiss()
            except:
                pass

            try:
                alert = driver.switch_to.alert
                alert.dismiss()
            except:
                pass
            

            #modal 1
            try:
                modal = driver.find_element(By.CSS_SELECTOR, 'div.modal-dialog')

                if modal:
                    btn_cierre_modal = driver.find_element(By.XPATH, '//*[@id="ModalEmergente"]/div/div/div[3]/button')
                    btn_cierre_modal.click()
            except:
                pass

            time.sleep(2)

            #modal 2
            try:
                modal = driver.find_element(By.ID,'myMainCorreoVigente')
                if modal.is_displayed():
                    driver.execute_script("arguments[0].style.display = 'none';", modal)
            except:
                pass

            time.sleep(2)
            #seccion de datos personales
            datos_personales = driver.find_element(By.ID,"menu_datos_contribuyente")
            datos_personales.click()

            time.sleep(2)

            try:
                modal = driver.find_element(By.ID,'myMainActeco')
                if modal:
                    btn_cierre_modal = driver.find_element(By.XPATH, '//*[@id="myMainActeco"]/div/div/div[3]/button')
                    btn_cierre_modal.click()                
            except:
                pass
            
            
            time.sleep(1)
            #informacion
            box_info = driver.find_element(By.ID,"box_profile")

            nombre = box_info.find_element(By.ID,"nameCntr").text
            direccion = box_info.find_element(By.ID,"domiCntr").text
            mail = box_info.find_element(By.ID,'mailCntrNoti').text
            maill2 = box_info.find_element(By.ID,'mailCntr').text

            #submenu de contacto
            submenu_contacto = driver.find_element(By.ID,'ctracc_2')
            time.sleep(2)
            submenu_contacto.click()

            time.sleep(2)
            mail_de_contacto = driver.find_element(By.XPATH,'//*[@id="collapse11Cntrb"]/div/table/tbody/tr[3]/td[2]').text
            mail_de_notis = driver.find_element(By.XPATH,'//*[@id="collapse11Cntrb"]/div/table/tbody/tr[4]/td[2]').text

            btn_actividad_comercial = driver.find_element(By.ID,'ctracc_6')
            btn_actividad_comercial.click()

            time.sleep(3)

            actividad_comercial = driver.find_element(By.XPATH,'//*[@id="divActEcos"]/table/thead/tr/td').text
            
            time.sleep(2)

            return {
                "rut": rut,
                "password": password,
                "nombre" : nombre,
                "direccion" : direccion,
                "mail" : mail,
                "mail2" : maill2,
                "mail_de_contacto": mail_de_contacto,
                "mail_de_notis": mail_de_notis,
                "giro" : actividad_comercial
            }

    except Exception as e:
        print (e)
        return {"rut": rut,"password": password,"error": "Error en el proceso de obtención de datos de facturación"}
    


if __name__ == "__main__":
    #incia el navegador
    driver = iniciar_chrome()

    #ejecuta la funcion
    data = traer_datos("761310895","tambor56")
    #traer_datos("761310895","tambor56")
    #muestra por consola el resultado
    print(data)

    #cierra el navegador
    input('presiona enter')
    driver.quit()


