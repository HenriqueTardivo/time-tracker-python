#!/usr/bin/env python3
import argparse
import sqlite3
import datetime

DB_FILE = "tarefas.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            inicio TEXT NOT NULL,
            fim TEXT
        )
    """)
    conn.commit()
    conn.close()

def start(nome):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Fecha qualquer tarefa aberta
    c.execute("UPDATE tarefas SET fim = ? WHERE fim IS NULL", (datetime.datetime.now().isoformat(),))
    # Inicia nova
    c.execute("INSERT INTO tarefas (nome, inicio) VALUES (?, ?)", (nome, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()
    print(f"⏱️ Tarefa '{nome}' iniciada.")

def stop():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, nome, inicio FROM tarefas WHERE fim IS NULL ORDER BY inicio DESC LIMIT 1")
    row = c.fetchone()
    if row:
        c.execute("UPDATE tarefas SET fim = ? WHERE id = ?", (datetime.datetime.now().isoformat(), row[0]))
        conn.commit()
        print(f"✅ Tarefa '{row[1]}' finalizada.")
    else:
        print("⚠️ Nenhuma tarefa em andamento.")
    conn.close()

def status():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT nome, inicio FROM tarefas WHERE fim IS NULL ORDER BY inicio DESC LIMIT 1")
    row = c.fetchone()
    if row:
        inicio = datetime.datetime.fromisoformat(row[1])
        duracao = datetime.datetime.now() - inicio
        print(f"⏳ Tarefa atual: '{row[0]}' (em andamento há {format_duration(duracao)})")
    else:
        print("⚠️ Nenhuma tarefa em andamento.")
    conn.close()

def format_duration(duration):
    """Formata uma duração no formato 'Xh Ym'."""
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours}h {minutes}m"

def report():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    hoje = datetime.datetime.now().date()
    c.execute("SELECT nome, inicio, fim FROM tarefas WHERE DATE(inicio) = ? ORDER BY inicio", (hoje,))
    rows = c.fetchall()
    total = datetime.timedelta()
    print(f"📅 Relatório de {hoje}:")
    for nome, inicio, fim in rows:
        inicio_dt = datetime.datetime.fromisoformat(inicio)
        fim_dt = datetime.datetime.fromisoformat(fim) if fim else datetime.datetime.now()
        duracao = fim_dt - inicio_dt
        total += duracao
        print(f"- {nome}: {format_duration(duracao)}")
    print(f"\n⏲️ Total do dia: {format_duration(total)}")
    conn.close()

def main():
    parser = argparse.ArgumentParser(description="⏱️ Controle de tempo de tarefas")
    subparsers = parser.add_subparsers(dest="comando")

    start_parser = subparsers.add_parser("start", help="Inicia uma nova tarefa")
    start_parser.add_argument("nome", help="Nome da tarefa")

    subparsers.add_parser("stop", help="Finaliza a tarefa atual")
    subparsers.add_parser("status", help="Mostra a tarefa atual")
    subparsers.add_parser("report", help="Mostra relatório das tarefas")

    args = parser.parse_args()

    init_db()

    if args.comando == "start":
        start(args.nome)
    elif args.comando == "stop":
        stop()
    elif args.comando == "status":
        status()
    elif args.comando == "report":
        report()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()