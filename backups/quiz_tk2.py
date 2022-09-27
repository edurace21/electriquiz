#librerias del gui
import tkinter as tk
from PIL import Image, ImageTk
#librerias para algoritmos
import pandas as pd
import numpy as np
import random

#imagenes
logo_im = Image.open("imag/LogoCFIE.png")                #logo congreso
bienv_im = Image.open("imag/bienvenida.png")             #bienvenida
begin_im = Image.open("imag/comenzar_bt.png")            #boton comenzar
logo2_im = Image.open("imag/LogoCFIE2.png")              #logo congreso 2
home_img = Image.open("imag/hogar.png")                  #home button
ele_im = Image.open("imag/electriquiz.png")              #electriquiz 2022

db = pd.read_excel("Base2_Gabo.xlsx", engine='openpyxl')   #base de datos

ask_q = []  #vector de las preg realizadas
cant_q = len(db)
print('Cantidad de preguntas:', cant_q)
actual_q = 0    #pregunta actual
actual_dif = '1'  #dificultad actual
h_state = 0     #estado del home

preg, cat, resp, dif = ["Ya se realizaron todas las preguntas \n de este nivel de dificultad"], [""], [""], [""]

for i in range(cant_q):     #descomposicion de la base de datos en vectores
    preg = np.append(preg, db.PREGUNTA[i])
    cat = np.append(cat, db.CATEGORIA[i])
    dif = np.append(dif, db.DIFICULTAD[i])
    resp = np.append(resp, db.RESPUESTA[i])

#inicio de la ventana
root = tk.Tk()
root.title("Electri-Quiz")
winsize = str(root.winfo_screenwidth()-10) + 'x' + str(root.winfo_screenheight()-50)
root.geometry(winsize)
root.iconbitmap("imag/LogoCFIE.ico")

#funcion para seleccion de preguntas no-repetidas
def q_sel():    
    global ask_q, cant_q, dif, actual_dif
    if (len(ask_q) >= cant_q):
        return 0
    #algoritmo para seleccion de preguntas segun dificultad
    dif_matrix = []
    for index in range(len(dif)):
        if dif[index] == actual_dif:
            dif_matrix = np.append(dif_matrix, index)   #matriz con indices de preguntas segun dificultad
    num_rand = random.randint(0, len(dif_matrix)-1)
    it_cnt = 0      #contador de iteraciones
    while dif_matrix[num_rand] in ask_q:    #discriminacion si la pregunta fue seleccionada
        num_rand = random.randint(0, len(dif_matrix)-1)
        if it_cnt >= len(dif_matrix):       # si todas las preguntas fueron seleccionadas se envia el mensaje
            return 0                        # "todas las preguntas ya fueron seleccionadas"
        it_cnt += 1
    ask_q = np.append(ask_q, dif_matrix[num_rand])
    print('preguntas realizadas:\n', ask_q)
    return dif_matrix[num_rand]

#callback respuestas
def resp_callback():
    print("\nresp_callback()\n")
    global frame2, action_button, preg_text, resp_text
    #imprimir respuestas en la gui
    resp_text = tk.Label(frame2, text=resp[actual_q], font=("TkMenuFont", '22','italic'),
                        bg="#03061a", fg="#fcfcfc")
    if len(resp[actual_q]) <= 50:   #tamano de texto dinamico
        resp_text.config(wraplength=400)
    else:
        resp_text.config(wraplength=750)
    resp_text.place(relx=0.5, rely=0.45, anchor='center')
    #boton de pregunta
    action_button.config(text="Nueva Pregunta", command=preg_callback, font=("Helvetica",'16'))

#callback preguntas
def preg_callback():
    print("\npreg_callback()")
    global actual_q, frame2, preg_text, h_state, cat, cat_text, dif, dif_slider, actual_dif, resp_text, action_button
    if (len(ask_q) <= 0) or (h_state == 1):
        #seleccion de pregunta
        actual_q = int(q_sel())  
        #imprime primera pregunta
        preg_text = tk.Label(frame2, text=preg[actual_q], font=("TkMenuFont", '20', 'bold'),
                            bg="#03061a", fg="#fcfcfc", wraplength=750)
        preg_text.place(relx=0.5, rely=0.35, anchor='center')
        h_state = 0     #reset del home
        #imprime categoria
        cat_text = tk.Label(frame2, text="Categoria: \n" + cat[actual_q],
                            fg="#03061a", bg="#fcfcfc", wraplength=250,
                            font=("Rockwell Extra Bold",'16'), height=4, width=14)
        cat_text.place(relx=0.25, rely=0.75, anchor='center')
        #slider - seleccion dificultad
        dif_slider = tk.Scale(frame2, label="Dificultad:", length=150,
                              font=("Rockwell Extra Bold",'16'),
                              from_=1, to=3, orient='horizontal', width=35)
        dif_slider.place(relx=1-0.25, rely=0.75, anchor='center')
    else:
        actual_dif = str(dif_slider.get())      #seleccion de dificultad
        actual_q = int(q_sel())     #seleccion de pregunta
        resp_text.destroy()     #destruye respuesta
        preg_text.config(text=preg[actual_q])   #modifica el texto de la pregunta
        cat_text.config(text="Categoria: \n" + cat[actual_q])     #modifica texto de categoria
    #boton de respuesta    
    action_button.config(text="Mostrar Respuesta", command=resp_callback, font=("Helvetica",'16','italic'))

    # monitoreo de preguntas
    print("indice:", actual_q, "\ndif de pregunta:", dif[actual_q], "\nactual dif:", actual_dif)

#callback boton home
def home_callback():
    print("callback_home()")
    global frame1, frame2, h_state
    h_state = 1     #set estado de home
    frame1.destroy()
    frame2.destroy()
    inicio()

#callback boton Comenzar
def begin_callback():
    print("callback_begin()")
    
    #destruir boton "Comenzar"
    global bienv_label, begin_bt, root, frame2, frame1
    bienv_label.destroy()
    begin_bt.destroy()
    frame1.destroy()
    frame2.destroy()

    #config-frame1
    global logo2_im, logo_photo
    frame1 = tk.Frame(root, width=root.winfo_width(), height=100,
                      padx=0, pady=0, bg="#fcfcfc")
    frame1.place(relx=0.5, rely=1, relheight=0.1, relwidth=1, anchor='s')
    #logo congreso - frame1
    logo2_im.thumbnail((round(100*1.23), 100))
    logo_photo = ImageTk.PhotoImage(logo2_im)
    print(logo_photo.width(), logo_photo.height())
    logo_label = tk.Label(frame1, image=logo_photo, background="#fcfcfc", anchor="center")
    logo_label.place(relx=0.5, rely=0.5, anchor='center', relheight=1, relwidth=1)
    #boton de regreso a pantalla principal
    global home_button, home_img, home_photo      
    home_img.thumbnail((35,35))
    home_photo = ImageTk.PhotoImage(home_img)
    home_button = tk.Button(frame1, image=home_photo, bg="#fcfcfc", 
                            command=home_callback, borderwidth=0)
    home_button.place(relx=0.95, rely=0.5, anchor='center')
    
    #config-frame2
    frame2 = tk.Frame(root, height=root.winfo_height(), width=root.winfo_width(),
                      padx=0, pady=0, bg="#03061a")
    frame2.place(relx=0.5, rely=0, relheight=0.9, relwidth=1, anchor='n')
    #Label - ElectriQuiz 2022
    global ele_im, ele_photo, ele_label
    ele_photo = ImageTk.PhotoImage(ele_im)
    ele_label = tk.Label(frame2, image=ele_photo, bg="#03061a", borderwidth=0)
    ele_label.place(relx=0.5, rely=0.1, anchor='n')
    #boton de accion
    global action_button   
    action_button = tk.Button(frame2, text="Nueva pregunta", command=preg_callback,
                              height=2, font=("Helvetica",'16'))
    action_button.place(relx=0.5, rely=0.75, anchor='center')

#funcion para iniciar
def inicio():
    #configuracion ventana
    global root
    root.columnconfigure(0,weight=1)
    root.columnconfigure(1, weight=2)
    root.rowconfigure(0,weight=1)
    root.minsize(int(1080*(7/8)),720)
    root.maxsize(root.winfo_screenwidth(),root.winfo_screenheight())
    print(root.winfo_width(), root.winfo_height())

    #frame 1 - logo
    global frame1
    frame1 = tk.Frame(root, height=root.winfo_height(), padx=0, pady=0,
                      width=int(root.winfo_width()*1/3), bg="#fcfcfc")
    frame1.grid(column=0,row=0,sticky='NSEW')
    #label - logo
    global logo_im, logo_photo
    logo_im.thumbnail((450,450*1.1855))
    logo_photo = ImageTk.PhotoImage(logo_im)
    print(logo_photo.width(), logo_photo.height())
    logo_label = tk.Label(frame1, image=logo_photo, background="#fcfcfc", anchor="center")
    logo_label.place(relx=0.5, rely=0.5, anchor='center')

    #frame2 - preguntas
    global frame2
    frame2 = tk.Frame(root, height=root.winfo_height(), padx=0, pady=0,
                      width=int(root.winfo_width()*2/3), bg="#03061a")
    frame2.grid(column=1,row=0,sticky='NSEW')
    print(frame2.winfo_width())
    #imagen - bienvenida
    global bienv_im, bienv_photo, bienv_label
    bienv_im.thumbnail((720,720))
    bienv_photo = ImageTk.PhotoImage(bienv_im)
    bienv_label = tk.Label(frame2, image=bienv_photo, bg="#03061a")
    bienv_label.place(relx=0.5, rely=0.4, relheight=1, relwidth=1, anchor='center')
    #button - "comenzar"
    global begin_bt, begin_im, begin_photo
    begin_im.thumbnail((250,250))
    begin_photo = ImageTk.PhotoImage(begin_im)
    begin_bt = tk.Button(frame2, image=begin_photo, command=begin_callback,
                        bg="#03061a", borderwidth=0)
    begin_bt.place(relx=0.5, rely=0.65, anchor='center')

    #inicio ventana
    root.mainloop()

inicio()