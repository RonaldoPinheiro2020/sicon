# ...existing code...
import customtkinter as ctk
import os
from pathlib import Path
from PIL import Image

# Importa a lógica de validação do core.database_access
from core.user_manager import validate_user

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller, system_name, system_version, creation_year):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        self.system_name = system_name
        self.system_version = system_version
        self.creation_year = creation_year

        # --- CALCULA A RAIZ DO PACOTE Sicon_NEW ---
        # Path(__file__).parents[0] -> .../Sicon_NEW/ui
        # Path(__file__).parents[1] -> .../Sicon_NEW  <-- queremos este
        base_path = Path(__file__).resolve().parents[1]
        # --- FIM DO CÁLCULO DE BASE_PATH ---

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
        symbol_path = base_path / "assets" / "images" / "system-symbol.png"
        if symbol_path.exists():
            try:
                symbol_img = Image.open(symbol_path)
            except Exception:
                symbol_img = Image.new("RGBA", (200, 200), (255, 255, 255, 0))
        else:
            symbol_img = Image.new("RGBA", (200, 200), (255, 255, 255, 0))

        system_symbol_image = ctk.CTkImage(light_image=symbol_img, size=(200, 200))
        # mantém referência para evitar garbage-collection
        self._system_symbol_image = system_symbol_image

        symbol_label = ctk.CTkLabel(content_frame, image=system_symbol_image, text="")
        symbol_label.grid(row=0, column=0, padx=20, pady=20)

        # --- Lado Direito: Formulário de Login ---
        form_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        form_frame.grid(row=0, column=1, padx=40, pady=40)

        # Nome do Sistema
        system_name_label = ctk.CTkLabel(form_frame, text=self.system_name, font=ctk.CTkFont(size=24, weight="bold"))
        system_name_label.pack(pady=(0, 20), anchor="center")

        # Campo de Usuário
        self.username_entry = ctk.CTkEntry(form_frame, placeholder_text="Usuário", width=300)
        self.username_entry.pack(pady=10, anchor="center")

        # Campo de Senha
        self.password_entry = ctk.CTkEntry(form_frame, placeholder_text="Senha", show="*", width=300)
        self.password_entry.pack(pady=10, anchor="center")

        # Botões
        login_button = ctk.CTkButton(form_frame, text="Entrar", command=self.handle_login, width=300)
        login_button.pack(pady=(20, 10), anchor="center")

        create_user_button = ctk.CTkButton(form_frame, text="Criar Usuário", command=lambda: controller.show_frame("CreateUserPage"), width=300)
        create_user_button.pack(pady=(0, 20), anchor="center")

        # Mensagem de erro
        self.error_label = ctk.CTkLabel(form_frame, text="", fg_color="transparent", text_color="red")
        self.error_label.pack(anchor="center")

        # --- Rodapé ---
        footer_frame = ctk.CTkFrame(self, fg_color="transparent", height=30)
        footer_frame.grid(row=3, column=0, sticky="ew")
        footer_frame.grid_columnconfigure(0, weight=1)
        footer_frame.grid_columnconfigure(1, weight=1)

        # Informações da Empresa
        company_path = base_path / "assets" / "images" / "company-logo.png"
        if company_path.exists():
            try:
                company_img = Image.open(company_path)
            except Exception:
                company_img = Image.new("RGBA", (20, 20), (255, 255, 255, 0))
        else:
            company_img = Image.new("RGBA", (20, 20), (255, 255, 255, 0))

        company_logo_image = ctk.CTkImage(light_image=company_img, size=(20, 20))
        self._company_logo_image = company_logo_image

        company_info_label = ctk.CTkLabel(footer_frame, image=company_logo_image, text=f"© {self.creation_year}", compound="left", font=ctk.CTkFont(size=12))
        company_info_label.grid(row=0, column=0, sticky="w", padx=10)

        # Versão do Sistema
        version_label = ctk.CTkLabel(footer_frame, text=f"Versão: {self.system_version}", font=ctk.CTkFont(size=12))
        version_label.grid(row=0, column=1, sticky="e", padx=10)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Chama a função de validação da pasta core
        if validate_user(username, password):
            self.error_label.configure(text="")
            self.controller.show_frame("HomePage")
        else:
            self.error_label.configure(text="Usuário ou senha inválidos.")

    def handle_create_user(self):
        # Aqui você pode adicionar a lógica para a criação de um novo usuário
        print("Botão 'Criar Usuário' pressionado. Adicione a sua lógica aqui.")
        # Se for para uma nova tela, use:
        # self.controller.show_frame("CreateUserPage")
# ...existing code...