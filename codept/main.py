import json
import os

# Função para verificar e instalar as dependências necessárias
def verificar_instalar_dependencias():
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        print("Bibliotecas necessárias não encontradas.")
        choice = input("Deseja instalar as bibliotecas necessárias? (s/n): ").strip().lower()
        if choice == 's':
            os.system('pip install -r requirements.txt')
        else:
            print("Instalação cancelada. O programa pode não funcionar corretamente.")
            input("\nPressione Enter para continuar...")
            return False
    return True

def modificar_config(opcao):
    # Abrir o arquivo config.json e modificar a opção "cortar_logomarca"
    try:
        with open('code/config.json', 'r+') as f:
            config = json.load(f)
            if opcao == 1:
                # Trocar o valor entre True e False
                config['cortar_logomarca'] = not config.get('cortar_logomarca', False)
                f.seek(0)  # Mover o cursor para o início do arquivo
                json.dump(config, f, indent=4)
                f.truncate()  # Truncar qualquer conteúdo que possa estar além deste ponto
            elif opcao == 2:
                pass  # Nenhuma modificação para a opção 2 neste exemplo
            else:
                print("Opção inválida.")
                return False
    except FileNotFoundError:
        print("Arquivo config.json não encontrado.")
        return False
    return True

def limpar_console():
    # Limpar o console (funciona em sistemas Unix e Windows)
    os.system('cls' if os.name == 'nt' else 'clear')

def carregar_script():
    # Executar o script code/main.py
    try:
        os.system('python code/main.py')
    except FileNotFoundError:
        print("Script code/main.py não encontrado.")

def main():
    # Verificar e instalar as dependências necessárias
    if not verificar_instalar_dependencias():
        return

    # Carregar o estado atual de cortar_logomarca do config.json
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            cortar_logomarca = config.get('cortar_logomarca', False)
    except FileNotFoundError:
        print("Arquivo config.json não encontrado.")
        return

    while True:
        # Determinar o texto para exibir com base no estado atual de cortar_logomarca
        if cortar_logomarca:
            estado_logo = "ativada"
        else:
            estado_logo = "desativada"

        print("Ifunny Downloader\n")
        print("Este script permite baixar posts do site iFunny.co, podendo baixar posts individuais ou vários posts sequencialmente\n")
        print(f"1. Remoção de logo do Ifunny: {estado_logo}")
        print("2. Desejo baixar posts do Ifunny\n")
        opcao = input("Digite a opção: ")

        if opcao == '1':
            if modificar_config(1):
                cortar_logomarca = not cortar_logomarca  # Atualizar o estado após a modificação
                limpar_console()
                continue
        elif opcao == '2':
            limpar_console()
            carregar_script()
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
