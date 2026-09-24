# Catálogo de Colunas — Residencial (`templates/template_residencial.xlsx`)

Uma linha = uma massa completa. Cabeçalho na **linha 2**, dados a partir da **linha 3**. Mesmo
mecanismo de pareamento por nome do empresarial — ver `scripts/preencher_massa.py`.

## Campos diretos (obrigatórios) — chave `campos`

| Cabeçalho | Conteúdo |
|---|---|
| `Corretor` | Nome do corretor |
| `Tipo Pessoa` | CPF/CNPJ do segurado — ver "Tokens de aleatoriedade" em `catalogo_empresarial.md` (mesmas regras: `#cpf`/`#cnpj`/`#cnpjalfa` ou valor literal) |
| `Cep` | CEP do risco — token `#cep` ou valor literal |

## Combos (obrigatórios) — chave `combos`

| Cabeçalho | Valores válidos |
|---|---|
| `Tipo de Residência` | `Apartamento Desocupado` · `Apartamento Habitual` · `Apartamento Veraneio` · `Casa Desocupada` · `Casa em Condomínio Fechado Desocupada` · `Casa em Condomínio Fechado Habitual` · `Casa em Condomínio Fechado Veraneio` · `Casa Habitual` · `Casa Veraneio` |
| `Tipo de Construção` | `Superior / Sólida` · `Mista` · `Inferior` |
| `Objeto Segurado` | `Prédio e Conteúdo` · `Prédio` · `Conteúdo` |
| `Assistência 24h` | `Assistência Residencial Plano Superior` · `Assistência Residencial Plano Intermediário` · `Assistência Residencial Plano Básico` · `Não Contratado` |

Sem campo `texto` neste ramo (não existe atividade nem valor em risco separado — o "valor em
risco" de cada cobertura é o próprio valor da cobertura).

**Atenção**: `Para Casa Desocupada deve ser contratado objeto segurado Prédio` — numa massa
válida com `Tipo de Residência = Casa Desocupada`, use sempre `Objeto Segurado = Prédio`
(ver `references/normas_residencial.md`).

## Campos booleanos independentes — chave `bool`

Cada um é um `sim`/`<IGNORE>` isolado (não fazem parte de grupo — pode marcar quantos quiser):

`Residencial Benefícios Essenciais` · `Benefícios Bike` · `Benefícios Pet` · `Inspeção Kids` ·
`Inspeção para Acessibilidade` · `Inspeção Sênior` · `Limpeza de Placa Solar`

## Grupos de escolha — chave `grupos`, **os 2 abaixo são obrigatórios**

O script recusa se algum dos dois não aparecer em `grupos`. Se o usuário não disser nada sobre
proteção/indenização, use o padrão indicado em cada um.

### `Deseja contratar indenização a valor de novo?` — escolha única, obrigatório
Opções: `SIM` · `NÃO`. Padrão quando o usuário não especificar: `["NÃO"]`.

### `Equipamentos de Proteção` — múltipla escolha, obrigatório
Opções: `Alarme` · `Grades Metálicas em Janelas` · `Inexistência de terreno baldio` ·
`Porteiro Eletrônico` · `Vigilância exclusiva e permanente` · `Extintores` · `Não informado`.
Padrão: `["Não informado"]`.

Pode marcar mais de uma ao mesmo tempo (ex.: `Alarme` + `Extintores`), **exceto** `Não informado`,
que é exclusiva — o script recusa se ela vier junto com qualquer outra opção do grupo.

## Coberturas — chave `coberturas`

29 coberturas com coluna `TXT "<nome>" Valor da Cobertura`. **Nenhuma tem Período Indenitário**
neste ramo — nunca envie `periodo_indenitario` numa massa residencial (o script rejeita).

**Sete coberturas existem na planilha mas NÃO podem ser usadas numa massa válida** (sem
aceitação comercial — ver `references/normas_residencial.md` §Coberturas não permitidas e
`references/lmi_residencial.md`): `Alagamento`, `All risks`, `Desmoronamento`, `PAISAGISMO`,
`Objetos de arte e obras de arte`, `Responsabilidade civil - tacos de golfe` e
`Responsabilidade civil - hole-in-one`. Só marque uma delas se o pedido for explicitamente testar essa rejeição.

**Lista completa (29):**

Alagamento · All risks · Anfitrião · Bicicletas · Carro Na Garagem · Danos Elétricos ·
Desmoronamento · Equipamentos Eletrônicos e Eletrodomésticos ·
Equipamentos de Energia Solar e Fotovoltaico · Escritório Em Residência · Impacto de Veículos ·
Incêndio, queda de raio, explosão, implosão e queda de aeronaves ·
Microempreendedor Em Residência · Objetos de arte e obras de arte · PAISAGISMO ·
Perda Ou Pagamento de Aluguel · Quebra de Vidros ·
Responsabilidade Civil - Danos Morais · Responsabilidade Civil - Empregados Domésticos ·
Responsabilidade Civil - Familiar · Responsabilidade Civil - Prática de Esporte ·
Responsabilidade civil - hole-in-one · Responsabilidade civil - tacos de golfe ·
Roubo E/ou Furto Qualificado de Bens · Roubo E/ou Furto Qualificado de Bicicleta Fora da Residência ·
Ruptura de Tubulações e Vazamento Acidental · Tumultos, Greves e Lockout ·
Vendaval, Furacão, Ciclone, Tornado, Granizo, Neve e Geada ·
Vendaval, furacão, ciclone, tornado, granizo e fumaça para bens ao ar livre

### Sobre o antigo "defeito de template"

O template antigo (removido desta skill) tinha um CHK órfão em `Microempreendedor Em Residência`
(sem coluna de valor). **Esse defeito não existe mais** neste template novo — a cobertura tem
coluna de valor normal e pode ser usada livremente.

### Correção do template (22/09)

A coluna `TXT "Vendaval, Furacão, Ciclone, Tornado, Granizo e Impacto de Veículos - para Bens Ao
Ar Livre" Valor da Cobertura` foi **removida** do template residencial pelo dono do produto — era
uma cobertura empresarial vazada por engano no template residencial (mesmo defeito de arquivo
vazado que já existia com `CHK Residencial Benefícios Essenciais` no empresarial). Essa cobertura
**não existe mais** no ramo residencial; se aparecer numa referência antiga ou o usuário pedir
"vendaval e impacto de veículos" para residencial, é sinal de confusão com o catálogo empresarial
— use uma das duas variantes de vendaval que restam.

### Regras de desambiguação

- **Vendaval**: duas variantes distintas — "...Neve e Geada" (sem "para Bens Ao Ar Livre") e
  "...fumaça para bens ao ar livre" (minúsculo — confira a grafia exata na lista antes de gravar).
  Só "vendaval" no pedido → pergunte qual.
- **Incêndio, queda de raio...** ≠ a cobertura homônima do empresarial: aqui a ordem/redação é
  "Incêndio, queda de raio, explosão, implosão e queda de aeronaves" (minúsculo, sem "Fumaça").
- **Responsabilidade Civil**: "Danos Morais" ≠ "Empregados Domésticos" ≠ "Familiar" ≠
  "Prática de Esporte" ≠ "hole-in-one" ≠ "tacos de golfe". Só "RC" → pergunte.
- **Roubo/Furto Qualificado de Bens** (da residência) ≠ "...de Bicicleta Fora da Residência".
- **Bicicletas** (cobre a bicicleta em si, dentro da residência) ≠
  **Roubo E/ou Furto Qualificado de Bicicleta Fora da Residência** (cobre o roubo/furto quando a
  bicicleta está fora de casa). Pedido genérico de "cobertura de bicicleta" sem dizer onde →
  pergunte qual das duas (ou as duas).
- **"Indenização a valor de novo"** não é cobertura neste template (a coluna de valor foi
  removida) — só existe o grupo `Deseja contratar indenização a valor de novo?` (SIM/NÃO).

## Overlap com Empresarial

Ver `references/catalogo_empresarial.md` §Overlap com Residencial — 7 nomes em comum, grafia
idêntica nos dois catálogos.
