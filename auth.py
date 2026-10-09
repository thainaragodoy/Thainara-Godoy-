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
          if not isinstance(dados[email], dict):
            dados[email] = {}
          if "perfil" not in dados[email]:
            dados[email]["perfil"] = "Patrão / Dono"
          if "sitio" not in dados[email]:
            dados[email]["sitio"] = "Sítio Boa Vista"
          if "nome" not in dados[email]:
            dados[email]["nome"] = "Granjeiro"
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
  if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

  if "utilizador_atual" not in st.session_state:
    st.session_state.utilizador_atual = {}

  if not st.session_state.autenticado:
    # CORREÇÃO: Usar window.parent.location para forçar a página principal a ler o localStorage
    js_auto_login = """
        <script>
        try {
            const savedEmail = localStorage.getItem('granja_user_email');
            if (savedEmail) {
                const parentLoc = window.parent.location;
                if (!parentLoc.search.includes('user_email=')) {
                    const urlParams = new URLSearchParams(parentLoc.search);
                    urlParams.set('user_email', savedEmail);
                    parentLoc.search = urlParams.toString();
                }
            }
        } catch (e) {
            console.error(e);
        }
        </script>
        """
    components.html(js_auto_login, height=0)

    saved_email = None
    try:
      if "user_email" in st.query_params:
        saved_email = st.query_params["user_email"]
        if isinstance(saved_email, list):
          saved_email = saved_email[0]
    except:
      saved_email = None

    if saved_email:
      base_u = carregar_utilizadores()
      if saved_email in base_u:
        u_data = base_u[saved_email]
        st.session_state.autenticado = True
        st.session_state.utilizador_atual = {
            "email": saved_email,
            "nome": u_data.get("nome", "Thainara"),
            "sitio": u_data.get("sitio", "Sítio Boa Vista"),
            "perfil": u_data.get("perfil", "Patrão / Dono"),
        }

  return st.session_state.autenticado
