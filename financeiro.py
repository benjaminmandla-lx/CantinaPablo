from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QComboBox, QDoubleSpinBox, QPushButton,
    QTableWidget, QTableWidgetItem
)
from banco.database import conectar
from servicos.financeiro_service import adicionar_despesa


class TelaFinanceiro(QWidget):
    def __init__(self, parent=None, ao_voltar=None):
        super().__init__(parent)
        self.ao_voltar = ao_voltar

        layout = QVBoxLayout(self)

        # ---------- Cabeçalho ----------
        topo = QHBoxLayout()
        titulo = QLabel("Controle financeiro")
        titulo.setObjectName("secao")
        topo.addWidget(titulo)
        topo.addStretch()
        if self.ao_voltar:
            bt = QPushButton("← Voltar")
            bt.clicked.connect(self.ao_voltar)
            topo.addWidget(bt)
        layout.addLayout(topo)

        # ---------- Formulário ----------
        form = QHBoxLayout()
        self.descricao = QLineEdit()
        self.descricao.setPlaceholderText("Descrição")

        self.categoria = QComboBox()
        self.categoria.addItems(
            ["Ingredientes", "Materiais", "Manutenção", "Outros"]
        )

        self.valor = QDoubleSpinBox()
        self.valor.setRange(0, 1_000_000)
        self.valor.setDecimals(2)
        self.valor.setPrefix("R$ ")

        adicionar = QPushButton("Adicionar despesa")
        adicionar.clicked.connect(self.salvar_despesa)

        form.addWidget(self.descricao)
        form.addWidget(self.categoria)
        form.addWidget(self.valor)
        form.addWidget(adicionar)
        layout.addLayout(form)

        # ---------- Tabela ----------
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(4)
        self.tabela.setHorizontalHeaderLabels(
            ["Descrição", "Categoria", "Valor", "Data"]
        )
        layout.addWidget(self.tabela)

        self.carregar()

    def salvar_despesa(self):
        if not self.descricao.text().strip() or self.valor.value() <= 0:
            return
        adicionar_despesa(
            self.descricao.text().strip(),
            self.categoria.currentText(),
            self.valor.value(),
        )
        self.descricao.clear()
        self.valor.setValue(0)
        self.carregar()

    def carregar(self):
        c = conectar()
        rows = c.execute(
            "SELECT * FROM despesas ORDER BY id DESC"
        ).fetchall()
        c.close()

        self.tabela.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self.tabela.setItem(i, 0, QTableWidgetItem(row["descricao"]))
            self.tabela.setItem(i, 1, QTableWidgetItem(row["categoria"] or ""))
            self.tabela.setItem(i, 2, QTableWidgetItem(f"R$ {row['valor']:.2f}"))
            self.tabela.setItem(i, 3, QTableWidgetItem(row["data"]))