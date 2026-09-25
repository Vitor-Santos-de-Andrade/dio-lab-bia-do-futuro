# 🛡️ GuIAFin — Guia Financeiro Inteligente

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Google Gemini API](https://img.shields.io/badge/Google%20Gemini-3.6%20Flash-8E75B2?logo=google&logoColor=white)](https://aistudio.google.com/)

Mentor de Inteligência Artificial para recuperação orçamentária, planejamento de dívidas e proteção ativa contra golpes financeiros.

---

## 📌 Contexto e Problema

No Brasil, milhões de pessoas enfrentam o ciclo do endividamento e a sobrecarga emocional do aperto financeiro. Ao buscarem saídas rápidas, tornam-se o alvo prioritário de criminosos digitais — sendo vítimas de **falsas centrais de renegociação, boletos adulterados e cobranças ilegais de taxas de "limpeza de nome" via Pix**.

---

## 💡 A Solução: GuIAFin

O **GuIAFin** é um assistente virtual consultivo desenvolvido com Inteligência Artificial Generativa para apoiar clientes do setor bancário a retomarem o controle financeiro de forma sustentável e protegida.

### 🌟 Pilares Fundamentais:
1. **Diagnóstico Acolhedor:** Escuta ativa e mapeamento de despesas essenciais (moradia, saúde e alimentação) sem emitir julgamentos de valor sobre os gastos do usuário.
2. **Decisão Baseada em Dados (Método Avalanche):** Priorização matemática das dívidas com maiores taxas de juros (como o rotativo do cartão), sempre apresentando os **prós e contras** de cada escolha.
3. **Cibersegurança Ativa (Zero Trust & LGPD):**
   - **Zero Trust:** Nunca solicita nem armazena senhas, tokens ou números de cartão.
   - **Detecção Antifraude em Tempo Real:** Alerta proativamente sobre padrões de golpes ao identificar abordagens suspeitas de renegociação.
   - **Respostas Diretas e Objetivas:** Limitação estrita a no máximo 4 parágrafos para não sobrecarregar quem já se encontra em situação de estresse.

---

## 🏗️ Arquitetura e Engenharia de Dados

```mermaid
flowchart TD
    A[Usuário] -->|Pergunta / Dúvida| B["Streamlit (Interface Visual)"]
    B --> C[Google Gemini API]
    D[(Base de Conhecimento: data/)] -->|Dados Orçamentários e Antifraude| C
    C --> E[Validação e Pós-processamento]
    E --> B
    B -->|Exibição Formatada| A
```

### ⚙️ Destaques de Engenharia (src/app.py):
- Cálculo Determinístico pelo Pandas: O saldo real (entradas menos saídas) é calculado matematicamente no backend em Python, impedindo que a LLM erre operações aritméticas.
- Ordenação Automática de Juros: As dívidas são ordenadas da maior para a menor taxa antes de serem injetadas no prompt, forçando a aplicação do Método Avalanche.
- Mitigação do Bug do Cifrão (Markdown/KaTeX): Sanitização de texto na camada de visualização (.replace("$", r"\$")), evitando que valores em reais sejam interpretados incorretamente como fórmulas matemáticas pelo Streamlit.

## 📁 Estrutura do Repositório
```
dio-lab-bia-do-futuro/
├── 📄 README.md
|
├── 📁 data/                            
│   ├── transacoes.csv                
│   ├── dividas_pendentes.csv          
│   ├── estrategias_renegociacao.json   
│   └── alertas_fraude_financeira.json
| 
├── 📁 docs/
│   ├── 01-documentacao-agente.md       
│   ├── 02-base-conhecimento.md         
│   ├── 03-prompts.md                   
│   ├── 04-metricas.md                  
│   └── 05-pitch.md
|               
│── 📁 src/                             
│   ├── app.py
│   └── 📄 requirements.txt
│
└── 📁 assets/
    └── ...
```

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.10 ou superior instalado;
- Uma chave de API gratuita do Google Gemini (obtida no [Google AI Studio](https://aistudio.google.com/apps)).

### Passo a passo
1. Instale as dependências
```bash
pip install -r requirements.txt
```
2. Inicie o aplicativo
```bash
streamlit run src/app.py
```
3. Interaja com o GuIAFin:
    - O navegador abrirá automaticamente.
    - Insira sua chave de API na barra lateral esquerda e comece a conversa!

## 📑 Documentação do Projeto
- 📄 [Documentação do Agente](https://github.com/Vitor-Santos-de-Andrade/dio-lab-bia-do-futuro/blob/main/docs/01-documentacao-agente.md) — Caso de Uso, Persona, Arquitetura e Guardrails.
- 📄 [Base de Conhecimento](https://github.com/Vitor-Santos-de-Andrade/dio-lab-bia-do-futuro/blob/main/docs/02-base-conhecimento.md) — Dados Utilizados, Adaptações nos Dados, Estratégia de Dados e Exemplo de Contexto.
- 📄 [Engenharia de Prompts](https://github.com/Vitor-Santos-de-Andrade/dio-lab-bia-do-futuro/blob/main/docs/03-prompts.md) — System Prompt, Exemplos de Interação, Edge Cases e Observações.
- 📄 [Avaliação e Métricas](https://github.com/Vitor-Santos-de-Andrade/dio-lab-bia-do-futuro/blob/main/docs/04-metricas.md) — Métricas de Qualidade, Cenários de Teste Reais e Resultados.
- 📄 [Roteiro do Pitch](https://github.com/Vitor-Santos-de-Andrade/dio-lab-bia-do-futuro/blob/main/docs/05-pitch.md) — Estrutura de Apresentação em 3 Minutos.
