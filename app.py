import json
import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Gestão da Granja Profissional", layout="wide")

# ==================== ESTILIZAÇÃO CSS ====================
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

    p, span, label, h1, h2, h3, h4, h5, h6 {{
        color: inherit !important;
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


# ==================== CONTROLE DE SESSÃO INTELIGENTE (COM LEMBRAR NESTE NAVEGADOR) ====================
if "autenticado" not in st.session_state:
  # Verifica se existe um login salvo na memória do navegador deste aparelho específico
  params = st.query_params
  saved_email = params.get("user_email", None)

  if saved_email:
    base_usuarios = carregar_utilizadores()
    if saved_email in base_usuarios:
      dados_user = base_usuarios[saved_email]
      st.session_state.autenticado = True
      st.session_state.utilizador_atual = {
          "email": saved_email,
          "nome": dados_user["nome"],
          "sitio": dados_user["sitio"],
          "perfil": dados_user.get("perfil", "Patrão / Dono"),
      }
    else:
      st.session_state.autenticado = False
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
            <h2 style="margin:0; color: white; font-size: 28px;">🐔 Sistema de Gestão Avícola Profissional</h2>
            <p style="margin:8px 0 0 0; color: #f8f9fa; font-size: 15px; opacity: 0.9;">Plataforma de controlo operacional e financeiro de lotes</p>
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
      lembrar_login = st.checkbox(
          "Lembrar de mim neste dispositivo", value=True
      )
      st.write("")

      if st.button("Entrar no Sistema", type="primary", use_container_width=True):
        base_usuarios = carregar_utilizadores()
        if email_login in base_usuarios:
          if base_usuarios[email_login]["senha"] == senha_login:
            st.session_state.autenticado = True
            dados_user = base_usuarios[email_login]
            st.session_state.utilizador_atual = {
                "email": email_login,
                "nome": dados_user["nome"],
                "sitio": dados_user["sitio"],
                "perfil": dados_user.get("perfil", "Patrão / Dono"),
            }
            if lembrar_login:
              st.query_params["user_email"] = email_login
            st.session_state.lote_config["sitio"] = dados_user["sitio"]
            st.success("Login efetuado com sucesso!")
            st.rerun()
          else:
            st.error("Senha incorreta.")
        else:
          st.error("E-mail não registado.")

    with tab_cadastro:
      st.write("")
      nome_cad = st.text_input("Nome do Granjeiro", key="reg_nome")
      sitio_cad = st.text_input("Nome do Sítio", key="reg_sitio")
      idade_cad = st.number_input(
          "Idade", min_value=1, max_value=120, value=25, key="reg_idade"
      )
      perfil_cad = st.selectbox(
          "Perfil de Acesso", ["Patrão / Dono", "Funcionário / Granjeiro"]
      )
      email_cad = st.text_input("E-mail", key="reg_email")
      senha_cad = st.text_input("Senha", type="password", key="reg_senha")
      st.write("")

      if st.button(
          "Registar e Aceder", type="primary", use_container_width=True
      ):
        base_usuarios = carregar_utilizadores()
        if idade_cad < 18:
          st.error(
              "Tem de ser maior de idade (18 anos) para registar uma conta."
          )
        elif not nome_cad or not sitio_cad or not email_cad or not senha_cad:
          st.warning("Por favor, preencha todos os campos obrigatórios.")
        elif email_cad in base_usuarios:
          st.error("Este e-mail já está registado. Utilize a aba 'Entrar'.")
        else:
          salvar_utilizador(
              email_cad, senha_cad, nome_cad, sitio_cad, perfil_cad
          )
          st.session_state.autenticado = True
          st.session_state.utilizador_atual = {
              "email": email_cad,
              "nome": nome_cad,
              "sitio": sitio_cad,
              "perfil": perfil_cad,
          }
          st.query_params["user_email"] = email_cad
          st.session_state.lote_config["sitio"] = sitio_cad
          guardar_dados_granja()
          st.success("Conta criada com sucesso! A entrar...")
          st.rerun()

# ==================== APLICAÇÃO PRINCIPAL (PÓS-LOGIN) ====================
else:
  perfil_atual = st.session_state.utilizador_atual.get(
      "perfil", "Patrão / Dono"
  )

  col_cab1, col_cab2 = st.columns([4, 1])
  with col_cab1:
    st.markdown(
        f"""
        <div style="background-color: #343a40; padding: 12px; border-radius: 8px; color: white;">
            <h4 style="margin:0; color: white;">📦 Sítio: {st.session_state.lote_config['sitio']} | Lote: {st.session_state.lote_config['lote']}</h4>
            <p style="margin:0; font-size: 12px; color: #f8f9fa;">Granjeiro(a): {st.session_state.utilizador_atual.get('nome', 'Utilizador')} &nbsp;|&nbsp; <b>Perfil: {perfil_atual}</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )
  with col_cab2:
    if st.button("🚪 Sair", type="secondary"):
      st.session_state.autenticado = False
      st.session_state.utilizador_atual = {}
      st.query_params.clear()
      st.rerun()

  st.write("")

  if perfil_atual == "Patrão / Dono":
    lista_menus = [
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
    lista_menus = [
        "🏠 Início",
        "📉 Mortalidade",
        "🚚 Ração & Estoque",
        "⚖️ Balança",
        "🧮 Conversão",
        "📝 Observações",
        "📂 Histórico & Estatísticas",
    ]

  menu = st.radio(
      "Navegação", lista_menus, horizontal=True, label_visibility="collapsed"
  )

  st.divider()

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

      num_granjas_input = st.selectbox(
          "Número de Granjas/Aviários Ativos (1 a 10)",
          options=list(range(1, 11)),
          index=num_g - 1,
      )

      st.markdown("---")
      st.write("### Aves Alojadas por Granja")
      aves_temp = {}

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
        guardar_dados_granja()
        st.success("Dados do sítio, lote e granjas atualizados com sucesso!")
        st.rerun()

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
        <div style="background: linear-gradient(135deg, #495057 0%, #343a40 100%); padding: 15px; border-radius: 10px; color: white;">
            <h4 style="margin:0; color: white;">🏡 Sítio: {st.session_state.lote_config['sitio']} | Lote: {st.session_state.lote_config['lote']}</h4>
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

    if perfil_atual == "Patrão / Dono":
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
                "Lote": st.session_state.lote_config["lote"],
                "Início": st.session_state.lote_config["inicio"],
                "Aves Alojadas": total_aloj_geral,
                "Total Aves Mortas": mortes_geral_total,
                "Ração Consumida (Kg)": racao_utilizada_geral,
                "Conversão Final": 1.500,
                "R$ por Cabeça": 1.95,
                "Comissão Total (R$)": total_aloj_geral * 1.95,
            }
            st.session_state.historico_lotes.append(novo_historico)
            st.session_state.lote_config["lote"] = "Novo Lote - NÚCLEO 1"
            for i in range(1, 11):
              st.session_state.df_mortalidade[f"Granja {i}"] = 0
            st.session_state.confirmar_finalizacao = False
            guardar_dados_granja()
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
        <div style="background: linear-gradient(135deg, #495057 0%, #343a40 100%); padding: 15px; border-radius: 10px; color: white; margin-bottom: 15px;">
            <h5 style="margin:0; text-align:center; color: white;">📊 Aves Vivas Atuais ({st.session_state.lote_config['sitio']})</h5>
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
    df_mort_editado = st.data_editor(
        st.session_state.df_mortalidade[colunas_mostrar_mort],
        num_rows="fixed",
        use_container_width=True,
        key="editor_mortalidade",
    )
    if not df_mort_editado.equals(
        st.session_state.df_mortalidade[colunas_mostrar_mort]
    ):
      for g in granjas_ativas:
        st.session_state.df_mortalidade[g] = df_mort_editado[g]
      guardar_dados_granja()

  # ==================== 3. RAÇÃO & ESTOQUE ====================
  elif menu == "🚚 Ração & Estoque":
    st.subheader("Gestão de Cargas de Ração e Estoque no Silo")

    with st.expander(
        "📦 Atualizar Estoque Atual nos Silos (Restante)", expanded=True
    ):
      mudou_silo = False
      for g in granjas_ativas:
        novo_val_silo = st.number_input(
            f"Sobra no Silo - {g} (Kg)",
            value=float(
                st.session_state.lote_config["estoque_silo"].get(g, 0.0)
            ),
            step=50.0,
            key=f"silo_{g}",
        )
        if (
            novo_val_silo
            != st.session_state.lote_config["estoque_silo"].get(g, 0.0)
        ):
          st.session_state.lote_config["estoque_silo"][g] = novo_val_silo
          mudou_silo = True
      if mudou_silo:
        guardar_dados_granja()

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
    df_rac_editado = st.data_editor(
        st.session_state.df_racao[colunas_mostrar_racao],
        num_rows="fixed",
        use_container_width=True,
        key="editor_racao",
    )
    if not df_rac_editado.equals(
        st.session_state.df_racao[colunas_mostrar_racao]
    ):
      for col in colunas_mostrar_racao:
        st.session_state.df_racao[col] = df_rac_editado[col]
      guardar_dados_granja()

  # ==================== 4. BALANÇA ====================
  elif menu == "⚖️ Balança":
    st.subheader("Pesagens Semanais (De 7 em 7 Dias)")
    colunas_mostrar_bal = ["Semana / Idade"] + [
        f"{g} (Peso g)" for g in granjas_ativas
    ]
    df_bal_editado = st.data_editor(
        st.session_state.df_balanca[colunas_mostrar_bal],
        num_rows="fixed",
        use_container_width=True,
        key="editor_balanca",
    )
    if not df_bal_editado.equals(
        st.session_state.df_balanca[colunas_mostrar_bal]
    ):
      for col in colunas_mostrar_bal:
        st.session_state.df_balanca[col] = df_bal_editado[col]
      guardar_dados_granja()

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
    df_med_editado = st.data_editor(
        st.session_state.df_medicacao,
        num_rows="fixed",
        use_container_width=True,
        key="editor_medicacao",
    )
    if not df_med_editado.equals(st.session_state.df_medicacao):
      st.session_state.df_medicacao = df_med_editado
      guardar_dados_granja()

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
      guardar_dados_granja()
      st.success("Lembretes atualizados com sucesso!")

    st.write("")
    st.markdown("---")
    st.markdown("### 💰 Fase 3: Anotações Financeiras e Resumo do Lote")

    with st.form("form_anotacoes_financeiras"):
      f_sitio = st.text_input(
          "Sítio", value=st.session_state.anotacoes_financeiras["sitio"]
      )
      col_fin1, col_fin2 = st.columns(2)
      with col_fin1:
        f_alojada = st.number_input(
            "Quantidade alojada",
            value=int(
                st.session_state.anotacoes_financeiras["qtd_alojada"]
            ),
            step=100,
        )
        f_abatidas = st.number_input(
            "Quantidade abatidas",
            value=int(
                st.session_state.anotacoes_financeiras["qtd_abatidas"]
            ),
            step=100,
        )
        f_conversao = st.number_input(
            "Conversão do lote",
            value=float(
                st.session_state.anotacoes_financeiras["conversao_lote"]
            ),
            format="%.3f",
            step=0.005,
        )
      with col_fin2:
        f_pagamento = st.number_input(
            "Pagamento por ave (R$)",
            value=float(
                st.session_state.anotacoes_financeiras["pagamento_ave"]
            ),
            format="%.2f",
            step=0.01,
        )
        f_valor_final = st.number_input(
            "Valor final recebido (R$)",
            value=float(
                st.session_state.anotacoes_financeiras["valor_final"]
            ),
            format="%.2f",
            step=100.0,
        )

      btn_salvar_fin = st.form_submit_button(
          "Guardar Anotações Financeiras"
      )
      if btn_salvar_fin:
        st.session_state.anotacoes_financeiras = {
            "sitio": f_sitio,
            "qtd_alojada": f_alojada,
            "qtd_abatidas": f_abatidas,
            "conversao_lote": f_conversao,
            "pagamento_ave": f_pagamento,
            "valor_final": f_valor_final,
        }
        guardar_dados_granja()
        st.success("Anotações financeiras guardadas com sucesso!")

  # ==================== 7. FECHAMENTO & ACERTO (EXCLUSIVO PATRÃO) ====================
  elif menu == "💰 Fechamento & Acerto" and perfil_atual == "Patrão / Dono":
    st.subheader("Fechamento do Lote e Acerto com a Integradora")
    st.info(
        "Registe abaixo os dados comerciais do lote encerrado (empresa/integradora,"
        " conversão obtida, fator de produção e valores de comissão recebidos)."
    )

    with st.form("form_fechamento_lote"):
      col_f_1, col_f_2 = st.columns(2)
      with col_f_1:
        integradora_input = st.text_input(
            "Nome da Integradora (ex: Zanqueta)", value="Zanqueta"
        )
        conv_final_input = st.number_input(
            "Conversão Alimentar (CA) Final",
            value=1.55,
            format="%.3f",
            step=0.005,
        )
      with col_f_2:
        fator_prod_input = st.number_input(
            "Fator de Produção (FP)", value=432.5, format="%.1f", step=0.5
        )
        val_cabeca_input = st.number_input(
            "Valor Recebido por Cabeça (R$)",
            value=1.95,
            format="%.2f",
            step=0.01,
        )

      comissao_total_calc = total_aloj_geral * val_cabeca_input
      st.write(
          f"💡 **Comissão Total Estimada Calculada:** R$"
          f" {comissao_total_calc:,.2f} (para {total_aloj_geral:,} aves)"
      )
      comissao_final_input = st.number_input(
          "Valor Final Recebido da Comissão (R$)",
          value=float(comissao_total_calc),
          step=100.0,
      )

      btn_salvar_fechamento = st.form_submit_button(
          "Guardar Acerto no Histórico"
      )
      if btn_salvar_fechamento:
        novo_acerto = {
            "Lote": st.session_state.lote_config["lote"],
            "Início": st.session_state.lote_config["inicio"],
            "Aves Alojadas": total_aloj_geral,
            "Total Aves Mortas": mortes_geral_total,
            "Ração Consumida (Kg)": racao_utilizada_geral,
            "Conversão Final": conv_final_input,
            "R$ por Cabeça": val_cabeca_input,
            "Comissão Total (R$)": comissao_final_input,
        }
        st.session_state.historico_lotes.append(novo_acerto)
        guardar_dados_granja()
        st.success(
            "Acerto financeiro e comercial guardado com sucesso no Histórico!"
        )

  # ==================== 8. HISTÓRICO & ESTATÍSTICAS ====================
  elif menu == "📂 Histórico & Estatísticas":
    st.subheader(
        "📊 Histórico de Lotes e Análise Estatística / Filtros Comparativos"
    )

    if not st.session_state.historico_lotes:
      st.info("Ainda não existem lotes arquivados no histórico.")
    else:
      df_hist = pd.DataFrame(st.session_state.historico_lotes)

      st.markdown("### 🏆 Destaques Estatísticos dos Lotes")
      col_e1, col_e2, col_e3, col_e4 = st.columns(4)

      lote_menor_morte = df_hist.loc[df_hist["Total Aves Mortas"].idxmin()]
      with col_e1:
        st.metric(
            label="📉 Menor Mortalidade",
            value=lote_menor_morte["Lote"],
            delta=f"{lote_menor_morte['Total Aves Mortas']:,} mortes",
            delta_color="inverse",
        )

      lote_maior_pagto = df_hist.loc[df_hist["R$ por Cabeça"].idxmax()]
      with col_e2:
        st.metric(
            label="💰 Maior Pagamento/Ave",
            value=lote_maior_pagto["Lote"],
            delta=f"R$ {lote_maior_pagto['R$ por Cabeça']:.2f} por ave",
        )

      lote_maior_aloj = df_hist.loc[df_hist["Aves Alojadas"].idxmax()]
      with col_e3:
        st.metric(
            label="📈 Maior Alojamento",
            value=lote_maior_aloj["Lote"],
            delta=f"{lote_maior_aloj['Aves Alojadas']:,} aves",
        )

      lote_menos_racao = df_hist.loc[
          df_hist["Ração Consumida (Kg)"].idxmin()
      ]
      with col_e4:
        st.metric(
            label="🌾 Menor Consumo Ração",
            value=lote_menos_racao["Lote"],
            delta=f"{lote_menos_racao['Ração Consumida (Kg)']:,.0f} kg",
            delta_color="inverse",
        )

      st.write("")
      st.markdown("---")
      st.markdown("### 📋 Tabela Completa do Histórico de Lotes")
      st.dataframe(df_hist, use_container_width=True, hide_index=True)
