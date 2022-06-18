import random
import itertools
import string
import itertools as it
import tkinter as  tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

expr=''
gramatica = {}
PRIMEROS = {}
SIGUIENTES = {}
CP = {}
"""----------------------------------------Diseño de interfaz------------------------------------------------------"""

# Se crea la ventana:
ventana = tk.Tk()

# Se le da un tamaño:
ventana.geometry("1350x700+0+0")

# Agregando un titulo a la ventana
ventana.title("Proyecto LL(1)")

# En este canvas colocaremos las herramientas que nos permitan manipular el programa
canvas_principal = tk.Canvas(ventana, width=530, height=700, bg="#bde0fe")
canvas_principal.place(x=830, y=0)

# En este canvas se va a dibujar el analizador LL(1) que se genere:
canvas_dibujo = tk.Canvas(ventana, width=830, height=700, bg="#bde0fe")
canvas_dibujo.place(x=0, y=0)

# Titulo del dibujo
etiqueta = tk.Label(canvas_dibujo, text="LL(1)", fg="white", bg="#bde0fe", font=("Arial", 18))
etiqueta.place(x=350, y=2)


#outputs canvas dibujo
txt_Primeros=ScrolledText(canvas_dibujo,state="disable")
txt_Siguientes=ScrolledText(canvas_dibujo,state="disable")
txt_ConjuntoPrediccion=ScrolledText(canvas_dibujo,state="disable")


#ubicacion de outputs
txt_Primeros.place(x = 10, y = 100,width=400,height=400)
txt_Siguientes.place(x = 425, y = 100,width=400,height=400)
txt_ConjuntoPrediccion.place(x = 10, y = 550,width=815,height=100)

#labels canvas dibujo(titulos)
etiqueta1 = tk.Label(canvas_dibujo, text="Primeros", fg="white", bg="#bde0fe", font=("Arial", 18))
etiqueta2 = tk.Label(canvas_dibujo, text="Siguientes", fg="white", bg="#bde0fe", font=("Arial", 18))
etiqueta3 = tk.Label(canvas_dibujo, text="Conjunto predicción", fg="white", bg="#bde0fe", font=("Arial", 18))

#ubicacion labels
etiqueta1.place(x=50, y=50)
etiqueta2.place(x=500, y=50)
etiqueta3.place(x=350, y=510)

#input canvas principal
txt_gramatica=ScrolledText(canvas_principal)

#ubicacion canvas principal
txt_gramatica.place(x = 10, y = 100,width=500,height=400)

#label canvas principal (titulo)
etiqueta = tk.Label(canvas_principal, text="Gramatica", fg="white", bg="#bde0fe", font=("Arial", 18))

#ubicacion canvas principal
etiqueta.place(x=50, y=50)



"""----------------------------------------Funciones---------------------------------------------------"""

def ingresarAlfabeto():
    gramatica1=txt_gramatica.get("0.0","end")
    
    if gramatica1.isspace() or len(gramatica1)==0:
        messagebox.showinfo(message="Campo vacío \n Verifica la gramatica...", title="Error")
    else:
        for x in gramatica1.split("\n"):
            y=x.split("->")
            k=y.pop(0)
            if k is not  '':
                lista=[w.split("|")  for w in y]
                if not lista:
                    messagebox.showinfo(message="Verifica la gramatica!.", title="Error")
                else:
                    gramatica[k]=lista.pop()
            y.clear()


        ejecución(gramatica)
       
def ejecución(gramatica):       
    """
    factor=factorizar(gramatica)
    
    if factor!=gramatica:
        gramatica=factor
        #txt_gramatica.delete("0.0","end")
        txt_gramatica.insert("end",gramatica)

    recursion=RecursionIzquierda(gramatica)
    if recursion!=gramatica:
        gramatica=recursion
        #txt_gramatica.delete("0.0","end")
        txt_gramatica.insert("end",gramatica)
    
    """
    k=list(gramatica.keys())
    PRIMEROS,SIGUIENTES,CP=ConjuntoPrediccionG(gramatica,k[0])
    p1=showDict(PRIMEROS)
    s2=showDict(SIGUIENTES)
    #c3=showDict(CP)
    txt_Primeros.configure(state ='normal')
    txt_Primeros.insert("end",p1)
    txt_Primeros.configure(state ='disabled')
    txt_Siguientes.configure(state ='normal')
    txt_Siguientes.insert("end",s2)
    txt_Siguientes.configure(state ='disabled')
    txt_ConjuntoPrediccion.configure(state ='normal')
    txt_ConjuntoPrediccion.insert("end",CP)
    txt_ConjuntoPrediccion.configure(state ='disabled')
        

def ConjuntoPrediccionG(gramatica,key,cp={}):
    primeros=PrimerosG(gramatica,key)  
    siguientes=SiguientesG(gramatica,key,primeros)  
    print("primeros",primeros)
    print("siguientes",siguientes)
    for k,v in gramatica.items():
        temp=[]
        for j in v:
            t=primeros[k]
            if '' in t or 'λ' in t:
                cp[k+'->'+j]=siguientes[k]
            else:
                cp[k+'->'+j]=[x  if x is not None  else primeros[j[0]] for x in prim(gramatica,j)]
            temp.append(cp[k+'->'+j])
            print(k+'->'+j,temp)
        if list(set.intersection(*map(set, temp))):
            cp={}
            break
        temp.clear()
    return primeros,siguientes,cp

def SiguientesG(gramatica,key,primeros,siguientes={}):
    if not siguientes :
        if key == list(gramatica.keys())[0]:
            siguientes[key]=['$']
            SiguientesG(gramatica,key,siguientes)
            k=list(gramatica.keys())[list(gramatica.keys()).index(key)+1]
            SiguientesG(gramatica,k,primeros,siguientes)           
    else:
        for r,i in gramatica.items():   
            for j in i:
                if key in j:
                    t=j.split(key)[1]
                    if t is '' or t is 'λ' :
                        try:
                            if t not in list(siguientes[key]) :
                                siguientes[key].extend([w for w in siguientes[r] if w not in siguientes[key]])
                        except KeyError :
                            siguientes[key]=siguientes[r]

                    elif t[0] in gramatica.keys():
                        
                        siguientes[key].extend(list(primeros[key]))                     
                    else:
                        try:
                            if t in list(siguientes[key]) :
                                siguientes[key].append(t)

                        except KeyError :
                            siguientes[key]=[t]
        if list(gramatica.keys()).index(key)+1 <= len(gramatica.keys())-1:
            k=list(gramatica.keys())[list(gramatica.keys()).index(key)+1]
            SiguientesG(gramatica,k,primeros,siguientes)

    for h in siguientes.values():
        if [...] in h:
            h.remove([...])
 
    return siguientes

def PrimerosG(gramatica,key,primeros={}):
    w=[]
    if not primeros:
       
        for i in gramatica[key]:
            if i[0] in gramatica.keys():
                PrimerosG(gramatica,i[0],primeros)
                primeros[key].extend(primeros[i[0]])
            else:
                w.append(i[0])
                primeros[key]=w
    else:
        for i in gramatica[key]:
            if i[0] in gramatica.keys():
                primeros[key]=PrimerosG(gramatica,i[0],primeros)
            else:
                w.append(i[0])
                primeros[key]=w
        if list(gramatica.keys()).index(key)+1 <= len(gramatica.keys())-1:
            k=list(gramatica.keys())[list(gramatica.keys()).index(key)+1]
            PrimerosG(gramatica,k,primeros)
    return primeros
    
def prim(gramatica,l):
    y=[]
    for i in l:
        if i in gramatica.keys():
            return y
        y.append(i)
    return y



def factorizar(gramatica):
    g=gramatica.copy()
    for k,v in gramatica.items():
        factor=''.join(c[0] for c in it.takewhile(lambda x:
        all(x[0] == y for y in x), zip(*v)))
        if factor:
            temp=[i.replace(factor,'') for i in v if (factor in i)]
            if '' in temp:
                temp.remove('')
                temp.append('λ')
            g[k]=factor+k+'°'
            g[k+'°']=temp
            print(temp)
        else:
            g[k]=v
    return g
 
def RecursionIzquierda(gram):
    #l=[]
    g=gram.copy()
    for k,v in gram.items():
        l=[]
        for e in v:
            if e.startswith(k) :
                g[k][g[k].index(e)]=e.replace(k,'')
                l.append(e.replace(k,'')+k+'*')
                g[k].remove(e.replace(k,''))
        if l:
            g[k]=[x+k+'*' for x in g[k]]
            l.append('λ')
            g[k]
            g[k+'*']=l
            #l.clear()
    return g

   

def subStrings(strg):
    ss=[]
    for x in range(len(strg)+1):
        ss.append(strg[:x])
    ss.remove('')
    return ss

def showDict(dicti):
    out=""
    for k,v in dicti.items():
        out=''.join((out,' '+k+':{'+','.join(v)+'}\n'))

    return out


def reset():
    #limpieza de todas las variables y outputs
    gramatica.clear()
    txt_Primeros.configure(state ='normal')
    txt_Primeros.delete("0.0","end")
    txt_Primeros.configure(state ='disabled')
    txt_Siguientes.configure(state ='normal')
    txt_Siguientes.delete("0.0","end")
    txt_Siguientes.configure(state ='disabled')
    txt_ConjuntoPrediccion.configure(state ='normal')
    txt_ConjuntoPrediccion.delete("0.0","end")
    txt_ConjuntoPrediccion.configure(state ='disabled')
    txt_gramatica.delete("0.0","end")



"""---------------------------------------Botonera---------------------------------------------------------------------------"""

btn_ingresarAlfabeto = tk.Button(canvas_principal, width=53, text="Ingresar Alfabeto", font=("Arial", 11), fg="#ffffff",
                          command=ingresarAlfabeto, background="#1E6F4A", state="normal")
btn_ingresarAlfabeto.place(x=20, y=600)


btn_reset = tk.Button(canvas_principal, width=53, text="Reset", font=("Arial", 11), fg="#ffffff",
                          command=reset, background="#1E6F4A", state="normal")
btn_reset.place(x=20, y=650)




"""---------------------------------------------Hilo principal de ejecución----------------------------------------------------------"""

# Hace que la ventana se mantenga persistente en pantalla
ventana.mainloop()


"""
some grammar examples
s->abc12345|abcskdfjh|abc456|abc098g|abc
D->123fg|123skdfjh|123456|123098g|123
s->abc12345|Dfggf|abc
D->ksdjf|hkc

S->Swedf|dfggfd|wer
D->defd|qwer|345


s->abc12345|Dfggf|abc
D->ksdjf|hkc|T
T->2345|18765A
A->wert

S->123|2345|345D4543|Dert
D->gvfcx|34rtfg|ertY34|erdf
Y->1|2|3|4



"""