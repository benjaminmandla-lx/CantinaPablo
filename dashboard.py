from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QGridLayout, QPushButton
)
from servicos.financeiro_service import resumo_financeiro


class TelaDashboard(QWidget):
    def __init__(self, parent=None, ao_voltar=None):
        super().__init__(parent)
        self.ao_voltar = ao_voltar

        layout = QVBoxLayout(self)

        # ---------- Cabeçalho ----------
        topo = QHBoxLayout()
        titulo = QLabel("Dashboard da cantina")
        titulo.setObjectName("secao")
        topo.addWidget(titulo)
        topo.addStretch()
        if self.ao_voltar:
            bt = QPushButton("← Voltar")
            bt.clicked.connect(self.ao_voltar)
            topo.addWidget(bt)
        layout.addLayout(topo)

        # ---------- Grid de indicadores ----------
        self.grid = QGridLayout()
        layout.addLayout(self.grid)

        atualizar = QPushButton("Atualizar indicadores")
        atualizar.clicked.connect(self.carregar)
        layout.addWidget(atualizar)

        self.carregar()

    def carregar(self):
        receita, despesa, saldo, pedidos = resumo_financeiro()

        # Limpa o grid antes de repovoar
        for i in reversed(range(self.grid.count())):
            item = self.grid.takeAt(i)
            if item.widget():
                item.widget().deleteLater()

        dados = [
            ("Receita", f"R$ {receita:.2f}"),
            ("Despesas", f"R$ {despesa:.2f}"),
            ("Saldo", f"R$ {saldo:.2f}"),
            ("Pedidos", str(pedidos)),
        ]

        for i, (rotulo, valor) in enumerate(dados):
            box = QLabel(f"{rotulo}\n\n{valor}")
            box.setObjectName("indicador")
            self.grid.addWidget(box, i // 2, i % 2)