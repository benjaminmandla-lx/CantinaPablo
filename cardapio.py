from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QSpinBox, QGroupBox, QScrollArea, QMessageBox
)
from banco.database import conectar
from telas.carrinho import TelaCarrinho


class TelaCardapio(QWidget):
    def __init__(self, parent=None, ao_voltar=None, cliente_nome="Cliente"):
        super().__init__(parent)
        self.carrinho = []
        self.ao_voltar = ao_voltar
        self.cliente_nome = cliente_nome

        root = QVBoxLayout(self)

        # ---------- Cabeçalho ----------
        topo = QHBoxLayout()
        titulo = QLabel("CARDÁPIO")
        titulo.setObjectName("secao")
        topo.addWidget(titulo)
        topo.addStretch()

        if self.cliente_nome:
            nome_label = QLabel(f"Olá, {self.cliente_nome}!")
            nome_label.setObjectName("secao")
            topo.addWidget(nome_label)

        if self.ao_voltar:
            bt_voltar = QPushButton("← Voltar")
            bt_voltar.clicked.connect(self.ao_voltar)
            topo.addWidget(bt_voltar)

        root.addLayout(topo)
        root.addSpacing(15)

        # ---------- Lista de produtos ----------
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        container = QWidget()
        self.lista = QVBoxLayout(container)
        self.lista.setSpacing(10)
        self.lista.setContentsMargins(10, 10, 10, 10)

        c = conectar()
        produtos = c.execute("""
            SELECT p.*, c.nome AS categoria
            FROM produtos p
            JOIN categorias c ON c.id = p.categoria_id
            WHERE p.ativo = 1
            ORDER BY c.nome, p.nome
        """).fetchall()

        variacoes_por_produto = {}
        for p in produtos:
            variacoes_por_produto[p["id"]] = []
        if produtos:
            ids = ",".join(str(p["id"]) for p in produtos)
            variacoes = c.execute(
                f"SELECT * FROM variacoes WHERE produto_id IN ({ids}) ORDER BY nome"
            ).fetchall()
            for v in variacoes:
                variacoes_por_produto[v["produto_id"]].append(v)
        c.close()

        categoria_atual = None
        for p in produtos:
            if p["categoria"] != categoria_atual:
                categoria_atual = p["categoria"]
                label = QLabel(categoria_atual.upper())
                label.setObjectName("categoria")
                self.lista.addWidget(label)

            box = QGroupBox()
            linha = QHBoxLayout(box)

            info = QLabel(f"{p['nome']}  —  R$ {p['preco']:.2f}")
            linha.addWidget(info)
            linha.addStretch()

            variacoes = variacoes_por_produto.get(p["id"], [])
            combo = None
            if variacoes:
                combo = QComboBox()
                combo.addItem("Escolha uma opção")
                for v in variacoes:
                    combo.addItem(v["nome"], v["id"])
                linha.addWidget(combo)

            qtd = QSpinBox()
            qtd.setRange(1, 20)
            qtd.setValue(1)
            linha.addWidget(qtd)

            botao = QPushButton("Adicionar")
            linha.addWidget(botao)

            botao.clicked.connect(
                lambda checked=False, p=p, combo=combo, qtd=qtd:
                self.adicionar(p, combo, qtd)
            )
            self.lista.addWidget(box)

        self.lista.addStretch()
        self.scroll.setWidget(container)
        root.addWidget(self.scroll)

        # ---------- Rodapé ----------
        rodape = QHBoxLayout()
        self.total_label = QLabel("Itens no carrinho: 0")
        rodape.addWidget(self.total_label)
        rodape.addStretch()

        ver = QPushButton("Ver carrinho")
        ver.clicked.connect(self.abrir_carrinho)
        rodape.addWidget(ver)

        root.addLayout(rodape)

    def adicionar(self, produto, combo, qtd):
        variacao_id = None
        variacao_nome = ""

        if combo:
            if combo.currentIndex() == 0:
                QMessageBox.warning(self, "Variação", "Escolha uma opção do produto.")
                return
            variacao_id = combo.currentData()
            variacao_nome = combo.currentText()

        self.carrinho.append({
            "produto_id": produto["id"],
            "nome": produto["nome"],
            "variacao_id": variacao_id,
            "variacao_nome": variacao_nome,
            "quantidade": qtd.value(),
            "preco_unitario": produto["preco"],
        })
        self.total_label.setText(
            f"Itens no carrinho: {sum(x['quantidade'] for x in self.carrinho)}"
        )

    def abrir_carrinho(self):
        self.tela_carrinho = TelaCarrinho(
            self.carrinho,
            cliente_nome=self.cliente_nome
        )
        self.tela_carrinho.show()