import customtkinter as ctk
import os

# Importa as telas da pasta ui
from ui.login_page import LoginPage
from ui.home_page import HomePage
from ui.create_user_page import CreateUserPage

class MainApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # --- Definições Globais do Sistema (SemVer) ---
        self.system_name = "SICON"
        self.system_version = "0.1.2" 
        self.creation_year = "2025"

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
    app = App(system_name="SICON", system_version="0.1.2", creation_year="2025")
    app = MainApp()
    app.mainloop()