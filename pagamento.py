from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox,
    QPushButton, QMessageBox, QApplication
)
from servicos.pedido_service import criar_pedido
from telas.pedido_confirmado import TelaPedidoConfirmado


class TelaPagamento(QWidget):
    def __init__(self, itens, total, cliente_nome="Cliente", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pagamento")
        self.resize(500, 480)
        self.itens = itens
        self.total = total
        self.cliente_nome = cliente_nome

        layout = QVBoxLayout(self)

        titulo = QLabel("PAGAMENTO")
        titulo.setObjectName("secao")
        layout.addWidget(titulo)

        layout.addWidget(QLabel(f"Cliente: {self.cliente_nome}"))
        layout.addWidget(QLabel(f"Valor do pedido: R$ {total:.2f}"))

        self.forma = QComboBox()
        self.forma.addItems(["PIX", "Cartão", "Dinheiro"])
        layout.addWidget(QLabel("Forma de pagamento:"))
        layout.addWidget(self.forma)

        confirmar = QPushButton("CONFIRMAR PAGAMENTO")
        confirmar.clicked.connect(self.finalizar)
        layout.addWidget(confirmar)

    def finalizar(self):
        try:
            numero, total = criar_pedido(
                self.itens,
                self.forma.currentText(),
                cliente_nome=self.cliente_nome
            )

            # Descobre se estamos no modo totem lendo o QApplication
            principal = getattr(QApplication.instance(), "principal", None)
            ao_finalizar = None
            if principal and getattr(principal, "modo_totem", False):
                ao_finalizar = principal.finalizar_pedido

            self.tela = TelaPedidoConfirmado(
                numero, total, self.cliente_nome,
                ao_finalizar=ao_finalizar
            )
            self.tela.show()
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))