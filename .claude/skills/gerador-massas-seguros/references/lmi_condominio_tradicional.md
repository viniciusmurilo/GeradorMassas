# LMI por Cobertura — Condomínio Tradicional (base "Coberturas x LMI", aba `Condominio Tradicional`)

> **Sem template nesta skill ainda.** Não existe `templates/template_condominio_tradicional.xlsx`
> nem catálogo de colunas — não gere massa deste ramo. Estas regras ficam salvas para quando o
> template chegar (aí: criar `catalogo_condominio_tradicional.md`, conferir a grafia exata das
> coberturas no cabeçalho e ligar este arquivo no fluxo do `SKILL.md`). Nomes abaixo estão na
> grafia da planilha de origem, **não** necessariamente na do futuro template.

## Como aplicar

Teto efetivo = o menor entre o máximo absoluto e o percentual × LMI da cobertura de referência.
Aqui a cobertura básica é **`Incêndio, Queda de Raio, Explosão, Queda de Aeronave e Fumaça`**
("básica" na tabela).

## Cobertura básica e LMG

- Básica: LMI entre **R$ 600.000,00** e **R$ 150.000.000,00**.
- LMG do item ≤ **R$ 150.000.000,00**.

## Tabela de LMI

| Cobertura | Mín (R$) | Máx (R$) | Máx % | Observação |
|---|---:|---:|---|---|
| Incêndio, Queda de Raio, Explosão, Queda de Aeronave e Fumaça | 600.000,00 | 150.000.000,00 | — | básica |
| Responsabilidade Civil - Condomínio + Síndico | 50.000,00 | 5.000.000,00 | 50% da básica | |
| Alagamento | 30.000,00 | 300.000,00 | 50% da básica | |
| Anúncios Luminosos | 2.000,00 | 500.000,00 | 50% da básica | |
| Danos Elétricos | 30.000,00 | 2.000.000,00 | 50% da básica | |
| Derrame Ou Vazamento de Chuveiros Automáticos (sprinklers) | 15.000,00 | 1.000.000,00 | 20% da básica | |
| Desmoronamento e Tremor de Terra | 30.000,00 | 1.000.000,00 | 50% da básica | |
| Despesas com Aluguel Condôminos | 35.000,00 | 20.000.000,00 | 100% de Incêndio de Bens dos Condôminos | exige Incêndio de Bens dos Condôminos |
| Incêndio de Bens Dos Condôminos | 75.000,00 | 30.000.000,00 | 30% da básica | |
| Perda Ou Pagamento de Aluguel a Terceiros | 35.000,00 | 2.000.000,00 | 10% da básica | aparece duplicada na fonte (mesmos limites) |
| Quebra de Vidros | 5.000,00 | 500.000,00 | 50% da básica | aparece duplicada na fonte (mesmos limites) |
| Responsabilidade Civil - Danos Morais | 10.000,00 | 600.000,00 | 20% de RC Condomínio + Síndico | |
| Responsabilidade Civil - Empregador | 10.000,00 | 600.000,00 | 100% de RC Condomínio + Síndico | |
| Responsabilidade Civil - Guarda de Veículos + Portões Automáticos (incêndio e Roubo/furto) | 20.000,00 | 2.500.000,00 | 100% de RC Condomínio + Síndico | |
| Responsabilidade Civil - Guarda de Veículos + Portões Automáticos (colisão, Incêndio e Roubo/furto) | 20.000,00 | 2.500.000,00 | 100% de RC Condomínio + Síndico | excludente com a versão (incêndio e Roubo/furto) |
| Responsabilidade Civil - Portões | 20.000,00 | 2.500.000,00 | 50% de RC Condomínio + Síndico | |
| Roubo de Valores | 3.000,00 | 50.000,00 | 50% da básica | |
| Roubo E/ou Furto Qualificado de Bens do Condomínio | 5.000,00 | 500.000,00 | 50% da básica | |
| Roubo E/ou Furto Qualificado de Bens Dos Condôminos | 20.000,00 | 500.000,00 | 15% de Incêndio de Bens dos Condôminos | |
| Ruptura de Tanques e Tubulações | 20.000,00 | 750.000,00 | 100% da básica | |
| Tumultos, Greves e Lockout | 10.000,00 | 1.000.000,00 | 50% da básica | |
| Vendaval, Furacão, Ciclone, Tornado, Granizo e Impacto de Veículos | 30.000,00 | 2.000.000,00 | 25% da básica | |
| Morte | 5.000,00 | 100.000,00 | — | exige IPA (Plano Vida) · franquia obrigatória |

## Dependências e excludentes (resumo)

- `Despesas com Aluguel Condôminos` → exige `Incêndio de Bens Dos Condôminos`.
- Coberturas de RC com % sobre `Responsabilidade Civil - Condomínio + Síndico` (Danos Morais,
  Empregador, Guarda de Veículos, Portões) → incluir a RC Condomínio + Síndico na massa.
- `Roubo E/ou Furto Qualificado de Bens Dos Condôminos` → incluir `Incêndio de Bens Dos
  Condôminos` (base do %).
- `RC - Guarda de Veículos + Portões Automáticos (colisão, Incêndio e Roubo/furto)` cancela
  `RC - Guarda de Veículos + Portões Automáticos (incêndio e Roubo/furto)` — escolha uma.
- `Morte` → exige `Invalidez Permanente Total Ou Parcial Por Acidente (IPA)` e franquia.
