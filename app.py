import pandas as pd
import streamlit as st

st.set_page_config(page_title="Gestão da Granja", layout="wide")

# Estilo visual limpo para telemóvel
st.markdown(
    """
    <style>
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; }
    </style>
""",
    unsafe_allow_html=True,
)

# Cabeçalho fixo
st.markdown(
    """
    <div style="background-color: #3b5bdb; padding: 12px; border-radius: 8px; color: white; text-align: center;">
        <h4 style="margin:0;">📦 Apont. de Produção - Granja</h4>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

# Barra de Navegação Superior (Estilo de Botões / Abas para telemóvel)
menu = st.radio(
    "Navegação",
    ["🏠 Início", "📉 Mortalidade", "⚖️ Balança", "🧮 Conversão", "🚚 Ração", "📂 Histórico"],
    horizontal=True,
    label_visibility="collapsed",
)

st.divider()

# ==================== 1. INÍCIO ====================
if menu == "🏠 Início":
  st.subheader("Detalhes do Lote Atual")

  st.markdown(
      """
        <div style="background: linear-gradient(135deg, #2b8a3e 0%, #2f9e44 100%); padding: 15px; border-radius: 10px; color: white;">
            <h4 style="margin:0;">Lote Ativo: 44490 - NÚCLEO 1</h4>
            <hr style="margin: 8px 0; border-color: rgba(255,255,255,0.3);">
            <table style="width:100%; color: white; text-align: center;">
                <tr>
                    <td><b>Início</b><br>23/08</td>
                    <td><b>Idade</b><br>47 dias</td>
                    <td><b>Saldo</b><br>5.826</td>
                </tr>
            </table>
            <p style="margin-top: 10px; margin-bottom: 0;"><b>Sexo:</b> Machos | <b>Linhagem:</b> COBB</p>
        </div>
        """,
      unsafe_allow_html=True,
  )

  st.info(
      "Use a barra acima para navegar entre Mortalidade, Balança, Conversão,"
      " Ração e Histórico."
  )

# ==================== 2. MORTALIDADE ====================
elif menu == "📉 Mortalidade":
  st.subheader("Controle de Mortalidade (45 Dias)")
  st.write("Clique nas células para editar os valores de cada granja a qualquer momento.")

  # Criar estrutura para 45 dias e colunas por granja (G1, G2, G3, etc.)
  dias_mortalidade = [f"Dia {i}" for i in range(1, 46)]
  df_mortalidade_padrao = pd.DataFrame({
      "Dia": dias_mortalidade,
      "Granja 1": [0] * 45,
      "Granja 2": [0] * 45,
      "Granja 3": [0] * 45,
  })

  # Tabela interativa editável
  mortalidade_editada = st.data_editor(
      df_mortalidade_padrao,
      num_rows="fixed",
      use_container_width=True,
      key="tabela_mortalidade",
  )

# ==================== 3. BALANÇA ====================
elif menu == "⚖️ Balança":
  st.subheader("Pesagens Semanais (Até 45 Dias)")
  st.write("Registe as pesagens realizadas de 7 em 7 dias.")

  # Tabela interativa para pesagens (7, 14, 21, 28, 35, 42 dias)
  df_balanca_padrao = pd.DataFrame({
      "Idade / Período": [
          "7 dias",
          "14 dias",
          "21 dias",
          "28 dias",
          "35 dias",
          "42 dias",
      ],
      "Granja 1 (Peso g)": [0.0] * 6,
      "Granja 2 (Peso g)": [0.0] * 6,
      "Granja 3 (Peso g)": [0.0] * 6,
      "Média Lote": [0.0] * 6,
  })

  balanca_editada = st.data_editor(
      df_balanca_padrao, use_container_width=True, key="tabela_balanca"
  )

# ==================== 4. CONVERSÃO ====================
elif menu == "🧮 Conversão":
  st.subheader("Cálculos e Conversão Alimentar")

  col1, col2 = st.columns(2)
  with col1:
    racao_total = st.number_input(
        "Total de Ração Consumida (kg)", value=10000.0, step=100.0
    )
  with col2:
    peso_total_vivo = st.number_input(
        "Peso Total Vivo (kg)", value=5000.0, step=50.0
    )

  if peso_total_vivo > 0:
    conversao_alimentar = racao_total / peso_total_vivo
    st.success(
        f"### 📊 Conversão Alimentar Calculada: **{conversao_alimentar:.3f}**"
    )
  else:
    st.warning("Insira um peso total vivo válido para calcular.")

# ==================== 5. RAÇÃO ====================
elif menu == "🚚 Ração":
  st.subheader("Registo de Chegada de Ração")
  st.write("Adicione os dados dos caminhões de ração que vão chegando à granja.")

  # Tabela editável para camiões/fórmulas de ração
  df_racao_padrao = pd.DataFrame({
      "Data": ["", "", ""],
      "Camião / Nota": ["", "", ""],
      "Quantidade (Kg)": [0.0, 0.0, 0.0],
      "Fórmula": ["", "", ""],
  })

  racao_editada = st.data_editor(
      df_racao_padrao, num_rows="dynamic", use_container_width=True, key="tabela_racao"
  )

# ==================== 6. HISTÓRICO ====================
elif menu == "📂 Histórico":
  st.subheader("Histórico de Lotes Anteriores")
  st.write("Consulte os dados consolidados dos lotes anteriores.")

  df_historico = pd.DataFrame({
      "Lote": ["Lote 01 - Anterior", "Lote 02 - Anterior"],
      "Início": ["10/06/2026", "15/07/2026"],
      "Encerramento": ["10/08/2026", "14/09/2026"],
      "Aves Alojadas": [120000, 123900],
      "Conversão": [1.510, 1.480],
  })
  st.dataframe(df_historico, use_container_width=True, hide_index=True)
