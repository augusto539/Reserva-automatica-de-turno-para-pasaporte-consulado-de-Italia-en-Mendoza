# INPORTACIONES
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# VARIABLES
user = ''  # e-mail
pasword = ''    # contraseña
numero_hijos = '0'  # numero de hijos
direccion_completa = '' # direccion completa del solicitante
estatura = '172'  # estatura en centimetros
nombre_del_conyuge = 'no hay cónyuge'  # como es un campo obligatorio yo, al no tener cónyuge, puse eso
pdf_documento = 'D:\\Folders\\Documents\\turno pasaporto\\DNI.pdf' # direccion completa al pdf con tu dni (poner ambos lados del dni en un solo pdf)
pdf_documento_hijos = 'D:\\Folders\\Documents\\turno pasaporto\\DNI.pdf' # direccion completa al pdf con el dni del\los hijos (poner todos los dni en el mismo pdf) ((como es un campo obligatorio, y yo no tengo hijos, envie mi documento de nuevo))
nota_para_la_sede = '' # info adicional que quieras dar (puede quedar en blanco)

inentos_loging = 0
intentos_formulario = 0

# FUNCIONES
def LogIn():
    driver.find_element(By .XPATH, '//*[@id="login-email"]').send_keys(user)    # envio del usuario
    driver.find_element(By .XPATH, '//*[@id="login-password"]').send_keys(pasword + Keys.ENTER) # envio de la contraseña y enter para avanzar

def ListInput(OPCION,xpath):    #para los casos de List inputs, esta funcion simplifica el proseso, parametros (OPCION = numero de la opcion que desees, el espacio en blanco cuenta como 1; xpath = ruta al elemento )
    a = driver.find_element(By .XPATH, xpath)  #busqueda del elemento
    a.click() # click en el elemento
    for i in range(OPCION): # deciende hasta la opcion deceada y selecciona con un enter
        a.send_keys(Keys.ARROW_DOWN)
    a.send_keys(Keys.ENTER)

def formulario():   # funcion para reyenar el formulario    (REEMPLAZAR LOS NUMEROS EN LOS LISTINPUTS SEGUN SEA TU CASO)
    driver.implicitly_wait(4)

    try:
        ListInput(1,'//*[@id="ddls_0"]') #tiene pasaporte?
        ListInput(1,'//*[@id="ddls_1"]') #hijos menores

        driver.find_element(By .XPATH, '//*[@id="DatiAddizionaliPrenotante_2___testo"]').send_keys(numero_hijos)  #numero de hijos

        driver.find_element(By .XPATH, '//*[@id="DatiAddizionaliPrenotante_3___testo"]').send_keys(direccion_completa)  #direccion completa

        ListInput(4,'//*[@id="ddls_4"]') #hijos menores

        driver.find_element(By .XPATH, '//*[@id="DatiAddizionaliPrenotante_5___testo"]').send_keys(estatura)  #estatura en centrimetros

        ListInput(2,'//*[@id="ddls_6"]') #color de hojos

        driver.find_element(By .XPATH, '//*[@id="DatiAddizionaliPrenotante_7___testo"]').send_keys(nombre_del_conyuge)  #nombre completo del conyuge

        driver.find_element(By .XPATH, '//*[@id="File_2"]').send_keys(pdf_documento) #documento del solicitante
        driver.find_element(By .XPATH, '//*[@id="File_3"]').send_keys(pdf_documento_hijos) #documento de los hijos del solicitante

        driver.find_element(By .XPATH, '//*[@id="BookingNotes"]').send_keys(nota_para_la_sede)  #nota para la cede

        driver.find_element(By .XPATH, '//*[@id="PrivacyCheck"]').click()  #info sobre privacidad

        driver.find_element(By .XPATH, '//*[@id="btnAvanti"]').click()  #avanzar
        
    except:
        driver.find_element(By .XPATH, '//*[@id="advanced"]').click()
        driver.find_element(By .XPATH, '//*[@id="dataTableServices"]/tbody/tr[3]/td[4]/a/button').click() 
        formulario()




# SCRIPT PRINCIPAL
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options) #en caso de tener chromedriver en otro lugar reemplazar la direccion en esta linea

driver.get('https://prenotami.esteri.it/UserArea')  #url de la paguina

LogIn()

driver.implicitly_wait(3)

while True: #loop para el logIn, aveses al loguearte sale un capcha, en esa caso esto recarga la paguina y vuelve a intentarlo, luego de 5 inentos entra en una espera de 30mis, se puede completar el capcha a mano en este tiempo y el script continua sin problemas
    try:
        driver.find_element(By .XPATH, '//*[@id="advanced"]').click()
        break
    except:
        inentos_loging += 1
        print(inentos_loging)
        if inentos_loging >= 5:
            print('waiting for 30 mins')
            driver.implicitly_wait(1800)
        driver.refresh()
        LogIn()

driver.implicitly_wait(3)
inentos_loging = 0

while True: # loop para reyenar el formulario, avisa por consola la cantidad de intentos y la respuesta, el loop se detiene cuando se a reservado el turno
    intentos_formulario += 1
    try:
        a = driver.find_element(By .XPATH, '/html/body/div[2]/div[2]/div/div/div/div/div/div/div/div[3]/div/div')
        print(f'inento n* {intentos_formulario} - {a.text}')
        if a.text == 'Al momento non ci sono date disponibili per il servizio richiesto':
            driver.find_element(By .XPATH, '/html/body/div[2]/div[2]/div/div/div/div/div/div/div/div[4]/button').click()

            driver.find_element(By .XPATH, '//*[@id="dataTableServices"]/tbody/tr[3]/td[4]/a/button').click() 
            formulario()
        else:
            break
    except:
        try:
            driver.find_element(By .XPATH, '//*[@id="dataTableServices"]/tbody/tr[3]/td[4]/a/button').click() 
            formulario()
        except:
            driver.refresh()
            driver.execute_script("window.scrollTo(0, -20)") 
            driver.implicitly_wait(3)
            formulario()