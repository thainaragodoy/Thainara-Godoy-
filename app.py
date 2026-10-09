import json
import os
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# Importa o módulo isolado de autenticação
from auth import carregar_utilizadores, gerenciar_autenticacao, salvar_utilizador

st.set_page_config(
    page_title="Sistema de Gestão Avícola Profissional", layout="wide"
)

# Executa o controlo de login persistente de forma segura
esta_logado = gerenciar_autenticacao()

# =====================================================================
# 1. MÓDULO DE ESTILO (CSS RESPONSIVO E TEMA CLARO/ESCURO)
# =====================================================================
FUNDO_URL = "fundo_pintinhos.png"

st.markdown(
    f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.90), rgba(240, 242, 245, 0.92)), url("{FUNDO_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #212529 !important;
    }}
    @media (prefers-color-scheme: dark) {{
        .stApp {{
            background: linear-gradient(rgba(15, 17, 21, 0.92), rgba(22, 27, 34, 0.95)), url("{FUNDO_URL}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: #f8f9fa !important;
        }}
    }}
    p, span, label, h1, h2, h3, h4, h5, h6 {{ color: inherit !important; }}
    div[data-baseweb="tab-highlight"] {{ background-color: #495057 !important; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# =====================================================================
# 2. MÓDULO DE DADOS OPERACIONAIS (JSON)
# =====================================================================
ARQ_DADOS = "dados_granja.json"


def carregar_dados_operacionais():
  """Gere exclusivamente as informações operacionais da granja (dados_granja.json)"""
  if os.path.exists(ARQ_DADOS):
    try:
      with open(ARQ_DADOS, "r", encoding="utf-8") as f:
        return json.load(f)
    except:
      pass
  return None


def guardar_dados_operacionais():
  """Salva o estado atual da granja no ficheiro JSON"""
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
  with open(ARQ_DADOS, "w", encoding="utf-8") as f:
    json.dump(dados_para_salvar, f, ensure_ascii=False, indent=4)


# =====================================================================
# 3. INICIALIZAÇÃO DOS DADOS DO APLICATIVO
# =====================================================================
dados_salvos = carregar_dados_operacionais()

aves_iniciais = {f"Granja {i}": (62000 if i <= 2 else 0) for i in range(1, 11)}

if "lote_config" not in st.session_state:
  st.session_state.lote_config = (
      dados_salvos.get("lote_config")
      if dados_salvos
      else {
          "sitio": "Sítio Boa Vista",
          "lote": "Lote 01 - NÚCLEO 1",
          "inicio": "23/08/2026",
          "num_granjas": 2,
          "aves": aves_iniciais,
          "estoque_silo": {f"Granja {i}": 0.0 for i in range(1, 11)},
      }
  )

if "historico_lotes" not in st.session_state:
  st.session_state.historico_lotes = (
      dados_salvos.get("historico_lotes")
      if dados_salvos
      else [
          {
              "Lote": "Lote Anterior 01",
              "Início": "10/06/2026",
              "Aves Alojadas": 120000,
              "Total Aves Mortas": 2400,
              "Ração Consumida (Kg)": 180000.0,
              "Conversão Final": 1.510,
              "R$ por Cabeça": 1.92,
              "Comissão Total (R$)": 230400.0,
          }
      ]
  )

if "df_mortalidade" not in st.session_state:
  st.session_state.df_mortalidade = (
      pd.DataFrame(dados_salvos["df_mortalidade"])
      if dados_salvos
      else pd.DataFrame(
          {"Dia": [f"Dia {i}" for i in range(1, 46)]}
          | {f"Granja {i}": [0] * 45 for i in range(1, 11)}
      )
  )

if "df_racao" not in st.session_state:
  st.session_state.df_racao = (
      pd.DataFrame(dados_salvos["df_racao"])
      if dados_salvos
      else pd.DataFrame(
          {
              "Nº Caminhão / Nota": [
                  f"Caminhão {i}" if i <= 5 else "" for i in range(1, 41)
              ],
              "Data": ["" for _ in range(40)],
          }
          | {f"Granja {i} (Kg)": [0.0] * 40 for i in range(1, 11)}
          | {"Fórmula / Tipo": ["" for _ in range(40)]}
      )
  )

if "df_balanca" not in st.session_state:
  st.session_state.df_balanca = (
      pd.DataFrame(dados_salvos["df_balanca"])
      if dados_salvos
      else pd.DataFrame(
          {
              "Semana / Idade": [
                  "1ª Semana (7 dias)",
                  "2ª Semana (14 dias)",
                  "3ª Semana (21 dias)",
                  "4ª Semana (28 dias)",
                  "5ª Semana (35 dias)",
                  "6ª Semana (42 dias)",
              ]
          }
          | {f"Granja {i} (Peso g)": [0.0] * 6 for i in range(1, 11)}
      )
  )

if "df_medicacao" not in st.session_state:
  st.session_state.df_medicacao = (
      pd.DataFrame(dados_salvos["df_medicacao"])
      if dados_salvos
      else pd.DataFrame({
          "Dia": [f"Dia {i}" for i in range(1, 46)],
          "Medicação / Produto": ["" for _ in range(45)],
          "Dosagem / Quantidade": ["" for _ in range(45)],
          "Observações Aplicação": ["" for _ in range(45)],
      })
  )

if "lembretes_manutencao" not in st.session_state:
  st.session_state.lembretes_manutencao = (
      dados_salvos.get("lembretes_manutencao", "- Verificar bicos de nipple.")
      if dados_salvos
      else "- Verificar bicos de nipple."
  )

if "anotacoes_financeiras" not in st.session_state:
  st.session_state.anotacoes_financeiras = (
      dados_salvos.get("anotacoes_financeiras")
      if dados_salvos
      else {
          "sitio": "Sítio Boa Vista",
          "qtd_alojada": 124000,
          "qtd_abatidas": 120000,
          "conversao_lote": 1.520,
          "pagamento_ave": 1.95,
          "valor_final": 234000.0,
      }
  )


# =====================================================================
# 4. TELA DE AUTENTICAÇÃO (LOGIN / REGISTO)
# =====================================================================
if not st.session_state.autenticado:
  st.markdown(
      """
        <div style="background: linear-gradient(135deg, #343a40 0%, #212529 100%); padding: 30px; border-radius: 12px; color: white; text-align: center; margin-bottom: 25px;">
            <h2 style="margin:0; color: white;">🐔 Sistema de Gestão Avícola Profissional</h2>
            <p style="margin:8px 0 0 0; color: #f8f9fa;">Plataforma de controlo operacional e financeiro</p>
        </div>
        """,
      unsafe_allow_html=True,
  )

  _, col_centro, _ = st.columns([1, 2.2, 1])
  with col_centro:
    aba_login, aba_registo = st.tabs(["🔐 Entrar na Conta", "📝 Criar Registo"])

    with aba_login:
      email_l = st.text_input("E-mail", key="l_email")
      senha_l = st.text_input("Senha", type="password", key="l_senha")
      st.write("")
      if st.button("Entrar no Sistema", type="primary", use_container_width=True):
        base_u = carregar_utilizadores()
        if email_l in base_u and base_u[email_l]["senha"] == senha_l:
          st.session_state.autenticado = True
          u_data = base_u[email_l]
          st.session_state.utilizador_atual = {
              "email": email_l,
              "nome": u_data["nome"],
              "sitio": u_data["sitio"],
              "perfil": u_data.get("perfil", "Patrão / Dono"),
          }
          js_gravar = f"""
                <script>
                localStorage.setItem('granja_user_email', '{email_l}');
                window.parent.location.href = window.parent.location.pathname + '?user_email={email_l}';
                </script>
                """
          components.html(js_gravar, height=0)
          st.success("Login efetuado com sucesso!")
          st.rerun()
        else:
          st.error("E-mail ou senha incorretos.")

    with aba_registo:
      nome_c = st.text_input("Nome do Granjeiro", key="r_nome")
      sitio_c = st.text_input("Nome do Sítio", key="r_sitio")
      idade_c = st.number_input("Idade", min_value=1, max_value=120, value=25)
      perfil_c = st.selectbox(
          "Perfil de Acesso", ["Patrão / Dono", "Funcionário / Granjeiro"]
      )
      email_c = st.text_input("E-mail", key="r_email")
      senha_c = st.text_input("Senha", type="password", key="r_senha")
      st.write("")
      if st.button(
          "Registar e Aceder", type="primary", use_container_width=True
      ):
        base_u = carregar_utilizadores()
        if idade_c < 18:
          st.error("Tem de ser maior de idade para registar.")
        elif email_c in base_u:
          st.error("Este e-mail já está registado.")
        elif not nome_c or not sitio_c or not email_c or not senha_c:
          st.warning("Preencha todos os campos obrigatórios.")
        else:
          salvar_utilizador(email_c, senha_c, nome_c, sitio_c, perfil_c)
          st.session_state.autenticado = True
          st.session_state.utilizador_atual = {
              "email": email_c,
              "nome": nome_c,
              "sitio": sitio_c,
              "perfil": perfil_c,
          }
          guardar_dados_operacionais()
          js_gravar = f"""
                <script>
                localStorage.setItem('granja_user_email', '{email_c}');
                window.parent.location.href = window.parent.location.pathname + '?user_email={email_c}';
                </script>
                """
          components.html(js_gravar, height=0)
          st.success("Conta criada com sucesso!")
          st.rerun()

# =====================================================================
# 5. APLICAÇÃO PRINCIPAL (INTERFACE E FUNCIONALIDADES)
# =====================================================================
else:
  perfil_atual = st.session_state.utilizador_atual.get(
      "perfil", "Patrão / Dono"
  )

  col_h1, col_h2 = st.columns([4, 1])
  with col_h1:
    st.markdown(
        f"""
        <div style="background-color: #343a40; padding: 12px; border-radius: 8px; color: white;">
            <h4 style="margin:0; color: white;">📦 Sítio: {st.session_state.lote_config['sitio']} | Lote: {st.session_state.lote_config['lote']}</h4>
            <p style="margin:0; font-size: 12px; color: #f8f9fa;">Utilizador: {st.session_state.utilizador_atual.get('nome')} | <b>Perfil: {perfil_atual}</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )
  with col_h2:
    if st.button("🚪 Sair", type="secondary"):
      js_sair = """
            <script>
            localStorage.removeItem('granja_user_email');
            window.parent.location.href = window.parent.location.pathname;
            </script>
            """
      components.html(js_sair, height=0)
      st.session_state.autenticado = False
      st.session_state.utilizador_atual = {}
      st.rerun()

  st.write("")

  if perfil_atual == "Patrão / Dono":
    menus = [
        "🏠 Início",
        "📉 Mortalidade",
        "🚚 Ração & Estoque",
        "⚖️ Balança",
        "🧮 Conversão",
        "📝 Observações",
        "💰 Fechamento & Acerto",
        "📂 Histórico & Estatísticas",
    ]
  else:
    menus = [
        "🏠 Início",
        "📉 Mortalidade",
        "🚚 Ração & Estoque",
        "⚖️ Balança",
        "🧮 Conversão",
        "📝 Observações",
        "📂 Histórico & Estatísticas",
    ]

  menu = st.radio(
      "Navegação", menus, horizontal=True, label_visibility="collapsed"
  )
  st.divider()

  num_g = st.session_state.lote_config["num_granjas"]
  granjas_ativas = [f"Granja {i}" for i in range(1, num_g + 1)]

  total_aloj = sum(
      st.session_state.lote_config["aves"][g] for g in granjas_ativas
  )
  total_mortes = sum(
      st.session_state.df_mortalidade[g].sum() for g in granjas_ativas
  )
  total_vivas = total_aloj - total_mortes
  racao_chegada = sum(
      st.session_state.df_racao[f"{g} (Kg)"].sum() for g in granjas_ativas
  )
  estoque_silo = sum(
      st.session_state.lote_config["estoque_silo"][g] for g in granjas_ativas
  )
  racao_utilizada = max(0.0, racao_chegada - estoque_silo)

  # [MENU 1] INÍCIO
  if menu == "🏠 Início":
    st.subheader("Configuração do Sítio, Lote e Aviários")
    with st.form("cfg_lote"):
      s_in = st.text_input(
          "Nome do Sítio", value=st.session_state.lote_config["sitio"]
      )
      l_in = st.text_input(
          "Identificação do Lote", value=st.session_state.lote_config["lote"]
      )
      n_granjas_in = st.selectbox(
          "Número de Granjas Ativas (1 a 10)",
          options=list(range(1, 11)),
          index=num_g - 1,
      )

      st.markdown("---")
      st.write("### Aves Alojadas por Granja")
      aves_temp = {}
      for i in range(1, n_granjas_in + 1):
        g_nome = f"Granja {i}"
        val_atual = int(st.session_state.lote_config["aves"].get(g_nome, 0))
        aves_temp[g_nome] = st.number_input(
            f"Aves - {g_nome}", value=val_atual, step=100
        )

      if st.form_submit_button("Atualizar Informações"):
        st.session_state.lote_config["sitio"] = s_in
        st.session_state.lote_config["lote"] = l_in
        st.session_state.lote_config["num_granjas"] = n_granjas_in
        for g_nome, val in aves_temp.items():
          st.session_state.lote_config["aves"][g_nome] = val
        guardar_dados_operacionais()
        st.success("Informações atualizadas com sucesso!")
        st.rerun()

  # [MENU 2] MORTALIDADE
  elif menu == "📉 Mortalidade":
    st.subheader("Controle Diário de Mortalidade (45 Dias)")
    cols_m = ["Dia"] + granjas_ativas
    df_m_edit = st.data_editor(
        st.session_state.df_mortalidade[cols_m],
        num_rows="fixed",
        use_container_width=True,
    )
    if not df_m_edit.equals(st.session_state.df_mortalidade[cols_m]):
      for g in granjas_ativas:
        st.session_state.df_mortalidade[g] = df_m_edit[g]
      guardar_dados_operacionais()

  # [MENU 3] RAÇÃO & ESTOQUE
  elif menu == "🚚 Ração & Estoque":
    st.subheader("Gestão de Cargas de Ração e Estoque no Silo")
    with st.expander("📦 Atualizar Silos", expanded=True):
      mudou = False
      for g in granjas_ativas:
        val_s = st.number_input(
            f"Sobra Silo - {g} (Kg)",
            value=float(
                st.session_state.lote_config["estoque_silo"].get(g, 0.0)
            ),
            step=50.0,
            key=f"s_{g}",
        )
        if (
            val_s
            != st.session_state.lote_config["estoque_silo"].get(g, 0.0)
        ):
          st.session_state.lote_config["estoque_silo"][g] = val_s
          mudou = True
      if mudou:
        guardar_dados_operacionais()

    cols_r = (
        ["Nº Caminhão / Nota", "Data"]
        + [f"{g} (Kg)" for g in granjas_ativas]
        + ["Fórmula / Tipo"]
    )
    df_r_edit = st.data_editor(
        st.session_state.df_racao[cols_r],
        num_rows="fixed",
        use_container_width=True,
    )
    if not df_r_edit.equals(st.session_state.df_racao[cols_r]):
      for c in cols_r:
        st.session_state.df_racao[c] = df_r_edit[c]
      guardar_dados_operacionais()

  # [MENU 4] BALANÇA
  elif menu == "⚖️ Balança":
    st.subheader("Pesagens Semanais")
    cols_b = ["Semana / Idade"] + [f"{g} (Peso g)" for g in granjas_ativas]
    df_b_edit = st.data_editor(
        st.session_state.df_balanca[cols_b],
        num_rows="fixed",
        use_container_width=True,
    )
    if not df_b_edit.equals(st.session_state.df_balanca[cols_b]):
      for c in cols_b:
        st.session_state.df_balanca[c] = df_b_edit[c]
      guardar_dados_operacionais()

  # [MENU 5] CONVERSÃO
  elif menu == "🧮 Conversão":
    st.subheader("Análise de Conversão Alimentar")
    analise = []
    limites = [7, 14, 21, 28, 35, 42]
    for i, d in enumerate(limites):
      v_d = 0
      for g in granjas_ativas:
        v_d += (
            st.session_state.lote_config["aves"][g]
            - st.session_state.df_mortalidade[g].head(d).sum()
        )
      p_semana = [
          st.session_state.df_balanca.loc[i, f"{g} (Peso g)"]
          for g in granjas_ativas
          if st.session_state.df_balanca.loc[i, f"{g} (Peso g)"] > 0
      ]
      p_medio = sum(p_semana) / len(p_semana) if p_semana else 0.0
      fator = min(1.0, (i + 1) / 6.0)
      r_acum = max(0.0, racao_utilizada * fator)
      biomassa = (v_d * p_medio) / 1000.0
      ca = (r_acum / biomassa) if biomassa > 0 else 0.0
      analise.append({
          "Período": f"Semana {i+1} ({d} dias)",
          "Aves Vivas": v_d,
          "Peso Médio (g)": p_medio,
          "Peso Vivo Total (Kg)": round(biomassa, 1),
          "Ração Consumida (Kg)": round(r_acum, 1),
          "Conversão (CA)": round(ca, 3) if ca > 0 else "Pendente",
      })
    st.dataframe(
        pd.DataFrame(analise), use_container_width=True, hide_index=True
    )

  # [MENU 6] OBSERVAÇÕES
  elif menu == "📝 Observações":
    st.subheader("Observações e Lembretes")
    st.markdown("### 💊 Controle de Medicações")
    df_med_edit = st.data_editor(
        st.session_state.df_medicacao,
        num_rows="fixed",
        use_container_width=True,
    )
    if not df_med_edit.equals(st.session_state.df_medicacao):
      st.session_state.df_medicacao = df_med_edit
      guardar_dados_operacionais()

    st.write("")
    novo_l = st.text_area(
        "Lembretes e Manutenção",
        value=st.session_state.lembretes_manutencao,
        height=120,
    )
    if st.button("Guardar Lembretes"):
      st.session_state.lembretes_manutencao = novo_l
      guardar_dados_operacionais()
      st.success("Lembretes guardados!")

  # [MENU 7] FECHAMENTO (EXCLUSIVO PATRÃO)
  elif menu == "💰 Fechamento & Acerto" and perfil_atual == "Patrão / Dono":
    st.subheader("Fechamento do Lote")
    with st.form("form_fech"):
      c_fin = st.number_input(
          "Conversão Final", value=1.55, format="%.3f", step=0.005
      )
      v_cab = st.number_input(
          "Valor Recebido por Cabeça (R$)", value=1.95, format="%.2f", step=0.01
      )
      comissao_calc = total_aloj * v_cab
      st.write(f"💡 Comissão Calculada: R$ {comissao_calc:,.2f}")
      v_final = st.number_input(
          "Comissão Final Recebida (R$)",
          value=float(comissao_calc),
          step=100.0,
      )

      if st.form_submit_button("Guardar no Histórico"):
        st.session_state.historico_lotes.append({
            "Lote": st.session_state.lote_config["lote"],
            "Início": st.session_state.lote_config["inicio"],
            "Aves Alojadas": total_aloj,
            "Total Aves Mortas": total_mortes,
            "Ração Consumida (Kg)": racao_utilizada,
            "Conversão Final": c_fin,
            "R$ por Cabeça": v_cab,
            "Comissão Total (R$)": v_final,
        })
        guardar_dados_operacionais()
        st.success("Acerto guardado no histórico com sucesso!")

  # [MENU 8] HISTÓRICO & ESTATÍSTICAS
  elif menu == "📂 Histórico & Estatísticas":
    st.subheader("📊 Histórico de Lotes e Estatísticas")
    if not st.session_state.historico_lotes:
      st.info("Sem lotes arquivados.")
    else:
      df_h = pd.DataFrame(st.session_state.historico_lotes)
      st.dataframe(df_h, use_container_width=True, hide_index=True)
