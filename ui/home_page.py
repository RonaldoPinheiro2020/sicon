import customtkinter as ctk
import os
import time
from PIL import Image

# Importa a lógica de gerenciamento de sessão da pasta core
from core.session_manager import get_logged_in_user, get_login_time, clear_session

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller, system_name, system_version, creation_year):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        
        self.system_name = system_name
        self.system_version = system_version
        self.creation_year = creation_year
        
        # --- Configuração do Layout Principal ---
        # 0: cabeçalho, 1: conteúdo principal (expansível), 2: rodapé
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # --- Cabeçalho (Barra do Usuário) ---
        header_frame = ctk.CTkFrame(self, height=50)
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Informações do sistema no cabeçalho
        try:
            symbol_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'images', 'system-symbol.png')
            system_symbol_image = ctk.CTkImage(light_image=Image.open(symbol_path), size=(30, 30))
            system_info_label = ctk.CTkLabel(header_frame, image=system_symbol_image, text=self.system_name, compound="left", font=ctk.CTkFont(size=16, weight="bold"))
            system_info_label.grid(row=0, column=0, sticky="w", padx=10)
        except FileNotFoundError:
            system_info_label = ctk.CTkLabel(header_frame, text=self.system_name, font=ctk.CTkFont(size=16, weight="bold"))
            system_info_label.grid(row=0, column=0, sticky="w", padx=10)
        
        # Informações do usuário
        user_info_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        user_info_frame.grid(row=0, column=1, sticky="e", padx=10)
        self.user_label = ctk.CTkLabel(user_info_frame, text="", font=ctk.CTkFont(size=14))
        self.user_label.pack(side="left", padx=5)
        self.time_label = ctk.CTkLabel(user_info_frame, text="", font=ctk.CTkFont(size=14))
        self.time_label.pack(side="left", padx=5)
        
        # Botão de Logout
        logout_button = ctk.CTkButton(user_info_frame, text="Sair", command=self.handle_logout)
        logout_button.pack(side="right", padx=5)
        
        # --- Conteúdo Principal (Centralizado) ---
        main_content_frame = ctk.CTkFrame(self)
        main_content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        
        # Usamos pack para centralizar o conteúdo de forma mais previsível
        welcome_label = ctk.CTkLabel(main_content_frame, text="Bem-vindo(a) ao SICON!", font=ctk.CTkFont(size=20, weight="bold"))
        welcome_label.pack(expand=True)
        
        # --- Rodapé ---
        # Este frame agora é parte do grid principal, na última linha
        footer_frame = ctk.CTkFrame(self, height=30, fg_color="transparent")
        footer_frame.grid(row=2, column=0, sticky="ew")
        footer_frame.grid_columnconfigure(0, weight=1)
        footer_frame.grid_columnconfigure(1, weight=1)
        
        # Símbolo e ano da Empresa
        try:
            company_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'images', 'company-logo.png')
            company_logo_image = ctk.CTkImage(light_image=Image.open(company_path), size=(20, 20))
            company_info_label = ctk.CTkLabel(footer_frame, image=company_logo_image, text=f"© {self.creation_year}", compound="left", font=ctk.CTkFont(size=12))
            company_info_label.grid(row=0, column=0, sticky="w", padx=10)
        except FileNotFoundError:
            company_info_label = ctk.CTkLabel(footer_frame, text=f"© {self.creation_year}", font=ctk.CTkFont(size=12))
            company_info_label.grid(row=0, column=0, sticky="w", padx=10)
        
        # Versão do Sistema (SemVer)
        version_label = ctk.CTkLabel(footer_frame, text=f"Versão: {self.system_version}", font=ctk.CTkFont(size=12))
        version_label.grid(row=0, column=1, sticky="e", padx=10)

    def update_user_info(self):
        user = get_logged_in_user()
        login_time = get_login_time()
        
        if user and login_time:
            elapsed_time = int(time.time() - login_time)
            minutes, seconds = divmod(elapsed_time, 60)
            
            self.user_label.configure(text=f"Usuário: {user}")
            self.time_label.configure(text=f"Tempo logado: {minutes:02d}:{seconds:02d}")
        
        self.after(1000, self.update_user_info)

    def handle_logout(self):
        clear_session()
        self.controller.show_frame("LoginPage")