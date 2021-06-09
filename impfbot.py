from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import telegram_send
import time
import config

try:
    driver = webdriver.Chrome()
    driver.get("https://sachsen.impfterminvergabe.de")

    checkElements = driver.find_elements_by_xpath("//*[contains(text(), 'leider keinen Termin anbiete')]")
    driver.implicitly_wait(300000000)

    elem = driver.find_element_by_partial_link_text("TERMIN")
    elem.click()

    driver.switch_to.window(driver.window_handles[-1])

    #login
    elemUsername = driver.find_element_by_id("gwt-uid-3")
    elemPasswort = driver.find_element_by_id("gwt-uid-5")
    elemUsername.send_keys(config.username)
    elemPasswort.send_keys(config.passwort)

    elem = driver.find_element_by_css_selector("#WorkflowButton-4212")
    time.sleep(2)
    elem.click()

    #login finished

    telegram_send.send(messages=["Bitte weitere eingaben durchführen und nach Auswahl des Impfzentrums Script fortsetzen."])

    while input("go eingeben wenn impfzentrum ausgewählt: ")!="go" :
        print()
        print("Eingabe nicht erkannt.")

    driver.implicitly_wait(30)
    while True:
        #continue to next page and look for aviable event
        elem = driver.find_element_by_css_selector("#WorkflowButton-4212")
        elem.click()
        time.sleep(4)
        
        checkKeinImpfstoff = driver.find_elements_by_xpath("//*[contains(text(), 'leider keinen Termin anbiete')]")

        if(len(checkKeinImpfstoff)==0):
            checkServerError = driver.find_elements_by_xpath("//*[contains(text(), 'Bei der Verarbeitung der Anfrage ist ein Fehler aufgetreten.')]")
            if(len(checkServerError)>0):
                telegram_send.send(messages=["Fehler auf Website aufgetreten, bitte Script neustarten."]) 
                break
            else:
                telegram_send.send(messages=["Termin gefunden bitte zeitnah prüfen."])
                while input("Wenn nicht einverstanden mit dem Termin dann weiter eingeben:")!="weiter" :
                    print()
                    print("Eingabe nicht erkannt.")

        elem = driver.find_element_by_css_selector("#WorkflowButton-4255")
        elem.click()
        time.sleep(4)


    # driver.implicitly_wait(3)
    # while True :
    #     try:
    #         cmd = input("Command: ")
    #         print(eval(cmd))
    #     except Exception as err:
    #         print(err)


    telegram_send.send(messages=["Script wurde beendet. Bitte ggf. neustarten."])
except Exception as err:
    telegram_send.send(messages=["Fehler in Scriptausführung aufgetreten, bitte neustarten."])
    print(err)
