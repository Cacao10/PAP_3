"""
database.py
Ligação à base de dados MariaDB e operações CRUD para simulações.
"""
import mysql.connector

DB_CONFIG = {
    "host":     "localhost",
    "port":     3306,
    "user":     "root",
    "password": "herman",
    "database": "fibra",
}

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS simulacoes (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    nome          VARCHAR(120)  NOT NULL,
    fibra         VARCHAR(80)   NOT NULL,
    distancia_km  DOUBLE        NOT NULL,
    potencia_mw   DOUBLE        NOT NULL,
    perda_pct     DOUBLE        NOT NULL,
    qualidade     VARCHAR(20)   NOT NULL,
    criado_em     DATETIME      DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(CREATE_TABLE_SQL)
    conn.commit()
    cur.close()
    conn.close()


def save_simulation(nome: str, fibra: str, distancia: float,
                    potencia_mw: float, perda_pct: float, qualidade: str) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO simulacoes (nome, fibra, distancia_km, potencia_mw, perda_pct, qualidade) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (nome, fibra, distancia, potencia_mw, perda_pct, qualidade)
    )
    conn.commit()
    new_id = cur.lastrowid
    cur.close()
    conn.close()
    return new_id


def load_all_simulations() -> list:
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM simulacoes ORDER BY criado_em DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def delete_simulation(sim_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM simulacoes WHERE id = %s", (sim_id,))
    conn.commit()
    cur.close()
    conn.close()
