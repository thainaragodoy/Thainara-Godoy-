import pandas as pd
import streamlit as st

st.set_page_config(page_title="Calculadora da Granja", layout="wide")

# Cabeçalho azul idêntico ao estilo da empresa
st.markdown(
    """
    <div style="background-color: #3b5bdb; padding: 15px; border-radius: 10px; color: white;">
        <h3>📦 Apont. de Produção</h3>
        <p style="margin:0;">Lote: 44490 - RICARDO CURY 02 - NÚCLEO 1 - G-4,5</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

# Cartão de resumo rápido (Início, Idade, Saldo, Sexo)
with st.container():
  st.markdown(
      """
        <div style="background: linear-gradient(135deg, #2b8a3e 0%, #2f9e44 100%); padding: 15px; border-radius: 10px; color: white;">
            <h4>Lote Ativo</h4>
            <table style="width:100%; color: white;">
                <tr>
                    <td><b>Inicio</b><br>23/08</td>
                    <td><b>Idade</b><br>47</td>
                    <td><b>Saldo</b><br>5.826</td>
                </tr>
            </table>
            <p style="margin-top: 10px; margin-bottom: 0;"><b>Sexo:</b> Machos</p>
        </div>
        """,
      unsafe_allow_html=True,
  )

st.write("")

# Secção recolhível: Alojamento (Estilo acordeão)
with st.expander("🏠 Alojamento", expanded=False):
  st.write("**Integrado:** RICARDO CURY")
  st.write("**Supervisor:** REGIÃO 07 - BEATRIZ MACEDO")
  st.write("**Linhagem:** COBB")
  st.write("**Aves alojadas:** 123.900")
  st.write("**Nº de aviários:** 5")

# Secção recolhível: Controle de Mortalidade
with st.expander("📉 Controle de Mortalidade", expanded=True):
  st.write("Clique sobre a semana para ver mais detalhes.")

  # Tabela limpa de mortalidade
  df_mortalidade = pd.DataFrame({
      "Semana": ["Totais", "04", "05"],
      "1ª Sem": [2323, 1027, 1296],
      "2ª Sem": [1311, 594, 717],
      "3ª Sem": [1062, 520, 542],
      "4ª Sem": [1134, 497, 637],
  })
  st.dataframe(df_mortalidade, use_container_width=True, hide_index=True)

# Secção recolhível: Pesagens Semanais
with st.expander("⚖️ Pesagens semanais", expanded=False):
  df_pesagens = pd.DataFrame({
      "Semana": ["Idade", "Peso", "04", "05"],
      "1ª Sem": ["7", "170,5", "143", "198"],
      "2ª Sem": ["14", "529,5", "515", "544"],
      "3ª Sem": ["21", "1.112", "1.126", "1.098"],
  })
  st.dataframe(df_pesagens, use_container_width=True, hide_index=True)
