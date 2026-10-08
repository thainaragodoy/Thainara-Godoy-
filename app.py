import pandas as pd
import streamlit as st

st.set_page_config(page_title="Gestão da Granja Profissional", layout="wide")

# 1. ESTADO DE AUTENTICAÇÃO E SESSÃO
if "autenticado" not in st.session_state:
  st.session_state.autenticado = False

if "utilizador_atual" not in st.session_state:
  st.session_state.utilizador_atual = {}

if "base_dados_utilizadores" not in st.session_state:
  st.session_state.base_dados_utilizadores = {
      "admin@granja.com": {
          "senha": "123",
          "nome": "João Granjeiro",
          "sitio": "Sítio Boa Vista",
      }
  }

# Inicializa o dicionário completo para até 10 granjas
aves_iniciais = {f"Granja {i}": (62000 if i <= 2 else 0) for i in range(1, 11)}
silos_iniciais = {f"Granja {i}": 0.0 for i in range(1, 11)}

if "lote_config" not in st.session_state:
  st.session_state.lote_config = {
      "sitio": "Sítio Boa Vista",
      "lote": "Lote 01 - NÚCLEO 1",
      "inicio": "23/08/2026",
      "num_granjas": 2,  # Abre por padrão com 2, editável até 10
      "aves": aves_iniciais,
      "estoque_silo": silos_iniciais,
  }

if "historico_lotes" not in st.session_state:
  st.session_state.historico_lotes = [
      {
          "Sítio": "Sítio Boa Vista",
          "Lote": "Lote Anterior 01",
          "Início": "10/06/2026",
          "Aves Alojadas": 120000,
          "Conversão Final": 1.510,
      }
  ]

if "df_mortalidade" not in st.session_state:
  dias = [f"Dia {i}" for i in range(1, 46)]
  dict_mort = {"Dia": dias}
  for i in range(1, 11):
    dict_mort[f"Granja {i}"] = [0] * 45
  st.session_state.df_mortalidade = pd.DataFrame(dict_mort)

if "df_racao" not in st.session_state:
  dict_rac = {
      "Nº Caminhão / Nota": [f"Caminhão {i}" if i <= 5 else "" for i in range(1, 41)],
      "Data": ["" for _ in range(40)],
  }
  for i in range(1, 11):
    dict_rac[f"Granja {i} (Kg)"] = [0.0 for _ in range(40)]
  dict_rac["Fórmula / Tipo"] = ["" for _ in range(40)]
  st.session_state.df_racao = pd.DataFrame(dict_rac)

if "df_balanca" not in st.session_state:
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
  dias_med = [f"Dia {i}" for i in range(1, 46)]
  st.session_state.df_medicacao = pd.DataFrame({
      "Dia": dias_med,
      "Medicação / Produto": ["" for _ in range(45)],
      "Dosagem / Quantidade": ["" for _ in range(45)],
      "Observações Aplicação": ["" for _ in range(45)],
  })

if "lembretes_manutencao" not in st.session_state:
  st.session_state.lembretes_manutencao = (
      "- Verificar bicos de nipple das granjas.\n- Agendar manutenção do"
      " gerador."
  )


# ==================== TELA DE LOGIN / CADASTRO ====================
if not st.session_state.autenticado:
  st.markdown(
      """
        <div style="background-color: #3b5bdb; padding: 15px; border-radius: 8px; color: white; text-align: center; margin-bottom: 20px;">
            <h3 style="margin:0;">🐔 Sistema de Gestão Avícola Profissional</h3>
            <p style="margin:0; font-size: 14px;">Faça login ou crie a sua conta para aceder à granja</p>
        </div>
        """,
      unsafe_allow_html=True,
  )

  tab_login, tab_cadastro = st.tabs(["🔐 Entrar", "📝 Criar Conta / Registo"])

  with tab_login:
    st.subheader("Aceder à Aplicação")
    email_login = st.text_input("E-mail", key="login_email")
    senha_login = st.text_input("Senha", type="password", key="login_senha")

    if st.button("Entrar", type="primary"):
      if email_login in st.session_state.base_dados_utilizadores:
        if (
            st.session_state.base_dados_utilizadores[email_login]["senha"]
            == senha_login
        ):
          st.session_state.autenticado = True
          dados_user = st.session_state.base_dados_utilizadores[email_login]
          st.session_state.utilizador_atual = {
              "email": email_login,
              "nome": dados_user["nome"],
              "sitio": dados_user["sitio"],
          }
          st.session_state.lote_config["sitio"] = dados_user["sitio"]
          st.success("Login efetuado com sucesso!")
          st.rerun()
        else:
          st.error("Senha incorreta.")
      else:
        st.error("E-mail não registado.")

  with tab_cadastro:
    st.subheader("Registo de Novo Granjeiro / Sítio")
    nome_cad = st.text_input("Nome do Granjeiro", key="reg_nome")
    sitio_cad = st.text_input("Nome do Sítio", key="reg_sitio")
    idade_cad = st.number_input(
        "Idade", min_value=1, max_value=120, value=25, key="reg_idade"
    )
    email_cad = st.text_input("E-mail", key="reg_email")
    senha_cad = st.text_input("Senha", type="password", key="reg_senha")

    if st.button("Registar e Entrar", type="primary"):
      if idade_cad < 18:
        st.error("Tem de ser maior de idade (18 anos) para registar uma conta.")
      elif not nome_cad or not sitio_cad or not email_cad or not senha_cad:
        st.warning("Por favor, preencha todos os campos obrigatórios.")
      elif email_cad in st.session_state.base_dados_utilizadores:
        st.error(
            "Este e-mail já está registado. Utilize a aba 'Entrar' para aceder."
        )
      else:
        st.session_state.base_dados_utilizadores[email_cad] = {
            "senha": senha_cad,
            "nome": nome_cad,
            "sitio": sitio_cad,
        }
        st.session_state.autenticado = True
        st.session_state.utilizador_atual = {
            "email": email_cad,
            "nome": nome_cad,
            "sitio": sitio_cad,
        }
        st.session_state.lote_config["sitio"] = sitio_cad
        st.success("Conta criada com sucesso! A entrar na aplicação...")
        st.rerun()

# ==================== APLICAÇÃO PRINCIPAL (PÓS-LOGIN) ====================
else:
  col_cab1, col_cab2 = st.columns([4, 1])
  with col_cab1:
    st.markdown(
        f"""
        <div style="background-color: #3b5bdb; padding: 12px; border-radius: 8px; color: white;">
            <h4 style="margin:0;">📦 Sítio: {st.session_state.lote_config['sitio']} | Lote: {st.session_state.lote_config['lote']}</h4>
            <p style="margin:0; font-size: 12px;">Granjeiro(a): {st.session_state.utilizador_atual.get('nome', 'Utilizador')}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
  with col_cab2:
    if st.button("🚪 Sair", type="secondary"):
      st.session_state.autenticado = False
      st.rerun()

  st.write("")

  menu = st.radio(
      "Navegação",
      [
          "🏠 Início",
          "📉 Mortalidade",
          "🚚 Ração & Estoque",
          "⚖️ Balança",
          "🧮 Conversão",
          "📝 Observações",
          "📂 Histórico",
      ],
      horizontal=True,
      label_visibility="collapsed",
  )

  st.divider()

  # Variáveis dinâmicas para o número de granjas ativas (1 a 10)
  num_g = st.session_state.lote_config["num_granjas"]
  granjas_ativas = [f"Granja {i}" for i in range(1, num_g + 1)]

  total_aloj_geral = sum(
      st.session_state.lote_config["aves"][g] for g in granjas_ativas
  )
  mortes_geral_total = sum(
      st.session_state.df_mortalidade[g].sum() for g in granjas_ativas
  )
  saldo_geral_vivas = total_aloj_geral - mortes_geral_total

  racao_chegada_geral = sum(
      st.session_state.df_racao[f"{g} (Kg)"].sum() for g in granjas_ativas
  )
  estoque_silo_geral = sum(
      st.session_state.lote_config["estoque_silo"][g] for g in granjas_ativas
  )
  racao_utilizada_geral = max(
      0.0, racao_chegada_geral - estoque_silo_geral
  )

  # ==================== 1. INÍCIO ====================
  if menu == "🏠 Início":
    st.subheader("Configuração do Sítio, Lote e Aviários/Granjas")

    with st.form("form_config_lote"):
      sitio_input = st.text_input(
          "Nome do Sítio", value=st.session_state.lote_config["sitio"]
      )
      lote_input = st.text_input(
          "Identificação do Lote", value=st.session_state.lote_config["lote"]
      )

      # Seletor flexível de 1 a 10 granjas
      num_granjas_input = st.selectbox(
          "Número de Granjas/Aviários Ativos (1 a 10)",
          options=list(range(1, 11)),
          index=num_g - 1,
      )

      st.markdown("---")
      st.write("### Aves Alojadas por Granja")
      aves_temp = {}

      # Organiza os inputs de aves em grelha de colunas (máx 3 colunas por linha visualmente)
      for i in range(1, num_granjas_input + 1):
        g_nome = f"Granja {i}"
        val_atual = int(st.session_state.lote_config["aves"].get(g_nome, 0))
        aves_temp[g_nome] = st.number_input(
            f"Aves alojadas - {g_nome}", value=val_atual, step=100
        )

      btn_salvar = st.form_submit_button("Atualizar Informações do Lote")
      if btn_salvar:
        st.session_state.lote_config["sitio"] = sitio_input
        st.session_state.lote_config["lote"] = lote_input
        st.session_state.lote_config["num_granjas"] = num_granjas_input
        for g_nome, val in aves_temp.items():
          st.session_state.lote_config["aves"][g_nome] = val
        st.success("Dados do sítio, lote e granjas atualizados com sucesso!")
        st.rerun()

    # Cartão de resumo verde dinâmico
    resumo_cards_html = ""
    for g in granjas_ativas:
      vivas_g = (
          st.session_state.lote_config["aves"][g]
          - st.session_state.df_mortalidade[g].sum()
      )
      resumo_cards_html += (
          f"<td><b>{g} (Vivas)</b><br>{vivas_g:,}</td>"
      )

    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #2b8a3e 0%, #2f9e44 100%); padding: 15px; border-radius: 10px; color: white;">
            <h4 style="margin:0;">🏡 Sítio: {st.session_state.lote_config['sitio']} | Lote: {st.session_state.lote_config['lote']}</h4>
            <hr style="margin: 8px 0; border-color: rgba(255,255,255,0.3);">
            <table style="width:100%; color: white; text-align: center;">
                <tr>
                    {resumo_cards_html}
                    <td><b>Total Lote</b><br>{saldo_geral_vivas:,}</td>
                </tr>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.markdown("---")
    st.subheader("⚠️ Zona de Gestão do Lote")

    if "confirmar_finalizacao" not in st.session_state:
      st.session_state.confirmar_finalizacao = False

    if not st.session_state.confirmar_finalizacao:
      if st.button("🏁 Finalizar Lote Atual", type="secondary"):
        st.session_state.confirmar_finalizacao = True
        st.rerun()
    else:
      st.warning(
          "⚠️ **Atenção:** Ao finalizar o lote, os dados atuais serão"
          " arquivados no Histórico e o sistema será redefinido. Deseja mesmo"
          " prosseguir?"
      )
      col_f1, col_f2 = st.columns(2)
      with col_f1:
        if st.button("✅ Sim, Finalizar Definitivamente", type="primary"):
          novo_historico = {
              "Sítio": st.session_state.lote_config["sitio"],
              "Lote": st.session_state.lote_config["lote"],
              "Início": st.session_state.lote_config["inicio"],
              "Aves Alojadas": total_aloj_geral,
              "Conversão Final": 1.490,
          }
          st.session_state.historico_lotes.append(novo_historico)
          st.session_state.lote_config["lote"] = "Novo Lote - NÚCLEO 1"
          for i in range(1, 11):
            st.session_state.df_mortalidade[f"Granja {i}"] = 0
          st.session_state.confirmar_finalizacao = False
          st.success("Lote finalizado e arquivado com sucesso!")
          st.rerun()
      with col_f2:
        if st.button("❌ Cancelar"):
          st.session_state.confirmar_finalizacao = False
          st.rerun()

  # ==================== 2. MORTALIDADE ====================
  elif menu == "📉 Mortalidade":
    st.subheader("Controle Diário de Mortalidade (45 Dias)")

    mortes_topo_html = ""
    for g in granjas_ativas:
      vivas_g = (
          st.session_state.lote_config["aves"][g]
          - st.session_state.df_mortalidade[g].sum()
      )
      mortes_topo_html += f"<td><b>{g}:</b><br>{vivas_g:,} aves (Mortes: {st.session_state.df_mortalidade[g].sum()})</td>"

    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #2b8a3e 0%, #2f9e44 100%); padding: 15px; border-radius: 10px; color: white; margin-bottom: 15px;">
            <h5 style="margin:0; text-align:center;">📊 Aves Vivas Atuais ({st.session_state.lote_config['sitio']})</h5>
            <table style="width:100%; color: white; text-align: center; margin-top: 8px;">
                <tr>
                    {mortes_topo_html}
                </tr>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )

    colunas_mostrar_mort = ["Dia"] + granjas_ativas
    st.session_state.df_mortalidade = st.data_editor(
        st.session_state.df_mortalidade[colunas_mostrar_mort],
        num_rows="fixed",
        use_container_width=True,
        key="editor_mortalidade",
    )

  # ==================== 3. RAÇÃO & ESTOQUE ====================
  elif menu == "🚚 Ração & Estoque":
    st.subheader("Gestão de Cargas de Ração e Estoque no Silo")

    with st.expander(
        "📦 Atualizar Estoque Atual nos Silos (Restante)", expanded=True
    ):
      for g in granjas_ativas:
        st.session_state.lote_config["estoque_silo"][g] = st.number_input(
            f"Sobra no Silo - {g} (Kg)",
            value=float(
                st.session_state.lote_config["estoque_silo"].get(g, 0.0)
            ),
            step=50.0,
        )

    st.info(
        f"🚚 **Resumo Geral:** Chegado: **{racao_chegada_geral:,.1f} kg** | Silo:"
        f" **{estoque_silo_geral:,.1f} kg** | Utilizada:"
        f" **{racao_utilizada_geral:,.1f} kg**"
    )

    colunas_mostrar_racao = (
        ["Nº Caminhão / Nota", "Data"]
        + [f"{g} (Kg)" for g in granjas_ativas]
        + ["Fórmula / Tipo"]
    )
    st.session_state.df_racao = st.data_editor(
        st.session_state.df_racao[colunas_mostrar_racao],
        num_rows="fixed",
        use_container_width=True,
        key="editor_racao",
    )

  # ==================== 4. BALANÇA ====================
  elif menu == "⚖️ Balança":
    st.subheader("Pesagens Semanais (De 7 em 7 Dias)")
    colunas_mostrar_bal = ["Semana / Idade"] + [
        f"{g} (Peso g)" for g in granjas_ativas
    ]
    st.session_state.df_balanca = st.data_editor(
        st.session_state.df_balanca[colunas_mostrar_bal],
        num_rows="fixed",
        use_container_width=True,
        key="editor_balanca",
    )

  # ==================== 5. CONVERSÃO ====================
  elif menu == "🧮 Conversão":
    st.subheader("Análise de Conversão Alimentar Interligada por Ciclos")

    semanas_analise = []
    dias_limite = [7, 14, 21, 28, 35, 42]

    for i, d in enumerate(dias_limite):
      vivas_d = 0
      for g in granjas_ativas:
        aloj_g = st.session_state.lote_config["aves"][g]
        mortes_g = st.session_state.df_mortalidade[g].head(d).sum()
        vivas_d += aloj_g - mortes_g

      pesos_semana = []
      for g in granjas_ativas:
        p_val = st.session_state.df_balanca.loc[i, f"{g} (Peso g)"]
        if p_val > 0:
          pesos_semana.append(p_val)
      peso_medio = (
          sum(pesos_semana) / len(pesos_semana) if pesos_semana else 0.0
      )

      fator = min(1.0, (i + 1) / 6.0)
      racao_acum = max(0.0, racao_utilizada_geral * fator)
      biomassa = (vivas_d * peso_medio) / 1000.0
      ca = (racao_acum / biomassa) if biomassa > 0 else 0.0

      semanas_analise.append({
          "Período": f"Semana {i+1} ({d} dias)",
          "Aves Vivas": vivas_d,
          "Peso Médio (g)": peso_medio,
          "Peso Vivo Total (Kg)": round(biomassa, 1),
          "Ração Consumida (Kg)": round(racao_acum, 1),
          "Conversão (CA)": round(ca, 3) if ca > 0 else "Pendente",
      })

    st.dataframe(
        pd.DataFrame(semanas_analise), use_container_width=True, hide_index=True
    )

  # ==================== 6. OBSERVAÇÕES ====================
  elif menu == "📝 Observações":
    st.subheader("Área de Observações e Lembretes")
    st.markdown("### 💊 Fase 1: Controle de Medicações e Aplicações (45 Dias)")
    st.session_state.df_medicacao = st.data_editor(
        st.session_state.df_medicacao,
        num_rows="fixed",
        use_container_width=True,
        key="editor_medicacao",
    )
    st.write("")
    st.markdown("---")
    st.markdown("### 📌 Fase 2: Lembretes e Manutenção")
    novo_lembrete = st.text_area(
        "Bloco de Notas / Manutenção",
        value=st.session_state.lembretes_manutencao,
        height=150,
    )
    if st.button("Guardar Lembretes"):
      st.session_state.lembretes_manutencao = novo_lembrete
      st.success("Lembretes atualizados com sucesso!")

  # ==================== 7. HISTÓRICO ====================
  elif menu == "📂 Histórico":
    st.subheader("Histórico de Lotes Anteriores")
    st.dataframe(
        pd.DataFrame(st.session_state.historico_lotes),
        use_container_width=True,
        hide_index=True,
    )
