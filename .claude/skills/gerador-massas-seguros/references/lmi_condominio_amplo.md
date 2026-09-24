# LMI por Cobertura — Condomínio Amplo (base "Coberturas x LMI", aba `Condominio Ampla`)

> **Sem template nesta skill ainda.** Não existe `templates/template_condominio_amplo.xlsx` nem
> catálogo de colunas — não gere massa deste ramo. Estas regras ficam salvas para quando o
> template chegar (aí: criar `catalogo_condominio_amplo.md`, conferir a grafia exata das
> coberturas no cabeçalho e ligar este arquivo no fluxo do `SKILL.md`). Nomes abaixo estão na
> grafia da planilha de origem, **não** necessariamente na do futuro template.

## Como aplicar

Mesma lógica dos outros ramos: teto efetivo = o menor entre o máximo absoluto e o percentual ×
LMI da cobertura de referência. Aqui a cobertura básica é **`Ampla`**.

## Cobertura básica e LMG

- `Ampla`: LMI entre **R$ 1.000.000,00** e **R$ 150.000.000,00** (fonte também cita faixa técnica
  até R$ 999.999.999,99, mas o limite de negócio é 150 mi).
- "O valor de LMI da cobertura básica não pode ser maior que **R$ 100.000.000,00**" — mensagem
  também presente na fonte; numa massa válida mantenha `Ampla` ≤ 100.000.000,00 (o mais
  restritivo).
- LMG do item ≤ **R$ 150.000.000,00** ("O item 1 possui LMG de ..., que excede o limite máximo
  permitido de R$ 150.000.000,00").
- `Condomínio Benefícios Essenciais` e `Assistência Condomínio Plano Básico`: LMI ≤ LMI da básica.

## Tabela de LMI

| Cobertura | Mín (R$) | Máx (R$) | Máx % | Observação |
|---|---:|---:|---|---|
| Ampla | 1.000.000,00 | 150.000.000,00 | — | básica (ver acima: ≤ 100 mi) |
| Responsabilidade Civil - Condomínio + Síndico | 50.000,00 | 5.000.000,00 | 50% da Ampla | erro de teto CB16.26019 |
| Despesas com Aluguel Condôminos | 35.000,00 | 20.000.000,00 | 100% de Incêndio de Bens dos Condôminos | exige Incêndio de Bens dos Condôminos · ≤ LMI da básica |
| Incêndio de Bens Dos Condôminos | 75.000,00 | 30.000.000,00 | 30% da Ampla | |
| Perda Ou Pagamento de Aluguel a Terceiros | 35.000,00 | 2.000.000,00 | 10% da Ampla | |
| Responsabilidade Civil - Danos Morais | 10.000,00 | 600.000,00 | 20% de RC Condomínio + Síndico | exige RC Condomínio + Síndico |
| Responsabilidade Civil - Empregador | 10.000,00 | 600.000,00 | 100% de RC Condomínio + Síndico | exige RC Condomínio + Síndico |
| Responsabilidade Civil - Guarda de Veículos + Portões Automáticos (incêndio e Roubo/furto) | 20.000,00 | 2.500.000,00 | 100% de RC Condomínio + Síndico | |
| Responsabilidade Civil - Guarda de Veículos + Portões Automáticos (colisão, Incêndio e Roubo/furto) | 20.000,00 | 2.500.000,00 | — | exige RC Condomínio + Síndico · excludente com a versão (incêndio e Roubo/furto) |
| Responsabilidade Civil - Portões | 20.000,00 | 2.500.000,00 | — | exige RC Condomínio + Síndico |
| Roubo de Valores | 3.000,00 | 50.000,00 | 50% da Ampla | |
| Roubo E/ou Furto Qualificado de Bens Dos Condôminos | 35.000,00 | 500.000,00 | 15% de Incêndio de Bens dos Condôminos | exige Incêndio de Bens dos Condôminos |
| Morte | 5.000,00 | 100.000,00 | 100% da Ampla | exige IPA (Plano Vida) · franquia obrigatória |
| Invalidez Permanente Total Ou Parcial Por Acidente (IPA) | 5.000,00 | 5.000,00 | — | valor fixo |
| Indenização Especial Por Acidente (IEA) | 5.000,00 | 5.000,00 | — | valor fixo |
| Invalidez Funcional Permanente Total Por Doença (IFPD) | 5.000,00 | 5.000,00 | — | valor fixo |
| Cesta Básica | 1.000,00 | 1.000,00 | — | valor fixo |
| Morte Cônjuge | 2.500,00 | 2.500,00 | — | fonte: "LMI tem que ser 50% menor que o valor da cobertura Morte" |
| Auxílio Funeral | 3.000,00 | 3.000,00 | — | valor fixo |

## Dependências e excludentes (resumo)

- `Despesas com Aluguel Condôminos` e `Roubo E/ou Furto Qualificado de Bens Dos Condôminos` →
  exigem `Incêndio de Bens Dos Condôminos`.
- `RC - Danos Morais`, `RC - Empregador`, `RC - Portões`, `RC - Guarda de Veículos + Portões
  Automáticos (colisão...)` → exigem `Responsabilidade Civil - Condomínio + Síndico`.
- `RC - Guarda de Veículos + Portões Automáticos (colisão, Incêndio e Roubo/furto)` cancela
  `RC - Guarda de Veículos + Portões Automáticos (incêndio e Roubo/furto)` — escolha uma.
- `Morte` → exige `Invalidez Permanente Total Ou Parcial Por Acidente (IPA)` e franquia.
