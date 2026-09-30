from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton,
    QMessageBox, QInputDialog
)
from banco.database import conectar


class TelaProdutosAdmin(QWidget):
    def __init__(self, parent=None, ao_voltar=None):
        super().__init__(parent)
        self.ao_voltar = ao_voltar

        layout = QVBoxLayout(self)

        # ---------- Cabeçalho ----------
        topo = QHBoxLayout()
        titulo = QLabel("Gerenciar produtos")
        titulo.setObjectName("secao")
        topo.addWidget(titulo)
        topo.addStretch()
        if self.ao_voltar:
            bt = QPushButton("← Voltar")
            bt.clicked.connect(self.ao_voltar)
            topo.addWidget(bt)
        layout.addLayout(topo)

        # ---------- Tabela ----------
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(5)
        self.tabela.setHorizontalHeaderLabels(
            ["ID", "Produto", "Categoria", "Preço", "Ativo"]
        )
        layout.addWidget(self.tabela)

        botoes = QHBoxLayout()
        alterar = QPushButton("Alterar preço")
        alterar.clicked.connect(self.alterar_preco)
        atualizar = QPushButton("Atualizar")
        atualizar.clicked.connect(self.carregar)
        botoes.addWidget(alterar)
        botoes.addWidget(atualizar)
        layout.addLayout(botoes)

        self.carregar()

    def carregar(self):
        c = conectar()
        rows = c.execute("""
            SELECT p.id, p.nome, c.nome AS categoria, p.preco, p.ativo
            FROM produtos p
            JOIN categorias c ON c.id = p.categoria_id
            ORDER BY c.nome, p.nome
        """).fetchall()
        c.close()

        self.tabela.setRowCount(len(rows))
        for i, row in enumerate(rows):
            valores = [
                row["id"],
                row["nome"],
                row["categoria"],
                f"R$ {row['preco']:.2f}",
                "Sim" if row["ativo"] else "Não",
            ]
            for j, val in enumerate(valores):
                self.tabela.setItem(i, j, QTableWidgetItem(str(val)))

    def alterar_preco(self):
        row = self.tabela.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Produto", "Selecione um produto.")
            return

        pid = int(self.tabela.item(row, 0).text())
        atual = (
            self.tabela.item(row, 3).text()
            .replace("R$ ", "")
            .replace(",", ".")
        )
        valor, ok = QInputDialog.getDouble(
            self, "Alterar preço", "Novo preço:",
            float(atual), 0, 100000, 2
        )
        if ok:
            c = conectar()
            c.execute("UPDATE produtos SET preco = ? WHERE id = ?", (valor, pid))
            c.commit()
            c.close()
            self.carregar()