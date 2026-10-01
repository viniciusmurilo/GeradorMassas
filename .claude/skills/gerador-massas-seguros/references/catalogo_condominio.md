# Catálogo de Colunas — Condomínio Amplo e Tradicional

Templates: `templates/template_condominio_amplo.xlsx` (aba `Cotação`, 44 colunas de dados) e
`templates/template_condominio_tradicional.xlsx` (aba `Planilha1`, 56 colunas). Os dois têm o
cabeçalho na **linha 2** e os dados a partir da **linha 3**. No template original, as linhas 3 a
10 trazem **listas de opções** (não massas). O script sobrescreve e limpa essas linhas.

`ramo` no JSON: `"condominio_amplo"` ou `"condominio_tradicional"`.

**Formato de preenchimento dos condomínios** (diferente do empresarial/residencial, segue a linha
de exemplo do template Tradicional enviado pelo usuário):

| | Condomínio |
|---|---|
| opção marcada (grupos/RDB/CHK) | `Sim` |
| opção não marcada | `Não` |
| cobertura / período / qt de vidas não contratados | célula **vazia** |
| valores (coberturas e Valor em Risco) | **número** (`1000000`), não texto BR |
| perguntas | `Sim` / `Não`; quantidade de elevadores como número |

O script aplica esse formato sozinho quando o `ramo` começa com `condominio`.

## Campos diretos — chave `campos` (obrigatórios)

| Cabeçalho | Conteúdo |
|---|---|
| `Perfil` | `Corretor` (padrão) · `Operações` · `Subscrição` |
| `Corretor` | Nome do corretor (ex.: `COI`) |
| `Tipo Pessoa` | CPF/CNPJ: tokens `#cpf` / `#cnpj` / `#cnpjalfa` ou valor literal |
| `Cep` | token `#cep` ou valor literal |

## Combos — chave `combos` (obrigatórios)

| Cabeçalho | Valores válidos |
|---|---|
| `Tipo de Condomínio` | `Condomínio Comercial - Vertical` · `Condomínio de Consultórios` · `Condomínio de Escritórios` · `Condomínio Exclusivamente Residencial - Horizontal` · `Condomínio Exclusivamente Residencial - Vertical` · `Condomínio Flat / Apart-Hotel` · `Condomínio Misto - Vertical` · `Condomínio Residencial com Comércio no Térreo` |
| `Tipo de Construção` | `Superior / Sólida` · `Mista` · `Inferior` |
| `Objeto Segurado` | `Prédio e Conteúdo` |
| `Assistência 24h INPUT` | `Assistência Condomínio Plano Intermediário` · `Assistência Condomínio Plano Básico` · `Não Contratado` |
| `Valor em Risco Danos Materiais` | **número** (o script grava como texto BR `20.000.000,00`) |

No **Amplo**, o `Valor em Risco Danos Materiais` faz o papel da cobertura básica `Ampla`, que não
tem coluna no template: os percentuais "da Ampla" são calculados sobre ele (1.000.000,00 a
100.000.000,00).

## Perguntas de coluna única — chave `perguntas`

| Pergunta | Resposta |
|---|---|
| `O condomínio está legalmente constituído?` | `Sim` · `Não` |
| `O Condomínio possui elevador?` | `Sim` · `Não` |
| `Qual a quantidade de elevadores?` | só quando tem elevador (ex.: `4`). Sem elevador, o script deixa vazio |
| `O Condomínio Possui Central Telefônica e/ou equipamentos de segurança e/ou monitoramento?` | `Sim` · `Não` |

As respostas exatas aceitas pelo sistema nessas perguntas **ainda serão confirmadas pelo
usuário**. Até lá, use `Sim`/`Não`. Na quantidade de elevadores, se o pedido não disser,
pergunte.

## Grupos — chave `grupos`

| Grupo | Opções | Regra |
|---|---|---|
| `Deseja contratar indenização a valor de novo? Condominio` | `SIM` | opcional: `["SIM"]` contrata (grava `Sim`); sem o grupo = não contrata (grava `Não`) |
| `Quantidade de Pavimentos (incluindo térreo, garagem e subsolos)?` | `1 a 5 andares` · `6 a 10 andares` · `11 a 15 andares` · `Acima de 15 andares` · `Não informado` | obrigatório, escolha única |
| `Qual a idade do Condomínio?` | `Até 5 anos` · `De 6 a 10` · `De 11 a 20` · `De 21 a 30` · `Mais que 30 anos` | obrigatório, escolha única |

## Coberturas — chave `coberturas`

### Condomínio Amplo (18)

Responsabilidade Civil - Condomínio + Síndico · Despesas com Aluguel Condôminos ·
Incêndio de Bens Dos Condôminos · Perda Ou Pagamento de Aluguel a Terceiros (com
`periodo_indenitario`) · Responsabilidade Civil - Danos Morais · Responsabilidade Civil -
Empregador · Responsabilidade Civil - Guarda de Veículos + Portões Automáticos (incêndio e
Roubo/furto) · Responsabilidade Civil - Guarda de Veículos + Portões Automáticos (colisão,
Incêndio e Roubo/furto) · Responsabilidade Civil - Portões · Roubo de Valores · Roubo E/ou Furto
Qualificado de Bens Dos Condôminos · e o Plano de Vida (abaixo)

### Condomínio Tradicional (29)

`Incêndio, Queda de Raio, Explosão, Queda de Aeronave e Fumaça` (**básica**) ·
Responsabilidade Civil - Condomínio + Síndico · Responsabilidade Civil - Empregador · Alagamento ·
Anúncios Luminosos · Danos Elétricos · Derrame Ou Vazamento de Chuveiros Automáticos (sprinklers)
· Desmoronamento e Tremor de Terra · Despesas com Aluguel Condôminos (com
`periodo_indenitario`) · Incêndio de Bens Dos Condôminos · Perda Ou Pagamento de Aluguel a
Terceiros (com `periodo_indenitario`) · Quebra de Vidros · Responsabilidade Civil - Danos Morais ·
RC - Guarda de Veículos + Portões Automáticos (incêndio e Roubo/furto) · RC - Guarda de Veículos +
Portões Automáticos (colisão, Incêndio e Roubo/furto) · Responsabilidade Civil - Portões · Roubo
de Valores · Roubo E/ou Furto Qualificado de Bens do Condomínio · Roubo E/ou Furto Qualificado de
Bens Dos Condôminos · Ruptura de Tanques e Tubulações · Tumultos, Greves e Lockout · Vendaval,
Furacão, Ciclone, Tornado, Granizo e Impacto de Veículos · e o Plano de Vida (abaixo)

### Plano de Vida (os dois ramos)

`Morte` (aceita `"qt_vidas": N` no item, que vai para a coluna "Qt de vidas") ·
`Invalidez Permanente Total Ou Parcial Por Acidente (ipa)` · `Indenização Especial Por Acidente
(iea)` · `Invalidez Funcional Permanente Total Por Doença (ifpd)` · `Cesta Básica` ·
`Morte Cônjuge` · `Auxílio Funeral`

Valores fixos: IPA, IEA e IFPD = 5.000,00 · Cesta Básica = 1.000,00 · Morte Cônjuge = 2.500,00 ·
Auxílio Funeral = 3.000,00. `Morte` vai de 5.000,00 a 100.000,00 e exige IPA.

Limites, dependências e excludentes: `lmi_condominio_amplo.md` / `lmi_condominio_tradicional.md`
(em dados: `regras_condominio_amplo.json` / `regras_condominio_tradicional.json`).

## Exemplo (Amplo)

```json
{"ramo": "condominio_amplo", "massas": [{
  "campos": {"Perfil": "Corretor", "Corretor": "COI", "Tipo Pessoa": "#cnpj", "Cep": "#cep"},
  "combos": {"Tipo de Condomínio": "Condomínio Exclusivamente Residencial - Vertical",
             "Tipo de Construção": "Superior / Sólida", "Objeto Segurado": "Prédio e Conteúdo",
             "Assistência 24h INPUT": "Assistência Condomínio Plano Básico",
             "Valor em Risco Danos Materiais": 20000000},
  "perguntas": {"O condomínio está legalmente constituído?": "Sim",
                "O Condomínio possui elevador?": "Sim", "Qual a quantidade de elevadores?": "2",
                "O Condomínio Possui Central Telefônica e/ou equipamentos de segurança e/ou monitoramento?": "Sim"},
  "grupos": {"Deseja contratar indenização a valor de novo? Condominio": ["SIM"],
             "Quantidade de Pavimentos (incluindo térreo, garagem e subsolos)?": ["11 a 15 andares"],
             "Qual a idade do Condomínio?": ["De 11 a 20"]},
  "coberturas": [
    {"nome": "Responsabilidade Civil - Condomínio + Síndico", "valor": 1000000},
    {"nome": "Incêndio de Bens Dos Condôminos", "valor": 500000},
    {"nome": "Perda Ou Pagamento de Aluguel a Terceiros", "valor": 300000, "periodo_indenitario": 6},
    {"nome": "Morte", "valor": 20000, "qt_vidas": 10},
    {"nome": "Invalidez Permanente Total Ou Parcial Por Acidente (ipa)", "valor": 5000}]}]}
```

No Tradicional, inclua sempre a básica `Incêndio, Queda de Raio, Explosão, Queda de Aeronave e
Fumaça` (600.000,00 a 150.000.000,00) e calcule as demais a partir dela.
