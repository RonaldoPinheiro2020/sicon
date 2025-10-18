import customtkinter as ctk
import os

# Importa as telas da pasta ui
from ui.login_page import LoginPage
from ui.home_page import HomePage
from ui.create_user_page import CreateUserPage

class MainApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        
        # --- CORREÇÃO DO VALUEROR: CONSUMIR ARGUMENTOS PERSONALIZADOS ---
        # 1. Extrai os argumentos personalizados do kwargs para que não sejam repassados 
        # para a classe pai (ctk.CTk), que não os suporta.
        self.system_name = kwargs.pop("system_name", "App Padrão")
        self.system_version = kwargs.pop("system_version", "0.0.0") 
        self.creation_year = kwargs.pop("creation_year", "2024")
        
        # 2. Chama o __init__ da classe pai SOMENTE com argumentos que ela suporta.
        super().__init__(*args, **kwargs)
        # --- FIM DA CORREÇÃO ---
        
        # --- Definições Globais do Sistema (SemVer) ---
        # Estas linhas foram movidas e agora são definidas pelo kwargs.pop() acima.
        # Mantendo-as aqui, você pode definir valores padrão caso o app seja chamado sem argumentos.
        # Se você quer garantir que os valores passados na chamada sejam usados, 
        # esta redefinição é desnecessária se os valores padrão acima forem suficientes.
        # Deixarei apenas a lógica do kwargs.pop para usar os valores passados na inicialização.
        
        self.title(self.system_name)
        self.geometry("800x600")
        self.resizable(False, False)

        # --- CONTAINER ---
        # Container para as telas
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        # Adiciona todas as telas ao dicionário de frames
        for F in (LoginPage, HomePage, CreateUserPage):
            page_name = F.__name__
            # Passa os atributos do sistema (agora definidos no self) para as telas
            frame = F(parent=self.container, controller=self,
                      system_name=self.system_name,
                      system_version=self.system_version,
                      creation_year=self.creation_year)
            
            self.frames[page_name] = frame
            
            frame.grid(row=0, column=0, sticky="nsew")

        # Exibe a tela de login ao iniciar
        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        """
        Mostra a tela selecionada.
        """
        frame = self.frames[page_name]
        frame.tkraise()

        if page_name == "HomePage":
            frame.update_user_info()

if __name__ == "__main__":
    # Define o tema para "branco gelo"
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("green") # Exemplo: Pode usar "blue", "green" ou um tema personalizado
    
    # --- CORREÇÃO DA DUPLICAÇÃO ---
    # Removida a linha 'app = MainApp()' duplicada, que causava o NameError.
    app = MainApp(system_name="SICON_NEW", system_version="0.1.3", creation_year="2025")
    
    app.mainloop()