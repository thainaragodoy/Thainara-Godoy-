import pandas as pd
import streamlit as st

st.set_page_config(page_title="Gestão da Granja", layout="wide")

# Inicializar o estado da sessão para persistir os dados ao navegar entre abas
if "lote_config" not in st.session_state:
  st.session_state.lote_config = {
      "lote": "44490 - NÚCLEO 1",
      "inicio": "23/08/2026",
      "sexo": "Machos",
      "linhagem": "COBB",
      "aves_g1": 62000,
      "aves_g2": 61900,
  }

if "df_mortalidade" not in st.session_state:
  dias = [f"Dia {i}" for i in range(1, 46)]
  st.session_state.df_mortalidade = pd.DataFrame(
      {"Dia": dias, "Granja 1": [0] * 45, "Granja 2": [0] * 45}
  )

if "df_racao" not in st.session_state:
  # Cerca de 40 linhas para registo de caminhões de ração
  st.session_state.df_racao = pd.DataFrame({
      "Nº Caminhão / Nota": [f"Caminhão {i}" if i <= 5 else "" for i in range(1, 41)],
      "Data": ["" for _ in range(40)],
      "Granja 1 (Kg)": [0.0 for _ in range(40)],
      "Granja 2 (Kg)": [0.0 for _ in range(40)],
      "Fórmula / Tipo": ["" for _ in range(40)],
  })

if "df_balanca" not in st.session_state:
  st.session_state.df_balanca = pd.DataFrame({
      "Idade (Dias)": [7, 14, 21, 28, 35, 42],
      "Granja 1 (g)": [0.0] * 6,
      "Granja 2 (g)": [0.0] * 6,
  })

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

# Barra de Navegação Superior
menu = st.radio(
    "Navegação",
    ["🏠 Início", "📉 Mortalidade", "🚚 Ração", "⚖️ Balança", "🧮 Conversão", "📂 Histórico"],
    horizontal=True,
    label_visibility="collapsed",
)

# Botão Flutuante / Ação Rápida Destacada com ícone de Mais (+)
with st.expander("➕ Adicionar / Registar Novo Apontamento (Ação Rápida)", expanded=False):
  tipo_acao = st.selectbox(
      "Selecione o que deseja atualizar:",
      [
          "Registar Mortalidade Diária",
          "Adicionar Caminhão de Ração",
          "Registar Pesagem da Balança",
      ],
  )
  if tipo_acao == "Registar Mortalidade Diária":
    dia_mort = st.selectbox(
        "Selecione o Dia:", [f"Dia {i}" for i in range(1, 46)]
    )
    m_g1 = st.number_input("Mortes Granja 1", min_value=0, step=1, value=0)
    m_g2 = st.number_input("Mortes Granja 2", min_value=0, step=1, value=0)
    if st.button("Atualizar Mortalidade"):
      idx = int(dia_mort.split(" ")[1]) - 1
      st.session_state.df_mortalidade.loc[idx, "Granja 1"] = m_g1
      st.session_state.df_mortalidade.loc[idx, "Granja 2"] = m_g2
      st.success("Mortalidade atualizada com sucesso!")

  elif tipo_acao == "Adicionar Caminhão de Ração":
    c_num = st.text_input("Identificação do Caminhão / Nota")
    c_g1 = st.number_input("Quantidade Granja 1 (Kg)", min_value=0.0, step=100.0)
    c_g2 = st.number_input("Quantidade Granja 2 (Kg)", min_value=0.0, step=100.0)
    c_form = st.text_input("Fórmula / Tipo de Ração")
    if st.button("Registar Caminhão"):
      # Encontrar primeira linha vazia ou adicionar
      vazios = st.session_state.df_racao[
          st.session_state.df_racao["Nº Caminhão / Nota"] == ""
      ]
      if not vazios.empty:
        idx = vazios.index[0]
        st.session_state.df_racao.loc[idx, "Nº Caminhão / Nota"] = c_num
        st.session_state.df_racao.loc[idx, "Granja 1 (Kg)"] = c_g1
        st.session_state.df_racao.loc[idx, "Granja 2 (Kg)"] = c_g2
        st.session_state.df_racao.loc[idx, "Fórmula / Tipo"] = c_form
        st.success("Caminhão registado com sucesso na tabela de ração!")
      else:
        st.warning("A tabela de ração está cheia.")

st.divider()

# ==================== 1. INÍCIO ====================
if menu == "🏠 Início":
  st.subheader("Detalhes e Configuração do Lote")

  with st.form("form_lote"):
    st.write("**Configuração Inicial das Aves por Granja:**")
    cfg_g1 = st.number_input(
        "Aves Alojadas - Granja 1",
        value=st.session_state.lote_config["aves_g1"],
        step=100,
    )
    cfg_g2 = st.number_input(
        "Aves Alojadas - Granja 2",
        value=st.session_state.lote_config["aves_g2"],
        step=100,
    )
    salvar_cfg = st.form_submit_button("Guardar Alterações do Lote")
    if salvar_cfg:
      st.session_state.lote_config["aves_g1"] = cfg_g1
      st.session_state.lote_config["aves_g2"] = cfg_g2
      st.success("Configuração de aves atualizada!")

  total_alojadas = (
      st.session_state.lote_config["aves_g1"]
      + st.session_state.lote_config["aves_g2"]
  )
  total_mortas = (
      st.session_state.df_mortalidade["Granja 1"].sum()
      + st.session_state.df_mortalidade["Granja 2"].sum()
  )
  saldo_atual = total_alojadas - total_mortas

  st.markdown(
      f"""
        <div style="background: linear-gradient(135deg, #2b8a3e 0%, #2f9e44 100%); padding: 15px; border-radius: 10px; color: white;">
            <h4 style="margin:0;">Lote Ativo: {st.session_state.lote_config['lote']}</h4>
            <hr style="margin: 8px 0; border-color: rgba(255,255,255,0.3);">
            <table style="width:100%; color: white; text-align: center;">
                <tr>
                    <td><b>Início</b><br>{st.session_state.lote_config['inicio']}</td>
                    <td><b>Alojadas</b><br>{total_alojadas:,}</td>
                    <td><b>Saldo Atual</b><br>{saldo_atual:,}</td>
                </tr>
            </table>
            <p style="margin-top: 10px; margin-bottom: 0;"><b>Sexo:</b> {st.session_state.lote_config['sexo']} | <b>Mortes Acumuladas:</b> {total_mortas}</p>
        </div>
        """,
      unsafe_allow_html=True,
  )

# ==================== 2. MORTALIDADE ====================
elif menu == "📉 Mortalidade":
  st.subheader("Controle Diário de Mortalidade (45 Dias)")
  st.write("Preencha diretamente na tabela ou use a ação rápida acima.")

  st.session_state.df_mortalidade = st.data_editor(
      st.session_state.df_mortalidade,
      num_rows="fixed",
      use_container_width=True,
      key="editor_mortalidade",
  )

  t_m1 = st.session_state.df_mortalidade["Granja 1"].sum()
  t_m2 = st.session_state.df_mortalidade["Granja 2"].sum()
  st.info(
      f"**Total de Mortes Acumuladas:** Granja 1: {t_m1} | Granja 2:"
      f" {t_m2} | **Geral:** {t_m1 + t_m2}"
  )

# ==================== 3. RAÇÃO ====================
elif menu == "🚚 Ração":
  st.subheader("Registo de Chegada de Ração (Caminhões)")
  st.write("Espaço com 40 linhas para controle detalhado de cada carga.")

  st.session_state.df_racao = st.data_editor(
      st.session_state.df_racao,
      num_rows="fixed",
      use_container_width=True,
      key="editor_racao",
  )

  t_racao_g1 = st.session_state.df_racao["Granja 1 (Kg)"].sum()
  t_racao_g2 = st.session_state.df_racao["Granja 2 (Kg)"].sum()
  st.success(
      f"**Total de Ração Recebida:** Granja 1: {t_racao_g1:,.1f} kg | Granja 2:"
      f" {t_racao_g2:,.1f} kg | **Total Geral:**"
      f" {t_racao_g1 + t_racao_g2:,.1f} kg"
  )

# ==================== 4. BALANÇA ====================
elif menu == "⚖️ Balança":
  st.subheader("Pesagens Semanais (Até 45 Dias)")
  st.write("Insira o peso médio (em gramas) registado nas pesagens de 7 em 7 dias.")

  st.session_state.df_balanca = st.data_editor(
      st.session_state.df_balanca,
      num_rows="fixed",
      use_container_width=True,
      key="editor_balanca",
  )

# ==================== 5. CONVERSÃO ====================
elif menu == "🧮 Conversão":
  st.subheader("Conversão Alimentar Automatizada")
  st.write(
      "Esta área está totalmente interligada com a ração que chega e as aves"
      " alojadas/mortas."
  )

  total_racao_geral = (
      st.session_state.df_racao["Granja 1 (Kg)"].sum()
      + st.session_state.df_racao["Granja 2 (Kg)"].sum()
  )
  total_alojadas = (
      st.session_state.lote_config["aves_g1"]
      + st.session_state.lote_config["aves_g2"]
  )
  total_mortas = (
      st.session_state.df_mortalidade["Granja 1"].sum()
      + st.session_state.df_mortalidade["Granja 2"].sum()
  )
  saldo_atual = total_alojadas - total_mortas

  col1, col2, col3 = st.columns(3)
  col1.metric("Ração Total (Kg)", f"{total_racao_geral:,.1f}")
  col2.metric("Saldo de Aves", f"{saldo_atual:,}")

  # Estimativa baseada no peso médio atual ou padrão
  peso_medio_recente = 2200.0  # Exemplo em gramas
  if not st.session_state.df_balanca.empty:
    ultimos_pesos = [
        p
        for p in list(
            st.session_state.df_balanca["Granja 1 (g)"]
        )
        + list(st.session_state.df_balanca["Granja 2 (g)"])
        if p > 0
    ]
    if ultimos_pesos:
      peso_medio_recente = ultimos_pesos[-1]

  peso_total_vivo_kg = (saldo_atual * peso_medio_recente) / 1000.0
  col3.metric("Peso Vivo Estimado (Kg)", f"{peso_total_vivo_kg:,.1f}")

  if peso_total_vivo_kg > 0:
    ca = total_racao_geral / peso_total_vivo_kg
    st.markdown(
        f"""
        <div style="background-color: #2b8a3e; padding: 20px; border-radius: 10px; color: white; text-align: center; margin-top: 20px;">
            <h3>📊 Conversão Alimentar Calculada: {ca:.3f}</h3>
            <p style="margin:0;">(Ração Total Consumida ÷ Peso Vivo Total do Lote)</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
  else:
    st.warning(
        "Insira dados de ração e pesagem para calcular a conversão alimentar."
    )

# ==================== 6. HISTÓRICO ====================
elif menu == "📂 Histórico":
  st.subheader("Histórico de Lotes Anteriores")
  df_historico = pd.DataFrame({
      "Lote": ["Lote Anterior 01", "Lote Anterior 02"],
      "Início": ["10/06/2026", "15/07/2026"],
      "Aves Alojadas": [120000, 123900],
      "Conversão": [1.510, 1.480],
  })
  st.dataframe(df_historico, use_container_width=True, hide_index=True)
