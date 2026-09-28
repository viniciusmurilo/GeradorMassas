# Normas de Subscrição — Empresarial (HDI Seguros, base "Normas - HML")

Extraído e organizado de `Normas_-_HML.xlsx` (99 regras do produto Empresarial). Fonte: planilha
de controle de normas de homologação — texto de origem preservado, só limpo de artefatos de
formatação (`\xa0`, espaços duplicados).

**Como usar**: por padrão (pedido sem menção a testar erro), uma massa gerada **nunca** deve
violar nenhuma regra abaixo — mantenha valores dentro dos limites, evite combinações banidas,
respeite mínimos de proteção. Se o usuário pedir para **testar** uma regra específica (ex.: "gera
uma massa que estoura o limite de Alagamento"), gere de propósito o valor/combinação que a
dispara, e avise no resumo qual norma está sendo testada.

## Tipo de Construção

- `Mista` e `Inferior` **não têm aceitação comercial** — nunca use em massa válida.
- Atividades abaixo só aceitam `Sólida` (não `Superior`, mesmo sendo opção da lista):
  Arroz - Beneficiamento e Engenho · Grãos em Geral - Loja · Grãos em Geral - Beneficiamento /
  Depósito (Exceto Amendoim).

## Objeto Segurado restrito a "Prédio"

Só é permitido `Objeto Segurado = Prédio` (não `Prédio e Conteúdo` nem `Conteúdo`) para estas
atividades: Edificação Vertical Exclusivamente Comercial · Joalheria - Loja e Depósito ·
Joias - Fábrica · Edifício, Desocupado · Guarda-Móveis.

## Coberturas sem aceitação comercial (nunca usar em massa válida)

Lista completa e atualizada em `lmi_empresarial.md` §Coberturas sem aceitação comercial (fonte
"Resumo coberturas"). Inclui, entre outras, Responsabilidade Civil - Guarda de Embarcações de
Terceiros e Responsabilidade Civil - Produtos.

## Cobertura restrita para atividades específicas

`Bens Depositados em Guarda Volume` não é permitida para uma lista extensa de atividades (comércio
de autopeças, automóveis, alimentos, bebidas, bijuterias, etc. — lista longa e **possivelmente
incompleta na fonte**, o texto original corta abruptamente). Se o pedido envolver essa cobertura
junto com uma atividade de varejo/fábrica citada na lista original, confira antes de incluir; na
dúvida, pergunte.

## Limite máximo por cobertura

Os tetos por cobertura (máximo do corretor, se bloqueia ou vai para análise técnica, alçadas e
% da básica) estão em `lmi_empresarial.md` §Tabela de limites. Essa tabela, da fonte "Resumo
coberturas", substitui a que ficava aqui. Os limites mais restritivos por CEP/UF (abaixo)
continuam valendo por cima dela.

## Soma de coberturas de Responsabilidade Civil (LMG RC)

A **soma de todas** as coberturas "Responsabilidade Civil - *" numa mesma massa não pode
ultrapassar **R$ 5.000.000,00** no total — mesmo que cada uma isolada esteja dentro do próprio teto
da tabela acima.

## Limite Máximo de Garantia (LMG) por atividade

- **Bicicleta - Loja, Depósito e Oficina**: LMG de R$ 50.000.000,00 (Valor em Risco não deve
  passar disso quando a atividade for essa).

## Mudança de enquadramento por valor

- Atividade **Bijuteria - Loja e Depósito** com Valor em Risco acima de R$ 4.000.000,00 deve, na
  prática, ser reclassificada como **Plástico, Artigos - Loja e Depósito**. Numa massa válida com
  essa atividade e valor alto, use a atividade já reclassificada.

## Necessita Análise Técnica por atividade (Valor em Risco acima do limite)

Massa válida = atividade abaixo com Valor em Risco **até** o limite (inclusive):

| Atividade | Limite (R$) |
|---|---:|
| Academias | 150.000.000,00 |
| Supermercado / Hipermercado | 10.000.000,00 |
| Armazéns sem Depósito de Inflamáveis - Sem Armazenamento de Algodão | 10.000.000,00 |
| Transportadora - Sem Armazenamento de Algodão | 5.000.000,00 |
| Adubo - Depósito | 4.000.000,00 |
| Armarinho - Loja e Depósito | 4.000.000,00 |
| Barco / Bote / Jet Ski - Loja e Depósito | 4.000.000,00 |
| Agência Correio | 30.000.000,00 |
| Agropecuários, Produtos - Loja e Depósito | 30.000.000,00 |
| Água, Extração e Engarrafamento | 30.000.000,00 |
| Alimento para Animais - Fábrica | 30.000.000,00 |
| Alimento para Animais - Loja e Depósito | 30.000.000,00 |
| Alimento, Conservas - Loja e Depósito | 30.000.000,00 |
| Arroz - Beneficiamento e Engenho | 30.000.000,00 |
| Asilo / Albergue / Creche | 30.000.000,00 |
| Bicicleta - Loja, Depósito e Oficina | 30.000.000,00 |

Atividade fora desta tabela: sem limite documentado — use bom senso.

## Inspeção de risco obrigatória

- Cobertura **Alagamento** com valor acima de R$ 50.000,00.
- Cobertura **Quebra de Máquinas** com valor acima de R$ 100.000,00.
- Cobertura **Roubo E/ou Furto Qualificado de Bens** com valor acima de R$ 100.000,00.
- Atividade **Banca de Jornal e Revista** com Valor em Risco acima de R$ 500.000,00.
- Atividade **Bijuterias - Fábricas** (excluindo metais/artefatos/joias/pedras preciosas) com
  Valor em Risco acima de R$ 500.000,00.
- Atividade **Brechó** com Valor em Risco acima de R$ 500.000,00.
- Atividade **Chapéu - Loja e Depósito** com Valor em Risco acima de R$ 500.000,00.
- Atividade **Açúcar - Depósito** — inspeção obrigatória independente de valor.
- Atividade **Açúcar, Usina sem Produção de Álcool** — inspeção obrigatória independente de valor.

(A skill não gera automaticamente o resultado da inspeção — só evita, por padrão, gerar massa que
force essa exigência, a menos que peçam para testar.)

## Protecionais mínimos de incêndio (exigem "Extintores" ou superior no grupo de proteção)

Para estas atividades, o grupo `Existem equipamentos de proteção contra incêndio?` numa massa
válida precisa de pelo menos `Extintores` marcado (nunca deixe em branco/"Não informado"):
Supermercado / Hipermercado · Arroz - Beneficiamento e Engenho ·
Grãos em Geral - Beneficiamento / Depósito (Exceto Amendoim) · Grãos em Geral - Loja · Papelaria ·
Automóvel - Concessionária · Livraria (Exceto Depósito) ·
Metal, Artigos - Fábrica sem Processo a Quente · Posto de Serviço, com Venda de Combustíveis ·
Posto de Serviço, sem Venda de Combustíveis · Tintas e Vernizes - Loja e Depósito.

## Protecionais mínimos de roubo (exigem "Sistema de alarme contra roubo" no grupo de proteção)

- **Arroz - Beneficiamento e Engenho**: obrigatório quando a cobertura de Roubo passar de
  R$ 100.000,00.
- **Grãos em Geral - Beneficiamento / Depósito (Exceto Amendoim)**: obrigatório quando a
  cobertura de Roubo passar de R$ 100.000,00.
- **Grãos em Geral - Loja**: obrigatório em **qualquer valor** de cobertura de Roubo.

## Combinações excludentes (não podem coexistir na mesma massa)

Lista completa em `lmi_empresarial.md` §Excludentes, incluindo `Despesas Fixas - Ampla` ×
DF/LC-Incêndio e todas as variantes de DF/LC por danos elétricos e vendaval.

## UF / CEP bloqueados

- **UF bloqueada**: AC (Acre), RR (Roraima), AP (Amapá) — exceto para os corretores
  "JGS CORRETORA DE SEGUROS LTDA" e "LOJACORR R C S".
- **UF bloqueada para Alagamento**: RS (Rio Grande do Sul) e SC (Santa Catarina) — não incluir
  cobertura de Alagamento em massa com risco nesses estados.
- **CEP bloqueado (geral)**: `01021-000` (Região 25 de Março, São Paulo/SP).
- **CEP bloqueado para Alagamento/Desmoronamento**: `25650-001` (Petrópolis/RJ, ambas as
  coberturas) e `95671-715` (Gramado/RS, Desmoronamento).
- **CEP com limite reduzido de Vendaval**: `83880-000`, `84145-000`, `85450-000` — teto de
  R$ 6.000.000,00 para `Vendaval, Furacão, Ciclone, Tornado, Granizo e Impacto de Veículos`,
  `Vendaval para concessionárias (exceto veículos ao ar livre)` e
  `Vendaval para concessionárias (inclusive veículos ao ar livre)` (mais restritivo que o teto
  geral de R$ 7.500.000,00 da tabela principal).

## Fora de escopo

Regras de "Condomínio Tradicional", "Condomínio Amplo" e "Condomínio Tradicional e Amplo" existem
na planilha de origem mas **não têm template** nesta skill. Os limites de LMI desses ramos já
estão salvos em `lmi_condominio_amplo.md` e `lmi_condominio_tradicional.md` para quando o
template chegar.
