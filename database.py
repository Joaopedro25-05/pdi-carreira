import sqlite3
from datetime import datetime

DB_NAME = "pdi_carreira.db"


def conectar():
    return sqlite3.connect(DB_NAME)


def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cargo_atual TEXT NOT NULL,
            objetivo TEXT NOT NULL,
            criado_em TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico_pdi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            competencias TEXT,
            dificuldades TEXT,
            certificacoes TEXT,
            resposta_ia TEXT,
            criado_em TEXT NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    """)

    conexao.commit()
    conexao.close()


def salvar_usuario(nome, cargo_atual, objetivo):
    conexao = conectar()
    cursor = conexao.cursor()

    criado_em = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO usuarios (nome, cargo_atual, objetivo, criado_em)
        VALUES (?, ?, ?, ?)
    """, (nome, cargo_atual, objetivo, criado_em))

    usuario_id = cursor.lastrowid

    conexao.commit()
    conexao.close()

    return usuario_id


def listar_usuarios():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, cargo_atual, objetivo, criado_em
        FROM usuarios
        ORDER BY id DESC
    """)

    usuarios = cursor.fetchall()

    conexao.close()

    return usuarios

def salvar_historico_pdi(usuario_id, competencias, dificuldades, certificacoes, resposta_ia):
    conexao = conectar()
    cursor = conexao.cursor()

    criado_em = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO historico_pdi (
            usuario_id,
            competencias,
            dificuldades,
            certificacoes,
            resposta_ia,
            criado_em
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        usuario_id,
        competencias,
        dificuldades,
        certificacoes,
        resposta_ia,
        criado_em
    ))

    conexao.commit()
    conexao.close()


def listar_historico_pdi():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT 
            h.id,
            u.nome,
            u.cargo_atual,
            h.competencias,
            h.dificuldades,
            h.certificacoes,
            h.resposta_ia,
            h.criado_em
        FROM historico_pdi h
        INNER JOIN usuarios u ON u.id = h.usuario_id
        ORDER BY h.id DESC
    """)

    historico = cursor.fetchall()

    conexao.close()

    return historico