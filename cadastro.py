import json
import os
import re  # Usado para validação de email com expressões regulares

ARQUIVO = "usuarios.json"

# Exibe o menu principal com as opções disponíveis
def exibir_menu():
    print("\n===== MENU =====")
    print("1 - Cadastrar novo usuário")
    print("2 - Listar usuários")
    print("3 - Alterar cadastro de usuário")
    print("4 - Excluir cadastro de usuário")
    print("5 - Pesquisar usuários (geral)")
    print("6 - Pesquisa avançada de usuários")
    print("7 - Sair")

# Carrega os usuários do arquivo JSON, se existir

def carregar_usuarios():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    else:
        return []

# Salva a lista de usuários no arquivo JSON

def salvar_usuarios(usuarios):
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)

# Verifica se o email possui um formato válido

def validar_email(email):
    padrao_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(padrao_email, email):
        return True
    return False

# Verifica se a idade é um número inteiro positivo

def validar_idade(idade):
    if idade.isdigit() and int(idade) > 0:
        return True
    return False

# Realiza o cadastro de um novo usuário com validações

def cadastrar_usuario(usuarios):
    print("\n--- Cadastro de Usuário ---")
    
    # Validando o nome (não pode ser vazio)
    while True:
        nome = input("Nome: ")
        if nome.strip():  # Verifica se não está vazio
            break
        print("Nome não pode ser vazio. Tente novamente.")
    
    # Validando o email
    while True:
        email = input("Email: ")
        # Verifica se o email já está cadastrado
        if any(usuario["email"] == email for usuario in usuarios):
            print("⚠️ Email já cadastrado. Tente novamente.")
        elif validar_email(email):
            break
        else:
            print("Email inválido. Tente novamente.")
    
    # Validando a idade
    while True:
        idade = input("Idade: ")
        if validar_idade(idade):
            break
        print("Idade inválida. Digite um número maior que zero.")
    
    usuario = {
        "nome": nome,
        "email": email,
        "idade": idade
    }

    usuarios.append(usuario)
    salvar_usuarios(usuarios)
    print("✅ Usuário cadastrado com sucesso!")

# Lista todos os usuários cadastrados

def listar_usuarios(usuarios):
    print("\n--- Lista de Usuários ---")
    if not usuarios:
        print("Nenhum usuário cadastrado.")
    else:
        for i, usuario in enumerate(usuarios, start=1):
            print(f"\nUsuário {i}:")
            print(f"Nome: {usuario['nome']}")
            print(f"Email: {usuario['email']}")
            print(f"Idade: {usuario['idade']}")

# Permite alterar os dados de um usuário existente

def alterar_usuario(usuarios):
    print("\n--- Alterar Cadastro de Usuário ---")

    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return

    listar_usuarios(usuarios)
    try:
        indice = int(input("\nDigite o número do usuário que deseja alterar: ")) - 1
        if 0 <= indice < len(usuarios):
            usuario = usuarios[indice]
            print(f"\nEditando o usuário: {usuario['nome']}")

            novo_nome = input(f"Novo nome (pressione Enter para manter '{usuario['nome']}'): ")
            novo_email = input(f"Novo email (pressione Enter para manter '{usuario['email']}'): ")
            nova_idade = input(f"Nova idade (pressione Enter para manter '{usuario['idade']}'): ")

            if novo_nome.strip():
                usuario['nome'] = novo_nome
            if novo_email.strip():
                if validar_email(novo_email):
                    usuario['email'] = novo_email
                else:
                    print("⚠️ Email inválido. Mantendo o email antigo.")
            if nova_idade.strip():
                if validar_idade(nova_idade):
                    usuario['idade'] = nova_idade
                else:
                    print("⚠️ Idade inválida. Mantendo a idade antiga.")

            salvar_usuarios(usuarios)
            print("✅ Usuário alterado com sucesso!")
        else:
            print("Índice inválido.")
    except ValueError:
        print("Entrada inválida. Digite um número.")

# Permite excluir um usuário da lista

def excluir_usuario(usuarios):
    print("\n--- Excluir Cadastro de Usuário ---")

    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return

    listar_usuarios(usuarios)

    try:
        indice = int(input("\nDigite o número do usuário que deseja excluir: ")) - 1
        if 0 <= indice < len(usuarios):
            usuario = usuarios[indice]
            confirmacao = input(f"Tem certeza que deseja excluir o usuário '{usuario['nome']}'? (s/n): ").lower()
            if confirmacao == 's':
                usuarios.pop(indice)
                salvar_usuarios(usuarios)
                print("✅ Usuário excluído com sucesso!")
            else:
                print("❌ Exclusão cancelada.")
        else:
            print("Índice inválido.")
    except ValueError:
        print("Entrada inválida. Digite um número.")

# Permite buscar usuários pelo nome ou email (busca parcial)

def pesquisar_usuarios(usuarios):
    print("\n--- Pesquisa Geral de Usuários ---")

    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return

    termo = input("Digite o nome ou email (ou parte deles) para buscar: ").lower()
    resultados = []

    for usuario in usuarios:
        if termo in usuario["nome"].lower() or termo in usuario["email"].lower():
            resultados.append(usuario)

    if resultados:
        print(f"\n🔎 {len(resultados)} resultado(s) encontrado(s):")
        for i, usuario in enumerate(resultados, start=1):
            print(f"\nUsuário {i}:")
            print(f"Nome: {usuario['nome']}")
            print(f"Email: {usuario['email']}")
            print(f"Idade: {usuario['idade']}")
    else:
        print("Nenhum usuário encontrado com esse termo.")

# Permite realizar buscas específicas por nome, email ou idade (exatos)

def pesquisa_avancada(usuarios):
    print("\n--- Pesquisa Avançada de Usuários ---")

    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return

    print("Pesquisar por:")
    print("1 - Nome exato")
    print("2 - Email exato")
    print("3 - Idade exata")
    opcao = input("Escolha uma opção: ")

    resultados = []

    if opcao == "1":
        nome = input("Digite o nome exato: ").strip().lower()
        resultados = [u for u in usuarios if u["nome"].lower() == nome]

    elif opcao == "2":
        email = input("Digite o email exato: ").strip().lower()
        resultados = [u for u in usuarios if u["email"].lower() == email]

    elif opcao == "3":
        idade = input("Digite a idade exata: ").strip()
        resultados = [u for u in usuarios if u["idade"] == idade]

    else:
        print("Opção inválida.")
        return

    if resultados:
        print(f"\n🔍 {len(resultados)} resultado(s) encontrado(s):")
        for i, usuario in enumerate(resultados, start=1):
            print(f"\nUsuário {i}:")
            print(f"Nome: {usuario['nome']}")
            print(f"Email: {usuario['email']}")
            print(f"Idade: {usuario['idade']}")
    else:
        print("Nenhum usuário encontrado com esse critério.")

# ==============================
# Parte principal do programa
# ==============================

usuarios = carregar_usuarios()

# Loop principal do sistema, exibe o menu e executa ações com base na escolha
while True:
    exibir_menu()
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cadastrar_usuario(usuarios)
    elif opcao == "2":
        listar_usuarios(usuarios)
    elif opcao == "3":
        alterar_usuario(usuarios)
    elif opcao == "4":
        excluir_usuario(usuarios)
    elif opcao == "5":
        pesquisar_usuarios(usuarios)
    elif opcao == "6":
        pesquisa_avancada(usuarios)
    elif opcao == "7":
        print("Encerrando o programa.")
        break
    else:
        print("Opção inválida. Tente novamente.")