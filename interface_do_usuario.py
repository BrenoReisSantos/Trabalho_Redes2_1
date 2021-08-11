import tkinter
from tkinter import *
from tkinter import font
from usuario import Usuario
from servidor import Servidor
import socket
import pickle

class InterfaceDoUsuario(tkinter.Frame):
  def __init__(self, master=None):
    super().__init__(master)
    self.fonte = ("Verdana", "8")
    self.master = master
    self.pack()

    self.ip_host = "127.0.0.1"
    self.porta_host = 5000

    self.porta_usuario = 50000

    self.conectado = False
    self.mostrando_consulta = False

    self.cria_container_do_form_do_usuario()
    #self.cria_formulario_de_consulta_de_usuario()
    #self.cria_botao_de_desconectar()

  def create_widgets(self):
    self.hi_there = tkinter.Button(self)
    self.hi_there["text"] = "Hello World\n(click me)"
    self.hi_there["command"] = self.say_hi
    self.hi_there.pack(side="top")

    self.quit = tkinter.Button(self, text="QUIT", fg="red",
                          command=self.master.destroy)
    self.quit.pack(side="bottom")

  def cria_container_do_form_do_usuario(self):
    self.container_do_formulario = Frame(self.master)
    self.container_do_formulario.pack()

    self.container_nome_usuario = Frame(self.container_do_formulario)
    self.container_nome_usuario.pack()
    self.label_nome_usuario = Label(self.container_nome_usuario, text="Nome", font=self.fonte)
    self.label_nome_usuario.pack(side=LEFT)
    self.formulario_nome_usuario = Entry(self.container_nome_usuario)
    self.formulario_nome_usuario["font"] = self.fonte
    self.formulario_nome_usuario.pack(side=LEFT)

    self.container_botao_submit = Frame(self.container_do_formulario)
    self.container_botao_submit.pack()
    self.botar_de_submeter_form = Button(self.container_botao_submit, text="CONECTAR", fg="white", bg="green" , command=self.conectar_usuario)
    self.botar_de_submeter_form.pack(side=BOTTOM)

  def conectar_usuario(self):
    self.nome = self.formulario_nome_usuario.get()
    if (self.nome == ""):
      return
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((self.ip_host, self.porta_host))
      mensagem = pickle.dumps({"operacao": "criar", "data": self.nome})
      s.sendall(mensagem)
      data = s.recv(1024)
      usuarios_conectados = pickle.loads(data)
    
    usuario = pickle.loads(data)["data"]
    if usuario:
      self.ip = usuario.ip
      self.porta = usuario.porta

      self.label_nome_usuario["fg"] = "black"

      self.cria_label_para_usuario_conectado()
      self.container_do_formulario.destroy()
      self.cria_formulario_de_consulta_de_usuario()
      self.cria_botao_de_desconectar()
    else:
      self.label_nome_usuario["fg"] = "red"

  def cria_label_para_usuario_conectado(self):
    self.container_para_label_do_nome_do_usuario_conectado = Frame(self.master)
    self.container_para_label_do_nome_do_usuario_conectado.pack(side=TOP)
    self.label_nome_do_usuario_conectado = Label(self.container_para_label_do_nome_do_usuario_conectado, text=f"BEM VINDO!\n {self.nome} ({self.ip}:{self.porta}))")
    self.label_nome_do_usuario_conectado.pack(side=TOP)

  def cria_formulario_de_consulta_de_usuario(self):
    self.container_do_formulario_de_consulta_de_usuario = Frame(self.master)
    self.container_do_formulario_de_consulta_de_usuario.pack(side=BOTTOM)
    self.label_formulario_de_consulta = Label(self.container_do_formulario_de_consulta_de_usuario, text="Consulta: ", font=self.fonte)
    self.label_formulario_de_consulta.pack(side=LEFT)
    self.formulario_de_consulta = Entry(self.container_do_formulario_de_consulta_de_usuario)
    self.formulario_de_consulta.pack(side=LEFT)
    self.botao_de_consultar = Button(self.container_do_formulario_de_consulta_de_usuario, text="CONSULTAR", bg="blue", fg="white", font=self.fonte, command=self.cria_tela_de_usuario_consultado)
    self.botao_de_consultar.pack(side=LEFT)

  def cria_tela_de_usuario_consultado(self):

    self.nome_consultado = self.formulario_de_consulta.get()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((self.ip_host, self.porta_host))
      mensagem = pickle.dumps({"operacao": "consultar", "data": self.nome_consultado})
      s.sendall(mensagem)
      data = s.recv(1024)
      usuario_consultado = pickle.loads(data)["data"]

    print(f"Consultado usuário: {usuario_consultado}")

    if self.mostrando_consulta:
      self.container_tela_de_usuario_consultado.destroy()
      self.label_usuario_consultado.destroy()


    self.container_tela_de_usuario_consultado = Frame(self.master)
    self.container_tela_de_usuario_consultado.pack(side=TOP)
    self.label_usuario_consultado = Label(self.container_tela_de_usuario_consultado, text=f"NOME: {usuario_consultado.nome}\nIP: {usuario_consultado.ip}\nPORTA: {usuario_consultado.porta}")
    self.label_usuario_consultado.pack(side=BOTTOM)
    self.mostrando_consulta = True

  def mostra_mensagem_de_usuario_ja_cadastrado(self):
    self.container_de_alerta = Frame(self.master)
    self.container_de_alerta(side=TOP)
    self.label_de_mensagem = Label(self.container_de_alerta, text="Conectado com Sucesso!", font=self.fonte, fg="green")
    self.label_de_mensagem.pack(side=TOP)

  def cria_botao_de_desconectar(self):
    self.container_do_botao_de_desconectar = Frame(self.master)
    self.container_do_botao_de_desconectar.pack(side=TOP)
    self.botao_de_desconectar = Button(self.container_do_botao_de_desconectar, text="DESCONECTAR", fg="white", bg="red", command=self.desconecta)
    self.botao_de_desconectar.pack(side=TOP)

  def desconecta(self):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect((self.ip_host, self.porta_host))
      mensagem = pickle.dumps({"operacao": "desconectar", "data": self.nome})
      s.sendall(mensagem)
      data = s.recv(1024)
      resultado = pickle.loads(data)["data"]

    if (resultado):
      self.container_para_label_do_nome_do_usuario_conectado.destroy()
      self.container_do_formulario_de_consulta_de_usuario.destroy()
      self.container_do_botao_de_desconectar.destroy()
      self.cria_container_do_form_do_usuario()

      if self.mostrando_consulta:
        self.container_tela_de_usuario_consultado.destroy()
        self.label_usuario_consultado.destroy()

      self.nome = ""
      self.ip = ""
      self.porta = ""
