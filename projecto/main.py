from tkinter import *
from tkinter import messagebox
from random import randint


tela = Tk()

class aplicativo:
    def __init__(self,root):
        self.root = root
        self.root.geometry('400x350')
        self.root.title("Jogo de Advinha")
        self.Pontos = 0
        self.header()
        self.body()

        self.root.mainloop()
    def header(self):
        head = Frame(self.root,bg='#135790')
        head.place(relx=0.00, rely=0.00, relwidth=1.00, relheight=0.10)

        Label(head, text="Jogo de Advinha", font=("Arial", 10, "bold"), bg="#135790", fg='white').place(relx=0.50, rely=0.50, anchor=CENTER)
    def body(self):

        Label(self.root, text='Escolha um Número de 0 á 15', font=("Arial", 10, "bold")).place(relx=0.50, rely=0.20, anchor=CENTER)
        global entrada

        entrada = Entry(self.root)
        entrada.place(relx=0.50, rely=0.40, anchor=CENTER, relwidth=0.50, relheight=0.10)

        enviar = Button(self.root, text="Comparar", bg='#135790', fg='white', command=self.funcionamento)
        enviar.place(relx=0.50, rely=0.60, anchor=CENTER, relwidth=0.50, relheight=0.10)


        pontos = Label(self.root, text='Pontos :', font=("Arial", 10, "bold"))
        pontos.place(relx=0.50, rely=0.80, anchor=CENTER)

        cituacao = Label(self.root, text='', font=("Arial", 10, "bold"))
    def funcionamento(self):
        global entrada
        try:
            valor = int(entrada.get())
            numeroAleatorio =  randint(0,15)
            
            if valor == numeroAleatorio:
                messagebox.showinfo('Sucesso','Voçê Acertou!')
                self.Pontos += 10
            else:
                messagebox.showinfo("Perdeste","Voçê errou!")
                if self.Pontos == 0 or self.Pontos < 0:
                    messagebox.showinfo("termina",'Voçê perdeu!')
                    self.root.destroy()
                self.Pontos -= 5         
        except ValueError as e:
            pass 

aplicativo(tela)
        