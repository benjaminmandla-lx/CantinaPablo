from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton,
    QHeaderView, QMessageBox
)
from banco.database import conectar
from servicos.pedido_service import atualizar_status


class TelaEntrega(QWidget):
    def __init__(self, parent=None, ao_voltar=None):
        super().__init__(parent)
        self.ao_voltar = ao_voltar

        layout = QVBoxLayout(self)

        topo = QHBoxLayout()
        titulo = QLabel("Pedidos aguardando retirada")
        titulo.setObjectName("secao")
        topo.addWidget(titulo)
        topo.addStretch()

        atualizar = QPushButton("Atualizar")
        atualizar.clicked.connect(self.carregar)
        topo.addWidget(atualizar)

        if self.ao_voltar:
            bt = QPushButton("← Voltar")
            bt.clicked.connect(self.ao_voltar)
            topo.addWidget(bt)
        layout.addLayout(topo)

        self.tabela = QTableWidget()
        self.tabela.setColumnCount(4)
        self.tabela.setHorizontalHeaderLabels(
            ["Pedido", "Cliente", "Total", "Ação"]
        )
        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabela.verticalHeader().setVisible(False)
        self.tabela.verticalHeader().setDefaultSectionSize(42)

        header = self.tabela.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)

        layout.addWidget(self.tabela, stretch=1)
        self.carregar()

    def carregar(self):
        c = conectar()
        rows = c.execute("""
            SELECT * FROM pedidos
            WHERE status = 'AGUARDANDO RETIRADA'
            ORDER BY id
        """).fetchall()
        c.close()

        self.tabela.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.tabela.setItem(i, 0, QTableWidgetItem(f"#{row['numero']}"))
            self.tabela.setItem(i, 1, QTableWidgetItem(row["cliente_nome"]))
            self.tabela.setItem(i, 2, QTableWidgetItem(f"R$ {row['total']:.2f}"))

            celula = QWidget()
            celula_layout = QHBoxLayout(celula)
            celula_layout.setContentsMargins(0, 0, 0, 0)

            bt_entregar = QPushButton("Confirmar retirada")
            bt_entregar.clicked.connect(
                lambda checked=False, pid=row["id"]:
                self.entregar(pid)
            )
            celula_layout.addWidget(bt_entregar)

            bt_cancelar = QPushButton("Cancelar")
            bt_cancelar.setObjectName("botao_cancelar")
            bt_cancelar.clicked.connect(
                lambda checked=False, pid=row["id"], num=row["numero"]:
                self.cancelar(pid, num)
            )
            celula_layout.addWidget(bt_cancelar)

            self.tabela.setCellWidget(i, 3, celula)

    def entregar(self, pedido_id):
        atualizar_status(pedido_id, "ENTREGUE")
        self.carregar()

    def cancelar(self, pedido_id, numero):
        resposta = QMessageBox.question(
            self, "Cancelar pedido",
            f"Cancelar o pedido #{numero}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if resposta == QMessageBox.Yes:
            atualizar_status(pedido_id, "CANCELADO")
            self.carregar()