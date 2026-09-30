from datetime import datetime
from banco.database import conectar


def proximo_numero(cur):
    row = cur.execute("SELECT MAX(numero) AS n FROM pedidos").fetchone()
    return (row["n"] or 0) + 1


def criar_pedido(itens, forma_pagamento, cliente_nome="Cliente"):
    """
    itens: lista de dicts:
      produto_id, variacao_id, quantidade, preco_unitario
    cliente_nome: nome informado pelo cliente
    """
    if not itens:
        raise ValueError("O carrinho está vazio.")

    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = sum(i["quantidade"] * i["preco_unitario"] for i in itens)

    c = conectar()
    cur = c.cursor()
    numero = proximo_numero(cur)

    cur.execute(
        "INSERT INTO pedidos(numero,data,status,total,cliente_nome) VALUES(?,?,?,?,?)",
        (numero, agora, "RECEBIDO", total, cliente_nome)
    )
    pedido_id = cur.lastrowid

    for item in itens:
        subtotal = item["quantidade"] * item["preco_unitario"]
        cur.execute("""
            INSERT INTO itens_pedido
            (pedido_id,produto_id,variacao_id,quantidade,preco_unitario,subtotal)
            VALUES(?,?,?,?,?,?)
        """, (
            pedido_id,
            item["produto_id"],
            item.get("variacao_id"),
            item["quantidade"],
            item["preco_unitario"],
            subtotal
        ))

    cur.execute("""
        INSERT INTO pagamentos
        (pedido_id,forma_pagamento,valor,status,data)
        VALUES(?,?,?,?,?)
    """, (pedido_id, forma_pagamento, total, "PAGO", agora))

    c.commit()
    c.close()
    return numero, total


def atualizar_status(pedido_id, novo_status):
    c = conectar()
    c.execute("UPDATE pedidos SET status=? WHERE id=?", (novo_status, pedido_id))
    c.commit()
    c.close()