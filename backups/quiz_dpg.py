#librerias backend
import numpy as np
import random
import pandas as pd
#libreria gui
import dearpygui.dearpygui as dpg

dpg.create_context()

db = pd.read_excel("D:/LabSI/ElectriQuiz/Base2_Gabo.xlsx")   #base de datos

ask_q = []  #vector de las preg realizadas
cant_q = len(db)  #cantidad total de preg
actual_q = 0 #pregunta actual

preg, cat, dif, resp = [""], [""], [""], [""]
for i in range(len(db)):
    preg = np.append(preg, db.PREGUNTA[i])
    cat = np.append(cat, db.CATEGORIA[i])
    dif = np.append(dif, db.DIFICULTAD[i])
    resp = np.append(resp, db.RESPUESTA[i])

#definicion de funciones  para el programa
def q_sel():    #funcion para seleccion de preg no-repetidas
    global ask_q
    if (len(ask_q) >= cant_q):
        return 0
    num_rand = random.randint(1, cant_q)
    while num_rand in ask_q:
        num_rand = random.randint(1, cant_q)
    ask_q = np.append(ask_q, num_rand)
    return num_rand

def begin_callback():  #funcion callback del boton "comenzar"
    global preg_n
    print("comenzar presionado")
    preg_n = dpg.add_button(label="Nueva pregunta", tag="preg_n", parent="prim_window")
    dpg.set_item_callback(preg_n, preg_callback)
    dpg.set_item_pos("preg_n", [300,300])
    dpg.delete_item("begin")

def preg_callback():  #funcion callback del boton "Pregunta"
    global ask_q, actual_q, preg
    print("pregunta presionado")
    actual_q = q_sel()  #aplica la funcion de seleccion de pregunta
    print(actual_q, ask_q)
    print(preg[actual_q])
    #impresion de la pregunta en la GUI
    if len(ask_q) <= 1: 
        dpg.add_text(preg[actual_q], tag="text_preg", parent="prim_window", pos=(300,100))
        dpg.configure_item("text_preg", wrap= 250)
    else:
        dpg.delete_item("text_preg")
        dpg.delete_item("text_resp")
        dpg.add_text(preg[actual_q], tag="text_preg", parent="prim_window", pos=(300,100))
        dpg.configure_item("text_preg", wrap= 250)
    #creacion de boton "mostrar respuesta"
    dpg.add_button(label="mostrar respuesta", tag="resp_n", parent="prim_window")
    dpg.set_item_callback("resp_n",resp_callback)
    dpg.set_item_pos("resp_n",[300,350])
    dpg.configure_item("preg_n", enabled=False)  #deshabilita el boton "preg_n"

def resp_callback():    #funcion callback del boton "respuesta"
    global ask_q, actual_q, resp
    print("respuesta")
    print(resp[actual_q])
    #impresion de la respuesta en la GUI
    if len(ask_q) <= 1: 
        dpg.add_text(resp[actual_q], tag="text_resp", parent="prim_window", pos=(300,200))
        dpg.configure_item("text_resp", wrap= 250)
    else:
        dpg.add_text(resp[actual_q], tag="text_resp", parent="prim_window", pos=(300,200))
        dpg.configure_item("text_resp", wrap= 250)
    dpg.configure_item("preg_n", enabled=True) #habilita boton "pregunta"
    dpg.delete_item("resp_n") #elimina boton "respuesta"


#configuracion de la gui
with dpg.window(tag="prim_window"):
    dpg.add_text("Bienvenidos al ElectriQuiz!", pos=(300,10))
    dpg.add_spacing(count=10)
    dpg.add_separator()
    #generacion del boton "comenzar"
    begin = dpg.add_button(label="Comenzar", tag="begin", width=200, height=100)
    dpg.set_item_callback(begin, begin_callback)
    dpg.set_item_pos("begin", [300,300])

#creacion del viewport
dpg.create_viewport(title='ElectriQuiz', width=720, height=720) 
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("prim_window", True) #configurar ventana primaria
dpg.start_dearpygui()
dpg.destroy_context()