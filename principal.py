from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QStackedWidget
)
from telas.cardapio import TelaCardapio
from telas.fila import TelaFila
from telas.atendimento import TelaAtendimento
from telas.produtos_admin import TelaProdutosAdmin
from telas.financeiro import TelaFinanceiro
from telas.dashboard import TelaDashboard
from telas.entrega import TelaEntrega
from telas.meus_pedidos import TelaMeusPedidos


class TelaPrincipal(QWidget):
    def __init__(self, tipo_usuario="cliente", nome_usuario="Cliente",
                 modo_totem=False, ao_voltar_totem=None):
        super().__init__()
        self.tipo_usuario = tipo_usuario
        self.nome_usuario = nome_usuario
        self.modo_totem = modo_totem
        self.ao_voltar_totem = ao_voltar_totem

        self.setWindowTitle("Cantina do IFSP - CJO - Sistema da Cantina")
        if modo_totem:
            self.showFullScreen()
        else:
            self.resize(1000, 700)

        layout = QVBoxLayout(self)

        # ---------- Cabeçalho ----------
        topo = QHBoxLayout()
        titulo = QLabel("Cantina do IFSP - CJO")
        titulo.setObjectName("titulo")
        topo.addWidget(titulo)
        topo.addStretch()

        perfil_label = QLabel(f"{self.nome_usuario} ({self.tipo_usuario})")
        perfil_label.setObjectName("secao")
        topo.addWidget(perfil_label)

        # Só mostra "Sair" se NÃO for totem
        if not modo_totem:
            sair = QPushButton("Sair")
            sair.clicked.connect(self.sair)
            topo.addWidget(sair)

        layout.addLayout(topo)

        subtitulo = QLabel("Sistema de atendimento e gestão da cantina")
        layout.addWidget(subtitulo)

        # ---------- Botões por perfil ----------
        botoes = QHBoxLayout()

        if self.tipo_usuario == "admin":
            acoes = [
                ("Fazer pedido", self.abrir_cardapio),
                ("Fila", self.abrir_fila),
                ("Atendimento", self.abrir_atendimento),
                ("Entregas", self.abrir_entrega),
                ("Produtos", self.abrir_produtos),
                ("Financeiro", self.abrir_financeiro),
                ("Dashboard", self.abrir_dashboard),
            ]
        else:
            acoes = [
                ("Fazer pedido", self.abrir_cardapio),
                ("Meus pedidos", self.abrir_meus_pedidos),
            ]

        for texto, metodo in acoes:
            b = QPushButton(texto)
            b.clicked.connect(metodo)
            botoes.addWidget(b)

        layout.addLayout(botoes)

        # ---------- Stack ----------
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        boas_vindas = QWidget()
        bv_layout = QVBoxLayout(boas_vindas)
        bv_layout.addStretch()
        msg = QLabel(f"Olá, {self.nome_usuario}! Selecione uma opção no menu acima.")
        msg.setAlignment(Qt.AlignCenter)
        bv_layout.addWidget(msg)
        bv_layout.addStretch()
        self.stack.addWidget(boas_vindas)

        self.telas = {}

    def _ir_para(self, chave, classe_tela, **kwargs):
        if chave not in self.telas:
            try:
                tela = classe_tela(ao_voltar=self._voltar_ao_menu, **kwargs)
            except TypeError:
                tela = classe_tela(**kwargs)
            self.telas[chave] = tela
            self.stack.addWidget(tela)
        self.stack.setCurrentWidget(self.telas[chave])

    def _voltar_ao_menu(self):
        self.stack.setCurrentIndex(0)

    def sair(self):
        from telas.login import TelaLogin
        self.tela_login = TelaLogin(ao_logar=iniciar_app)
        self.tela_login.show()
        self.close()

    # ---------- Callback do totem ----------
    def finalizar_pedido(self):
        """Chamado quando o cliente termina o pedido (modo totem)."""
        if self.ao_voltar_totem:
            self.ao_voltar_totem()
        else:
            self._voltar_ao_menu()

    # ---------- Admin ----------
    def abrir_cardapio(self):
        self._ir_para(
            "cardapio", TelaCardapio,
            cliente_nome=self.nome_usuario
        )

    def abrir_fila(self):
        self._ir_para("fila", TelaFila)

    def abrir_atendimento(self):
        self._ir_para("atendimento", TelaAtendimento)

    def abrir_entrega(self):
        self._ir_para("entrega", TelaEntrega)

    def abrir_produtos(self):
        self._ir_para("produtos", TelaProdutosAdmin)

    def abrir_financeiro(self):
        self._ir_para("financeiro", TelaFinanceiro)

    def abrir_dashboard(self):
        self._ir_para("dashboard", TelaDashboard)

    # ---------- Cliente ----------
    def abrir_meus_pedidos(self):
        self._ir_para(
            "meus_pedidos", TelaMeusPedidos,
            nome_usuario=self.nome_usuario
        )


_janela_principal = None

def iniciar_app(usuario, tipo):
    global _janela_principal
    _janela_principal = TelaPrincipal(tipo_usuario=tipo, nome_usuario=usuario)
    _janela_principal.show()