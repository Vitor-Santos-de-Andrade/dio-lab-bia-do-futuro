# Base de Conhecimento

## Dados Utilizados

A base de conhecimento do **GuIAFin** foi estruturada em 4 arquivos focados em recuperação financeira e cibersegurança, sem conter nenhum dado pessoal sensível ou identificador real (em total conformidade com a LGPD e o princípio de Zero Trust):

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `data/transacoes.csv` | CSV | Mapear o histórico recente de entradas e saídas para apurar receitas e despesas essenciais (moradia, alimentação e saúde). |
| `data/dividas_pendentes.csv` | CSV | Fornecer a relação de dívidas ativas com valores nominais e taxas reais de juros mensais e anuais (CET). |
| `data/estrategias_renegociacao.json` | JSON | Catálogo de métodos de quitação e crédito contendo descrições, vantagens, desvantagens e próximos passos práticos. |
| `data/alertas_fraude_financeira.json` | JSON | Base de cibersegurança contendo assinaturas de golpes comuns em renegociações (engenharia social, boletos adulterados e cobranças prévias indevidas). |

---

## Adaptações nos Dados

Em relação aos dados originais do laboratório, foram feitas as seguintes transformações para atender ao caso de uso do GuIAFin:

1. **Substituição de Investimentos por Recuperação Financeira:**
   - Os arquivos originais (`perfil_investidor.json` e `produtos_financeiros.json`) foram substituídos por pendências de crédito e métodos de amortização, focando no público que precisa sair do vermelho.
2. **Inclusão de Taxas Médias Reais de Mercado:**
   - O arquivo `dividas_pendentes.csv` reflete as taxas praticadas no Sistema Financeiro Nacional (rotativo do cartão a 14,5% a.m., cheque especial a 8,2% a.m. e consignado a 1,8% a.m.), dando embasamento matemático concreto às recomendações.
3. **Mapeamento Explícito de Vantagens e Riscos:**
   - Em `estrategias_renegociacao.json`, cada alternativa traz campos obrigatórios de `vantagens` e `desvantagens`, impedindo o modelo de recomendar soluções sem ponderação prévia.
4. **Camada Exclusiva de Cibersegurança:**
   - Criação do `alertas_fraude_financeira.json`, permitindo ao agente atuar preventivamente contra tentativas de golpe comuns enfrentadas por pessoas endividadas.
5. **Garantia de Anonimização (LGPD):**
   - Eliminação de qualquer dado sensível (nomes, CPFs, números de conta ou senhas), usando apenas valores médios e categorias orçamentárias genéricas.

---

## Estratégia de Integração

### Como os dados são carregados?
O carregamento é feito pelo backend em Python dentro do arquivo `src/app.py` na função `carregar_base_conhecimento()`:

1. **Leitura com Pandas:** Os arquivos CSV são lidos via `pandas.read_csv()`.
2. **Cálculo Determinístico de Saldo:** O saldo líquido do mês (entradas subtraídas das saídas) é calculado diretamente no código Python (`df_trans.loc[df_trans["tipo"] == "entrada", "valor"].sum() - ...`), evitando que o modelo de linguagem erre cálculos aritméticos básicos.
3. **Ordenação pelo Método Avalanche:** O código converte a coluna de taxa de juros do `dividas_pendentes.csv` em número (`float`) e ordena a tabela em ordem decrescente (da maior para a menor taxa) antes de passá-la ao modelo.
4. **Serialização Compacta de JSON:** Funções auxiliares (`formatar_estrategias()` e `formatar_fraudes()`) convertem os dados dos arquivos JSON em listas textuais sumarizadas, reduzindo o consumo de tokens e facilitando a leitura pelo modelo.
5. **Tratamento de Falhas e Logs:** A aplicação verifica a existência de cada arquivo (`os.path.exists`) e registra avisos em log interno (`guiafin.log`) caso algum arquivo esteja ausente ou mal formatado.

### Como os dados são usados no prompt?
Os dados pré-processados são agrupados em uma única string estruturada com marcadores Markdown (`### DADOS ORÇAMENTÁRIOS`, `### SALDO CALCULADO`, `### DÍVIDAS PENDENTES`, etc.) e injetados diretamente na configuração do modelo via parâmetro `system_instruction` do Google Gemini:

```python
base_conhecimento = carregar_base_conhecimento()
instrucoes_completas = f"{SYSTEM_PROMPT}\n\nBASE DE CONHECIMENTO DISPONÍVEL:\n{base_conhecimento}"

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
    system_instruction=instrucoes_completas
)
```

## Exemplo de Contexto Montado

```text
### DADOS ORÇAMENTÁRIOS (Transações Recentes):
      data     descricao   categoria   valor    tipo
2025-10-01       Salário     receita 5000.00 entrada
2025-10-02       Aluguel     moradia 1200.00   saida
2025-10-03  Supermercado alimentacao  450.00   saida
2025-10-05       Netflix       lazer   55.90   saida
2025-10-07      Farmácia       saude   89.00   saida
2025-10-10  Conta de Luz     moradia  180.00   saida
2025-10-12   Restaurante alimentacao  120.00   saida

### SALDO CALCULADO (entradas - saídas): R$ 2905.10

### DÍVIDAS PENDENTES (já ordenadas da maior para a menor taxa de juros):
id_divida                     tipo_divida        credor  valor_atual taxa_juros_mensal custo_efetivo_anual                        status  taxa_juros_mensal_num
      D01 Cartao de Credito (Rotativo)       Banco A      3200.00             14.5%              410.0%              Atrasada 45 dias                   14.5
      D02              Cheque Especial       Banco B      1800.00              8.2%              158.0%              Em uso continuo                     8.2
      D03           Emprestimo Pessoal Financeira C      4500.00              5.8%               96.5%                        Em dia                     5.8
      D04        Emprestimo Consignado       Banco D      6000.00              1.8%               23.8% Em dia (desconto em folha)                     1.8

### CATÁLOGO DE ESTRATÉGIAS (Prós e Contras):
- Troca de Dívida Cara por Barata: Contratar uma linha de crédito mais barata (ex.: consignado ou garantia) para quitar à vista as dívidas com juros altos (cartão e cheque especial).
  Vantagens: Redução drástica da taxa de juros mensal (de ~14% para ~2%); Unificação de várias dívidas em um único boleto/parcela mensal; Estancamento do crescimento de juros compostos abusivos
  Desvantagens: Risco de voltar a usar o cartão de crédito e acumular uma nova dívida; Exige margem consignável ou bem para dar em garantia
  Próximo passo: Verificar no app oficial do banco se há margem consignável ou linha pré-aprovada com taxa inferior a 3% a.m.
- Método Avalanche (Foco no Maior Juro): Pagar o mínimo de todas as contas e concentrar todo o dinheiro extra disponível na dívida com a maior taxa de juros.
  Vantagens: Economiza a maior quantidade possível de dinheiro em juros ao longo do tempo; É a estratégia matematicamente mais eficiente
  Desvantagens: Pode demorar mais tempo para ver a primeira dívida quitada se o saldo for alto; Exige disciplina e paciência nos primeiros meses
  Próximo passo: Listar as dívidas em ordem decrescente de juros e destinar qualquer sobra orçamentária exclusivamente para a primeira da lista.

### GUIA DE CIBERSEGURANÇA E PREVENÇÃO A GOLPES:
- Falso Intermediário de Limpeza de Nome (canal: WhatsApp e Redes Sociais): Promessa de limpar o nome no Serasa/SPC em 24h mediante pagamento de taxa antecipada via Pix.
  Sinais de alerta: Cobrança de taxa prévia para liberação de crédito ou limpeza de restrição; Chave Pix vinculada a CPF de pessoa física desconhecida; Pressão com tom de urgência ('apenas hoje')
  Orientação segura: Nenhuma instituição oficial cobra taxa adiantada para renegociar dívidas. A negociação deve ser feita diretamente pelos canais oficiais do credor (ex.: app do banco) ou plataformas oficiais como o Serasa Limpa Nome.
- Boleto Adulterado de Renegociação (canal: E-mail, SMS ou WhatsApp): Envio de boleto em PDF com 'super desconto' para quitação imediata de dívida atrasada.
  Sinais de alerta: Código de barras com os primeiros dígitos diferentes do código do banco emissor; Nome do beneficiário no momento do pagamento diferente da razão social do banco/credor; Mensagens com erros gramaticais ou links encurtados (bit.ly, tinyurl)
  Orientação segura: Antes de pagar qualquer boleto de renegociação, confira sempre os dados do 'Beneficiário Final' na tela de confirmação do seu banco. Se o CNPJ ou nome não for exatamente da instituição credora, não conclua o pagamento.
```
