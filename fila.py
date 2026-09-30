from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton,
    QHeaderView
)
from banco.database import conectar


class TelaFila(QWidget):
    def __init__(self, parent=None, ao_voltar=None):
        super().__init__(parent)
        self.ao_voltar = ao_voltar

        layout = QVBoxLayout(self)

        topo = QHBoxLayout()
        titulo = QLabel("Fila de pedidos")
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
        self.tabela.setColumnCount(5)
        self.tabela.setHorizontalHeaderLabels(
            ["Pedido", "Cliente", "Data", "Status", "Total"]
        )
        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabela.verticalHeader().setVisible(False)
        self.tabela.verticalHeader().setDefaultSectionSize(34)

        header = self.tabela.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)

        layout.addWidget(self.tabela, stretch=1)
        self.carregar()

    def carregar(self):
        c = conectar()
        rows = c.execute("""
            SELECT numero, cliente_nome, data, status, total
            FROM pedidos
            ORDER BY id DESC
        """).fetchall()
        c.close()

        self.tabela.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.tabela.setItem(i, 0, QTableWidgetItem(f"#{row['numero']}"))
            self.tabela.setItem(i, 1, QTableWidgetItem(row["cliente_nome"]))
            self.tabela.setItem(i, 2, QTableWidgetItem(row["data"]))
            self.tabela.setItem(i, 3, QTableWidgetItem(row["status"]))
            self.tabela.setItem(i, 4, QTableWidgetItem(f"R$ {row['total']:.2f}"))