from banco.database import conectar

def resumo_financeiro():
    c = conectar()
    receita = c.execute(
        "SELECT COALESCE(SUM(valor),0) AS total FROM pagamentos WHERE status='PAGO'"
    ).fetchone()["total"]
    despesa = c.execute(
        "SELECT COALESCE(SUM(valor),0) AS total FROM despesas"
    ).fetchone()["total"]
    pedidos = c.execute("SELECT COUNT(*) AS total FROM pedidos").fetchone()["total"]
    c.close()
    return receita, despesa, receita - despesa, pedidos

def adicionar_despesa(descricao, categoria, valor):
    from datetime import datetime
    c = conectar()
    c.execute(
        "INSERT INTO despesas(descricao,categoria,valor,data) VALUES(?,?,?,?)",
        (descricao, categoria, valor, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    c.commit()
    c.close()
