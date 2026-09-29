# Normas de Subscrição — Residencial (HDI Seguros, base "Normas - HML")

Extraído e organizado de `Normas_-_HML.xlsx` (24 regras do produto Residencial). Mesma política
de uso do `normas_empresarial.md`: por padrão, massa gerada nunca viola nenhuma regra abaixo; só
viole de propósito quando o pedido for testar aquele erro específico.

## Coberturas não permitidas (nunca usar em massa válida)

- **Alagamento** — não disponível para contratação neste ramo, mesmo existindo coluna no template.
- **All risks** — idem.
- **Desmoronamento**, **PAISAGISMO**, **Objetos de arte e obras de arte**,
  **Responsabilidade civil - tacos de golfe**, **Responsabilidade civil - hole-in-one** — sem
  aceitação comercial segundo a planilha de LMI (ver `lmi_residencial.md`).

## Objeto Segurado x Tipo de Residência

- `Tipo de Residência = Casa Desocupada` exige `Objeto Segurado = Prédio` (nunca
  "Prédio e Conteúdo" nem "Conteúdo").
- Imóveis desocupados (Casa Desocupada, Casa em Condomínio Fechado Desocupada e Apartamento
  Desocupado) só aceitam Incêndio e `Vendaval, Furacão, Ciclone, Tornado, Granizo, Neve e Geada`.
  Detalhes em `lmi_residencial.md` §Por tipo de residência.

## Limite máximo por cobertura

Os tetos por cobertura (máximo do corretor por tipo de residência, % da básica, alçadas e
dependências) estão em `lmi_residencial.md`. A fonte é "Resumo coberturas Residencial", que
substitui a tabela que ficava aqui.

## Soma de coberturas de Responsabilidade Civil (LMG RC)

A soma de `Responsabilidade Civil - Familiar` + `Responsabilidade Civil - Danos Morais` +
`Responsabilidade Civil - Empregados Domésticos` + `Responsabilidade Civil - Prática de Esporte`
numa mesma massa não pode ultrapassar **R$ 3.000.000,00** no total.

## Cobertura obrigatória (dependência entre coberturas)

Se a massa incluir `Responsabilidade Civil - Danos Morais`, ela **também precisa** incluir
`Responsabilidade Civil - Familiar` (regra de produto, não só de homologação — sempre respeitar).

## Análise técnica por Valor em Risco

Para **qualquer** um dos 9 tipos de residência (Casa Habitual, Casa Veraneio, Apartamento
Habitual, Apartamento Veraneio, Casa em Condomínio Fechado Habitual, Casa em Condomínio Fechado
Veraneio, Casa Desocupada, Casa em Condomínio Fechado Desocupada, Apartamento Desocupado), Valor
em Risco acima de **R$ 10.000.000,00** exige análise técnica — numa massa válida, mantenha o valor
da cobertura principal (proxy de valor em risco, já que este ramo não tem coluna própria de "Valor
em Risco") até esse teto.

## Inspeção de risco obrigatória (cobertura de Roubo por tipo de residência)

| Tipo de Residência | Teto de Roubo sem inspeção (R$) |
|---|---:|
| Casa Habitual | 100.000,00 |
| Casa em Condomínio Fechado Habitual | 100.000,00 |
| Casa em Condomínio Fechado Veraneio | 50.000,00 |
| Casa Veraneio | 30.000,00 |

Nos três tipos de veraneio (Casa Veraneio, Apartamento Veraneio e Casa em Condomínio Fechado
Veraneio), o **máximo do corretor** para Roubo é 30.000,00. Acima disso a cotação é bloqueada
(ver `lmi_residencial.md`). Numa massa válida de veraneio, use Roubo ≤ 30.000,00.

## UF / CEP bloqueados ou restritos

- **UF com aceitação restrita para Vendaval Ao Ar Livre**: PR, RS, SC — evite a cobertura
  `Vendaval, furacão, ciclone, tornado, granizo e fumaça para bens ao ar livre` (ou as outras
  variantes de vendaval do ramo) em massa com risco nesses estados.
- **CEP bloqueado para Vendaval**: existe bloqueio de CEP específico para essa mesma cobertura
  (CEP exato não detalhado na fonte — se o pedido citar um CEP do Sul do país junto com cobertura
  de vendaval, trate como risco de violar a norma e avise/pergunte).
- **Região restrita**: bairros de Maceió/AL têm restrição geral para este produto.

## Fora de escopo

Regras de "Condomínio Tradicional", "Condomínio Amplo" e "Condomínio Tradicional e Amplo" existem
na planilha de origem mas **não têm template** nesta skill. Os limites de LMI desses ramos já
estão salvos em `lmi_condominio_amplo.md` e `lmi_condominio_tradicional.md` para quando o
template chegar.
