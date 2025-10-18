import customtkinter as ctk
import os
from PIL import Image

from core.user_manager import create_user

class CreateUserPage(ctk.CTkFrame):
    def __init__(self, parent, controller, system_name, system_version, creation_year):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.system_name = system_name
        self.system_version = system_version
        self.creation_year = creation_year
        
        # --- Configuração do Layout Principal ---
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # --- Frame para o Conteúdo (Logo e Formulário) ---
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        
        # --- Lado Esquerdo: Símbolo do Sistema ---
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        symbol_path = os.path.join(base_path, 'assets', 'images', 'system-symbol.png')
        system_symbol_image = ctk.CTkImage(light_image=Image.open(symbol_path), size=(200, 200))
        symbol_label = ctk.CTkLabel(content_frame, image=system_symbol_image, text="")
        symbol_label.grid(row=0, column=0, padx=20, pady=20)
        
        # --- Lado Direito: Formulário de Criação de Usuário ---
        form_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        form_frame.grid(row=0, column=1, padx=40, pady=40)
        
        # Nome do Formulário
        form_name_label = ctk.CTkLabel(form_frame, text="Criar Novo Usuário", font=ctk.CTkFont(size=24, weight="bold"))
        form_name_label.pack(pady=(0, 20), anchor="center")
        
        # Campo de Usuário
        self.username_entry = ctk.CTkEntry(form_frame, placeholder_text="Usuário", width=300)
        self.username_entry.pack(pady=10, anchor="center")
        
        # Campo de Senha
        self.password_entry = ctk.CTkEntry(form_frame, placeholder_text="Senha", show="*", width=300)
        self.password_entry.pack(pady=10, anchor="center")
        
        # Campo de Confirmação de Senha
        self.confirm_password_entry = ctk.CTkEntry(form_frame, placeholder_text="Confirmar Senha", show="*", width=300)
        self.confirm_password_entry.pack(pady=10, anchor="center")
        
        # Botão de Criar Usuário
        create_button = ctk.CTkButton(form_frame, text="Criar Usuário", command=self.handle_create_user, width=300)
        create_button.pack(pady=(20, 10), anchor="center")
        
        # Botão Voltar
        back_button = ctk.CTkButton(form_frame, text="Voltar para Login", command=lambda: controller.show_frame("LoginPage"), width=300)
        back_button.pack(pady=(0, 20), anchor="center")
        
        # Mensagem de erro
        self.error_label = ctk.CTkLabel(form_frame, text="", fg_color="transparent", text_color="red")
        self.error_label.pack(anchor="center")
        
        # --- Rodapé ---
        footer_frame = ctk.CTkFrame(self, fg_color="transparent", height=30)
        footer_frame.grid(row=3, column=0, sticky="ew")
        footer_frame.grid_columnconfigure(0, weight=1)
        footer_frame.grid_columnconfigure(1, weight=1)
        
        company_path = os.path.join(base_path, 'assets', 'images', 'company-logo.png')
        company_logo_image = ctk.CTkImage(light_image=Image.open(company_path), size=(20, 20))
        company_info_label = ctk.CTkLabel(footer_frame, image=company_logo_image, text=f"© {self.creation_year}", compound="left", font=ctk.CTkFont(size=12))
        company_info_label.grid(row=0, column=0, sticky="w", padx=10)

        version_label = ctk.CTkLabel(footer_frame, text=f"Versão: {self.system_version}", font=ctk.CTkFont(size=12))
        version_label.grid(row=0, column=1, sticky="e", padx=10)

    def handle_create_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        if not username or not password or not confirm_password:
            self.error_label.configure(text="Todos os campos são obrigatórios.")
            return

        if password != confirm_password:
            self.error_label.configure(text="As senhas não coincidem.")
            return

        if create_user(username, password):
            self.error_label.configure(text="Usuário criado com sucesso!", text_color="green")
            self.username_entry.delete(0, ctk.END)
            self.password_entry.delete(0, ctk.END)
            self.confirm_password_entry.delete(0, ctk.END)
            self.after(2000, lambda: self.controller.show_frame("LoginPage")) 
        else:
            self.error_label.configure(text="Erro ao criar usuário. Tente novamente.")