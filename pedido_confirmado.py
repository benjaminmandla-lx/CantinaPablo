from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class TelaPedidoConfirmado(QWidget):
    def __init__(self, numero, total, cliente_nome="Cliente",
                 ao_finalizar=None, parent=None):
        super().__init__(parent)
        self.ao_finalizar = ao_finalizar

        self.setWindowTitle("Pedido confirmado")
        self.resize(500, 520)
        layout = QVBoxLayout(self)

        titulo = QLabel("PEDIDO CONFIRMADO!")
        titulo.setObjectName("titulo")
        layout.addWidget(titulo)

        saudacao = QLabel(f"Obrigado, {cliente_nome}!")
        saudacao.setObjectName("secao")
        layout.addWidget(saudacao)

        numero_label = QLabel(f"#{numero}")
        numero_label.setObjectName("pedido")
        layout.addWidget(numero_label)

        layout.addWidget(QLabel(f"Total pago: R$ {total:.2f}"))
        layout.addWidget(QLabel("Aguarde seu nome ser chamado quando estiver PRONTO."))

        layout.addSpacing(20)

        fechar = QPushButton("Finalizar")
        fechar.clicked.connect(self._finalizar)
        layout.addWidget(fechar)

    def _finalizar(self):
        if self.ao_finalizar:
            self.ao_finalizar()
        self.close()