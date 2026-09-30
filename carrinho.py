from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QListWidget, QMessageBox
)
from telas.pagamento import TelaPagamento


class TelaCarrinho(QWidget):
    def __init__(self, itens, cliente_nome="Cliente", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Carrinho")
        self.resize(650, 550)
        self.itens = itens
        self.cliente_nome = cliente_nome

        layout = QVBoxLayout(self)

        titulo = QLabel("SEU PEDIDO")
        titulo.setObjectName("secao")
        layout.addWidget(titulo)

        nome_label = QLabel(f"Cliente: {self.cliente_nome}")
        layout.addWidget(nome_label)

        self.lista = QListWidget()
        total = 0
        for item in self.itens:
            subtotal = item["quantidade"] * item["preco_unitario"]
            total += subtotal
            variacao = f" — {item['variacao_nome']}" if item["variacao_nome"] else ""
            self.lista.addItem(
                f"{item['quantidade']}x {item['nome']}{variacao} | R$ {subtotal:.2f}"
            )
        layout.addWidget(self.lista)

        self.total = total
        label = QLabel(f"TOTAL: R$ {total:.2f}")
        label.setObjectName("total")
        layout.addWidget(label)

        botoes = QHBoxLayout()
        voltar = QPushButton("Voltar")
        voltar.clicked.connect(self.close)
        confirmar = QPushButton("Continuar para pagamento")
        confirmar.clicked.connect(self.pagamento)
        botoes.addWidget(voltar)
        botoes.addWidget(confirmar)
        layout.addLayout(botoes)

    def pagamento(self):
        if not self.itens:
            QMessageBox.warning(self, "Carrinho", "O carrinho está vazio.")
            return
        self.tela = TelaPagamento(
            self.itens,
            self.total,
            cliente_nome=self.cliente_nome
        )
        self.tela.show()
        self.close()