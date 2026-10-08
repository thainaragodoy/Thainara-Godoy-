import datetime
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Sistema de Controlo de Lotes", page_icon="📦", layout="wide"
)

# Inicializar Base de Dados em memória (Session State)
if "lotes" not in st.session_state:
  st.session_state.lotes = []
if "conversoes" not in st.session_state:
  st.session_state.conversoes = []
if "pesagens" not in st.session_state:
  st.session_state.pesagens = []

st.title("📦 Sistema de Controlo de Lotes e Pesagens")
st.sidebar.title("Navegação")
menu = st.sidebar.selectbox(
    "Escolha uma opção",
    [
        "Dashboard",
        "Registar Lote",
        "Registar Conversão",
        "Registar Pesagem",
        "Histórico e Relatórios",
    ],
)

# ----------------------------------------------------
# 1. DASHBOARD
# ----------------------------------------------------
if menu == "Dashboard":
  st.header("Visão Geral do Sistema")

  col1, col2, col3 = st.columns(3)
  with col1:
    st.metric("Total de Lotes", len(st.session_state.lotes))
  with col2:
    st.metric("Conversões Registadas", len(st.session_state.conversoes))
  with col3:
    st.metric("Pesagens Registadas", len(st.session_state.pesagens))

  st.divider()
  st.subheader("Lotes Ativos")
  if st.session_state.lotes:
    df_lotes = pd.DataFrame(st.session_state.lotes)
    st.dataframe(df_lotes, use_container_width=True)
  else:
    st.info("Ainda não existem lotes registados.")

# ----------------------------------------------------
# 2. REGISTAR LOTE
# ----------------------------------------------------
elif menu == "Registar Lote":
  st.header("Criar Novo Lote")

  with st.form("form_lote"):
    codigo = st.text_input("Código / Identificador do Lote")
    responsavel = st.text_input("Operador Responsável")
    observacoes = st.text_area("Observações Iniciais")
    submitted = st.form_submit_button("Guardar Lote")

    if submitted:
      if codigo:
        novo_lote = {
            "ID do Lote": codigo,
            "Responsável": responsavel,
            "Data de Criação": datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            ),
            "Observações": observacoes,
            "Estado": "Em Aberto",
        }
        st.session_state.lotes.append(novo_lote)
        st.success(f"Lote '{codigo}' registado com sucesso!")
      else:
        st.error("O código do lote é obrigatório.")

# ----------------------------------------------------
# 3. REGISTAR CONVERSÃO
# ----------------------------------------------------
elif menu == "Registar Conversão":
  st.header("Registo de Conversão do Lote")

  if not st.session_state.lotes:
    st.warning("Registe primeiro um lote para poder efetuar conversões.")
  else:
    lotes_disponiveis = [l["ID do Lote"] for l in st.session_state.lotes]

    with st.form("form_conversao"):
      lote_selecionado = st.selectbox(
          "Selecione o Lote",
          lotes_disponiveis,
      )
      etapa = st.selectbox(
          "Etapa de Conversão",
          [
              "Conversão do lote 1",
              "Conversão do lote 2",
              "Conversão do lote N",
          ],
      )
      detalhes = st.text_area("Detalhes da Conversão / Parâmetros")
      submitted = st.form_submit_button("Registar Conversão")

      if submitted:
        nova_conv = {
            "Lote": lote_selecionado,
            "Etapa": etapa,
            "Detalhes": detalhes,
            "Data/Hora": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        st.session_state.conversoes.append(nova_conv)
        st.success(f"Conversão para o lote '{lote_selecionado}' registada!")

# ----------------------------------------------------
# 4. REGISTAR PESAGEM (Pesagem N2, Pesagens N)
# ----------------------------------------------------
elif menu == "Registar Pesagem":
  st.header("Controlo de Pesagens (Pesagem N2 e Sequenciais)")

  if not st.session_state.lotes:
    st.warning("Registe primeiro um lote para efetuar pesagens.")
  else:
    lotes_disponiveis = [l["ID do Lote"] for l in st.session_state.lotes]

    with st.form("form_pesagem"):
      lote_selecionado = st.selectbox("Selecione o Lote", lotes_disponiveis)
      tipo_pesagem = st.selectbox(
          "Tipo de Pesagem",
          ["Pesagem Inicial", "Pesagem N2", "Pesagens N (Sequencial)"],
      )
      peso_esperado = st.number_input(
          "Peso Esperado / Teórico (kg)", min_value=0.0, format="%.2f"
      )
      peso_real = st.number_input(
          "Peso Real / Aferido (kg)", min_value=0.0, format="%.2f"
      )
      operador = st.text_input("Nome do Operador")
      submitted = st.form_submit_button("Registar Pesagem")

      if submitted:
        desvio = peso_real - peso_esperado
        nova_pesagem = {
            "Lote": lote_selecionado,
            "Tipo": tipo_pesagem,
            "Peso Esperado (kg)": peso_esperado,
            "Peso Real (kg)": peso_real,
            "Desvio (kg)": round(desvio, 2),
            "Operador": operador,
            "Data/Hora": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        st.session_state.pesagens.append(nova_pesagem)
        st.success(
            f"Pesagem registada com sucesso! Desvio calculado: {desvio:.2f} kg"
        )

# ----------------------------------------------------
# 5. HISTÓRICO E RELATÓRIOS
# ----------------------------------------------------
elif menu == "Histórico e Relatórios":
  st.header("Histórico Completo")

  st.subheader("Histórico de Conversões")
  if st.session_state.conversoes:
    st.dataframe(
        pd.DataFrame(st.session_state.conversoes), use_container_width=True
    )
  else:
    st.info("Sem conversões registadas.")

  st.subheader("Histórico de Pesagens (Pesagem N2 e N)")
  if st.session_state.pesagens:
    df_pesagens = pd.DataFrame(st.session_state.pesagens)
    st.dataframe(df_pesagens, use_container_width=True)
  else:
    st.info("Sem pesagens registadas.")
