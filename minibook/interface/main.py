from tkinter import *
from requests import post, get

URL='http://127.0.0.1:5000'

def add():
    dados = get(URL)
    dados.json.to_dict()
    print(dados)

def Actu():
    print('Actualizado')

def dele():
    print('deletado')


tela = Tk()

area_left = Frame(tela,bg='grey')
area_left.place(relx=0.00, rely=0.00, relwidth=0.60, relheight=1.00)

folha = Frame(area_left,bg='white')
folha.place(relx=0.50, rely=0.50,anchor=CENTER, relwidth=0.80, relheight=0.80)


area_right = Frame(tela,bg='lightgrey')
area_right.place(relx=0.60, rely=0.00, relwidth=0.40, relheight=1.00)

entrada = Entry(area_right)
entrada.place(relx=0.50, rely=0.10,anchor=CENTER, relwidth=0.80, relheight=0.10)

Add = Button(area_right,text="add", command=add)
Add.place(relx=0.10, rely=0.30, relwidth=0.20, relheight=0.05)

actu = Button(area_right,text="Update", command=Actu)
actu.place(relx=0.36, rely=0.30, relwidth=0.20, relheight=0.05)

dele = Button(area_right,text="delete", command=dele)
dele.place(relx=0.66, rely=0.30, relwidth=0.20, relheight=0.05)

tela.mainloop()