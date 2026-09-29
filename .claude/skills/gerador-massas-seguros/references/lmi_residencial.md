# Regras por Cobertura — Residencial (produto 5)

Fonte principal: planilha **"Resumo coberturas Residencial"**. A aba `Planilha1` traz os limites
por cobertura; a `Planilha2` traz a automaticidade e as alçadas por tipo de residência. Os códigos
de erro da homologação vêm da planilha "Coberturas x LMI". Se algo aqui divergir de
`normas_residencial.md`, **vale este arquivo**, exceto as restrições de UF/CEP da norma, que
continuam valendo por cima.

## Como aplicar numa massa válida

Cada cobertura tem estes limites ao mesmo tempo:

1. **Mínimo** (R$).
2. **Máximo do corretor** (R$). Depende do **tipo de residência** (ver §Por tipo de residência).
   Acima dele, a cotação é bloqueada ("não permite a cotação"). A única exceção é o Incêndio, que
   vai para análise técnica.
3. **% máx da básica**: percentual do LMI de
   `Incêndio, queda de raio, explosão, implosão e queda de aeronaves`.
4. Para as RC que exigem `Responsabilidade Civil - Familiar`: **até 100% do LMI da RC Familiar**.

Teto efetivo = **o menor** de todos esses valores. Consequências práticas:

- Toda massa precisa ter a **cobertura básica (Incêndio)** com valor. Defina ela primeiro e
  calcule as demais a partir dela.
- Ex.: Incêndio = 500.000 → Danos Elétricos ≤ min(1.000.000; 30% × 500.000) = **150.000**.

## LMG do item

A soma dos LMIs que compõem o LMG não pode passar de **R$ 76.000.000,00** (limite do Gerente).
Compõem o LMG: Incêndio, Perda Ou Pagamento de Aluguel, RC Familiar, RC Empregados Domésticos e
RC Prática de Esporte.

## Tabela de limites (tipos de residência habituais)

Nomes na grafia do template (`catalogo_residencial.md`). "Máx corretor" vale para Casa Habitual,
Apartamento Habitual e Casa em Condomínio Fechado Habitual. Para os tipos de veraneio e
desocupados, veja a seção seguinte. "Alçadas" = até quanto cada nível aprova acima do corretor
(Analista / Coordenador; o Gerente aprova até 76.000.000,00).

| Cobertura | Cód | Mín (R$) | Máx corretor (R$) | Acima do máx | % máx da básica | Exige | Alçadas Analista / Coord |
|---|---:|---:|---:|---|---:|---|---|
| Incêndio, queda de raio, explosão, implosão e queda de aeronaves | 1000 | 10.000,00 | 10.000.000,00 | análise técnica | — (básica) | — | 15.000.000,00 / 20.000.000,00 |
| Bicicletas | 0066 | 1.000,00 | 300.000,00 | BLOQUEIA | 30% | — | 300.000,00 / 400.000,00 |
| Danos Elétricos | 0007 | 500,00 | 1.000.000,00 | BLOQUEIA | 30% | — | 1.000.000,00 / 1.000.000,00 |
| Vendaval, Furacão, Ciclone, Tornado, Granizo, Neve e Geada | 0030 | 500,00 | 700.000,00 | BLOQUEIA | 50% | — | 700.000,00 / 1.000.000,00 |
| Vendaval, furacão, ciclone, tornado, granizo e fumaça para bens ao ar livre | 1068 | 500,00 | 150.000,00 | BLOQUEIA | 40% | — | 150.000,00 / 700.000,00 |
| Roubo E/ou Furto Qualificado de Bens | 0025 | 500,00 | 500.000,00 | BLOQUEIA | 20% | — | 500.000,00 / 600.000,00 |
| Perda Ou Pagamento de Aluguel | 0031 | 500,00 | 1.000.000,00 | BLOQUEIA | 50% | — | 1.000.000,00 / 1.200.000,00 |
| Equipamentos Eletrônicos e Eletrodomésticos | 0057 | 500,00 | 500.000,00 | BLOQUEIA | 30% | — | 500.000,00 / 1.000.000,00 |
| Quebra de Vidros | 0015 | 500,00 | 500.000,00 | BLOQUEIA | 30% | — | 500.000,00 / 600.000,00 |
| Responsabilidade Civil - Familiar | 0040 | 500,00 | 3.000.000,00 | BLOQUEIA | 100% | — | 3.000.000,00 / 3.000.000,00 |
| Responsabilidade Civil - Danos Morais | 0039 | 500,00 | 300.000,00 | BLOQUEIA | — | RC Familiar (≤100% dela) | 300.000,00 / 300.000,00 |
| Responsabilidade Civil - Empregados Domésticos | 0067 | 500,00 | 600.000,00 | BLOQUEIA | — | RC Familiar (≤100% dela) | 600.000,00 / 720.000,00 |
| Responsabilidade Civil - Prática de Esporte | 0068 | 500,00 | 600.000,00 | BLOQUEIA | — | RC Familiar (≤100% dela) | 600.000,00 / 720.000,00 |
| Ruptura de Tubulações e Vazamento Acidental | 0019 | 500,00 | 200.000,00 | BLOQUEIA | 50% | — | 200.000,00 / 500.000,00 |
| Tumultos, Greves e Lockout | 0006 | 500,00 | 1.000.000,00 | BLOQUEIA | 30% | — | 1.000.000,00 / 2.000.000,00 |
| Roubo E/ou Furto Qualificado de Bicicleta Fora da Residência | 0065 | 1.000,00 | 60.000,00 | BLOQUEIA | 30% | — | 60.000,00 / 72.000,00 |
| Microempreendedor Em Residência | 0022 | 500,00 | 500.000,00 | BLOQUEIA | 30% | — | 500.000,00 / 600.000,00 |
| Escritório Em Residência | 0020 | 500,00 | 500.000,00 | BLOQUEIA | 30% | — | 500.000,00 / 600.000,00 |
| Impacto de Veículos | 0005 | 500,00 | 10.000.000,00 | BLOQUEIA | 100% | — | 15.000.000,00 / 20.000.000,00 |
| Equipamentos de Energia Solar e Fotovoltaico | 0011 | 500,00 | 1.000.000,00 | BLOQUEIA | 10% | — | 1.000.000,00 / 2.000.000,00 |
| Carro Na Garagem | 0021 | 500,00 | 300.000,00 | BLOQUEIA | 30% | — | 300.000,00 / 360.000,00 |
| Anfitrião | 0023 | 500,00 | 500.000,00 | BLOQUEIA | 30% | — | 500.000,00 / 600.000,00 |

`Indenização a Valor de Novo` (0084) não tem limite na fonte e não tem coluna de valor no template.
Ela é só o grupo SIM/NÃO `Deseja contratar indenização a valor de novo?`.

## Por tipo de residência

| Tipo de Residência (template) | Ocupação na fonte | O que muda |
|---|---|---|
| Casa Habitual | 10000 Residência Habitual Casa | tabela acima, sem mudanças |
| Apartamento Habitual | 10002 Residência Habitual Apartamento | tabela acima, sem mudanças |
| Casa em Condomínio Fechado Habitual | 10019 Casa Habitual em Condomínio Fechado | tabela acima, sem mudanças |
| Casa Veraneio | 10001 Residência Veraneio Casa | `Roubo E/ou Furto Qualificado de Bens`: máx corretor **30.000,00** (acima bloqueia) |
| Apartamento Veraneio | 10003 Residência Veraneio Apartamento | idem: Roubo até **30.000,00** |
| Casa em Condomínio Fechado Veraneio | 10020 Casa Veraneio em Condomínio Fechado | idem: Roubo até **30.000,00** |
| Casa Desocupada | 10022 Imóvel Desocupado Casa | **só** Incêndio e `Vendaval, Furacão, Ciclone, Tornado, Granizo, Neve e Geada` |
| Casa em Condomínio Fechado Desocupada | 10023 Imóvel Desocupado Casa Condom. | idem: **só** Incêndio e Vendaval (Neve e Geada) |
| Apartamento Desocupado | 10024 Imóvel Desocupado Apto | idem: **só** Incêndio e Vendaval (Neve e Geada) |

Nos três tipos desocupados, todas as outras coberturas têm automaticidade 0 ("Cobertura
indisponível"), inclusive as RC, Danos Elétricos, Roubo, Perda de Aluguel e Quebra de Vidros.
Numa massa válida com imóvel desocupado, use apenas Incêndio e, se quiser, o Vendaval (Neve e
Geada). Alçadas acima do corretor continuam as da tabela.

## Coberturas sem aceitação comercial (nunca usar em massa válida)

Automaticidade 0 em todos os tipos de residência ("Cobertura indisponível"). O coordenador
aprova até 100.000,00. Só marque uma delas para testar a rejeição.

| Cobertura | Cód | Código do erro |
|---|---:|---|
| Alagamento | 0018 | CB14.26001 |
| All risks | 2110 | CB14.26002 (exige relação de bens) |
| Desmoronamento | 0032 | CB14.26009 |
| PAISAGISMO | 2113 | CB14.26017 |
| Objetos de arte e obras de arte | 1042 | CB14.26016 (exige relação de bens) |
| Responsabilidade civil - tacos de golfe | 2112 | CB14.26027 (exige RC Familiar) |
| Responsabilidade civil - hole-in-one | 2111 | CB14.26013 (exige RC Familiar) |

A fonte também lista Ressaca (1043) e Terremoto (1044) como indisponíveis, mas essas coberturas
não existem no template residencial.

## Assistências e benefícios (fonte, para referência)

A fonte lista os benefícios agrupados por plano de assistência:

- **Assistência Residencial Plano Básico**: Residencial Benefícios Essenciais · Inspeção Kids ·
  Inspeção Sênior · Inspeção para Acessibilidade · Benefícios Bike · Benefícios Pet · Limpeza de
  Placa Solar
- **Plano Intermediário**: Residencial Benefícios Intermediários · Assistência Funeral Familiar ·
  Benefícios HelpDesk
- **Plano Superior**: Residencial Benefícios Superiores · Assistência Funeral Familiar ·
  Benefícios HelpDesk

Os 7 benefícios do Plano Básico são exatamente os campos `bool` do template. A fonte não diz se
eles exigem esse plano. Na dúvida, numa massa válida com benefícios marcados, use
`Assistência 24h = Assistência Residencial Plano Básico`.

## Códigos de erro de teto (para massas que testam o limite)

Mensagem padrão: `ITEM 1 - <código> - O valor informado para a cobertura de <nome> excede o
limite máximo permitido de R$ <máx>.`

| Cobertura | Código |
|---|---|
| Anfitrião | CB14.26003 |
| Vendaval ... para bens ao ar livre | CB14.26004 |
| Bicicletas | CB14.26005 |
| Carro Na Garagem | CB14.26006 |
| Danos Elétricos | CB14.26007 |
| Equipamentos Eletrônicos e Eletrodomésticos | CB14.26011 |
| Escritório Em Residência | CB14.26012 |
| Impacto de Veículos | CB14.26014 |
| Microempreendedor Em Residência | CB14.26015 |
| Quebra de Vidros | CB14.26019 |
| Perda Ou Pagamento de Aluguel / RC Familiar | CB14.26022 (a fonte usa o mesmo código para as duas) |
| Roubo E/ou Furto Qualificado de Bens | CB14.26024 |
| Roubo E/ou Furto Qualificado de Bicicleta Fora da Residência | CB14.26025 |
| Ruptura de Tubulações e Vazamento Acidental | CB14.26026 |
| Tumultos, Greves e Lockout | CB14.26029 |
| Vendaval, Furacão, Ciclone, Tornado, Granizo, Neve e Geada | CB14.26030 |
