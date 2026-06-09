import streamlit as st
from database import (
    criar_tabelas,
    salvar_usuario,
    listar_usuarios,
    salvar_historico_pdi,
    listar_historico_pdi
)
from ai_service import gerar_pdi_com_ia

criar_tabelas()

st.set_page_config(
    page_title="PDI com IA para Carreira em TI",
    page_icon="💼",
    layout="wide"
)

st.title("💼 PDI com IA para Carreira em TI")

st.markdown("""
Aplicação desenvolvida para auxiliar estudantes e profissionais de tecnologia
na criação de um Plano de Desenvolvimento Individual com apoio de Inteligência Artificial.
""")

with st.sidebar:
    st.header("Sobre o projeto")

    st.write("""
    Este sistema utiliza IA generativa para analisar o perfil profissional do usuário
    e gerar um plano personalizado de desenvolvimento.
    """)

    st.subheader("Funcionalidades")
    st.write("""
    - Cadastro de usuário  
    - Geração de PDI com IA  
    - Sugestão de trilha de estudos  
    - Sugestão de certificações  
    - Histórico de PDIs gerados  
    - Download do plano  
    """)

    st.subheader("Tecnologias")
    st.write("""
    - Python  
    - Streamlit  
    - SQLite  
    - Gemini API  
    """)

aba_cadastro, aba_pdi, aba_historico = st.tabs([
    "👤 Cadastro",
    "🤖 Gerar PDI",
    "📚 Histórico"
])


with aba_cadastro:
    st.subheader("Cadastro do usuário")

    col1, col2 = st.columns(2)

    with col1:
        with st.form("form_usuario"):
            nome = st.text_input("Nome")
            cargo_atual = st.text_input("Cargo atual ou área de interesse")
            objetivo = st.text_area("Objetivo profissional")

            enviar = st.form_submit_button("Salvar usuário")

            if enviar:
                if nome and cargo_atual and objetivo:
                    usuario_id = salvar_usuario(nome, cargo_atual, objetivo)

                    st.success("Usuário salvo com sucesso.")
                    st.info(f"ID do usuário cadastrado: {usuario_id}")
                else:
                    st.warning("Preencha todos os campos para continuar.")

    with col2:
        st.info("""
        Nesta etapa, o usuário informa sua identificação básica e seu objetivo profissional.
        Esses dados serão usados pela IA para personalizar o Plano de Desenvolvimento Individual.
        """)

    st.divider()

    st.subheader("Usuários cadastrados")

    usuarios = listar_usuarios()

    if usuarios:
        for usuario in usuarios:
            id_usuario, nome, cargo_atual, objetivo, criado_em = usuario

            with st.expander(f"{nome} - {cargo_atual}"):
                st.write(f"**ID:** {id_usuario}")
                st.write(f"**Objetivo profissional:** {objetivo}")
                st.write(f"**Criado em:** {criado_em}")
    else:
        st.info("Nenhum usuário cadastrado ainda.")


with aba_pdi:
    st.subheader("Gerar Plano de Desenvolvimento Individual com IA")

    usuarios = listar_usuarios()

    if "ultimo_pdi" not in st.session_state:
        st.session_state.ultimo_pdi = None

    if usuarios:
        opcoes_usuarios = {
            f"{usuario[1]} - {usuario[2]}": usuario
            for usuario in usuarios
        }

        usuario_selecionado = st.selectbox(
            "Selecione o usuário",
            list(opcoes_usuarios.keys())
        )

        usuario = opcoes_usuarios[usuario_selecionado]

        usuario_id = usuario[0]
        nome = usuario[1]
        cargo_atual = usuario[2]
        objetivo = usuario[3]

        st.info(f"Objetivo profissional cadastrado: {objetivo}")

        with st.form("form_pdi"):
            competencias = st.text_area(
                "Quais competências ou tecnologias você já conhece?",
                placeholder="Exemplo: SQL, Python básico, lógica de programação, Git..."
            )

            dificuldades = st.text_area(
                "Quais são suas principais dificuldades atualmente?",
                placeholder="Exemplo: estudar com constância, aprender sozinho, falta de prática..."
            )

            certificacoes = st.text_input(
                "Tem interesse em alguma certificação?",
                placeholder="Exemplo: Oracle, AWS, Scrum, Azure, ITIL..."
            )

            disponibilidade = st.selectbox(
                "Quanto tempo você pode estudar por semana?",
                [
                    "Até 2 horas por semana",
                    "De 3 a 5 horas por semana",
                    "De 6 a 10 horas por semana",
                    "Mais de 10 horas por semana"
                ]
            )

            gerar = st.form_submit_button("Gerar PDI com IA")

        if gerar:
            if competencias and dificuldades:
                with st.spinner("Gerando PDI com Inteligência Artificial..."):
                    try:
                        resposta_ia = gerar_pdi_com_ia(
                            nome,
                            cargo_atual,
                            objetivo,
                            competencias,
                            dificuldades,
                            certificacoes,
                            disponibilidade
                        )

                        salvar_historico_pdi(
                            usuario_id,
                            competencias,
                            dificuldades,
                            certificacoes,
                            resposta_ia
                        )

                        st.session_state.ultimo_pdi = {
                            "usuario_id": usuario_id,
                            "nome": nome,
                            "cargo_atual": cargo_atual,
                            "objetivo": objetivo,
                            "competencias": competencias,
                            "dificuldades": dificuldades,
                            "certificacoes": certificacoes,
                            "disponibilidade": disponibilidade,
                            "resposta_ia": resposta_ia
                        }

                        st.success("PDI gerado e salvo com sucesso.")

                    except Exception as erro:
                        st.error("Não foi possível gerar o PDI.")
                        st.warning(str(erro))
            else:
                st.warning("Preencha pelo menos as competências e dificuldades.")

        if (
            st.session_state.ultimo_pdi
            and st.session_state.ultimo_pdi["usuario_id"] == usuario_id
        ):
            ultimo = st.session_state.ultimo_pdi

            st.subheader("Resultado gerado pela IA")
            st.markdown(ultimo["resposta_ia"])

            conteudo_download = f"""
PDI COM IA PARA CARREIRA EM TI

Usuário: {ultimo["nome"]}
Cargo atual ou área de interesse: {ultimo["cargo_atual"]}
Objetivo profissional: {ultimo["objetivo"]}

Competências informadas:
{ultimo["competencias"]}

Dificuldades informadas:
{ultimo["dificuldades"]}

Certificações de interesse:
{ultimo["certificacoes"] if ultimo["certificacoes"] else "Nenhuma informada"}

Disponibilidade de estudo:
{ultimo["disponibilidade"]}

Plano gerado pela IA:
{ultimo["resposta_ia"]}
"""

            nome_arquivo = ultimo["nome"].lower().replace(" ", "_")

            st.download_button(
                label="Baixar PDI em TXT",
                data=conteudo_download,
                file_name=f"pdi_{nome_arquivo}.txt",
                mime="text/plain",
                key="download_pdi_atual"
            )

    else:
        st.info("Cadastre um usuário antes de gerar o PDI.")


with aba_historico:
    st.subheader("Histórico de PDIs gerados")

    historico = listar_historico_pdi()

    if historico:
        for item in historico:
            (
                id_historico,
                nome,
                cargo_atual,
                competencias,
                dificuldades,
                certificacoes,
                resposta_ia,
                criado_em
            ) = item

            with st.expander(f"{nome} - {cargo_atual} - {criado_em}"):
                st.write(f"**Competências:** {competencias}")
                st.write(f"**Dificuldades:** {dificuldades}")
                st.write(f"**Certificações:** {certificacoes if certificacoes else 'Nenhuma informada'}")

                st.write("**Resposta da IA:**")
                st.markdown(resposta_ia)

                conteudo_historico = f"""
PDI COM IA PARA CARREIRA EM TI

Usuário: {nome}
Cargo atual ou área de interesse: {cargo_atual}
Data de geração: {criado_em}

Competências:
{competencias}

Dificuldades:
{dificuldades}

Certificações:
{certificacoes if certificacoes else "Nenhuma informada"}

Plano gerado pela IA:
{resposta_ia}
"""

                st.download_button(
                    label="Baixar este PDI",
                    data=conteudo_historico,
                    file_name=f"pdi_historico_{id_historico}.txt",
                    mime="text/plain",
                    key=f"download_{id_historico}"
                )
    else:
        st.info("Nenhum PDI gerado ainda.")