import os
from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)


def gerar_pdi_com_ia(
    nome,
    cargo_atual,
    objetivo,
    competencias,
    dificuldades,
    certificacoes,
    disponibilidade
):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("A chave GEMINI_API_KEY não foi encontrada no arquivo .env.")

    client = genai.Client(api_key=api_key)

    modelos = [
        os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite",
        "gemini-2.5-flash-lite",
        "gemini-3.1-flash-lite"
    ]

    prompt = f"""
Você é um mentor de carreira especializado em tecnologia da informação.

Crie um Plano de Desenvolvimento Individual para o usuário abaixo.

Dados do usuário:
Nome: {nome}
Cargo atual ou área de interesse: {cargo_atual}
Objetivo profissional: {objetivo}
Competências atuais: {competencias}
Dificuldades atuais: {dificuldades}
Certificações de interesse: {certificacoes if certificacoes else "Nenhuma informada"}
Disponibilidade de estudo: {disponibilidade}

O plano deve conter obrigatoriamente:

1. Análise breve do perfil
2. Principais gaps de competências
3. Plano de desenvolvimento individual
4. Trilha de estudos sugerida
5. Sugestões de certificações
6. Cronograma de estudos
7. Próximos passos práticos

Regras da resposta:
- Responda em português do Brasil.
- Use linguagem objetiva e organizada.
- Evite respostas genéricas.
- Relacione as recomendações diretamente aos dados informados.
- Monte um plano prático para estudo e evolução profissional.
"""

    erros = []

    for modelo in modelos:
        try:
            response = client.models.generate_content(
                model=modelo,
                contents=prompt
            )

            if response.text:
                return f"**Modelo utilizado:** {modelo}\n\n{response.text}"

        except Exception as erro:
            erros.append(f"{modelo}: {erro}")

    raise Exception(
        "Não foi possível gerar o PDI com nenhum dos modelos disponíveis. "
        "Tente novamente em alguns minutos.\n\nDetalhes:\n" + "\n".join(erros)
    )