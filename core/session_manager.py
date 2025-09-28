import time

# Estas variáveis globais armazenam a sessão do usuário.
# Elas são inicializadas como None (vazias)
_logged_in_user = None
_login_time = None

def set_logged_in_user(username):
    """
    Define o usuário logado e registra o tempo de login.
    """
    global _logged_in_user, _login_time
    _logged_in_user = username
    _login_time = time.time()  # Registra o tempo atual em segundos

def get_logged_in_user():
    """
    Retorna o nome do usuário logado.
    """
    return _logged_in_user

def get_login_time():
    """
    Retorna o timestamp do login do usuário.
    """
    return _login_time

def clear_session():
    """
    Limpa a sessão do usuário, usada para fazer logout.
    """
    global _logged_in_user, _login_time
    _logged_in_user = None
    _login_time = None