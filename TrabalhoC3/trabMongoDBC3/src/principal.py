from utils import config
from utils.splash_screen import SplashScreen
from reports.relatorios import Relatorio
from controller.controller_paciente import Controller_Paciente
from controller.controller_profissional import Controller_Profissional
from controller.controller_agendamento import Controller_Agendamento

tela_inicial = SplashScreen()
relatorio = Relatorio()
ctrl_paciente = Controller_Paciente()
ctrl_profissional = Controller_Profissional()
ctrl_agendamento = Controller_Agendamento()

def reports(opcao_relatorio:int=0):

    if opcao_relatorio == 1:
        relatorio.get_relatorio_agendamentos()
    elif opcao_relatorio == 2:
        relatorio.get_relatorio_pacientes()
    elif opcao_relatorio == 3:
        relatorio.get_relatorio_profissionais()

def inserir(opcao_inserir:int=0):

    if opcao_inserir == 1:                               
        novo_paciente = ctrl_paciente.inserir_paciente()
    elif opcao_inserir == 2:
        novo_profissional = ctrl_profissional.inserir_profissional()
    elif opcao_inserir == 3:
        novo_agendamento = ctrl_agendamento.inserir_agendamento()

def atualizar(opcao_atualizar:int=0):

    if opcao_atualizar == 1:
        relatorio.get_relatorio_pacientes()
        paciente_atualizado = ctrl_paciente.atualizar_paciente()
    elif opcao_atualizar == 2:
        relatorio.get_relatorio_profissionais()
        profissional_atualizado = ctrl_profissional.atualizar_profissional()
    elif opcao_atualizar == 3:
        relatorio.get_relatorio_agendamentos()
        agendamento_atualizado = ctrl_agendamento.atualizar_agendamento()

def excluir(opcao_excluir:int=0):

    if opcao_excluir == 1:
        relatorio.get_relatorio_pacientes()
        ctrl_paciente.excluir_paciente()
    elif opcao_excluir == 2:                
        relatorio.get_relatorio_profissionais()
        ctrl_profissional.excluir_profissional()
    elif opcao_excluir == 3:                
        relatorio.get_relatorio_agendamentos()
        ctrl_agendamento.excluir_agendamento()

def run():
    print(tela_inicial.get_updated_screen())
    config.clear_console()

    while True:
        print(config.MENU_PRINCIPAL)
        opcao = int(input("Escolha uma opção [1-5]: "))
        config.clear_console(1)
        
        if opcao == 1: # Relatórios
            
            print(config.MENU_RELATORIOS)
            opcao_relatorio = int(input("Escolha uma opção [0-3]: "))
            config.clear_console(1)

            reports(opcao_relatorio)

            config.clear_console(1)

        elif opcao == 2: # Inserir Novos Registros
            
            print(config.MENU_ENTIDADES)
            opcao_inserir = int(input("Escolha uma opção [1-3]: "))
            config.clear_console(1)

            inserir(opcao_inserir=opcao_inserir)

            config.clear_console()
            print(tela_inicial.get_updated_screen())
            config.clear_console()

        elif opcao == 3: # Atualizar Registros

            print(config.MENU_ENTIDADES)
            opcao_atualizar = int(input("Escolha uma opção [1-3]: "))
            config.clear_console(1)

            atualizar(opcao_atualizar=opcao_atualizar)

            config.clear_console()

        elif opcao == 4:

            print(config.MENU_ENTIDADES)
            opcao_excluir = int(input("Escolha uma opção [1-3]: "))
            config.clear_console(1)

            excluir(opcao_excluir=opcao_excluir)

            config.clear_console()
            print(tela_inicial.get_updated_screen())
            config.clear_console()

        elif opcao == 5:

            print(tela_inicial.get_updated_screen())
            config.clear_console()
            print("Obrigado por utilizar o nosso sistema.")
            exit(0)

        else:
            print("Opção incorreta.")
            exit(1)

if __name__ == "__main__":
    run()