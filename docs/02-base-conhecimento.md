# Base de Conhecimento

## Dados Utilizados

A base de conhecimento do **GuIAFin** foi estruturada para fundamentar a tomada de decisão do usuário em dados reais de mercado, padrões orçamentários e regras defensivas de cibersegurança:


| Arquivo | Formato | Utilização no GuIAFin |
|---------|---------|---------------------|
| `data/transacoes.csv` | CSV | Analisar o fluxo financeiro do usuário (entradas vs. saídas) e calcular o percentual de gastos essenciais sem emitir julgamentos de valor. |
| `data/dividas_pendentes.csv` | CSV | Mapear as pendências ativas com taxas de juros reais de mercado para orientar a priorização matemática das dívidas mais caras. |
| `data/estrategias_renegociacao.json` | JSON | Catálogo de soluções de amortização, renegociação e crédito com vantagens, desvantagens e próximos passos explícitos. |
| `data/alertas_fraude_financeira.json` | JSON | Base de cibersegurança inspirada em datasets de fraudes para detectar abordagens suspeitas de renegociação e orientar canais oficiais. |
| `data/perguntas_financas_pessoais.csv` | CSV | Banco de perguntas e respostas pedagógicas sobre corte de gastos e organização financeira (inspirado no dataset `fiqa-personal-finance-dataset` do Hugging Face). |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

1. **Diagnóstico Orçamentário Empático:** O `transacoes.csv` permite ao agente extrair a realidade financeira do usuário para não propor parcelas que comprometam a subsistência básica (alimentação e moradia).
2. **Priorização por Custo Efetivo Total:** O `dividas_pendentes.csv` impede o agente de sugerir quitações aleatórias, focando o esforço no estrangulamento das dívidas de juros compostos agressivos (rotativo e cheque especial).
3. **Ponderação Obrigatória de Decisão:** Cada registro de `estrategias_renegociacao.json` contém os campos `vantagens` e `desvantagens`, obrigando o modelo a apresentar ambos os lados antes do usuário escolher.
4. **Camada de Cibersegurança Proativa:** Com o `alertas_fraude_financeira.json`, o agente atua ativamente alertando contra engenharia social, boletos adulterados e cobranças ilegais de taxas de intermediação.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Existem duas possibilidades: injetar os dados diretamente no prompt (Ctrl + C, Ctrl + V) e carregar 2 arquivos CSV via código, como no exemplo abaixo:

```python
import pandas as pd

# CSV
dividas = pd.read_csv('data/dividas_pendentes.csv')
transacoes = pd.read_csv('data/transacoes.csv')
```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

De maneira simples, os dados são "injetados" nos prompts, garantindo que o Agente tenha o melhor contexto possível. Além disso, as informações de 2 arquivos CSV são carregadas dinamicamente em soluções mais robustas para ganhar flexibilidade.

```text
Dívidas Pendentes do Usuário (`data/dividas_pendentes.csv`):

id_divida,tipo_divida,credor,valor_atual,taxa_juros_mensal,custo_efetivo_anual,status
D01,Cartao de Credito (Rotativo),Banco A,3200.00,14.5%,,Atrasada 45 dias
D02,Cheque Especial,Banco B,1800.00,8.2%,158.0%,Em uso continuo
D03,Emprestimo Pessoal,Financeira C,4500.00,5.8%,96.5%,Em dia
D04,Emprestimo Consignado,Banco D,6000.00,1.8%,23.8%,Em dia (desconto em folha)

Transações do Usuário (`data/transacoes.csv`):

data,descricao,categoria,valor,tipo
2025-10-01,Salário,receita,5000.00,entrada
2025-10-02,Aluguel,moradia,1200.00,saida
2025-10-03,Supermercado,alimentacao,450.00,saida
2025-10-05,Netflix,lazer,55.90,saida
2025-10-07,Farmácia,saude,89.00,saida
2025-10-10,Restaurante,alimentacao,120.00,saida
2025-10-12,Uber,transporte,45.00,saida
2025-10-15,Conta de Luz,moradia,180.00,saida
2025-10-20,Academia,saude,99.00,saida
2025-10-25,Combustível,transporte,250.00,saida

Decisões Financeiras Estratégicas (`data/estrategias_renegociacao.json`):

[
  {
    "estrategia": "Troca de Dívida Cara por Barata",
    "descricao": "Contratar uma linha de crédito mais barata (ex.: consignado ou garantia) para quitar à vista as dívidas com juros altos (cartão e cheque especial).",
    "vantagens": [
      "Redução drástica da taxa de juros mensal (de ~14% para ~2%)",
      "Unificação de várias dívidas em um único boleto/parcela mensal",
      "Estancamento do crescimento de juros compostos abusivos"
    ],
    "desvantagens": [
      "Risco de voltar a usar o cartão de crédito e acumular uma nova dívida",
      "Exige margem consignável ou bem para dar em garantia"
    ],
    "proximo_passo": "Verificar no app oficial do banco se há margem consignável ou linha pré-aprovada com taxa inferior a 3% a.m."
  },
  {
    "estrategia": "Método Avalanche (Foco no Maior Juro)",
    "descricao": "Pagar o mínimo de todas as contas e concentrar todo o dinheiro extra disponível na dívida com a maior taxa de juros.",
    "vantagens": [
      "Economiza a maior quantidade possível de dinheiro em juros ao longo do tempo",
      "É a estratégia matematicamente mais eficiente"
    ],
    "desvantagens": [
      "Pode demorar mais tempo para ver a primeira dívida quitada se o saldo for alto",
      "Exige disciplina e paciência nos primeiros meses"
    ],
    "proximo_passo": "Listar as dívidas em ordem decrescente de juros e destinar qualquer sobra orçamentária exclusivamente para a primeira da lista."
  },
  {
    "estrategia": "Portabilidade de Crédito",
    "descricao": "Transferir a dívida para outra instituição financeira que ofereça uma taxa de juros mais baixa do que a atual.",
    "vantagens": [
      "Direito garantido por lei e regulamentação do Banco Central",
      "Não há cobrança de taxas para realizar a transferência de banco"
    ],
    "desvantagens": [
      "A nova instituição não é obrigada a aceitar a transferência",
      "Exige pesquisa e cotação ativa entre diferentes bancos"
    ],
    "proximo_passo": "Solicitar ao credor atual o extrato com o Custo Efetivo Total (CET) e o saldo devedor para apresentar a outros bancos."
  }
]

Alertas de Segurânça (`data/alertas_fraude_financeira.json`):

[
  {
    "id_golpe": "GOLPE-01",
    "nome_golpe": "Falso Intermediário de Limpeza de Nome",
    "canal_comum": "WhatsApp e Redes Sociais",
    "gatilho_suspeito": "Promessa de limpar o nome no Serasa/SPC em 24h mediante pagamento de taxa antecipada via Pix.",
    "sinais_de_alerta": [
      "Cobrança de taxa prévia para liberação de crédito ou limpeza de restrição",
      "Chave Pix vinculada a CPF de pessoa física desconhecida",
      "Pressão com tom de urgência ('apenas hoje')"
    ],
    "orientacao_segura": "Nenhuma instituição oficial cobra taxa adiantada para renegociar dívidas. A negociação deve ser feita diretamente pelos canais oficiais do credor (ex.: app do banco) ou plataformas oficiais como o Serasa Limpa Nome."
  },
  {
    "id_golpe": "GOLPE-02",
    "nome_golpe": "Boleto Adulterado de Renegociação",
    "canal_comum": "E-mail, SMS ou WhatsApp",
    "gatilho_suspeito": "Envio de boleto em PDF com 'super desconto' para quitação imediata de dívida atrasada.",
    "sinais_de_alerta": [
      "Código de barras com os primeiros dígitos diferentes do código do banco emissor",
      "Nome do beneficiário no momento do pagamento diferente da razão social do banco/credor",
      "Mensagens com erros gramaticais ou links encurtados (bit.ly, tinyurl)"
    ],
    "orientacao_segura": "Antes de pagar qualquer boleto de renegociação, confira sempre os dados do 'Beneficiário Final' na tela de confirmação do seu banco. Se o CNPJ ou nome não for exatamente da instituição credora, não conclua o pagamento."
  },
  {
    "id_golpe": "GOLPE-03",
    "nome_golpe": "Falsa Central Telefônica / Suporte de Segurança",
    "canal_comum": "Ligação telefônica",
    "gatilho_suspeito": "Golpista finge ser da área de segurança do banco avisando sobre uma transação suspeita e pede confirmação de dados.",
    "sinais_de_alerta": [
      "Solicitação de senhas, códigos de token, CVV do cartão ou código recebido por SMS",
      "Pedido para transferir dinheiro para uma 'conta segura' ou fazer Pix de teste",
      "Orientação para instalar aplicativos de suporte remoto no celular"
    ],
    "orientacao_segura": "Os bancos oficiais nunca ligam pedindo senha, token ou transferências de teste. Desligue imediatamente e ligue para o número oficial impresso no verso do seu cartão físico."
  }
]

Dúvidas do Usuário (`data/perguntas_financas_pessoais.csv`):

id,categoria,duvida_usuario,resposta_educativa,proximo_passo_recomendado
1,priorizacao_dividas,"Tenho dívida no cartão de crédito e um empréstimo consignado. Qual devo pagar primeiro?","Sempre priorize a dívida com maior taxa de juros (como o rotativo do cartão, que passa de 14% ao mês). O consignado tem juros muito menores descontados em folha.","Levantar o valor total e o Custo Efetivo Total (CET) da fatura do cartão para propor renegociação com taxa fixa."
2,renegociacao,"Recebi uma proposta para parcelar minha fatura em 24 vezes, vale a pena?","O parcelamento reduz o valor da parcela mensal, mas o prazo longo aumenta muito o total de juros pagos ao final. Vale a pena se a parcela couber no orçamento essencial, mas sempre tente negociar menos parcelas com desconto.","Simular o valor total final (parcela vezes 24) e comparar com uma linha de crédito mais barata para quitar à vista."
3,orcamento_apertado,"Meu salário não sobra nada para pagar as contas atrasadas. O que eu faço?","O primeiro passo é proteger suas despesas essenciais de sobrevivência (moradia, alimentação e saúde). Nunca use dinheiro de comida para pagar juros abusivos.","Fazer a lista dos 3 maiores gastos não essenciais do mês para avaliar pequenos cortes temporários."
4,reserva_emergencia,"Devo começar a investir mesmo estando com o nome negativado?","Não é recomendado investir em renda fixa ou variável enquanto você tiver dívidas com juros altos, pois o rendimento dos investimentos é menor do que os juros que você está pagando na dívida.","Focar 100% dos recursos extras na quitação das dívidas mais caras antes de aplicar qualquer valor."

```

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
Dívidas Pendentes do usuário: 
1. Cartão de Crédito(Rotativo):
    - Credor: Banco A
    - Valor Atual da Dívida: R$ 3200.00
    - Taxa de Juros Mensal: 14,5%
    - Custo Efetivo Anual: 410.0%
    - Status: Atrasada 45 dias
2. Cheque Especial:
    - Credor: Banco B
    - Valor Atual da Dívida: R$ 1800.00
    - Taxa de Juros Mensal: 8.2%
    - Custo Efetivo Anual: 158.0%
    - Status: Em uso continuo

Últimas Transações:
- 16/09/2026: Salário - R$ 4000.00
- 17/09/2026: Aluguel - R$ 1200.00
- 18/09/2026: Supermercado - R$ 450.00
- 19/09/2026: Netflix - R$ 55.90
- 20/09/2026: Conta de Luz - R$ 180.00

Dúvida do Usuário:
- Tenho dívida no cartão de crédito e um cheque especial. Qual devo pagar primeiro?
...
```
