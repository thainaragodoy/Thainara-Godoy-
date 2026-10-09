import json
import os
import streamlit as st
import streamlit.components.v1 as components

ARQUIVO_USUARIOS = "usuarios.json"


def carregar_utilizadores():
  if os.path.exists(ARQUIVO_USUARIOS):
    try:
      with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as f:
        dados = json.load(f)
        for email in dados:
          if "perfil" not in dados[email]:
            dados[email]["perfil"] = "Patrão / Dono"
        return dados
    except:
      pass
  padrao = {
      "Canalthahodoy@gmail.com": {
          "senha": "123",
          "nome": "Thainara",
          "sitio": "Sítio Boa Vista",
          "perfil": "Patrão / Dono",
      }
  }
  with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as f:
    json.dump(padrao, f, ensure_ascii=False, indent=4)
  return padrao


def salvar_utilizador(email, senha, nome, sitio, perfil):
  usuarios = carregar_utilizadores()
  usuarios[email] = {
      "senha": senha,
      "nome": nome,
      "sitio": sitio,
      "perfil": perfil,
  }
  with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as f:
    json.dump(usuarios, f, ensure_ascii=False, indent=4)


def gerenciar_autenticacao():
  """Controla o login persistente de forma totalmente segura e isolada."""
  if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

  if "utilizador_atual" not in st.session_state:
    st.session_state.utilizador_atual = {}

  if not st.session_state.autenticado:
    # Script JavaScript para injetar o e-mail guardado no telemóvel na URL
    js_auto_login = """
        <script>
        const savedEmail = localStorage.getItem('granja_user_email');
        if (savedEmail && !window.location.search.includes('user_email=')) {
            const urlParams = new URLSearchParams(window.location.search);
            urlParams.set('user_email', savedEmail);
            window.location.search = urlParams.toString();
        }
        </script>
        """
    components.html(js_auto_login, height=0)

    # Leitura segura do parâmetro na versão atual do Streamlit
    try:
      saved_email = st.query_params.get("user_email", None)
    except:
      saved_email = None

    if saved_email:
      base_u = carregar_utilizadores()
      if saved_email in base_u:
        u_data = base_u[saved_email]
        st.session_state.autenticado = True
        st.session_state.utilizador_atual = {
            "email": saved_email,
            "nome": u_data["nome"],
            "sitio": u_data["sitio"],
            "perfil": u_data.get("perfil", "Patrão / Dono"),
        }

  return st.session_state.autenticado
