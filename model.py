from datetime import datetime, timedelta, timezone
from banco import conectar, iniciar


def limpar_expiradas():
    with conectar() as con:
        con.execute("DELETE FROM reservas WHERE expira_em <= ?", (datetime.now(timezone.utc).isoformat(),))


def listar(termo=""):
    limpar_expiradas()
    with conectar() as con:
        return [dict(r) for r in con.execute("SELECT l.*, l.estoque - (SELECT COUNT(*) FROM reservas r WHERE r.livro_id=l.id) AS disponivel, (SELECT COUNT(*) FROM reservas r WHERE r.livro_id=l.id) AS reservado FROM livros l WHERE lower(l.titulo || ' ' || l.autor) LIKE lower(?) ORDER BY l.id", ('%'+termo+'%',)).fetchall()]


def reservas():
    limpar_expiradas()
    with conectar() as con:
        return [dict(r) for r in con.execute("SELECT l.titulo, r.livro_id, r.expira_em FROM reservas r JOIN livros l ON l.id=r.livro_id ORDER BY r.expira_em")]


def reservar(livro_id):
    limpar_expiradas()
    with conectar() as con:
        livro = con.execute("SELECT estoque FROM livros WHERE id=?", (livro_id,)).fetchone()
        if not livro:
            raise ValueError("Livro não encontrado.")
        if con.execute("SELECT 1 FROM reservas WHERE livro_id=?", (livro_id,)).fetchone():
            raise ValueError("Você já reservou esse livro.")
        if livro['estoque'] <= 0:
            raise ValueError("Livro indisponível.")
        expira = (datetime.now(timezone.utc)+timedelta(hours=24)).isoformat()
        con.execute("INSERT INTO reservas (livro_id,expira_em) VALUES (?,?)", (livro_id,expira))


def cancelar(livro_id):
    with conectar() as con:
        con.execute("DELETE FROM reservas WHERE livro_id=?", (livro_id,))
