import json
import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Gestão da Granja Profissional", layout="wide")

# ==================== ESTILIZAÇÃO CSS (FUNDO COM IMAGEM E PALETA ACINZENTADA) ====================
FUNDO_URL = "fundo_pintinhos.png"

st.markdown(
    f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.90), rgba(240, 242, 245, 0.92)), url("{FUNDO_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    @media (prefers-color-scheme: dark) {{
        .stApp {{
            background: linear-gradient(rgba(15, 17, 21, 0.92), rgba(22, 27, 34, 0.95)), url("{FUNDO_URL}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
    }}

    div[data-baseweb="tab-highlight"] {{
        background-color: #495057 !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ==================== PERSISTÊNCIA (JSON) ====================
ARQUIVO_USUARIOS = "usuarios.json"
ARQUIVO_DADOS = "dados_granja.json"
ARQUIVO_SESSAO = "sessao_ativa.json"


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


def carregar_sessao_salva():
  if os.path.exists(ARQUIVO_SESSAO):
    try:
      with open(ARQUIVO_SESSAO, "r", encoding="utf-8") as f:
        return json.load(f)
    except:
      pass
  return None


def guardar_sessao_ativa(dados_utilizador):
  with open(ARQUIVO_SESSAO, "w", encoding="utf-8") as f:
    json.dump(dados_utilizador, f, ensure_ascii=False, indent=4)


def limpar_sessao_ativa():
  if os.path.exists(ARQUIVO_SESSAO):
    try:
      os.remove(ARQUIVO_SESSAO)
    except:
      pass


def carregar_dados_granja():
  if os.path.exists(ARQUIVO_DADOS):
    try:
      with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
        return json.load(f)
    except:
      pass
  return None


def guardar_dados_granja():
  dados_para_salvar = {
      "lote_config": st.session_state.lote_config,
      "historico_lotes": st.session_state.historico_lotes,
      "df_mortalidade": st.session_state.df_mortalidade.to_dict(),
      "df_racao": st.session_state.df_racao.to_dict(),
      "df_balanca": st.session_state.df_balanca.to_dict(),
      "df_medicacao": st.session_state.df_medicacao.to_dict(),
      "lembretes_manutencao": st.session_state.lembretes_manutencao,
      "anotacoes_financeiras": st.session_state.anotacoes_financeiras,
  }
  with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
    json.dump(dados_para_salvar, f, ensure_ascii=False, indent=4)


# ==================== ESTADO DE AUTENTICAÇÃO ====================
if "autenticado" not in st.session_state:
  sessao_previa = carregar_sessao_salva()
  if sessao_previa:
    st.session_state.autenticado = True
    st.session_state.utilizador_atual = sessao_previa
  else:
    st.session_state.autenticado = False

if "utilizador_atual" not in st.session_state:
  st.session_state.utilizador_atual = {}

dados_salvos = carregar_dados_granja()

aves_iniciais = {f"Granja {i}": (62000 if i <= 2 else 0) for i in range(1, 11)}
silos_iniciais = {f"Granja {i}": 0.0 for i in range(1, 11)}

if "lote_config" not in st.session_state:
  if dados_salvos and "lote_config" in dados_salvos:
    st.session_state.lote_config = dados_salvos["lote_config"]
  else:
    st.session_state.lote_config = {
        "sitio": "Sítio Boa Vista",
        "lote": "Lote 01 - NÚCLEO 1",
        "inicio": "23/08/2026",
        "num_granjas": 2,
        "aves": aves_iniciais,
        "estoque_silo": silos_iniciais,
    }

if "historico_lotes" not in st.session_state:
  if dados_salvos and "historico_lotes" in dados_salvos:
    st.session_state.historico_lotes = dados_salvos["historico_lotes"]
  else:
    st.session_state.historico_lotes = [
        {
            "Lote": "Lote Anterior 01",
            "Início": "10/06/2026",
            "Aves Alojadas": 120000,
            "Total Aves Mortas": 2400,
            "Ração Consumida (Kg)": 180000.0,
            "Conversão Final": 1.510,
            "R$ por Cabeça": 1.92,
            "Comissão Total (R$)": 230400.0,
        },
        {
            "Lote": "Lote Anterior 02",
            "Início": "15/07/2026",
            "Aves Alojadas": 124000,
            "Total Aves Mortas": 1900,
            "Ração Consumida (Kg)": 182000.0,
            "Conversão Final": 1.490,
            "R$ por Cabeça": 1.98,
            "Comissão Total (R$)": 245520.0,
        },
    ]

if "df_mortalidade" not in st.session_state:
  if dados_salvos and "df_mortalidade" in dados_salvos:
    st.session_state.df_mortalidade = pd.DataFrame(
        dados_salvos["df_mortalidade"]
    )
  else:
    dias = [f"Dia {i}" for i in range(1, 46)]
    dict_mort = {"Dia": dias}
    for i in range(1, 11):
      dict_mort[f"Granja {i}"] = [0] * 45
    st.session_state.df_mortalidade = pd.DataFrame(dict_mort)

if "df_racao" not in st.session_state:
  if dados_salvos and "df_racao" in dados_salvos:
    st.session_state.df_racao = pd.DataFrame(dados_salvos["df_racao"])
  else:
    dict_rac = {
        "Nº Caminhão / Nota": [
            f"Caminhão {i}" if i <= 5 else "" for i in range(1, 41)
        ],
        "Data": ["" for _ in range(40)],
    }
    for i in range(1, 11):
      dict_rac[f"Granja {i} (Kg)"] = [0.0 for _ in range(40)]
    dict_rac["Fórmula / Tipo"] = ["" for _ in range(40)]
    st.session_state.df_racao = pd.DataFrame(dict_rac)

if "df_balanca" not in st.session_state:
  if dados_salvos and "df_balanca" in dados_salvos:
    st.session_state.df_balanca = pd.DataFrame(dados_salvos["df_balanca"])
  else:
    dict_bal = {
        "Semana / Idade": [
            "1ª Semana (7 dias)",
            "2ª Semana (14 dias)",
            "3ª Semana (21 dias)",
            "4ª Semana (28 dias)",
            "5ª Semana (35 dias)",
            "6ª Semana (42 dias)",
        ]
    }
    for i in range(1, 11):
      dict_bal[f"Granja {i} (Peso g)"] = [0.0] * 6
    st.session_state.df_balanca = pd.DataFrame(dict_bal)

if "df_medicacao" not in st.session_state:
  if dados_salvos and "df_medicacao" in dados_salvos:
    st.session_state.df_medicacao = pd.DataFrame(dados_salvos["df_medicacao"])
  else:
    dias_med = [f"Dia {i}" for i in range(1, 46)]
    st.session_state.df_medicacao = pd.DataFrame({
        "Dia": dias_med,
        "Medicação / Produto": ["" for _ in range(45)],
        "Dosagem / Quantidade": ["" for _ in range(45)],
        "Observações Aplicação": ["" for _ in range(45)],
    })

if "lembretes_manutencao" not in st.session_state:
  if dados_salvos and "lembretes_manutencao" in dados_salvos:
    st.session_state.lembretes_manutencao = dados_salvos[
        "lembretes_manutencao"
    ]
  else:
    st.session_state.lembretes_manutencao = (
        "- Verificar bicos de nipple das granjas.\n- Agendar manutenção do"
        " gerador."
    )

if "anotacoes_financeiras" not in st.session_state:
  if dados_salvos and "anotacoes_financeiras" in dados_salvos:
    st.session_state.anotacoes_financeiras = dados_salvos[
        "anotacoes_financeiras"
    ]
  else:
    st.session_state.anotacoes_financeiras = {
        "sitio": "Sítio Boa Vista",
        "qtd_alojada": 124000,
        "qtd_abatidas": 120000,
        "conversao_lote": 1.520,
        "pagamento_ave": 1.95,
        "valor_final": 234000.0,
    }


# ==================== TELA DE LOGIN / CADASTRO ====================
if not st.session_state.autenticado:
  st.markdown(
      """
        <div style="background: linear-gradient(135deg, #343a40 0%, #212529 100%); padding: 30px; border-radius: 12px; color: white; text-align: center; margin-bottom: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
            <h2 style="margin:0; font-size: 28px;">🐔 Sistema de Gestão Avícola Profissional</h2>
            <p style="margin:8px 0 0 0; font-size: 15px; opacity: 0.9;">Plataforma de controlo operacional e financeiro de lotes</p>
        </div>
        """,
      unsafe_allow_html=True,
  )

  _, col_centro, _ = st.columns([1, 2.2, 1])

  with col_centro:
    tab_login, tab_cadastro = st.tabs(["🔐 Entrar na Conta", "📝 Criar Registo"])

    with tab_login:
      st.write("")
      email_login = st.text_input("E-mail", key="login_email")
      senha_login = st.text_input("Senha", type="password", key="login_senha")
      st.write("")

      if st.button("Entrar no Sistema", type="primary", use_container_width=True):
        base_usuarios = carregar_utilizadores()
        if email_login in base_usuarios:
          if base_usuarios[email_login]["senha"] == senha_login:
            st.session
