import json
import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Gestão da Granja Profissional", layout="wide")

# ==================== PERSISTÊNCIA (JSON) ====================
ARQUIVO_USUARIOS = "usuarios.json"
ARQUIVO_DADOS = "dados_granja.json"


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
  return {
      "admin@granja.com": {
          "senha": "123",
          "nome": "João Granjeiro",
          "sitio": "Sítio Boa Vista",
          "perfil": "Patrão / Dono",
      }
  }


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
  }
  with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
    json.dump(dados_para_salvar, f, ensure_ascii=False, indent=4)


# 1. ESTADO DE AUTENTICAÇÃO E SESSÃO
if "autenticado" not in st.session_state:
  st.session_state.autenticado = False

if "utilizador_atual" not in st.session_state:
  st.session_state.utilizador_atual = {}

# Carrega dados salvos anteriormente ou define padrões
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
            "Sítio": "Sítio Boa Vista",
            "Lote": "Lote Anterior 01",
            "Integradora": "Zanqueta",
            "Início": "10/06/2026",
            "Aves Alojadas": 120000,
            "Conversão Final": 1.510,
            "Fator de Prod.": 425.5,
            "R$ por Cabeça": 1.92,
            "Comissão Total (R$)": 230400.0,
        }
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

if "lembretes_manutencao" not in st.session_
