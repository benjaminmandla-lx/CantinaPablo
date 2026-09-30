from banco.database import conectar

def listar_categorias():
    c = conectar()
    rows = c.execute("SELECT * FROM categorias ORDER BY nome").fetchall()
    c.close()
    return rows

def listar_produtos():
    c = conectar()
    rows = c.execute("""
        SELECT p.id,p.nome,p.preco,p.ativo,c.nome AS categoria
        FROM produtos p
        JOIN categorias c ON c.id=p.categoria_id
        ORDER BY c.nome,p.nome
    """).fetchall()
    c.close()
    return rows
