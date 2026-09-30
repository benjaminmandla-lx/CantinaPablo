from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QListWidget, QListWidgetItem
)
from banco.database import conectar


class TelaLogin(QWidget):
    def __init__(self, ao_logar):
        super().__init__()
        self.ao_logar = ao_logar
        self.setWindowTitle("Cantina do IFSP - CJO")
        self.resize(700, 650)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 25, 30, 25)

        # ---------- Título ----------
        titulo = QLabel("Cantina do IFSP - CJO")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        subtitulo = QLabel("Sistema de atendimento e gestão da cantina")
        subtitulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitulo)

        layout.addSpacing(15)

        # ---------- Lista de pedidos em aberto ----------
        label_lista = QLabel("Pedidos em aberto:")
        label_lista.setObjectName("secao")
        layout.addWidget(label_lista)

        self.lista_pedidos = QListWidget()
        self.lista_pedidos.setObjectName("lista_pedidos_login")
        self.lista_pedidos.setMinimumHeight(200)
        layout.addWidget(self.lista_pedidos)

        # ---------- Botão iniciar pedido (totem) ----------
        botao_totem = QPushButton("🛒  Iniciar pedido (totem)")
        botao_totem.setObjectName("botao_cliente")
        botao_totem.setMinimumHeight(55)
        botao_totem.clicked.connect(self.abrir_totem)
        layout.addWidget(botao_totem)

        # ---------- Separador ----------
        sep = QLabel("──────────  ou entre como administrador  ──────────")
        sep.setAlignment(Qt.AlignCenter)
        layout.addWidget(sep)

        # ---------- Login admin ----------
        form = QHBoxLayout()
        self.campo_usuario = QLineEdit()
        self.campo_usuario.setPlaceholderText("Usuário")
        self.campo_senha = QLineEdit()
        self.campo_senha.setPlaceholderText("Senha")
        self.campo_senha.setEchoMode(QLineEdit.Password)
        form.addWidget(self.campo_usuario)
        form.addWidget(self.campo_senha)
        layout.addLayout(form)

        botao_admin = QPushButton("Entrar como administrador")
        botao_admin.clicked.connect(self.fazer_login)
        layout.addWidget(botao_admin)

        self.campo_senha.returnPressed.connect(self.fazer_login)

        # ---------- Timer pra atualizar a lista ----------
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_lista)
        self.timer.start(3000)
        self.atualizar_lista()

        # Referência ao totem (se aberto)
        self.totem = None

    def atualizar_lista(self):
        """Mostra pedidos que ainda não foram entregues nem cancelados."""
        c = conectar()
        rows = c.execute("""
            SELECT numero, cliente_nome, status
            FROM pedidos
            WHERE status NOT IN ('ENTREGUE', 'CANCELADO')
            ORDER BY id
        """).fetchall()
        c.close()

        self.lista_pedidos.clear()
        if not rows:
            item = QListWidgetItem("(Nenhum pedido em aberto)")
            item.setFlags(Qt.NoItemFlags)
            self.lista_pedidos.addItem(item)
            return

        for row in rows:
            item = QListWidgetItem(
                f"#{row['numero']}  —  {row['cliente_nome']}  —  {row['status']}"
            )
            item.setFlags(Qt.NoItemFlags)
            self.lista_pedidos.addItem(item)

    def abrir_totem(self):
        from telas.totem import TelaTotem
        self.totem = TelaTotem(ao_voltar_login=self._voltar_do_totem)
        self.totem.show()
        self.hide()

    def _voltar_do_totem(self):
        """Chamado quando o cliente termina o pedido no totem."""
        self.atualizar_lista()
        self.show()
        if self.totem:
            self.totem.close()
            self.totem = None

    def fazer_login(self):
        usuario = self.campo_usuario.text().strip()
        senha = self.campo_senha.text().strip()

        if not usuario or not senha:
            QMessageBox.warning(self, "Login", "Preencha usuário e senha.")
            return

        c = conectar()
        row = c.execute(
            "SELECT usuario, tipo FROM usuarios WHERE usuario=? AND senha=?",
            (usuario, senha)
        ).fetchone()
        c.close()

        if not row or row["tipo"] != "admin":
            QMessageBox.warning(self, "Login", "Usuário ou senha inválidos.")
            self.campo_senha.clear()
            self.campo_senha.setFocus()
            return

        self.ao_logar(row["usuario"], row["tipo"])
        self.close()