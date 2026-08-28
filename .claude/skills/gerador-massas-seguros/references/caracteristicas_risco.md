# Planilha de Características de Risco (compartilhada entre os ramos, 7 colunas)

Mesmo arquivo de template para os dois ramos — o que muda são as listas de valores aceitos por
coluna e quais colunas ficam `<IGNORE>`.

| Col | Cabeçalho | Empresarial | Residencial |
|---|---|---|---|
| A | `CBO Tipo de Construção` | Superior · Sólida · Mista · Inferior | Superior / Sólida · Mista · Inferior |
| B | `CBO Objeto Segurado` | Prédio e Conteúdo · Prédio · Conteúdo | idem |
| C | `CBO Assistência 24h` | 4 planos Empresarial (abaixo) | 4 planos Residencial (abaixo) |
| D | `CHK Residencial Benefícios Essenciais` | `<IGNORE>` | `<IGNORE>` |
| E | `TXT Atividade` | atividade do catálogo (`atividades.txt`, 439 itens) | `<IGNORE>` |
| F | `CBO Tipo de Residência` | `<IGNORE>` | uma das 9 opções (abaixo) |
| G | `TXT Valor em Risco - Danos Materiais` | formato `1.000.000,00` | idem |

## Assistência 24h — Empresarial

- Assistência Empresarial Plano Superior
- Assistência Empresarial Plano Intermediário
- Assistência Empresarial Plano Básico
- Não Contratado

## Assistência 24h — Residencial

- Assistência Residencial Plano Superior
- Assistência Residencial Plano Intermediário
- Assistência Residencial Plano Básico
- Não Contratado

## Tipo de Residência (só residencial)

- Apartamento Desocupado
- Apartamento Habitual
- Apartamento Veraneio
- Casa Desocupada
- Casa em Condomínio Fechado Desocupada
- Casa em Condomínio Fechado Habitual
- Casa em Condomínio Fechado Veraneio
- Casa Habitual
- Casa Veraneio

## Observações

- `"Selecione um item"` é placeholder de combo. **Nunca sai nas massas geradas.**
- Valor fora da lista do ramo é erro — não aceite valor empresarial em massa residencial (ex.:
  "Assistência Empresarial Plano Superior" numa massa residencial, ou "Mista" sem "Superior /
  Sólida" combinado no residencial).
- Atividade: validada contra `references/atividades.txt` (439 itens, sem duplicatas), gravada com
  a grafia exata do arquivo. Campo só existe no ramo empresarial; no residencial fica `<IGNORE>`.
