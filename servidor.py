from lista_de_usuarios import ListaDeUsuarios
import socket
import selectors
import pickle
import types
import asyncio
from usuario import Usuario

class Servidor:
  def __init__(self):
    self.usuarios_conectados = ListaDeUsuarios()
    self.porta = 5000
    self.ip = "127.0.0.1"
    self.sel = selectors.DefaultSelector()
    self.inicializa_servidor()

  def inicializa_servidor(self):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.bind((self.ip, self.porta))

  def listen(self):
    self.socket.listen()
    self.conexao, self.end_origem = self.socket.accept()
    with self.conexao:
      print(f"Conectado por: {self.end_origem}")
      while True:
        mensagem_recebida = self.conexao.recv(1024)
        if not mensagem_recebida:
          break
        self.trata_mensagem(mensagem_recebida)

  def trata_mensagem(self, mensagem):
    mensagem = pickle.loads(mensagem)
    print(mensagem)
    if mensagem["operacao"] == "criar":
      self.conecta_um_usuario(mensagem["data"])
    elif mensagem["operacao"] == "desconectar":
      self.desconecta_um_usuario(mensagem["data"])
    elif mensagem["operacao"] == "consultar":
      self.busca_usuario(mensagem["data"])
    elif mensagem["operacao"] == "listar":
      self.lista_usuarios_conectados()

  def conecta_um_usuario(self, nome_do_novo_usuario):
    for usuario in self.usuarios_conectados:
      if (usuario.nome == nome_do_novo_usuario):
        msg = pickle.dumps({"data": None})
        self.conexao.sendall(msg)
        return
    novo_usuario = Usuario(nome_do_novo_usuario, self.end_origem[0], self.end_origem[1])
    self.usuarios_conectados.append(novo_usuario)
    print(self.usuarios_conectados)
    msg = pickle.dumps({"data": novo_usuario})
    self.conexao.sendall(msg)

  def desconecta_um_usuario(self, usuario_a_excluir):
    usuario_a_excluir =  self.busca_usuario_local(usuario_a_excluir)
    print(f"Excluindo: {usuario_a_excluir}")
    self.usuarios_conectados.remove_usuario(usuario_a_excluir)
    msg = pickle.dumps({"data": True})
    self.conexao.sendall(msg)

  def busca_usuario_local(self, nome):
    for usuario in self.usuarios_conectados:
      if nome == usuario.nome:
        return usuario
    return None

  def busca_usuario(self, nome):
    for usuario in self.usuarios_conectados:
      if nome == usuario.nome:
        msg = pickle.dumps({"data": usuario})
        self.conexao.sendall(msg)
        return
    msg = pickle.dumps({"data": None})
    self.conexao.sendall(msg)

  def lista_usuarios_conectados(self):
    lista_de_usuarios = self.usuarios_conectados.copy()
    lista_de_usuarios = pickle.dumps({"data": lista_de_usuarios})
    self.conexao.sendall(lista_de_usuarios)