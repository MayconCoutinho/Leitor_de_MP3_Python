from tkinter.ttk import *
from tkinter import *
from PIL import Image, ImageTk
from matplotlib.pyplot import text
import pygame
from pygame import mixer
import os
from time import sleep
from random import shuffle



################# Diretório ###########################

pasta_musica = './Music'
musica = []

pasta_capa = "./Images/img_musica/" 
capa_musica = []


for diretorio, subpastas, arquivos in os.walk(pasta_musica):
    for arquivo in arquivos:
        musica.append(os.path.join(diretorio, arquivo))


for diretorio, subpastas, arquivos in os.walk(pasta_capa):
    for arquivo in arquivos:
        capa_musica.append(os.path.join(diretorio, arquivo))

###################################### configurações inicial #################################



len_musica = int(len(musica)-1)

num_musica = len_musica 
    
pygame.mixer.init()
pygame.mixer.music.load(musica[num_musica])
pygame.mixer.music.play()
mixer.music.pause()

root = Tk()  

root.geometry("350x420")
root.configure(bg='black')
root.resizable(width=False, height=False)


###################################### Nome do programa ######################################

root.title("Leitor de MP3 em Python")

###################################### ICO ######################################

root.iconbitmap('./images/icon/ico_music.ico')

###################################### Nome da musica ##################################

def nome_musica():
    
  
    nome_musica =  (musica[num_musica].replace('.mp3','')).replace('./Music\\','')

    nome_musica = Label(root, text= nome_musica, font=("Corbel 12"), foreground='white' ,background='#000000').place(x=-15,y=290, width=400, height=25)

###################################### Capa musica ######################################

def replace_nome(retorna, diretorio):

    if retorna == "musica":

        nome_musica_1 = diretorio
        nome_musica_1 =  (nome_musica_1.replace('.mp3','')).replace('./Music\\','')
        return nome_musica_1

    elif retorna == "imagem":    

        nome_imagem_1 = diretorio
        nome_imagem_1 =  (nome_imagem_1.replace('./Images/img_musica/','')).replace('.jpg','')

        return nome_imagem_1
    

def nomes_limpo(musica_capa, retorna):

    if retorna == "musica":
        nome_musica_1 = (musica_capa.replace('.mp3','')).replace('./Music\\','')
        return nome_musica_1
    if retorna == "capa":
        nome_capa_1 = (musica_capa.replace('./Images/img_musica/','')).replace('.jpg','')

        return nome_capa_1

contador = 0 

def musica_capa_certa():

    global musica_capa_certa_on, contador
    
    capa_generica = "./Images/img_musica/Capa_generica.jpg"


    musica_capa_certa_on = capa_generica

    

    for capa in capa_musica:
        

        if nomes_limpo(capa,"capa") == nomes_limpo(musica[num_musica], "musica"):

            musica_capa_certa_on = capa
            contador = 0
            break

        contador += 1 

musica_capa_certa()

logo = Image.open(musica_capa_certa_on)
logo = ImageTk.PhotoImage(logo.resize((250,250)))

logo_label = Label(image=logo, border=2)
logo_label.image = logo
logo_label.place(x=50, y=30)


def muda_capa():
    
    musica_capa_certa()
    logo = Image.open(musica_capa_certa_on)
    logo = ImageTk.PhotoImage(logo.resize((250,250)))
    logo_label = Label(image=logo, border=2)
    logo_label.image = logo
    logo_label.place(x=50, y=30)

###################################### Funções ##############################################

musica_on = False

def linha_cinza():

    global linha_branca

    linha_branca = 0

    linha = Label(root, text= ' ', background= '#484d50')
    linha.place(x=20, y=325, width=305, height= 5)

linha_branca = 0
minuto = 0
segundo = 0

def musica_cronometro():

    if musica_on == True:
        tempo_musica_str()

def musica_tempo_total(diretorio, retorna):

    from email.mime import audio
    from mutagen.mp3 import MP3

    audio = MP3(diretorio)

    bruto = audio.info.length

    minuto_total, segundo_total = divmod(audio.info.length,60)

    minuto_total = round(minuto_total)

    segundo_total = round(segundo_total)

    tempo = "{:02d}:{:02d}".format(minuto,segundo)

    if retorna ==  "tempo":
        return tempo
    elif retorna == "minuto":
        return minuto_total
    elif retorna == "segundo":
        return segundo_total
    elif retorna == "bruto":
        return bruto

segundo_1_on = True

def tempo_musica_str():

    global minuto, segundo, segundo_1_on, linha_branca, musica_on

    minuto_1 = musica_tempo_total(musica[num_musica], "minuto")
    minuto_1 = int(minuto_1) - int(minuto)

    segundo_musica = musica_tempo_total(musica[num_musica], "segundo") 

    segundo_1 = (int(segundo_musica) - int(segundo))

    segundo_2 = segundo_1



    if musica_on == True:

        linha_branca += 300/musica_tempo_total(musica[num_musica], "bruto")
        
    


    linha = Label(root, text= ' ', background= '#ffffff')
    linha.place(x=20, y=325, width= linha_branca, height= 5)
    







    if segundo_1 == 0 and segundo_1_on == True:

        segundo = 0   
        segundo_1_on = False

        if segundo_1 == 0:
            minuto += 1


    
  
    if segundo_1_on == False:

        segundo_2 = 59 - int(segundo)
        
        if segundo_2 == 0:
            minuto += 1
            segundo = 0

    
        

    if segundo_2 > 0:
        if musica_on == True:
            segundo += 1 

    if segundo_2 <= 0 and minuto_1 <= 0:

        linha_cinza()
        passa_musica("")



    
    tempo_texto = Label(root, text= ' ', foreground='white', background='#000000')
    tempo_texto.place(x=285, y=299, width= 50, height= 20)
 
    tempo_formato = "{:02d}:{:02d}".format(minuto_1, segundo_2)

    sleep(0.1)
    
    tempo_texto.config(text=tempo_formato)


    root.after(900, tempo_musica_str)

def volume_diminui(_):
    volume(-0.1)

def volume_aumenta(_):
    volume(0.1)

altura = 0.3
mixer.music.set_volume(altura)

def volume_str(mensagem = altura):
    global altura
    
    volume_1 = altura 

    if  altura <= 0:
        volume_1 = "MUTE"
    elif  altura >= 1.0:
        volume_1 = "MAX"

    volume_str = Label(root, text= str(volume_1), font=("Digital-7 11"), foreground='white' ,background='#000000').place(x= 300, y=355, width= 30, height= 30)

volume_str()

def volume(volume):

    global altura


    if volume == -0.1:
        if altura <= 0:
            altura = 0

        elif altura <= 1.0: 
            altura = ((altura * 10) - 1)/10

    elif volume == 0.1:
        if altura >= 1.0:
            altura = 1.0

        elif altura >= 0: 
            altura = ((altura * 10) + 1)/10

        
    volume_str()

    
    mixer.music.set_volume(altura) # vai de 0 a 1.0
  
musica_aleatoria_on = False

def musica_aleatoria(_):

    global musica_aleatoria_on
 

    if musica_aleatoria_on == True:
        
        musica_aleatoria_on = False

        b_musica_aleatoria.config(image=photo_musica_aleatoria)

    elif musica_aleatoria_on == False:

        shuffle(musica)

        musica_aleatoria_on = True

        b_musica_aleatoria.config(image=photo_musica_aleatoria_cinza)

def ultima_musica():

    return 0

def primeira_musica():

    return len_musica

def tocar_musica():

    pygame.mixer.init()

    pygame.mixer.music.load(musica[num_musica])

    pygame.mixer.music.play()

def retorna_f(retorna):

    global musica_on
    
    if retorna == False:
        musica_on = True
    if retorna == True:
        musica_on = False

def numero_igual():

    global num_musica_2

    num_musica_2 = num_musica

cronomitro_ativado = False

def play(_):

    global cronomitro_ativado


    nome_musica()

    if musica_on == True:

        b_play.config(image=photo_pause)
        mixer.music.pause()
        
        retorna_f(True)   

    elif musica_on == False:

        b_play.config(image=photo_play)
        mixer.music.unpause()
        retorna_f(False)
        
    if cronomitro_ativado == False:
        linha_cinza()
        musica_cronometro()
        cronomitro_ativado = True

def passa_musica(_):

    global num_musica, minuto, segundo , cronomitro_ativado, segundo_1_on


    segundo_1_on = True

    minuto = 0
    segundo = 0


    if num_musica >= len_musica:

        if musica_aleatoria_on == True:
            shuffle(musica)

        num_musica = ultima_musica()        
        b_play.config(image=photo_play)

  
        retorna_f(False)
        nome_musica()
        muda_capa()
        
        tocar_musica()
        linha_cinza()

       
        

    elif num_musica >= 0 and num_musica < len_musica:
        if musica_aleatoria_on == True:
            shuffle(musica)
        
        num_musica += 1 
        b_play.config(image=photo_play)
        retorna_f(False)
        nome_musica()
        muda_capa()
   
        tocar_musica()
        linha_cinza()
    

    if cronomitro_ativado == False:
        musica_cronometro()
        cronomitro_ativado = True
         
def volta_musica(_):
    
    global num_musica , cronomitro_ativado, segundo_1_on 

    segundo_1_on = True

    if num_musica <= 0:
        if musica_aleatoria_on == True:
            shuffle(musica)

        
        num_musica = primeira_musica()

        b_play.config(image=photo_play)

        retorna_f(False)  

        nome_musica()
        muda_capa()
        
        
        tocar_musica()
        linha_cinza()

    

    elif num_musica > 0 and num_musica <= len_musica:
        if musica_aleatoria_on == True:
            shuffle(musica)
        
        num_musica -= 1 

        b_play.config(image=photo_play)

        retorna_f(False)
        nome_musica()
        muda_capa()

        segundo_1_on = True
        
        tocar_musica()
        linha_cinza()
    
    if cronomitro_ativado == False:
        musica_cronometro()
        cronomitro_ativado = True

###################################### Button Imagem e tamanho #############################

photo_play  = PhotoImage(file='./Images/button/play.png').subsample(2,2)
photo_pause = PhotoImage(file='./Images/button/pause.png').subsample(2,2)
photo_passa = PhotoImage(file='./Images/button/passa.png').subsample(2,2)
photo_volta = PhotoImage(file='./Images/button/volta.png').subsample(2,2)
photo_musica_aleatoria = PhotoImage(file='./Images/button/musica_aleatoria.png').subsample(4,4)
photo_musica_aleatoria_cinza = PhotoImage(file='./Images/button/musica_aleatoria_cinza.png').subsample(4,4)
photo_volume_aumenta = PhotoImage(file='./Images/button/volume_aumenta.png').subsample(3,3)
photo_volume_diminui = PhotoImage(file='./Images/button/volume_diminui.png').subsample(3,3)

###################################### Button Criação ######################################

b_play = Button(root, image=photo_pause, cursor='hand2', border=0 ,bg="black")
b_passa = Button(root, image=photo_passa, cursor='hand2', border=0,bg="black")
b_volta = Button(root, image=photo_volta, cursor='hand2', border=0,bg="black")
b_musica_aleatoria = Button(root, image=photo_musica_aleatoria, cursor='hand2', border=0,bg="black")
b_volume_aumenta = Button(root, image= photo_volume_aumenta, cursor='hand2', border=0 ,bg="black")
b_volume_diminui = Button(root, image= photo_volume_diminui, cursor='hand2', border=0 ,bg="black")

# Button Localização 

b_play.place(x=130, y=350)
b_passa.place(x=185, y=350)
b_volta.place(x=75, y=350)
b_musica_aleatoria.place(x= 40, y=360)
b_volume_aumenta.place(x= 275, y=355)
b_volume_diminui.place(x= 245, y=355)

###################################### Button Funções ######################################

b_play.bind('<Button>', play)
b_passa.bind('<ButtonPress>', passa_musica)
b_volta.bind('<ButtonPress>', volta_musica)
b_musica_aleatoria.bind('<Button>', musica_aleatoria)
b_volume_aumenta.bind('<ButtonPress>', volume_aumenta)
b_volume_diminui.bind('<ButtonPress>', volume_diminui)

####################################### Loop ######################################

root.mainloop()