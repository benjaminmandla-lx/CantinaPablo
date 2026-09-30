from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QApplication
)


class TelaTotem(QWidget):
    """
    Totem: cliente digita nome e faz o pedido.
    Não tem lista, não tem timer.
    """
    def __init__(self, ao_voltar_login=None):
        super().__init__()
        self.ao_voltar_login = ao_voltar_login
        self.setWindowTitle("Cantina do IFSP - CJO - Totem")
        self.showFullScreen()

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(60, 60, 60, 60)

        layout.addStretch()

        titulo = QLabel("Cantina do IFSP - CJO")
        titulo.setObjectName("titulo_totem")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        instrucao = QLabel("Digite seu nome para começar")
        instrucao.setObjectName("instrucao_totem")
        instrucao.setAlignment(Qt.AlignCenter)
        layout.addWidget(instrucao)

        layout.addSpacing(30)

        self.campo_nome = QLineEdit()
        self.campo_nome.setPlaceholderText("Seu nome")
        self.campo_nome.setMaxLength(30)
        self.campo_nome.setMinimumHeight(80)
        self.campo_nome.setAlignment(Qt.AlignCenter)
        self.campo_nome.setObjectName("campo_totem")
        self.campo_nome.returnPressed.connect(self.comecar)
        layout.addWidget(self.campo_nome)

        botao = QPushButton("Começar")
        botao.setObjectName("botao_totem")
        botao.setMinimumHeight(80)
        botao.clicked.connect(self.comecar)
        layout.addWidget(botao)

        # Botão voltar (caso o cliente desista antes de digitar)
        if self.ao_voltar_login:
            voltar = QPushButton("← Voltar")
            voltar.clicked.connect(self._voltar)
            layout.addWidget(voltar)

        layout.addStretch()

        self.principal = None

    def comecar(self):
        nome = self.campo_nome.text().strip()
        if not nome:
            QMessageBox.warning(self, "Nome", "Digite seu nome para começar.")
            return

        from telas.principal import TelaPrincipal
        self.principal = TelaPrincipal(
            tipo_usuario="cliente",
            nome_usuario=nome,
            modo_totem=True,
            ao_voltar_totem=self._voltar
        )
        QApplication.instance().principal = self.principal
        self.principal.show()
        self.hide()

    def _voltar(self):
        """Cliente terminou (ou desistiu) — volta pra tela de login."""
        self.campo_nome.clear()
        self.hide()
        if self.principal:
            self.principal.close()
            self.principal = None
        if self.ao_voltar_login:
            self.ao_voltar_login()