import sqlite3
from datetime import datetime

# ==========================================
# 🔹 CONEXÃO COM O BANCO DE DADOS (SQLite)
# ==========================================
def conectar():
    return sqlite3.connect("sistema_academico.db")

# ==========================================
# 🔹 CRIAÇÃO DAS TABELAS
# ==========================================
def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        turma TEXT NOT NULL,
        nota REAL CHECK (nota >= 0 AND nota <= 10),
        presencas INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS atividades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descricao TEXT,
        data_entrega TEXT
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Banco de dados inicializado com sucesso!\n")

# ==========================================
# 🔹 FUNÇÕES DE CADASTRO
# ==========================================
def cadastrar_aluno(nome, turma, nota):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO alunos (nome, turma, nota) VALUES (?, ?, ?)", (nome, turma, nota))
        conn.commit()
        print(f"✅ Aluno '{nome}' cadastrado com sucesso!\n")
    except Exception as e:
        print(f"❌ Erro ao cadastrar aluno: {e}")
    finally:
        conn.close()

def cadastrar_atividade(titulo, descricao, data_entrega):
    """Data em formato brasileiro: DD/MM/AAAA"""
    try:
        # Converte e valida a data
        data_formatada = datetime.strptime(data_entrega, "%d/%m/%Y")
        data_sql = data_formatada.strftime("%Y-%m-%d")  # salva no formato ISO no banco

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO atividades (titulo, descricao, data_entrega) VALUES (?, ?, ?)",
                       (titulo, descricao, data_sql))
        conn.commit()
        print(f"✅ Atividade '{titulo}' cadastrada com sucesso!\n")
    except ValueError:
        print("⚠️ Data inválida! Use o formato DD/MM/AAAA.\n")
    except Exception as e:
        print(f"❌ Erro ao cadastrar atividade: {e}")
    finally:
        conn.close()

# ==========================================
# 🔹 FUNÇÕES DE BUSCA
# ==========================================
def buscar_alunos(ordem="nome"):
    try:
        if ordem not in ["nome", "nota", "turma"]:
            print("⚠️ Opção inválida! Ordenando por nome.\n")
            ordem = "nome"

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM alunos ORDER BY {ordem}")
        alunos = cursor.fetchall()
        conn.close()

        if not alunos:
            print("📭 Nenhum aluno cadastrado.\n")
        else:
            print("\n📋 LISTA DE ALUNOS:")
            print("-" * 50)
            for a in alunos:
                print(f"ID: {a[0]} | Nome: {a[1]} | Turma: {a[2]} | Nota: {a[3]} | Presenças: {a[4]}")
            print("-" * 50 + "\n")
    except Exception as e:
        print(f"❌ Erro ao buscar alunos: {e}")

def buscar_atividades():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM atividades ORDER BY data_entrega")
        atividades = cursor.fetchall()
        conn.close()

        if not atividades:
            print("📭 Nenhuma atividade cadastrada.\n")
        else:
            print("\n🗓️ LISTA DE ATIVIDADES:")
            print("-" * 50)
            for a in atividades:
                # converte a data para formato brasileiro ao exibir
                try:
                    data_formatada = datetime.strptime(a[3], "%Y-%m-%d").strftime("%d/%m/%Y")
                except:
                    data_formatada = a[3]
                print(f"ID: {a[0]} | Título: {a[1]} | Entrega: {data_formatada} | Descrição: {a[2]}")
            print("-" * 50 + "\n")
    except Exception as e:
        print(f"❌ Erro ao buscar atividades: {e}")

# ==========================================
# 🔹 REGISTRO DE PRESENÇA
# ==========================================
def registrar_presenca(id_aluno):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE alunos SET presencas = presencas + 1 WHERE id = ?", (id_aluno,))
        if cursor.rowcount == 0:
            print("⚠️ Aluno não encontrado!\n")
        else:
            conn.commit()
            print("✅ Presença registrada com sucesso!\n")
    except Exception as e:
        print(f"❌ Erro ao registrar presença: {e}")
    finally:
        conn.close()

# ==========================================
# 🔹 RELATÓRIOS AUTOMÁTICOS
# ==========================================
def relatorio_notas():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT turma, AVG(nota) FROM alunos GROUP BY turma")
        relatorio = cursor.fetchall()
        conn.close()

        if not relatorio:
            print("📭 Nenhum dado de notas disponível.\n")
        else:
            print("\n📊 MÉDIA DE NOTAS POR TURMA:")
            print("-" * 40)
            for turma, media in relatorio:
                print(f"Turma: {turma} | Média: {media:.2f}")
            print("-" * 40 + "\n")
    except Exception as e:
        print(f"❌ Erro ao gerar relatório de notas: {e}")

def relatorio_presenca():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT turma, SUM(presencas) FROM alunos GROUP BY turma")
        relatorio = cursor.fetchall()
        conn.close()

        if not relatorio:
            print("📭 Nenhum dado de presença disponível.\n")
        else:
            print("\n👥 RELATÓRIO DE PRESENÇAS POR TURMA:")
            print("-" * 40)
            for turma, total in relatorio:
                print(f"Turma: {turma} | Total de presenças: {total}")
            print("-" * 40 + "\n")
    except Exception as e:
        print(f"❌ Erro ao gerar relatório de presença: {e}")

# ==========================================
# 🔹 MENU INTERATIVO
# ==========================================
def menu():
    criar_tabelas()

    while True:
        print("""
==============================
   🎓 SISTEMA ACADÊMICO UNIP
==============================
1. Cadastrar aluno
2. Cadastrar atividade
3. Listar alunos
4. Listar atividades
5. Registrar presença
6. Relatório de notas
7. Relatório de presença
0. Sair
""")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome = input("Nome do aluno: ").strip()
            turma = input("Turma: ").strip()
            try:
                nota = float(input("Nota (0 a 10): "))
                if 0 <= nota <= 10:
                    cadastrar_aluno(nome, turma, nota)
                else:
                    print("⚠️ A nota deve estar entre 0 e 10.\n")
            except ValueError:
                print("⚠️ Digite uma nota válida!\n")

        elif opcao == "2":
            titulo = input("Título da atividade: ").strip()
            descricao = input("Descrição: ").strip()
            data_entrega = input("Data de entrega (DD/MM/AAAA): ").strip()
            cadastrar_atividade(titulo, descricao, data_entrega)

        elif opcao == "3":
            ordem = input("Ordenar por (nome, nota, turma): ").strip().lower()
            buscar_alunos(ordem)

        elif opcao == "4":
            buscar_atividades()

        elif opcao == "5":
            try:
                id_aluno = int(input("ID do aluno: "))
                registrar_presenca(id_aluno)
            except ValueError:
                print("⚠️ ID inválido! Use apenas números.\n")

        elif opcao == "6":
            relatorio_notas()

        elif opcao == "7":
            relatorio_presenca()

        elif opcao == "0":
            print("👋 Saindo do sistema... Até logo!")
            break

        else:
            print("⚠️ Opção inválida, tente novamente!\n")

# ==========================================
# 🔹 EXECUÇÃO
# ==========================================
if __name__ == "__main__":
    menu()
