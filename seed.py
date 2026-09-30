from banco.database import conectar

def cadastrar_categoria(cursor, nome):
    row = cursor.execute("SELECT id FROM categorias WHERE nome=?", (nome,)).fetchone()
    if row:
        return row["id"]
    cursor.execute("INSERT INTO categorias(nome) VALUES(?)", (nome,))
    return cursor.lastrowid

def cadastrar_produto(cursor, nome, categoria, preco, variacoes=None):
    categoria_id = cadastrar_categoria(cursor, categoria)
    row = cursor.execute(
        "SELECT id FROM produtos WHERE nome=? AND categoria_id=?",
        (nome, categoria_id)
    ).fetchone()
    if row:
        produto_id = row["id"]
    else:
        cursor.execute(
            "INSERT INTO produtos(nome,categoria_id,preco) VALUES(?,?,?)",
            (nome, categoria_id, preco)
        )
        produto_id = cursor.lastrowid

    for variacao in variacoes or []:
        cursor.execute(
            "INSERT OR IGNORE INTO variacoes(produto_id,nome) VALUES(?,?)",
            (produto_id, variacao)
        )

def popular_banco():
    c = conectar()
    cur = c.cursor()

    doces = [
        ("Doce", 3.00, []),
        ("Paçoca", 1.00, []),
        ("Bom bom", 2.50, ["Sonho de valsa", "Ouro branco"]),
        ("Trento", 4.50, ["Mousse de maracujá", "Torta de limão", "Dark", "Chocolate"]),
        ("Biscoito", 3.50, ["Chocolate", "Morango"]),
        ("Emilia", 2.50, []),
        ("Halls", 2.50, ["Extra forte (preto)", "Morango", "Menta", "Melancia"]),
        ("Bolo", 6.00, []),
        ("Suspiro", 3.00, []),
        ("Pão de mel", 5.00, []),
        ("Copinho de banana", 3.00, []),
        ("Cocada", 3.00, []),
        ("Doce em massa de batata doce", 3.00, []),
        ("Cajuzinho", 3.00, []),
        ("Geladão", 7.00, []),
        ("Cremosinho", 2.50, [
            "Morango", "Maracujá", "Leite condensado", "Coco", "Uva",
            "Kiwi", "Açaí com banana", "Frutas tropicais",
            "Frutas cristalizadas", "Manga"
        ]),
        ("Maria bolacha", 3.00, []),
    ]

    salgados = [
        ("Croissant de presunto e queijo", 7.00, []),
        ("Risole de 4 queijos", 5.50, []),
        ("Risole de carne", 5.50, []),
        ("Croissant 3 queijos", 6.50, []),
        ("Hambúrguer com cheddar", 7.00, []),
        ("Enroladinho de bauru", 7.00, []),
        ("Pão de batata com calabresa", 6.50, []),
        ("Pão de batata de frango", 6.50, []),
        ("Esfiha de carne", 7.00, []),
        ("Coxinha", 5.50, []),
        ("Pão de queijo", 3.50, []),
        ("Caldo", 20.00, ["Mandioca", "Abóbora", "Verde", "Feijão"]),
        ("Espeto", 9.00, ["Carne", "Medalhão", "Coração"]),
    ]

    bebidas = [
        ("Café", 2.00, []),
        ("Guaraná 350ml", 5.50, []),
        ("Fanta uva 350ml", 5.50, []),
        ("Fanta laranja 350ml", 5.50, []),
        ("Coca-Cola Zero 350ml", 5.50, []),
        ("Coca-Cola 350ml", 5.50, []),
        ("Suco Tropical 480ml", 8.00, ["Uva", "Manga", "Abacaxi", "Açaí", "Goiaba"]),
        ("Suco Kmais 300ml", 7.50, ["Goiaba", "Laranja", "Uva", "Maracujá"]),
        ("Refrigerante Caçula 200ml", 3.00, ["Coca-Cola", "Pepsi", "Fanta uva", "Coca-Cola Zero"]),
    ]

    outros = [
        ("Cup noodles", "Cup Noodles", 7.00,
         ["Cheddar", "Galinha caipira", "Queijo", "Bolonhesa"]),
        ("Chokito", "Doces", 2.00, []),
    ]

    for nome, preco, vars_ in doces:
        cadastrar_produto(cur, nome, "Doces", preco, vars_)
    for nome, preco, vars_ in salgados:
        cadastrar_produto(cur, nome, "Salgados", preco, vars_)
    for nome, preco, vars_ in bebidas:
        cadastrar_produto(cur, nome, "Bebidas", preco, vars_)
    for nome, categoria, preco, vars_ in outros:
        cadastrar_produto(cur, nome, categoria, preco, vars_)

    c.commit()
    c.close()
