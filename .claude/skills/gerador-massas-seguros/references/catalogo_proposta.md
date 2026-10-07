# Catálogo do bloco de Proposta

As colunas de proposta existem em **dois lugares**:

1. **No fim dos 4 templates de cotação** (empresarial, residencial, condomínio amplo e
   tradicional): a massa de cotação pode trazer a proposta junto. É **opcional**: sem a chave
   `proposta`, todas essas colunas ficam `<IGNORE>`.
2. **No template próprio de proposta**, `templates/template_proposta.xlsx` (aba `Proposta`),
   igual para todos os produtos, para quando o usuário pede **só a proposta**. No JSON,
   `"ramo": "proposta"`.

Cabeçalho na linha 2, dados a partir da linha 3. No template, as linhas 3 a 5 trazem só as
**listas de opções**; o script sobrescreve e limpa essas linhas.

## Chave `proposta` (nas duas situações)

Passe só as colunas que quiser preencher; as demais ficam `<IGNORE>`.

| Coluna | Valores |
|---|---|
| `Proponente PF - Tipo Documento` | `RG` · `RNE` |
| `Proponente PF - Número Documento` | texto livre |
| `Proponente PF - Órgão Emissor` | texto livre |
| `Proponente PF - UF Órgão Emissor` | texto livre (UF) |
| `Proponente PF - Data Expedição` | texto livre (data) |
| `Proponente - CEP` | texto livre ou token `#cep` |
| `Endereco Proponente - Número` | texto livre |
| `Contato - Tipo Telefone` | `Celular` · `Residencial` · `Comercial` |
| `Contato - Telefone` | texto livre |
| `Contato - Email` | texto livre |
| `Proposta - Forma Pagamento` | `Carnê` · `Débito` · `Cartão de Crédito` |
| `Proposta - Quantidade Parcelas` | `1 + 1` · `1 + 2` · `0 + 1` |
| `Proposta Débito - Proponente Titular` | `Sim` · `Não` |
| `Proposta Débito - Documento Titular` | texto livre |
| `Proposta Débito - Nome Titular` | texto livre |
| `Proposta Débito - Banco` | texto livre |
| `Proposta Débito - Agência` | texto livre |
| `Proposta Débito - Dígito Agência` | texto livre |
| `Proposta Débito - Conta` | texto livre |
| `Proposta Débito - Dígito Conta` | texto livre |

Os templates de **condomínio** não têm as 5 colunas `Proponente PF - ...` (condomínio é pessoa
jurídica). Use só as colunas que o template do ramo tem.

O validador confere as colunas de lista: valor fora da lista = ERRO; diferença só de escrita
(`rg`, `1+2`) é corrigida com `--corrigir`. Regras entre colunas (ex.: o que a forma de
pagamento `Débito` exige) **ainda não foram passadas pelo usuário**; não invente.

## Template de proposta (`"ramo": "proposta"`)

`campos` obrigatórios: `Numero Cotacao` (número da cotação a que a proposta se refere),
`Perfil` (`Corretor` padrão · `Operações` · `Subscrição`) e `Corretor`. Sem combos, perguntas,
grupos nem coberturas.

```json
{"ramo": "proposta", "massas": [{
  "campos": {"Numero Cotacao": "123456", "Perfil": "Corretor", "Corretor": "COI"},
  "proposta": {"Proponente PF - Tipo Documento": "RG", "Proponente PF - Número Documento": "123456789",
               "Contato - Tipo Telefone": "Celular", "Contato - Telefone": "11999990000",
               "Proposta - Forma Pagamento": "Carnê", "Proposta - Quantidade Parcelas": "1 + 1"}}]}
```

## Proposta junto da cotação

Some a chave `proposta` na massa do ramo, com o mesmo formato acima:

```json
{"campos": {...}, "combos": {...}, "coberturas": [...],
 "proposta": {"Contato - Tipo Telefone": "Celular", "Proposta - Forma Pagamento": "Débito"}}
```
