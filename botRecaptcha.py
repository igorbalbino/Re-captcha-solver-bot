#system libraries
import os
import random
import time

#selenium libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options

#recaptcha libraries
import speech_recognition as sr
import ffmpy
#import requests
import urllib
import pydub

#interface
import PySimpleGUI as sg;

def delay():
    time.sleep(random.randint(2, 3))

class CaptchaSolver:
    def __init__(self, baseUrl):

        self.baseUrl = baseUrl;

        try:
            # create chrome driver
            # driver = webdriver.Chrome(os.getcwd() + "\\webdriver\\chromedriver.exe")
            #self.driver = webdriver.Firefox(os.getcwd() + "\\geckodriver\\geckodriver.exe");
            self.driver = webdriver.Firefox(executable_path=r'C:\Users\igorb\Documents\GitHub\Bot-Inscritos-Instagram\geckodriver\geckodriver.exe');
            delay();

        except:
            print("[-] ERRO !!! CHECK VERSION: selenium-python.readthedocs.io/installation.html");

    # CRIA FUNCAO solveAudioCaptcha
    def solveAudioCaptcha(self):

        driver = self.driver;

        # go to website
        #driver.get("https://www.google.com/recaptcha/api2/demo");
        driver.get(self.baseUrl);

        # switch to recaptcha frame
        frames = driver.find_elements_by_tag_name("iframe");
        driver.switch_to.frame(frames[0]);
        delay();

        # click on checkbox to activate recaptcha
        driver.find_element_by_class_name("recaptcha-checkbox-border").click();

        # switch to recaptcha audio control frame
        driver.switch_to.default_content();
        frames = driver.find_element_by_xpath("/html/body/div[2]/div[4]").find_elements_by_tag_name("iframe");
        driver.switch_to.frame(frames[0]);
        delay();

        # click on audio challenge
        driver.find_element_by_id("recaptcha-audio-button").click();

        # switch to recaptcha audio challenge frame
        driver.switch_to.default_content();
        frames = driver.find_elements_by_tag_name("iframe");
        driver.switch_to.frame(frames[-1]);
        delay();

        # click on the play button
        driver.find_element_by_xpath("/html/body/div/div/div[3]/div/button").click();
        # get the mp3 audio file
        src = driver.find_element_by_id("audio-source").get_attribute("src");
        print("[INFO] Audio src: %s" % src);
        # download the mp3 audio file from the source
        urllib.request.urlretrieve(src, os.getcwd() + "\\sample.mp3");
        sound = pydub.AudioSegment.from_mp3(os.getcwd() + "\\sample.mp3");
        sound.export(os.getcwd() + "\\sample.wav", format="wav");
        sample_audio = sr.AudioFile(os.getcwd() + "\\sample.wav");
        r = sr.Recognizer();

        with sample_audio as source:
            audio = r.record(source);

        # translate audio to text with google voice recognition
        key = r.recognize_google(audio);
        print("[INFO] Recaptcha Passcode: %s" % key);

        # key in results and submit
        driver.find_element_by_id("audio-response").send_keys(key.lower());
        driver.find_element_by_id("audio-response").send_keys(Keys.ENTER);
        driver.switch_to.default_content();
        delay();
        driver.find_element_by_id("recaptcha-demo-submit").click();
        delay();

    #FECHA FUNCAO solveAudioCaptcha

####################################################################
####################################################################
####################################################################

class TelaPython:
    #CRIA FUNCAO CONSTRUTOR
    def __init__(self):
        #LAYOUT
        layout = [
            #CRIA ELEMENTO NA TELA COM UM INPUT PARA RECEBER DADOS
            [sg.Text('URL', size=(10, 0)), sg.Input(size=(30, 0), key='baseUrl')],
            [sg.Button('Enviar Dados',size=(30, 0))]
            #CRIA TELA DE OUTPUT PARA MOSTRAR OS DADOS NO LAYOUT
            #[sg.Output(size=(50, 10))]
        ];
        #JANELA
        #CRIA A TELA E COLOCA OS ELEMENTOS DE LAYOUT NELA
        self.janela = sg.Window('Dados do Usuário').layout(layout);
        #EXTRAIR DADOS DA TELA
        #PEGA OS DADOS DOS INPUTS E USA O METODO READ() NA JANELA PARA GRAVAR OS DADOS
        #self.button, self.values = self.janela.Read();
        #^ ISSO FOI PASSADO PARA DENTRO DE UM "while" NA FUNCAO "Iniciar"

    #FECHA __init__

    def Iniciar(self):
        while True:
            # EXTRAIR DADOS DA TELA
            self.button, self.values = self.janela.Read();
            #IMPRIMI INFORMAÇÕES EXTRAIDAS DA TELA
            #print(self.values);
            baseUrl = self.values['baseUrl'];

            print(f'URL: {baseUrl}');

            resolutor = CaptchaSolver(baseUrl);
            resolutor.solveAudioCaptcha();
        #FECHA while
    # FECHA Iniciar

#INSTANCIA CLASSE TelaPython EM tela
tela = TelaPython();
tela.Iniciar();