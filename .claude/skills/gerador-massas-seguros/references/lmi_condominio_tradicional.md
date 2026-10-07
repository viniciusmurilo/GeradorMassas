# Regras por Cobertura — Condomínio Tradicional (produto 119)

Fonte: planilha **"Resumo coberturas condomínio"** (abas de coberturas, limites e "Cobertura
restrita"). Em dados: `regras_condominio_tradicional.json`, lido pelo `scripts/validar_massa.py`.
Catálogo de colunas e formato do JSON: `catalogo_condominio.md`.

## Como aplicar

Cobertura básica: `Incêndio, Queda de Raio, Explosão, Queda de Aeronave e Fumaça`. Teto efetivo de cada cobertura = o menor entre o máximo do corretor,
o % da básica e o % da cobertura exigida. Acima do máximo do corretor a cotação não é
automática (vai para as alçadas da tabela).

- Compõem o LMG (até 150.000.000,00): Incêndio, Queda de Raio, Explosão, Queda de Aeronave e Fumaça · Responsabilidade Civil - Condomínio + Síndico · Despesas com Aluguel Condôminos · Incêndio de Bens Dos Condôminos · Perda Ou Pagamento de Aluguel a Terceiros · Responsabilidade Civil - Danos Morais.

## Tabela de limites

| Cobertura | Cód | Mín (R$) | Máx corretor (R$) | % máx da básica | Exige (uma de) | % máx da exigida | Alçadas Analista / Coord / Gerente |
|---|---:|---:|---:|---:|---|---:|---|
| Incêndio, Queda de Raio, Explosão, Queda de Aeronave e Fumaça | 1000 | 600.000,00 | 150.000.000,00 | — | — | — | — / — / — |
| Responsabilidade Civil - Condomínio + Síndico | 1601 | 50.000,00 | 5.000.000,00 | 50% | — | — | — / — / 150.000.000,00 |
| Alagamento | 18 | 30.000,00 | 300.000,00 | 50% | — | — | — / 5.000.000,00 / 150.000.000,00 |
| Anúncios Luminosos | 20 | 2.000,00 | 500.000,00 | 50% | — | — | — / 5.000.000,00 / 150.000.000,00 |
| Danos Elétricos | 7 | 30.000,00 | 2.000.000,00 | 50% | — | — | — / 10.000.000,00 / 150.000.000,00 |
| Derrame Ou Vazamento de Chuveiros Automáticos (sprinklers) | 24 | 15.000,00 | 1.000.000,00 | 20% | — | — | 2.000.000,00 / 4.000.000,00 / 150.000.000,00 |
| Desmoronamento e Tremor de Terra | 32 | 30.000,00 | 1.000.000,00 | 50% | — | — | — / 5.000.000,00 / 150.000.000,00 |
| Despesas com Aluguel Condôminos | 1053 | 35.000,00 | 20.000.000,00 | — | Incêndio de Bens Dos Condôminos | 100% | — / 30.000.000,00 / 150.000.000,00 |
| Incêndio de Bens Dos Condôminos | 1055 | 75.000,00 | 30.000.000,00 | 30% | — | — | 50.000.000,00 / 100.000.000,00 / 150.000.000,00 |
| Perda Ou Pagamento de Aluguel a Terceiros | 31 | 35.000,00 | 2.000.000,00 | 10% | — | — | 5.000.000,00 / 20.000.000,00 / 150.000.000,00 |
| Quebra de Vidros | 15 | 5.000,00 | 500.000,00 | 50% | — | — | — / 5.000.000,00 / 150.000.000,00 |
| Responsabilidade Civil - Danos Morais | 310 | 10.000,00 | 600.000,00 | — | Responsabilidade Civil - Condomínio + Síndico | 20% | — / 1.000.000,00 / 150.000.000,00 |
| Responsabilidade Civil - Empregador | 1074 | 10.000,00 | 600.000,00 | — | Responsabilidade Civil - Condomínio + Síndico | 100% | 1.000.000,00 / 2.500.000,00 / 150.000.000,00 |
| Responsabilidade Civil - Guarda de Veículos + Portões Automáticos (incêndio e Roubo/furto) | 1038 | 20.000,00 | 2.500.000,00 | — | Responsabilidade Civil - Condomínio + Síndico | 100% | — / 3.000.000,00 / 150.000.000,00 |
| Responsabilidade Civil - Guarda de Veículos + Portões Automáticos (colisão, Incêndio e Roubo/furto) | 1037 | 20.000,00 | 2.500.000,00 | — | Responsabilidade Civil - Condomínio + Síndico | 100% | — / 3.000.000,00 / 150.000.000,00 |
| Responsabilidade Civil - Portões | 1058 | 20.000,00 | 2.500.000,00 | — | Responsabilidade Civil - Condomínio + Síndico | 50% | — / — / 150.000.000,00 |
| Roubo de Valores | 1062 | 3.000,00 | 50.000,00 | 50% | — | — | 100.000,00 / 200.000,00 / 150.000.000,00 |
| Roubo E/ou Furto Qualificado de Bens do Condomínio | 25 | 5.000,00 | 500.000,00 | 50% | — | — | — / 1.000.000,00 / 150.000.000,00 |
| Roubo E/ou Furto Qualificado de Bens Dos Condôminos | 1060 | 20.000,00 | 500.000,00 | — | Incêndio de Bens Dos Condôminos | 15% | — / 1.000.000,00 / 150.000.000,00 |
| Ruptura de Tanques e Tubulações | 1051 | 20.000,00 | 750.000,00 | 100% | — | — | 2.000.000,00 / 4.000.000,00 / 150.000.000,00 |
| Tumultos, Greves e Lockout | 6 | 10.000,00 | 1.000.000,00 | 50% | — | — | 5.000.000,00 / 10.000.000,00 / 150.000.000,00 |
| Vendaval, Furacão, Ciclone, Tornado, Granizo e Impacto de Veículos | 1070 | 30.000,00 | 2.000.000,00 | 25% | — | — | 5.000.000,00 / 20.000.000,00 / 150.000.000,00 |
| Auxílio Funeral | 1607 | 3.000,00 | 5.000.000,00 | — | Morte | 100% | — / 10.000.000,00 / 150.000.000,00 |
| Cesta Básica | 1605 | 1.000,00 | 5.000.000,00 | — | Invalidez Funcional Permanente Total Por Doença (ifpd) | 100% | — / 10.000.000,00 / 150.000.000,00 |
| Indenização Especial Por Acidente (iea) | 1077 | 5.000,00 | 5.000.000,00 | — | Invalidez Permanente Total Ou Parcial Por Acidente (ipa) | 100% | — / 10.000.000,00 / 150.000.000,00 |
| Invalidez Funcional Permanente Total Por Doença (ifpd) | 1079 | 5.000,00 | 5.000.000,00 | — | Indenização Especial Por Acidente (iea) · Invalidez Permanente Total Ou Parcial Por Acidente (ipa) | 100% | — / 10.000.000,00 / 150.000.000,00 |
| Invalidez Permanente Total Ou Parcial Por Acidente (ipa) | 1078 | 5.000,00 | 5.000.000,00 | — | Morte | 100% | — / 10.000.000,00 / 150.000.000,00 |
| Morte | 1076 | 5.000,00 | 5.000.000,00 | 100% | — | — | — / 10.000.000,00 / 150.000.000,00 |
| Morte Cônjuge | 1603 | 2.500,00 | 5.000.000,00 | — | Morte | 50% | — / 10.000.000,00 / 150.000.000,00 |

## Excludentes

- `Responsabilidade Civil - Guarda de Veículos + Portões Automáticos (incêndio e Roubo/furto)` × `Responsabilidade Civil - Guarda de Veículos + Portões Automáticos (colisão, Incêndio e Roubo/furto)`

## Coberturas restritas por Tipo de Condomínio

Não são aceitas quando o `Tipo de Condomínio` for `Condomínio Comercial - Vertical` · `Condomínio de Consultórios` · `Condomínio de Escritórios` · `Condomínio Misto - Vertical` · `Condomínio Residencial com Comércio no Térreo`:

- `Despesas com Aluguel Condôminos`
- `Incêndio de Bens Dos Condôminos`
- `Roubo E/ou Furto Qualificado de Bens Dos Condôminos`

Nesses tipos, use só as demais coberturas. Elas são aceitas em `Condomínio Exclusivamente
Residencial - Horizontal`, `Condomínio Exclusivamente Residencial - Vertical` e `Condomínio Flat /
Apart-Hotel`.

## Plano de Vida (dependências em cadeia)

`Morte` (até 100% da básica) → `IPA` exige Morte → `IEA` exige IPA → `IFPD` exige IEA ou IPA →
`Cesta Básica` exige IFPD. `Auxílio Funeral` exige Morte (até 100%) e `Morte Cônjuge` exige
Morte (até 50%). Todas de 5.000.000,00 no máximo do corretor. Os mínimos estão na tabela.
Não há mais valores fixos.
