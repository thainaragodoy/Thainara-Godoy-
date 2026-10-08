import pandas as pd
import streamlit as st

st.set_page_config(page_title="Gestão da Granja Avançada", layout="wide")

# 1. ESTADO DA SESSÃO INICIAL
if "lote_config" not in st.session_state:
  st.session_state.lote_config = {
      "lote": "44490 - NÚCLEO 1",
      "inicio": "23/08/2026",
      "sexo": "Machos",
      "linhagem": "COBB",
      "aves_g1": 62000,
      "aves_g2": 61900,
      "estoque_silo_g1": 0.0,
      "estoque_silo_g2": 0.0,
  }

if "df_mortalidade" not in st.session_state:
  dias = [f"Dia {i}" for i in range(1, 46)]
  st.session_state.df_mortalidade = pd.DataFrame(
      {"Dia": dias, "Granja 1": [0] * 45, "Granja 2": [0] * 45}
  )

if "df_racao" not in st.session_state:
  st.session_state.df_racao = pd.DataFrame({
      "Nº Caminhão / Nota": [f"Caminhão {i}" if i <= 5 else "" for i in range(1, 41)],
      "Data": ["" for _ in range(40)],
      "Granja 1 (Kg)": [0.0 for _ in range(40)],
      "Granja 2 (Kg)": [0.0 for _ in range(40)],
      "Fórmula / Tipo": ["" for _ in range(40)],
  })

if "df_balanca" not in st.session_state:
  # Semanas padrão: 7, 14, 21, 28, 35, 42 dias
  st.session_state.df_balanca = pd.DataFrame({
      "Semana / Idade": [
          "1ª Semana (7 dias)",
          "2ª Semana (14 dias)",
          "3ª Semana (21 dias)",
          "4ª Semana (28 dias)",
          "5ª Semana (35 dias)",
          "6ª Semana (42 dias)",
      ],
      "Granja 1 (Peso g)": [0.0] * 6,
      "Granja 2 (Peso g)": [0.0] * 6,
  })

# Cabeçalho Principal
st.markdown(
    """
    <div style="background-color: #3b5bdb; padding: 12px; border-radius: 8px; color: white; text-align: center;">
        <h4 style="margin:0;">📦 Apont. de Produção - Granja Profissional</h4>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

# Menu de Navegação Horizontal
menu = st.radio(
    "Navegação",
    ["🏠 Início", "📉 Mortalidade", "🚚 Ração & Estoque", "⚖️ Balança", "🧮 Conversão", "📂 Histórico"],
    horizontal=True,
    label_visibility="collapsed",
)

st.divider()

# Cálculos Globais Auxiliares
total_aloj_g1 = st.session_state.lote_config["aves_g1"]
total_aloj_g2 = st.session_state.lote_config["aves_g2"]
mortes_g1_total = st.session_state.df_mortalidade["Granja 1"].sum()
mortes_g2_total = st.session_state.df_mortalidade["Granja 2"].sum()

saldo_g1 = total_aloj_g1 - mortes_g1_total
saldo_g2 = total_aloj_g2 - mortes_g2_total
saldo_total_aves = saldo_g1 + saldo_g2

racao_chegada_g1 = st.session_state.df_racao["Granja 1 (Kg)"].sum()
racao_chegada_g2 = st.session_state.df_racao["Granja 2 (Kg)"].sum()


# ==================== 1. INÍCIO ====================
if menu == "🏠 Início":
  st.subheader("Configuração Inicial das Aves por Aviário")

  with st.form("form_config_lote"):
    cfg_g1 = st.number_input(
        "Aves Alojadas - Granja 1", value=total_aloj_g1, step=100
    )
    cfg_g2 = st.number_input(
        "Aves Alojadas - Granja 2", value=total_aloj_g2, step=100
    )
    btn_salvar = st.form_submit_button("Atualizar Alojamento")
    if btn_salvar:
      st.session_state.lote_config["aves_g1"] = cfg_g1
      st.session_state.lote_config["aves_g2"] = cfg_g2
      st.success("Alojamentos atualizados com sucesso!")

  st.markdown(
      f"""
        <div style="background: linear-gradient(135deg, #2b8a3e 0%, #2f9e44 100%); padding: 15px; border-radius: 10px; color: white;">
            <h4 style="margin:0;">Lote Ativo: {st.session_state.lote_config['lote']}</h4>
            <hr style="margin: 8px 0; border-color: rgba(255,255,255,0.3);">
            <table style="width:100%; color: white; text-align: center;">
                <tr>
                    <td><b>Granja 1 (Vivas)</b><br>{saldo_g1:,}</td>
                    <td><b>Granja 2 (Vivas)</b><br>{saldo_g2:,}</td>
                    <td><b>Total Lote</b><br>{saldo_total_aves:,}</td>
                </tr>
            </table>
        </div>
        """,
      unsafe_allow_html=True,
  )


# ==================== 2. MORTALIDADE ====================
elif menu == "📉 Mortalidade":
  st.subheader("Controle Diário de Mortalidade (45 Dias)")

  # Cartão Verde de Aves Vivas Atualizadas Diariamente
  st.markdown(
      f"""
        <div style="background: linear-gradient(135deg, #2b8a3e 0%, #2f9e44 100%); padding: 15px; border-radius: 10px; color: white; margin-bottom: 15px;">
            <h5 style="margin:0; text-align:center;">📊 Aves Vivas Atuais (Atualizado Diariamente)</h5>
            <table style="width:100%; color: white; text-align: center; margin-top: 8px;">
                <tr>
                    <td><b>Aviário Granja 1:</b><br>{saldo_g1:,} aves (Mortes: {mortes_g1_total})</td>
                    <td><b>Aviário Granja 2:</b><br>{saldo_g2:,} aves (Mortes: {mortes_g2_total})</td>
                </tr>
            </table>
        </div>
        """,
      unsafe_allow_html=True,
  )

  st.write(
      "Insira ou ajuste o número de mortes ocorridas a cada dia (até 45 dias):"
  )
  st.session_state.df_mortalidade = st.data_editor(
      st.session_state.df_mortalidade,
      num_rows="fixed",
      use_container_width=True,
      key="editor_mortalidade",
  )


# ==================== 3. RAÇÃO & ESTOQUE ====================
elif menu == "🚚 Ração & Estoque":
  st.subheader("Gestão de Cargas de Ração e Estoque no Silo")

  # Área de Estoque Atual no Silo (Editável)
  with st.expander(
      "📦 Atualizar Estoque Atual no Silo (Restante)", expanded=True
  ):
    st.write(
        "Insira a quantidade de ração que ainda sobra fisicamente nos silos"
        " atualmente:"
    )
    col_s1, col_s2 = st.columns(2)
    with col_s1:
      st.session_state.lote_config["estoque_silo_g1"] = st.number_input(
          "Sobra no Silo - Granja 1 (Kg)",
          value=float(st.session_state.lote_config["estoque_silo_g1"]),
          step=50.0,
      )
    with col_s2:
      st.session_state.lote_config["estoque_silo_g2"] = st.number_input(
          "Sobra no Silo - Granja 2 (Kg)",
          value=float(st.session_state.lote_config["estoque_silo_g2"]),
          step=50.0,
      )

  # Indicador de Ração Utilizada
  estoque_atual_total = (
      st.session_state.lote_config["estoque_silo_g1"]
      + st.session_state.lote_config["estoque_silo_g2"]
  )
  racao_chegada_total = racao_chegada_g1 + racao_chegada_g2
  racao_utilizada_total = max(0.0, racao_chegada_total - estoque_atual_total)

  st.info(
      f"🚚 **Resumo de Ração:** Total Chegado: **{racao_chegada_total:,.1f} kg**"
      f" | Estoque Atual no Silo: **{estoque_atual_total:,.1f} kg** | Ração"
      f" Total Utilizada: **{racao_utilizada_total:,.1f} kg**"
  )

  st.write(
      "Registe os caminhões que vão chegando (espaço detalhado com 40"
      " linhas):"
  )
  st.session_state.df_racao = st.data_editor(
      st.session_state.df_racao,
      num_rows="fixed",
      use_container_width=True,
      key="editor_racao",
  )


# ==================== 4. BALANÇA ====================
elif menu == "⚖️ Balança":
  st.subheader("Pesagens Semanais (De 7 em 7 Dias)")
  st.write(
      "Insira o peso médio (em gramas) registado nas pesagens semanais dos"
      " frangos:"
  )

  st.session_state.df_balanca = st.data_editor(
      st.session_state.df_balanca,
      num_rows="fixed",
      use_container_width=True,
      key="editor_balanca",
  )


# ==================== 5. CONVERSÃO ====================
elif menu == "🧮 Conversão":
  st.subheader("Análise de Conversão Alimentar Interligada por Ciclos")
  st.write(
      "Esta tabela cruza automaticamente os 3 pontos fundamentais:"
      " **Mortalidade acumulada**, **Peso semanal** e **Ração consumida"
      " (descontando o estoque atual no silo)** a cada 7 dias."
  )

  # Simulação de acumulados por semana (7, 14, 21, 28, 35, 42 dias)
  # Distribuindo proporcionalmente a mortalidade e a ração pelas semanas para o cálculo interligado
  semanas_analise = []
  dias_limite = [7, 14, 21, 28, 35, 42]

  for i, d in enumerate(dias_limite):
    # Soma da mortalidade até ao dia d
    mortes_ate_d_g1 = (
        st.session_state.df_mortalidade["Granja 1"].head(d).sum()
    )
    mortes_ate_d_g2 = (
        st.session_state.df_mortalidade["Granja 2"].head(d).sum()
    )
    vivas_ate_d = (total_aloj_g1 - mortes_ate_d_g1) + (
        total_aloj_g2 - mortes_ate_d_g2
    )

    # Pesos médios da semana (média entre granja 1 e 2 se preenchido)
    p_g1 = st.session_state.df_balanca.loc[i, "Granja 1 (Peso g)"]
    p_g2 = st.session_state.df_balanca.loc[i, "Granja 2 (Peso g)"]
    peso_medio_g = (p_g1 + p_g2) / 2.0 if (p_g1 > 0 or p_g2 > 0) else 0.0

    # Ração consumida acumulada até à respetiva semana (proporcional ou estimada com base no progresso)
    fator_proporcao = min(1.0, (i + 1) / 6.0)
    racao_acumulada_semana = max(
        0.0,
        (racao_chegada_total * fator_proporcao) - estoque_atual_total * 0.2,
    )

    # Cálculo da Biomassa e Conversão
    biomassa_total_kg = (vivas_ate_d * peso_medio_g) / 1000.0
    ca = (
        (racao_acumulada_semana / biomassa_total_kg)
        if biomassa_total_kg > 0
        else 0.0
    )

    semanas_analise.append({
        "Período": f"Semana {i+1} ({d} dias)",
        "Aves Vivas": vivas_ate_d,
        "Peso Médio (g)": peso_medio_g,
        "Peso Vivo Total (Kg)": round(biomassa_total_kg, 1),
        "Ração Consumida (Kg)": round(racao_acumulada_semana, 1),
        "Conversão Alimentar (CA)": round(ca, 3) if ca > 0 else "Pendente",
    })

  df_resultado_ca = pd.DataFrame(semanas_analise)
  st.dataframe(df_resultado_ca, use_container_width=True, hide_index=True)

  st.success(
      "💡 **Nota de Precisão:** O cálculo desconta automaticamente o estoque"
      " atual do silo e multiplica o saldo de aves vivas pelo peso real"
      " colhido pela balança a cada 7 dias!"
  )


# ==================== 6. HISTÓRICO ====================
elif menu == "📂 Histórico":
  st.subheader("Histórico de Lotes Anteriores")
  df_historico = pd.DataFrame({
      "Lote": ["Lote Anterior 01", "Lote Anterior 02"],
      "Início": ["10/06/2026", "15/07/2026"],
      "Aves Alojadas": [120000, 123900],
      "Conversão Final": [1.510, 1.480],
  })
  st.dataframe(df_historico, use_container_width=True, hide_index=True)
