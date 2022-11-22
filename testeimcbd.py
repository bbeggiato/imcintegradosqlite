# Python 3.10.8
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import banco

def pesquisar():
  tv.delete(*tv.get_children())
  vquery = "SELECT * FROM clientes WHERE nome LIkE'%" + vnomepesquisar.get() + "%' order by idcliente"
  linhas = banco.dql(vquery)
  for i in linhas:
    tv.insert("", "end", values=i)

def popular():
  tv.delete(*tv.get_children())  # Deleta todos os registros do Tree View
  vquery = "SELECT * FROM clientes order by idcliente desc"
  linhas = banco.dql(vquery)
  for i in linhas:
    tv.insert("", "end", values=i)

def deletar():
  vid = -1
  itemSelecionado = tv.selection()[0]
  valores = tv.item(itemSelecionado, "values")
  vid = valores[0]
  try:
    vquery = f"DELETE FROM clientes WHERE idcliente={vid}"
    resp = messagebox.askyesno("Resetar", "Deseja Apagar esse Usuário do Cadastro? \n Só é possível apagar um de cada vez")
    if resp == True:
      banco.dml(vquery)
      tv.delete(itemSelecionado)
      messagebox.showinfo(title="DELETADO", message="Item Deletado com Sucesso!")
  except:
    messagebox.showinfo(title="ERRO", message="Erro ao Deletar")
    return


###################################################################################################
# Sai do sistema
def sair():
  resposta2 = messagebox.askyesno("Sair", "Deseja Sair?")
  if resposta2 == True:
     main.quit()


# Validação para não permitir string nos campos peso e altura
def valida(entrada):
  if entrada.replace('.', '',1).isdigit():
    return True
  elif entrada == "":
    return True
  else:
    return False


# Executa comando da funcão ao clicar no botão Calcular
def analisaDados():
  # Recebe os valores com o get() e os atribui a variável
  if vnome.get() != "" and vnome.get() != "" and vendereco.get() != "" and valtura.get() != "" and vpeso.get() != "":
    nom = vnome.get()
    end = vendereco.get()
    alt = float(valtura.get())
    pes = float(vpeso.get())

    # Converte altura para metro
    altmetros = alt / 100


    # Cálculo do IMC jogado a uma variável
    imc = pes / (altmetros * altmetros)

    # Calcula como a pessoa se enquadra baseado no IMC
    estado = ''
    if imc < 17:
      estado = 'Muito abaixo do Peso'
    elif imc >= 17 and imc < 18.5:
      estado = 'Abaixo do Peso'
    elif imc >= 18.5 and imc <= 24.99:
      estado = 'Peso Normal'
    elif imc >= 25 and imc <= 29.99:
      estado = 'Acima do Peso'
    elif imc >= 30 and imc <= 34.99:
      estado = 'Obesidade I'
    elif imc >= 35 and imc <= 39.99:
      estado = 'Obesidade Severa'
    elif imc >= 40:
        estado = 'Obesidade Mórbida'

    # Atribui a resposta a res
    res = f' O IMC  é: {imc:.2f}\n\n {estado}'

    # Escreve o conteúdo de res
    lb["text"] = res

    #dados = salvar(nom, end, pes, altmetros, imc,  estado)

  else:
    messagebox.showwarning(title="Aviso",message="Favor Preencher Todos os Campos!")
# Salva os dados no BD
def salvar():

  if lb["text"] != '' and vnome.get() != "" and vnome.get() != "" and vendereco.get() != "" and valtura.get() != "" and vpeso.get() != "":
    nom = vnome.get()
    end = vendereco.get()
    alt = float(valtura.get())
    pes = float(vpeso.get())

    # Converte altura para metro
    altmetros = alt / 100

    # Cálculo do IMC jogado a uma variável
    imc = pes / (altmetros * altmetros)

    # Calcula como a pessoa se enquadra baseado no IMC
    estado = ''
    if imc < 17:
      estado = 'Muito abaixo do Peso'
    elif imc >= 17 and imc < 18.5:
      estado = 'Abaixo do Peso'
    elif imc >= 18.5 and imc <= 24.99:
      estado = 'Peso Normal'
    elif imc >= 25 and imc <= 29.99:
      estado = 'Acima do Peso'
    elif imc >= 30 and imc <= 34.99:
      estado = 'Obesidade I'
    elif imc >= 35 and imc <= 39.99:
      estado = 'Obesidade Severa'
    elif imc >= 40:
      estado = 'Obesidade Mórbida'

    querSalvar = messagebox.askyesno("Sair", "Deseja salvar os nados no Cadastro?")
    if querSalvar == True:
      vquery = f"INSERT INTO clientes (nome, endereco, peso, altura, imc, status) VALUES('{nom}','{end}',{pes},{altmetros},{imc:.2f},'{estado}')"
      banco.dml(vquery)
      # varnome.delete(0, END)
      # varendereco.delete(0, END)
      # varpeso.delete(0, END)
      # varaltura.delete(0, END)
      popular()
      print("Dados Gravados")
      messagebox.showinfo(title="Aviso", message="Dados Salvos com Sucesso!")
  else:
    messagebox.showwarning(title="Aviso", message="Não existem dados suficientes para Salvar!")


# Executa comando da funão ao clicar no botão Limpar
def reset():
  resposta = messagebox.askyesno("Resetar","Deseja Limpar todos os Dados?")
  if resposta == True:
    # Limpa o campo Resultado
    res = ''
    lb["text"] = res

    # Limpa as Entry
    vnome.delete(0, END)
    vendereco.delete(0, END)
    valtura.delete(0, END)
    vpeso.delete(0, END)

# Nome e configs do Container
main = Tk()
main.title("Cálculo do IMC - Índice de Massa Corporal")
main.geometry("900x600")

nb=ttk.Notebook(main)
nb.place(x=0,y=0,width=900,height=600)

tb1=Frame(nb, background="lightblue")
tb2=Frame(nb, background="lightblue")

nb.add(tb1,text="Cálculo IMC")
nb.add(tb2, text="Cadastro")

vnum_cstexto=StringVar()

frame1=Frame(tb1, borderwidth=3, background="#cecece")
frame1.place(x=400,y=257,width=330,height=200)

# Campo Nome
nome = Label(tb1, text="Nome do Paciente: ", font="14", bg='lightblue', anchor=W)
nome.place(x=120, y=80, width=180, height=35)
vnome=Entry(tb1, font=14)
vnome.place(x=280, y=80, width=450, height=35)

# Campo Endereço
endereco = Label(tb1, text="Endereço Completo: ", font=14, bg='lightblue', anchor=W)
endereco.place(x=120, y=170, width=180, height=35)
vendereco=Entry(tb1)
vendereco.place(x=280, y=170, width=450, height=35)

# Campo Altura
altura = Label(tb1, text="Altura(cm)", font=14, bg='lightblue', anchor=W)
altura.place(x=120, y=260, width=100, height=35)
valtura = Entry(tb1, font=14)
valtura.place(x=280, y=260, width=100, height=35)
registro = tb1.register(valida)
valtura.config(validate="key", validatecommand=(registro,'%P'))

# Campo Peso
peso = Label(tb1, text="Peso (Kg)", font=14, bg='lightblue', anchor=W)
peso.place(x=120, y=330, width=100, height=35)
vpeso = Entry(tb1, font=14)
vpeso.place(x=280, y=330, width=100, height=35)
registro = tb1.register(valida)
vpeso.config(validate="key", validatecommand=(registro, '%P'))

# Botão Calcular
btnCalcular = Button(tb1, text="Calcular", command=analisaDados)
btnCalcular.place(x=280, y=490, width=70, height=25)

# Botão Reiniciar
btnReiniciar = Button(tb1,text="Reiniciar", command=reset)
btnReiniciar.place(x=363, y=490, width=70, height=25)

# Salva no banco de dados
btnSalvar = Button(tb1, text="Salvar", command=salvar)
btnSalvar.place(x=581, y=490, width=70, height=25)

# Botão Sair
btnSair = Button(tb1, text="Sair", command=sair)
btnSair.place(x=661, y=490, width=70, height=25)

#Resultado
lb = Label(frame1,text="",fg="#696969", background="#fafdff", font=('arial', 16, 'bold'))
lb.place(x=0, y=0, width=330, height=200)

####################################################################################################################

quadroGrid = LabelFrame(tb2, text="Cadastro")
quadroGrid.pack(fill='both', expand=TRUE, padx=10, pady=10)

tv=ttk.Treeview(quadroGrid, height=20, columns=('id', 'nome', 'endereco', 'peso', 'altura', 'imc', 'status'), show='headings')
tv.column('id', minwidth=0, width=40)
tv.column('nome', minwidth=0, width=220)
tv.column('endereco', minwidth=0, width=320)
tv.column('peso', minwidth=0, width=50)
tv.column('altura', minwidth=0, width=50)
tv.column('imc', minwidth=0, width=50)
tv.column('status', minwidth=0, width=140)
tv.heading('id', text='ID')
tv.heading('nome', text='NOME')
tv.heading('endereco', text='ENDEREÇO')
tv.heading('peso', text='PESO')
tv.heading('altura', text='ALTURA')
tv.heading('imc', text='IMC')
tv.heading('status', text='STATUS')
tv.pack()
popular()


quadroPesquisar=LabelFrame(tb2, text="Pesquisar Contatos", bg="lightblue")
quadroPesquisar.pack(fill="both", padx=107, ipady=20, pady=7)

lbid=Label(quadroPesquisar, text="Nome: ")
lbid.pack(side="left", padx=20, ipadx=10, ipady=6)
vnomepesquisar=Entry(quadroPesquisar)
vnomepesquisar.pack(side="left", ipadx=90, ipady=6)
btn_pesquisar=Button(quadroPesquisar,text="  Pesquisar  ", command=pesquisar)
btn_pesquisar.pack(side="left", padx=5, ipady=1)
btn_todos=Button(quadroPesquisar, text="Mostrar Todos", command=popular)
btn_todos.pack(side="left", padx=5, ipady=1)
btn_deletar=Button(quadroPesquisar, text="  Deletar  ", command=deletar)
btn_deletar.pack(side="left", padx=5, ipady=1)
main.mainloop()

