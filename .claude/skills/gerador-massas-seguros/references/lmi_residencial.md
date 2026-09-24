# LMI por Cobertura — Residencial (base "Coberturas x LMI", aba `Residencial`)

Complementa `normas_residencial.md`. Onde as duas fontes divergem, **vale o valor mais
restritivo** (ex.: a norma já bloqueia Alagamento/All risks; esta planilha acrescenta mais
coberturas sem aceitação comercial).

## Como aplicar numa massa válida

Cada cobertura tem **três** limites que valem ao mesmo tempo:

1. **Mínimo** (R$) — valor abaixo disso é rejeitado.
2. **Máximo absoluto** (R$) — teto fixo.
3. **Máximo percentual** — % do LMI de outra cobertura (quase sempre a básica
   `Incêndio, queda de raio, explosão, implosão e queda de aeronaves`).

Teto efetivo = **o menor** entre o máximo absoluto e o percentual × LMI da cobertura de
referência. Consequências práticas:

- Toda massa com cobertura adicional precisa ter também a **cobertura básica (Incêndio)** com
  valor, senão o percentual não tem base. Defina o Incêndio primeiro e calcule as demais a partir
  dele.
- Coberturas de RC baseadas em `Responsabilidade Civil - Familiar` exigem a RC Familiar na massa
  (já era regra em `normas_residencial.md` para Danos Morais; aqui vale também para Empregados
  Domésticos e Prática de Esporte).
- Ex.: Incêndio = 500.000 → Danos Elétricos ≤ min(1.000.000; 30% × 500.000) = **150.000**.

## LMG do item

A soma dos LMIs do item (LMG) não pode passar de **R$ 76.000.000,00** (mensagem de origem: "O
item 1 possui LMG de R$ 100.000.000,00, que excede o limite máximo permitido de R$ 76.000.000,00").

## Tabela de LMI

Nomes na grafia do template (`catalogo_residencial.md`).

| Cobertura | Mín (R$) | Máx (R$) | Máx % | Observação |
|---|---:|---:|---|---|
| Incêndio, queda de raio, explosão, implosão e queda de aeronaves | 10.000,00 | 10.000.000,00 | — | cobertura básica |
| Bicicletas | 1.000,00 | 300.000,00 | 30% da básica | |
| Danos Elétricos | 500,00 | 1.000.000,00 | 30% da básica | |
| Vendaval, Furacão, Ciclone, Tornado, Granizo, Neve e Geada | 500,00 | 700.000,00 | 50% da básica | |
| Vendaval, furacão, ciclone, tornado, granizo e fumaça para bens ao ar livre | 500,00 | 150.000,00 | 40% da básica | |
| Roubo E/ou Furto Qualificado de Bens | 500,00 | 500.000,00 | 20% da básica | ver também inspeção por tipo de residência em `normas_residencial.md` |
| Perda Ou Pagamento de Aluguel (pi = 12 Meses) | 500,00 | 1.000.000,00 | 50% da básica | fonte chama de "Perda Ou Pagamento de Aluguel" |
| Equipamentos Eletrônicos e Eletrodomésticos | 500,00 | 500.000,00 | 30% da básica | |
| Quebra de Vidros | 500,00 | 500.000,00 | 30% da básica | |
| Responsabilidade Civil - Familiar | 500,00 | 3.000.000,00 | 100% da básica | |
| Responsabilidade Civil - Danos Morais | 500,00 | 300.000,00 | 100% da RC Familiar | exige RC Familiar |
| Responsabilidade Civil - Empregados Domésticos | 500,00 | 600.000,00 | 100% da RC Familiar | exige RC Familiar |
| Responsabilidade Civil - Prática de Esporte | 500,00 | 600.000,00 | 100% da RC Familiar | exige RC Familiar |
| Ruptura de Tubulações e Vazamento Acidental | 500,00 | 200.000,00 | 50% da básica | |
| Tumultos, Greves e Lockout | 500,00 | 1.000.000,00 | 30% da básica | |
| Roubo E/ou Furto Qualificado de Bicicleta Fora da Residência | 1.000,00 | 60.000,00 | 30% da básica | |
| Microempreendedor Em Residência | 500,00 | 500.000,00 | 30% da básica | |
| Escritório Em Residência | 500,00 | 500.000,00 | 30% da básica | |
| Impacto de Veículos | 500,00 | 10.000.000,00 | 100% da básica | |
| Equipamentos de Energia Solar e Fotovoltaico | 500,00 | 1.000.000,00 | 10% da básica | |
| Carro Na Garagem | 500,00 | 300.000,00 | 30% da básica | |
| Anfitrião | 500,00 | 500.000,00 | 30% da básica | |
| Indenização a valor de novo | 0,01 | — | ≤ LMI da básica | "não pode ser maior que a cobertura básica" |

## Coberturas sem aceitação comercial (nunca usar em massa válida)

A planilha retorna erro "não possui aceitação comercial na HDI Seguros" para:

| Cobertura | Código do erro |
|---|---|
| Alagamento | CB14.26001 |
| All risks | CB14.26002 |
| Desmoronamento | CB14.26009 |
| PAISAGISMO | CB14.26017 |
| Objetos de arte e obras de arte | CB14.26016 |
| Responsabilidade civil - tacos de golfe | CB14.26027 |
| Responsabilidade civil - hole-in-one | CB14.26013 |

Só marque uma delas quando o pedido for testar essa rejeição.

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
