from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton,
    QHeaderView
)
from banco.database import conectar


class TelaMeusPedidos(QWidget):
    def __init__(self, parent=None, ao_voltar=None, nome_usuario=None):
        super().__init__(parent)
        self.ao_voltar = ao_voltar
        self.nome_usuario = nome_usuario or "Cliente"

        layout = QVBoxLayout(self)

        topo = QHBoxLayout()
        titulo = QLabel(f"Meus pedidos — {self.nome_usuario}")
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
            ["Pedido", "Data", "Status", "Total"]
        )
        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabela.verticalHeader().setVisible(False)
        self.tabela.verticalHeader().setDefaultSectionSize(34)

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
            SELECT numero, data, status, total
            FROM pedidos
            WHERE cliente_nome = ?
            ORDER BY id DESC
        """, (self.nome_usuario,)).fetchall()
        c.close()

        self.tabela.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.tabela.setItem(i, 0, QTableWidgetItem(f"#{row['numero']}"))
            self.tabela.setItem(i, 1, QTableWidgetItem(row["data"]))
            self.tabela.setItem(i, 2, QTableWidgetItem(row["status"]))
            self.tabela.setItem(i, 3, QTableWidgetItem(f"R$ {row['total']:.2f}"))