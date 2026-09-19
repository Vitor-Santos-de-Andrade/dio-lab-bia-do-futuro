# Base de Conhecimento

## Dados Utilizados

| Arquivo | Formato | Utilização no GuIAFin |
|---------|---------|---------------------|
| `data/perfil_cliente.json` | JSON | Fornece o contexto orçamentário do cliente (renda e despesas básicas) para que o agente não recomende parcelas inviáveis. |
| `transacoes.csv` | CSV | Analisar padrão de gastos do usuário e usar essas informações de forma didática. |
| `data/dividas.csv` | CSV | Contém o histórico de pendências do cliente com taxas de juros reais de mercado para priorizar o pagamento das dívidas mais caras. |
| `data/opcoes_renegociacao.json` | JSON | Catálogo de estratégias de amortização e renegociação, detalhando vantagens e desvantagens de cada uma. |
| `data/guia_antifraude.json` | JSON | Repositório de cibersegurança contendo padrões de golpes frequentes em renegociações e regras de validação de canais oficiais. |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

1. **Substituição de Investimentos por Recuperação:** Em vez de focar em carteira de ações e fundos, os dados focam em comprometimento de renda e custo efetivo total das dívidas.
2. **Camada de Cibersegurança (`guia_antifraude.json`):** Adicionamos uma base de conhecimento defensiva. Quando o usuário menciona que recebeu uma proposta de desconto agressiva no WhatsApp, o agente cruza com esse guia para alertar sobre possíveis golpes.
3. **Mapeamento de Prós e Contras:** Cada opção de renegociação possui campos explícitos de vantagens e desvantagens, forçando o agente a ser imparcial e consultivo.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Existem duas possibilidades: injetar os dados diretamente no prompt (Ctrl + C, Ctrl + V) ou carregar os arquivos via código, como no exemplo abaixo:

```python
import pandas as pd
import json

# CSV
historico = pd.read_csv('data/dividas.csv')
transacoes = pd.read_csv('data/transacoes.csv')

# JSON
with open('data/perfil_cliente.json', 'r', encoding='utf-8') as f:
    perfil = json.load(f)
with open('data/opcoes_renegociacao.json', 'r', encoding='utf-8') as f:
    opcoes = json.load(f)
with open('data/guia_antifraude.json', 'r', encoding='utf-8') as f:
    seguranca = json.load(f)
```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

[Sua descrição aqui]

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
Dados do Cliente:
- Nome: João Silva
- Perfil: Moderado
- Saldo disponível: R$ 5.000

Últimas transações:
- 01/11: Supermercado - R$ 450
- 03/11: Streaming - R$ 55
...
```
