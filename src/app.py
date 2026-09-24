import streamlit as st
import google.generativeai as genai
import os
import pandas as pd
import json
import logging

# Configuração de log interno (não exibido ao usuário)
logging.basicConfig(
    filename="guiafin.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Formatando arquivos json
def formatar_estrategias(dados: list[dict]) -> str:
    """Recebe a lista já parseada (json.load) e monta um texto compacto para o prompt."""
    linhas = []
    for item in dados:
        linhas.append(
            f"- {item.get('estrategia', 'Estratégia sem nome')}: {item.get('descricao', '')}\n"
            f"  Vantagens: {'; '.join(item.get('vantagens', []))}\n"
            f"  Desvantagens: {'; '.join(item.get('desvantagens', []))}\n"
            f"  Próximo passo: {item.get('proximo_passo', '')}"
        )
    return "\n".join(linhas)

def formatar_fraudes(dados: list[dict]) -> str:
    """Recebe a lista já parseada (json.load) e monta um texto compacto para o prompt."""
    linhas = []
    for item in dados:
        linhas.append(
            f"- {item.get('nome_golpe', 'Golpe sem nome')} (canal: {item.get('canal_comum', '')}): "
            f"{item.get('gatilho_suspeito', '')}\n"
            f"  Sinais de alerta: {'; '.join(item.get('sinais_de_alerta', []))}\n"
            f"  Orientação segura: {item.get('orientacao_segura', '')}"
        )
    return "\n".join(linhas)

# 1. Configurações da Página
st.set_page_config(
    page_title="GuIAFin - Seu Guia Financeiro Seguro",
    page_icon="🛡️",
    layout="centered"
)

# 2. Carregamento da Base de Conhecimento (data/)
def carregar_base_conhecimento():
    contexto = []
    base_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    
    # Leitura das Transações
    caminho_transacoes = os.path.join(base_dir, "transacoes.csv")
    if os.path.exists(caminho_transacoes):
        df_trans = pd.read_csv(caminho_transacoes)
        contexto.append("### DADOS ORÇAMENTÁRIOS (Transações Recentes):\n" + df_trans.to_string(index=False))
        # Saldo calculado em Python (não deixamos o LLM somar valores)
        saldo = (
            df_trans.loc[df_trans["tipo"] == "entrada", "valor"].sum()
            - df_trans.loc[df_trans["tipo"] == "saida", "valor"].sum()
        )
        contexto.append(f"### SALDO CALCULADO (entradas - saídas): R$ {saldo:.2f}")
    else:
        logging.warning(f"Arquivo não encontrado: {caminho_transacoes}")        
        
    # Leitura das Dívidas Pendentes
    caminho_dividas = os.path.join(base_dir, "dividas_pendentes.csv")
    if os.path.exists(caminho_dividas):
        df_div = pd.read_csv(caminho_dividas)
        # Converte "14.5%" em número e ordena por juros (base pronta p/ método avalanche)
        df_div["taxa_juros_mensal_num"] = (
            df_div["taxa_juros_mensal"].str.rstrip("%").astype(float)
        )
        df_div = df_div.sort_values("taxa_juros_mensal_num", ascending=False)
        contexto.append("### DÍVIDAS PENDENTES (já ordenadas da maior para a menor taxa de juros):\n" + df_div.to_string(index=False))
    else:
        logging.warning(f"Arquivo não encontrado: {caminho_dividas}")

    # Leitura das Estratégias de Renegociação
    caminho_estrategias = os.path.join(base_dir, "estrategias_renegociacao.json")
    if os.path.exists(caminho_estrategias):
        try:
            with open(caminho_estrategias, "r", encoding="utf-8") as f:
                dados_estrategias = json.load(f)
            contexto.append(
                "### CATÁLOGO DE ESTRATÉGIAS (Prós e Contras):\n"
                + formatar_estrategias(dados_estrategias)
            )
        except json.JSONDecodeError as e:
            logging.error(f"JSON inválido em {caminho_estrategias}: {e}")
    else:
        logging.warning(f"Arquivo não encontrado: {caminho_estrategias}")

    # Leitura da Base de Cibersegurança / Antifraude
    caminho_fraudes = os.path.join(base_dir, "alertas_fraude_financeira.json")
    if os.path.exists(caminho_fraudes):
        try:
            with open(caminho_fraudes, "r", encoding="utf-8") as f:
                dados_fraudes = json.load(f)
            contexto.append(
                "### GUIA DE CIBERSEGURANÇA E PREVENÇÃO A GOLPES:\n"
                + formatar_fraudes(dados_fraudes)
            )
        except json.JSONDecodeError as e:
            logging.error(f"JSON inválido em {caminho_fraudes}: {e}")
    else:
        logging.warning(f"Arquivo não encontrado: {caminho_fraudes}")
            
    return "\n\n".join(contexto)

# 3. Definição do System Prompt com Guardrails
SYSTEM_PROMPT = """
Você é o GuIAFin (Guia Financeiro Inteligente), um mentor de finanças pessoais especializado em recuperação financeira, renegociação de dívidas e segurança digital no contexto bancário brasileiro.
OBJETIVO:
Ajudar pessoas em aperto financeiro a entenderem sua realidade orçamentária, priorizarem o pagamento de dívidas com foco no custo efetivo e se protegerem contra fraudes digitais, conduzindo-as à autonomia e tranquilidade.
PERSONALIDADE E TOM DE VOZ:
- Acolhedor, empático, encorajador e prudente.
- NUNCA julgue ou critique os hábitos de consumo ou escolhas passadas do usuário.
- Linguagem direta, simples e acessível (sem jargões sem explicação).
REGRAS INEGOCIÁVEIS (GUARDRAILS):
1. BASEIE-SE EM DADOS: Utilize como referência as informações da Base de Conhecimento fornecida abaixo.
2. ANTI-ALUCINAÇÃO E TRANSPARÊNCIA: Nunca invente taxas, regras de crédito ou prazos. Se faltarem informações essenciais, declare com transparência que não possui dados suficientes.
3. PRÓS E CONTRAS OBRIGATÓRIOS: Sempre explique explicitamente as vantagens e as desvantagens de qualquer decisão financeira antes de uma escolha.
4. ORIENTAÇÃO PARA PRÓXIMA DECISÃO: Termine suas respostas indicando qual é o próximo passo prático e imediato que o usuário deve avaliar.
5. DIAGNÓSTICO ANTES DA RECOMENDAÇÃO: Jamais sugira investimentos ou amortizações antes de garantir que as despesas essenciais (moradia, alimentação e saúde) estão preservadas.
6. CIBERSEGURANÇA (ZERO TRUST): NUNCA solicite senhas, tokens ou CVV. Alerte imediatamente se o usuário enviar dados sensíveis. Alerte sobre golpes (boletos falsos, Pix para PF) em qualquer tema de negociação.
7. ESCOPO ESTRITO: Foco exclusivo em finanças pessoais e segurança digital.
8. TAMANHO DA RESPOSTA: Responda de forma sucinta e direta, com no máximo 4 parágrafos.
9. INFORMAÇÕES DA RESPOSTA: Responda às perguntas sem citar nomes de arquivos ou referências internas do sistema.
"""

# 4. Barra Lateral (Sidebar)
with st.sidebar:
    st.title("🛡️ GuIAFin")
    st.caption("Seu mentor para sair do vermelho com segurança.")
    
    # Input da API Key do Gemini
    gemini_key = st.text_input(
        "Chave API do Gemini:",
        type="password",
        value=os.getenv("GEMINI_API_KEY", ""),
        help="Obtenha gratuitamente no Google AI Studio"
        )
    st.divider()
    st.markdown("### 🔒 Protocolo de Segurança")
    st.info("O GuIAFin nunca solicita senhas, tokens de acesso ou números de cartão. Este ambiente segue diretrizes de proteção e LGPD.")
    
    if st.button("Limpar 🔄"):
        st.session_state.messages = []
        st.rerun()

# 5. Inicialização do Histórico do Chat
if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Olá! Eu sou o **GuIAFin**, seu guia financeiro. Estou aqui para te apoiar a organizar as contas e sair do aperto, passo a passo e no seu ritmo — sem julgamentos! 🤝\n\n🔒 *Lembrete de segurança: Nunca compartilhe senhas, dados de cartão ou códigos por aqui.*\n\nPara começarmos: **o que está mais pesado no seu bolso hoje ou tirando o seu sono?**"
        }
    ]

# 6. Exibição das Mensagens Anteriores
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"].replace("$", r"\$"))

# 7. Interação do Usuário
if user_prompt := st.chat_input("Digite sua dúvida financeira ou situação aqui..."):
    # Exibe mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt.replace("$", r"\$"))

    # Verifica se a chave foi informada
    if not gemini_key:
        with st.chat_message("assistant"):
            st.warning("Por favor, insira sua Chave da API do Google Gemini na barra lateral esquerda para que eu possa te responder.")
    else:
        try:
            # Configuração do Gemini
            genai.configure(api_key=gemini_key)
            
            # Montagem do contexto com a Base de Conhecimento
            base_conhecimento = carregar_base_conhecimento()
            instrucoes_completas = f"{SYSTEM_PROMPT}\n\nBASE DE CONHECIMENTO DISPONÍVEL:\n{base_conhecimento}"
            
            model = genai.GenerativeModel(
                model_name="gemini-3.6-flash",
                system_instruction=instrucoes_completas
            )
            
            # Formatação do histórico para a API
            chat_history = []
            for m in st.session_state.messages[:-1]:
                role = "user" if m["role"] == "user" else "model"
                chat_history.append({"role": role, "parts": [m["content"]]})
                
            chat = model.start_chat(history=chat_history)
            
            with st.chat_message("assistant"):
                with st.spinner("Analisando com segurança..."):
                    response = chat.send_message(user_prompt)
                    st.markdown(response.text.replace("$", r"\$"))
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    
        except Exception as e:
            logging.error(f"Erro na chamada Gemini: {e}") 
            st.error("Não consegui me comunicar com a IA agora. Tente novamente em instantes.")