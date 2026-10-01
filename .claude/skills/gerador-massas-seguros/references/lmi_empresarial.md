# Regras por Cobertura — Empresarial (produto 425)

Fonte principal: planilha **"Resumo coberturas"** (abas `Coberturas limites e aceitação` e
`Coberturas obrig e exclus`), mais erros observados na homologação (marcados como tal). Esta é
a referência de LMI, dependências e exclusões do empresarial. Se algo aqui divergir de
`normas_empresarial.md`, **vale este arquivo**, exceto os limites por CEP/UF/atividade da norma,
que continuam valendo por cima.

## Como aplicar numa massa válida

Cada cobertura tem estes limites ao mesmo tempo:

1. **Mínimo** (R$).
2. **Máximo do corretor** (R$, "Automaticidade Corretor"). Acima dele a cotação é **bloqueada**
   ou vai para **análise técnica** (coluna "Acima do máx"). Massa válida fica **até** esse valor.
3. **% máx da básica**: percentual do LMI de
   `Incêndio, Queda de Raio, Queda de Aeronaves, Implosão, Explosão e Fumaça`.
4. Se a cobertura **exige** outra (tabela Dependências), também o **% máx sobre a exigida**.

Teto efetivo = **o menor** de todos esses valores. Por isso:

- Toda massa com cobertura adicional precisa ter a **cobertura básica (Incêndio)** com valor.
  Defina a básica primeiro (coerente com `Valor em Risco - Danos Materiais`) e calcule as demais.
- Ex.: básica = 1.000.000 → Danos Elétricos ≤ min(5.000.000; 60% × 1.000.000) = **600.000**;
  Quebra de Vidros ≤ min(1.000.000; 20%) = **200.000**.

## Campos de risco

| Campo (`texto`) | Mín (R$) | Máx (R$) |
|---|---:|---:|
| `Valor em Risco - Danos Materiais` | 55.000,00 | 150.000.000,00 |

`Despesas Fixas - Ampla`, `Despesas Fixas - Incêndio` e `Lucros Cessantes - Incêndio` não podem
passar do valor informado em `Lucros Cessantes` (campo de texto). Numa massa com qualquer uma
delas, preencha `Lucros Cessantes` com valor ≥ ao LMI dessas coberturas.

**VR Lucros Cessantes exige cobertura básica de LC/DF** (confirmado no sistema): se o campo
`Lucros Cessantes` tiver valor, a massa precisa ter `Lucros Cessantes - Incêndio` **ou**
`Despesas Fixas - Incêndio`. Mensagem: "Para contratar o VR Lucros Cessantes é necessário
contratar uma das coberturas: (LUCROS CESSANTES - BÁSICA ou DESPESAS FIXAS - BÁSICA)". Como as
duas são excludentes entre si, escolha **uma**. A mensagem não cita `Despesas Fixas - Ampla`,
então não conte com ela sozinha para satisfazer a regra.

**A regra vale nos dois sentidos:**

| VR `Lucros Cessantes` | Coberturas de LC/DF |
|---|---|
| **com valor** | obrigatório ter `Lucros Cessantes - Incêndio` **ou** `Despesas Fixas - Incêndio` (só uma), com LMI ≤ VR |
| **sem valor** (`"<IGNORE>"`) | **proibido** ter `Lucros Cessantes - Incêndio`, `Despesas Fixas - Incêndio` e `Despesas Fixas - Ampla`. Também ficam de fora as que dependem delas: `Despesas extraordinárias` e `Honorários de peritos contábeis` |

Padrão numa massa válida: VR Lucros Cessantes com valor + uma das duas coberturas básicas. Quando
o pedido for sem lucros cessantes, grave `Lucros Cessantes` como `"<IGNORE>"` e não inclua
nenhuma das coberturas acima.

Compõem o LMG (Limite Máximo de Garantia): básica, Perda Ou Pagamento de Aluguel a Terceiros,
Despesas Fixas - Ampla/Incêndio, Lucros Cessantes - Incêndio, Despesas com instalação em novo
local, Despesas extraordinárias e todas as RC Operações.

Período indenitário existe em: Perda Ou Pagamento de Aluguel a Terceiros, Despesas Fixas - Ampla,
Lucros Cessantes - Incêndio e Lucros cessantes - danos elétricos. Esta última não tem coluna de
período no template.

## Tabela de limites

Nomes na grafia do template (`catalogo_empresarial.md`). "Alçadas" = até quanto cada nível
aprova acima do corretor (Analista Júnior / Pleno / Sênior / Coordenador; o Gerente aprova
qualquer valor). Serve para massas que testam análise técnica.

| Cobertura | Cód | Mín (R$) | Máx corretor (R$) | Acima do máx | % máx da básica | Alçadas Jr / Pl / Sr / Coord |
|---|---:|---:|---:|---|---:|---|
| Incêndio, Queda de Raio, Queda de Aeronaves, Implosão, Explosão e Fumaça | 1 | 55.000,00 | 150.000.000,00 | por atividade | 100% | por atividade |
| Danos Elétricos | 7 | 1.000,00 | 5.000.000,00 | análise técnica | 60% | — / 7.000.000,00 / 10.000.000,00 / 20.000.000,00 |
| Vendaval para concessionárias (exceto veículos ao ar livre) | 535 | 5.000,00 | 7.500.000,00 | análise técnica | 50% | 10.000.000,00 / 15.000.000,00 / 25.000.000,00 / 30.000.000,00 |
| Vendaval, Furacão, Ciclone, Tornado, Granizo e Impacto de Veículos | 1070 | 5.000,00 | 7.500.000,00 | análise técnica | 50% | 10.000.000,00 / 15.000.000,00 / 25.000.000,00 / 30.000.000,00 |
| Vendaval para concessionárias (inclusive veículos ao ar livre) | 536 | 5.000,00 | 1.000.000,00 | análise técnica | 50% | 2.500.000,00 / 5.000.000,00 / 7.500.000,00 / 20.000.000,00 |
| Vendaval, Furacão, Ciclone, Tornado, Granizo e Impacto de Veículos - para Bens Ao Ar Livre | 1068 | 5.000,00 | 1.000.000,00 | análise técnica | 10% | 2.500.000,00 / 5.000.000,00 / 7.500.000,00 / 30.000.000,00 |
| Roubo E/ou Furto Qualificado de Bens | 25 | 1.000,00 | 500.000,00 | análise técnica | 30% | — / — / 600.000,00 / 1.000.000,00 |
| Perda Ou Pagamento de Aluguel a Terceiros | 31 | 1.000,00 | 15.000.000,00 | análise técnica | 50% | 30.000.000,00 / 30.000.000,00 / 30.000.000,00 / 30.000.000,00 |
| Quebra de Vidros | 15 | 1.000,00 | 1.000.000,00 | análise técnica | 20% | — / 1.500.000,00 / 3.000.000,00 / 5.000.000,00 |
| Equipamentos Eletrônicos | 1067 | 1.000,00 | 3.000.000,00 | BLOQUEIA | 20% | 3.500.000,00 / 4.000.000,00 / 4.500.000,00 / 5.000.000,00 |
| Alagamento | 18 | 1.000,00 | 500.000,00 | BLOQUEIA | 20% | 600.000,00 / 700.000,00 / 1.000.000,00 / 3.000.000,00 |
| Anúncios Luminosos | 20 | 1.000,00 | 1.000.000,00 | análise técnica | 20% | — / 1.500.000,00 / 3.000.000,00 / 5.000.000,00 |
| Demolição e Remoção de Entulho | 1048 | 5.000,00 | 30.000.000,00 | BLOQUEIA | 100% | — / — / — / — |
| Derrame Ou Vazamento de Chuveiros Automáticos (sprinklers) | 24 | 5.000,00 | 5.000.000,00 | análise técnica | 20% | 10.000.000,00 / 15.000.000,00 / 20.000.000,00 / 30.000.000,00 |
| Desmoronamento | 32 | 5.000,00 | 1.000.000,00 | análise técnica | 40% | 2.000.000,00 / 3.000.000,00 / 4.000.000,00 / 10.000.000,00 |
| Despesas Fixas - Ampla | 1050 | 5.000,00 | 20.000.000,00 | análise técnica | 100% | — / — / — / 30.000.000,00 |
| Despesas Fixas - Incêndio | 1051 | 5.000,00 | 20.000.000,00 | análise técnica | 100% | 30.000.000,00 / 30.000.000,00 / 30.000.000,00 / 30.000.000,00 |
| Deterioração de Mercadorias Em Ambientes Frigorificados | 21 | 1.000,00 | 500.000,00 | BLOQUEIA | 10% | — / — / 1.000.000,00 / 3.000.000,00 |
| Deterioração de Vacinas para Pet Shop, Consultório, Agropecuária e Veterinário | 1083 | 1.000,00 | 50.000,00 | BLOQUEIA | 10% | 100.000,00 / 200.000,00 / 1.000.000,00 / 3.000.000,00 |
| Equipamentos Estacionários | 22 | 1.000,00 | 3.000.000,00 | BLOQUEIA | 20% | 3.500.000,00 / 4.000.000,00 / 4.500.000,00 / 5.000.000,00 |
| Equipamentos Móveis | 9 | 1.000,00 | 3.000.000,00 | BLOQUEIA | 20% | 3.500.000,00 / 4.000.000,00 / 4.500.000,00 / 5.000.000,00 |
| Escritório Em Casa de Funcionário | 1400 | 1.000,00 | 50.000,00 | BLOQUEIA | 10% | 100.000,00 / 200.000,00 / 1.000.000,00 / 3.000.000,00 |
| Lucros Cessantes - Incêndio | 44 | 5.000,00 | 20.000.000,00 | análise técnica | 100% | — / — / — / 30.000.000,00 |
| Pátio - Até 100 Km | 529 | 5.000,00 | 10.000.000,00 | BLOQUEIA | 70% | — / — / 30.000.000,00 / 30.000.000,00 |
| Pátio - Até 200 Km | 530 | 5.000,00 | 10.000.000,00 | BLOQUEIA | 70% | — / — / — / 20.000.000,00 |
| Pátio - Até 300 Km | 531 | 5.000,00 | 10.000.000,00 | BLOQUEIA | 70% | — / — / — / 20.000.000,00 |
| Recomposição de Registros e Documentos | 14 | 1.000,00 | 5.000.000,00 | BLOQUEIA | 10% | — / 10.000.000,00 / 20.000.000,00 / 30.000.000,00 |
| Responsabilidade civil - operações concessionárias até 100 km | 532 | 1.000,00 | 3.000.000,00 | BLOQUEIA | 70% | — / — / — / — |
| Responsabilidade civil - operações concessionárias até 200 km | 533 | 1.000,00 | 3.000.000,00 | BLOQUEIA | 70% | — / — / — / — |
| Responsabilidade Civil - Operações | 26 | 1.000,00 | 3.000.000,00 | BLOQUEIA | 50% | — / — / — / — |
| RESPONSABILIDADE CIVIL - BARES E RESTAURANTES | 306 | 1.000,00 | 3.000.000,00 | BLOQUEIA | 50% | — / — / — / — |
| Responsabilidade civil - operações clubes, agremiações e associações recreativas | 1036 | 1.000,00 | 3.000.000,00 | BLOQUEIA | 50% | — / — / — / — |
| Responsabilidade civil - operações concessionárias até 300 km | 534 | 1.000,00 | 3.000.000,00 | BLOQUEIA | 70% | — / — / — / — |
| Responsabilidade civil - operações estabelecimento de ensino | 304 | 1.000,00 | 3.000.000,00 | BLOQUEIA | 50% | — / — / — / — |
| Responsabilidade civil - operações hotéis e pousadas | 510 | 1.000,00 | 3.000.000,00 | BLOQUEIA | 50% | — / — / — / — |
| Responsabilidade civil - operações pet shop e/ou clínica veterinária | 512 | 1.000,00 | 1.000.000,00 | BLOQUEIA | 50% | 3.000.000,00 / 3.000.000,00 / 3.000.000,00 / 3.000.000,00 |
| Responsabilidade civil - operações salões de beleza | 513 | 1.000,00 | 1.000.000,00 | BLOQUEIA | 50% | 3.000.000,00 / 3.000.000,00 / 3.000.000,00 / 3.000.000,00 |
| Responsabilidade Civil - Empregador | 1074 | 1.000,00 | 3.000.000,00 | BLOQUEIA | 50% | — / — / — / — |
| Responsabilidade Civil - Danos Morais | 310 | 1.000,00 | 1.000.000,00 | BLOQUEIA | 50% | — / — / — / — |
| Responsabilidade civil - banho e tosa | 505 | 1.000,00 | 50.000,00 | BLOQUEIA | 10% | — / — / — / — |
| Responsabilidade civil - dog walker | 506 | 1.000,00 | 50.000,00 | BLOQUEIA | 10% | — / — / — / — |
| Responsabilidade civil - guarda de bicicletas | 508 | 1.000,00 | 50.000,00 | BLOQUEIA | 10% | — / — / — / — |
| Responsabilidade Civil - Guarda de Veículo - Incêndio e Roubo | 1038 | 1.000,00 | 500.000,00 | análise técnica | 10% | — / — / — / 3.000.000,00 |
| Responsabilidade civil - hotel pet | 511 | 1.000,00 | 50.000,00 | BLOQUEIA | 10% | — / — / — / — |
| Responsabilidade civil - ocorrência de bullying em escolas | 507 | 1.000,00 | 50.000,00 | BLOQUEIA | 10% | — / — / — / — |
| Responsabilidade civil - taxi dog | 515 | 1.000,00 | 50.000,00 | BLOQUEIA | 10% | — / — / — / — |
| Responsabilidade civil - alimentos distribuídos pela escola | 504 | 1.000,00 | 50.000,00 | BLOQUEIA | 10% | — / — / — / — |
| Roubo de Valores Em Mãos de Portadores | 3 | 1.000,00 | 50.000,00 | análise técnica | 10% | 100.000,00 / 300.000,00 / 500.000,00 / 1.200.000,00 |
| Roubo de Valores No Interior do Estabelecimento | 4 | 1.000,00 | 50.000,00 | análise técnica | 10% | 100.000,00 / 300.000,00 / 500.000,00 / 1.200.000,00 |
| Roubo E/ou Furto Qualificado de Bens de Hóspedes | 1082 | 1.000,00 | 100.000,00 | BLOQUEIA | 20% | — / — / 150.000,00 / 300.000,00 |
| Tumultos, Greves e Lockout | 6 | 1.000,00 | 4.000.000,00 | análise técnica | 50% | — / — / — / — |
| Tumultos, Greves e Lockout - Atos Dolosos | 516 | 1.000,00 | 4.000.000,00 | análise técnica | 50% | — / — / — / — |
| Vazamento de Tanques e Ruptura de Tubulações | 538 | 1.000,00 | 1.000.000,00 | BLOQUEIA | 50% | 2.000.000,00 / 3.000.000,00 / 4.000.000,00 / 10.000.000,00 |
| Despesas com instalação em novo local | 76 | 5.000,00 | 12.000.000,00 | BLOQUEIA | 100% | — / — / — / 30.000.000,00 |
| Bens depositados em guarda volumes | 300 | 1.000,00 | 20.000,00 | BLOQUEIA | 20% | 200.000,00 / 200.000,00 / 200.000,00 / 1.000.000,00 |
| Danos à fabricação | 1079 | 5.000,00 | 500.000,00 | BLOQUEIA | 50% | 600.000,00 / 700.000,00 / 800.000,00 / 2.000.000,00 |
| Danos à mercadoria por quebra de vidro | 1084 | 1.000,00 | 50.000,00 | BLOQUEIA | 10% | 100.000,00 / 100.000,00 / 100.000,00 / 500.000,00 |
| Derrame de material em estado de fusão | 13 | 5.000,00 | 500.000,00 | BLOQUEIA | 50% | — / — / 1.000.000,00 / 2.000.000,00 |
| Despesas extraordinárias | 1057 | 5.000,00 | 2.000.000,00 | BLOQUEIA | 50% | 4.000.000,00 / 8.000.000,00 / 10.000.000,00 / 30.000.000,00 |
| Benefícios fiscais | 501 | 1.000,00 | 0 (corretor) | sem aceitação | 1% | — / — / — / — |
| Bens do segurado em locais especificados | 1080 | 1.000,00 | 0 (corretor) | sem aceitação | 5% | — / — / — / 10.000.000,00 |
| Bens do segurado em locais não especificados | 1081 | 1.000,00 | 0 (corretor) | sem aceitação | 5% | — / — / — / 10.000.000,00 |
| Bens do segurado em locais não especificados - ampla | 523 | 1.000,00 | 0 (corretor) | sem aceitação | 5% | — / — / — / 2.000.000,00 |
| Despesas fixas - danos elétricos | 502 | 1.000,00 | 1.000.000,00 | BLOQUEIA | 20% | 5.000.000,00 / 10.000.000,00 / 25.000.000,00 / 30.000.000,00 |
| Despesas fixas - vendaval | 503 | 1.000,00 | 3.000.000,00 | BLOQUEIA | 50% | 5.000.000,00 / 5.000.000,00 / 5.000.000,00 / 30.000.000,00 |
| Despesas fixas - vendaval para bens ao ar livre | 520 | 1.000,00 | 3.000.000,00 | BLOQUEIA | 50% | — / 5.000.000,00 / 5.000.000,00 / 30.000.000,00 |
| Despesas fixas - vendaval para concessionárias (exceto veículos ao ar livre) | 521 | 5.000,00 | 3.000.000,00 | BLOQUEIA | 50% | 5.000.000,00 / 5.000.000,00 / 5.000.000,00 / 30.000.000,00 |
| Despesas fixas - vendaval para concessionárias (inclusive veículos ao ar livre) | 522 | 5.000,00 | 3.000.000,00 | BLOQUEIA | 50% | — / 5.000.000,00 / 5.000.000,00 / 30.000.000,00 |
| Deterioração de flores em câmaras frias | 301 | 1.000,00 | 100.000,00 | BLOQUEIA | 20% | 200.000,00 / 300.000,00 / 1.000.000,00 / 3.000.000,00 |
| Equipamentos cinematográficos, fotográficos e de vídeo | 10 | 1.000,00 | 200.000,00 | BLOQUEIA | 20% | — / 300.000,00 / 500.000,00 / 1.000.000,00 |
| Equipamentos e/ou objetos portáteis | 1049 | 1.000,00 | 100.000,00 | BLOQUEIA | 20% | — / 250.000,00 / 500.000,00 / 1.000.000,00 |
| Equipamentos em exposição | 8 | 1.000,00 | 1.000.000,00 | BLOQUEIA | 20% | — / — / — / 1.500.000,00 |
| Fidelidade de empregados | 16 | 1.000,00 | 250.000,00 | BLOQUEIA | 10% | 500.000,00 / 1.000.000,00 / 2.000.000,00 / 4.000.000,00 |
| Honorários de peritos contábeis | 1046 | 1.000,00 | 500.000,00 | BLOQUEIA | 1% | — / 600.000,00 / 800.000,00 / 1.000.000,00 |
| Lucros cessantes - danos elétricos | 45 | 5.000,00 | 3.000.000,00 | BLOQUEIA | 20% | 5.000.000,00 / 10.000.000,00 / 25.000.000,00 / 30.000.000,00 |
| Lucros cessantes - vendaval | 46 | 5.000,00 | 3.000.000,00 | BLOQUEIA | 50% | 5.000.000,00 / 5.000.000,00 / 5.000.000,00 / 30.000.000,00 |
| Lucros cessantes - vendaval para bens ao ar livre | 525 | 5.000,00 | 3.000.000,00 | BLOQUEIA | 50% | — / 5.000.000,00 / 5.000.000,00 / 30.000.000,00 |
| Lucros cessantes - vendaval para concessionárias (exceto veículos ao ar livre) | 526 | 5.000,00 | 3.000.000,00 | BLOQUEIA | 50% | 5.000.000,00 / 5.000.000,00 / 5.000.000,00 / 30.000.000,00 |
| Lucros cessantes - vendaval para concessionárias (inclusive veículos ao ar livre) | 527 | 5.000,00 | 3.000.000,00 | BLOQUEIA | 30% | — / 5.000.000,00 / 5.000.000,00 / 30.000.000,00 |
| Moldes e matrizes | 1063 | 1.000,00 | 20.000,00 | análise técnica | 10% | 100.000,00 / 200.000,00 / 1.000.000,00 / 3.000.000,00 |
| Lucros cessantes - quebra de máquinas | 524 | 5.000,00 | 0 (corretor) | sem aceitação | 50% | — / — / — / — |
| Movimentação interna | 1085 | 1.000,00 | 500.000,00 | BLOQUEIA | 50% | — / — / 750.000,00 / 1.000.000,00 |
| Operações de carga, descarga, içamento e descida | 19 | 1.000,00 | 500.000,00 | BLOQUEIA | 50% | 1.000.000,00 / 1.500.000,00 / 2.000.000,00 / 3.000.000,00 |
| Pequenas obras de engenharia | 63 | 5.000,00 | 1.000.000,00 | BLOQUEIA | 5% | 2.000.000,00 / 3.000.000,00 / 4.000.000,00 / 10.000.000,00 |
| Obras de arte | 528 | 500,00 | 0 (corretor) | sem aceitação | 20% | — / — / — / 1.000.000,00 |
| Quebra de máquinas | 52 | 5.000,00 | 300.000,00 | BLOQUEIA | 50% | 500.000,00 / 1.000.000,00 / 2.000.000,00 / 10.000.000,00 |
| Quebra de vidro de utensílio de cozinha | 537 | 1.000,00 | 50.000,00 | BLOQUEIA | 10% | 100.000,00 / 100.000,00 / 100.000,00 / 500.000,00 |
| Responsabilidade civil - contingentes de veículos | 1076 | 1.000,00 | 3.000.000,00 | BLOQUEIA | 50% | — / — / — / — |
| Queimadas em zonas rurais | 1065 | 5.000,00 | 0 (corretor) | sem aceitação | 100% | — / — / — / 1.000.000,00 |
| Responsabilidade civil - guarda de veículos - compreensiva | 1037 | 1.000,00 | 500.000,00 | análise técnica | 10% | — / — / — / 3.000.000,00 |
| Responsabilidade civil - guarda de embarcações de terceiros | 509 | 1.000,00 | 0 (corretor) | sem aceitação | 50% | — / — / — / 1.000.000,00 |
| Responsabilidade civil - serviços de manobrista | 514 | 1.000,00 | 200.000,00 | BLOQUEIA | 10% | — / 300.000,00 / 500.000,00 / 1.000.000,00 |
| Responsabilidade civil - movimentação de carga e descarga | 309 | 1.000,00 | 0 (corretor) | sem aceitação | 50% | — / — / — / 1.000.000,00 |
| Roubo de valores e/ou bens de clientes | 302 | 1.000,00 | 20.000,00 | BLOQUEIA | 20% | 200.000,00 / 200.000,00 / 200.000,00 / 1.000.000,00 |
| Responsabilidade civil - produtos | 1064 | 1.000,00 | 0 (corretor) | sem aceitação | 50% | — / — / — / 1.000.000,00 |
| Terremoto, tremor de terra e maremoto | 539 | 1.000,00 | 0 (corretor) | sem aceitação | 20% | — / — / — / 3.000.000,00 |

## Coberturas sem aceitação comercial (nunca usar em massa válida)

Automaticidade do corretor = 0 ("Essa cobertura não possui aceitação comercial na HDI
Seguros"). Só marque para testar essa rejeição.

| Cobertura | Cód | Coordenador aprova até (R$) |
|---|---:|---:|
| Benefícios fiscais | 501 | — |
| Bens do segurado em locais especificados | 1080 | 10.000.000,00 |
| Bens do segurado em locais não especificados | 1081 | 10.000.000,00 |
| Bens do segurado em locais não especificados - ampla | 523 | 2.000.000,00 |
| Lucros cessantes - quebra de máquinas | 524 | — |
| Obras de arte | 528 | 1.000.000,00 |
| Queimadas em zonas rurais | 1065 | 1.000.000,00 |
| Responsabilidade civil - guarda de embarcações de terceiros | 509 | 1.000.000,00 |
| Responsabilidade civil - movimentação de carga e descarga | 309 | 1.000.000,00 |
| Responsabilidade civil - produtos | 1064 | 1.000.000,00 |
| Terremoto, tremor de terra e maremoto | 539 | 3.000.000,00 |

Erro observado na homologação para Terremoto: "ITEM 1 - CB18.26011 - Cobertura Terremoto,
Tremor de Terra e Maremoto não possui aceitação comercial na HDI Seguros."

## Dependências (cobertura X exige pelo menos uma das coberturas Y)

"Máx % da exigida" = teto do LMI de X sobre o LMI da cobertura exigida. Quando há várias exigidas
na massa, respeite o teto sobre **cada uma**, ou seja, fique ≤ o menor.

| Se incluir… | …precisa incluir pelo menos uma de | Máx % da exigida |
|---|---|---|
| Responsabilidade Civil - Empregador | RESPONSABILIDADE CIVIL - BARES E RESTAURANTES · Responsabilidade civil - operações clubes, agremiações e associações recreativas · Responsabilidade civil - operações concessionárias até 100 km · Responsabilidade civil - operações concessionárias até 200 km · Responsabilidade civil - operações concessionárias até 300 km · Responsabilidade civil - operações estabelecimento de ensino · Responsabilidade civil - operações hotéis e pousadas · Responsabilidade Civil - Operações · Responsabilidade civil - operações pet shop e/ou clínica veterinária · Responsabilidade civil - operações salões de beleza | 100% dela |
| Responsabilidade Civil - Danos Morais | RESPONSABILIDADE CIVIL - BARES E RESTAURANTES · Responsabilidade civil - operações clubes, agremiações e associações recreativas · Responsabilidade civil - operações concessionárias até 100 km · Responsabilidade civil - operações concessionárias até 200 km · Responsabilidade civil - operações concessionárias até 300 km · Responsabilidade civil - operações estabelecimento de ensino · Responsabilidade civil - operações hotéis e pousadas · Responsabilidade Civil - Operações · Responsabilidade civil - operações pet shop e/ou clínica veterinária · Responsabilidade civil - operações salões de beleza | 100% dela |
| Responsabilidade civil - banho e tosa | Responsabilidade civil - operações pet shop e/ou clínica veterinária | 20% dela |
| Responsabilidade civil - dog walker | Responsabilidade civil - operações pet shop e/ou clínica veterinária | 20% dela |
| Responsabilidade civil - guarda de bicicletas | Responsabilidade Civil - Operações · Responsabilidade civil - operações estabelecimento de ensino | 20% dela |
| Responsabilidade civil - hotel pet | Responsabilidade civil - operações pet shop e/ou clínica veterinária | 20% dela |
| Responsabilidade civil - ocorrência de bullying em escolas | Responsabilidade Civil - Operações · Responsabilidade civil - operações estabelecimento de ensino | 20% dela |
| Responsabilidade civil - taxi dog | Responsabilidade civil - operações pet shop e/ou clínica veterinária | 20% dela |
| Responsabilidade civil - alimentos distribuídos pela escola | Responsabilidade Civil - Operações · Responsabilidade civil - operações estabelecimento de ensino | 20% dela |
| Roubo E/ou Furto Qualificado de Bens de Hóspedes | Roubo E/ou Furto Qualificado de Bens | — |
| Despesas extraordinárias | Lucros Cessantes - Incêndio · Despesas Fixas - Ampla · Despesas Fixas - Incêndio | 10% dela |
| Despesas fixas - danos elétricos | Danos Elétricos | — |
| Despesas fixas - vendaval | Vendaval, Furacão, Ciclone, Tornado, Granizo e Impacto de Veículos | — |
| Despesas fixas - vendaval para bens ao ar livre | Vendaval, Furacão, Ciclone, Tornado, Granizo e Impacto de Veículos - para Bens Ao Ar Livre | — |
| Despesas fixas - vendaval para concessionárias (exceto veículos ao ar livre) | Vendaval para concessionárias (exceto veículos ao ar livre) | — |
| Despesas fixas - vendaval para concessionárias (inclusive veículos ao ar livre) | Vendaval para concessionárias (inclusive veículos ao ar livre) | — |
| Honorários de peritos contábeis | Lucros Cessantes - Incêndio · Despesas Fixas - Ampla · Despesas Fixas - Incêndio | — |
| Lucros cessantes - danos elétricos | Danos Elétricos | — |
| Lucros cessantes - vendaval | Vendaval, Furacão, Ciclone, Tornado, Granizo e Impacto de Veículos | — |
| Lucros cessantes - vendaval para bens ao ar livre | Vendaval, Furacão, Ciclone, Tornado, Granizo e Impacto de Veículos - para Bens Ao Ar Livre | — |
| Lucros cessantes - vendaval para concessionárias (exceto veículos ao ar livre) | Vendaval para concessionárias (exceto veículos ao ar livre) | — |
| Lucros cessantes - vendaval para concessionárias (inclusive veículos ao ar livre) | Vendaval para concessionárias (inclusive veículos ao ar livre) | — |
| Responsabilidade civil - contingentes de veículos | RESPONSABILIDADE CIVIL - BARES E RESTAURANTES · Responsabilidade civil - operações clubes, agremiações e associações recreativas · Responsabilidade civil - operações concessionárias até 100 km · Responsabilidade civil - operações concessionárias até 200 km · Responsabilidade civil - operações concessionárias até 300 km · Responsabilidade civil - operações estabelecimento de ensino · Responsabilidade civil - operações hotéis e pousadas · Responsabilidade Civil - Operações · Responsabilidade civil - operações pet shop e/ou clínica veterinária · Responsabilidade civil - operações salões de beleza | 100% dela |
| Responsabilidade civil - serviços de manobrista | Responsabilidade civil - guarda de veículos - compreensiva | 20% dela |

Confirmado na homologação para `Responsabilidade Civil - Danos Morais`: um erro por RC Operações
presente, com a mensagem "Cobertura Responsabilidade Civil - Danos Morais, não pode ter o
percentual maior (100%) que a Cobertura Responsabilidade Civil - Operações `<variante>`"
(Salões de Beleza, Pet Shop, Concessionárias até 100 km, Bares e Restaurantes, Estabelecimento
de Ensino, Hotéis e Pousadas).

## Excludentes (X cancela Y: nunca os dois na mesma massa)

| Cobertura | Não pode estar junto com |
|---|---|
| Vendaval para concessionárias (exceto veículos ao ar livre) | Vendaval para concessionárias (inclusive veículos ao ar livre) · Vendaval, Furacão, Ciclone, Tornado, Granizo e Impacto de Veículos |
| Vendaval, Furacão, Ciclone, Tornado, Granizo e Impacto de Veículos | Vendaval para concessionárias (exceto veículos ao ar livre) · Vendaval para concessionárias (inclusive veículos ao ar livre) |
| Vendaval para concessionárias (inclusive veículos ao ar livre) | Vendaval para concessionárias (exceto veículos ao ar livre) · Vendaval, Furacão, Ciclone, Tornado, Granizo e Impacto de Veículos |
| Despesas Fixas - Ampla | Despesas Fixas - Incêndio · Despesas fixas - danos elétricos · Lucros cessantes - danos elétricos · Lucros Cessantes - Incêndio · Despesas fixas - vendaval · Despesas fixas - vendaval para bens ao ar livre · Despesas fixas - vendaval para concessionárias (exceto veículos ao ar livre) · Despesas fixas - vendaval para concessionárias (inclusive veículos ao ar livre) · Lucros cessantes - vendaval · Lucros cessantes - vendaval para bens ao ar livre · Lucros cessantes - vendaval para concessionárias (exceto veículos ao ar livre) · Lucros cessantes - vendaval para concessionárias (inclusive veículos ao ar livre) |
| Despesas Fixas - Incêndio | Despesas Fixas - Ampla · Lucros Cessantes - Incêndio |
| Lucros Cessantes - Incêndio | Despesas Fixas - Ampla · Despesas Fixas - Incêndio |
| Pátio - Até 100 Km | Pátio - Até 200 Km · Pátio - Até 300 Km |
| Pátio - Até 200 Km | Pátio - Até 100 Km · Pátio - Até 300 Km |
| Pátio - Até 300 Km | Pátio - Até 100 Km · Pátio - Até 200 Km |
| Responsabilidade civil - operações concessionárias até 100 km | Responsabilidade civil - operações concessionárias até 200 km · Responsabilidade civil - operações concessionárias até 300 km |
| Responsabilidade civil - operações concessionárias até 200 km | Responsabilidade civil - operações concessionárias até 100 km · Responsabilidade civil - operações concessionárias até 300 km |
| Responsabilidade Civil - Operações | Responsabilidade civil - operações pet shop e/ou clínica veterinária |
| Responsabilidade civil - operações concessionárias até 300 km | Responsabilidade civil - operações concessionárias até 100 km · Responsabilidade civil - operações concessionárias até 200 km |
| Responsabilidade Civil - Guarda de Veículo - Incêndio e Roubo | Responsabilidade civil - guarda de veículos - compreensiva |
| Tumultos, Greves e Lockout | Tumultos, Greves e Lockout - Atos Dolosos |
| Tumultos, Greves e Lockout - Atos Dolosos | Tumultos, Greves e Lockout |
| Despesas fixas - danos elétricos | Despesas Fixas - Ampla |
| Despesas fixas - vendaval | Despesas Fixas - Ampla · Lucros cessantes - vendaval · Lucros cessantes - vendaval para bens ao ar livre · Lucros cessantes - vendaval para concessionárias (exceto veículos ao ar livre) · Lucros cessantes - vendaval para concessionárias (inclusive veículos ao ar livre) · Despesas fixas - vendaval para bens ao ar livre · Despesas fixas - vendaval para concessionárias (exceto veículos ao ar livre) · Despesas fixas - vendaval para concessionárias (inclusive veículos ao ar livre) |
| Despesas fixas - vendaval para bens ao ar livre | Despesas Fixas - Ampla · Lucros cessantes - vendaval · Lucros cessantes - vendaval para bens ao ar livre · Lucros cessantes - vendaval para concessionárias (exceto veículos ao ar livre) · Lucros cessantes - vendaval para concessionárias (inclusive veículos ao ar livre) · Despesas fixas - vendaval · Despesas fixas - vendaval para concessionárias (exceto veículos ao ar livre) · Despesas fixas - vendaval para concessionárias (inclusive veículos ao ar livre) |
| Despesas fixas - vendaval para concessionárias (exceto veículos ao ar livre) | Despesas Fixas - Ampla · Lucros cessantes - vendaval · Lucros cessantes - vendaval para bens ao ar livre · Lucros cessantes - vendaval para concessionárias (exceto veículos ao ar livre) · Lucros cessantes - vendaval para concessionárias (inclusive veículos ao ar livre) · Despesas fixas - vendaval · Despesas fixas - vendaval para bens ao ar livre · Despesas fixas - vendaval para concessionárias (inclusive veículos ao ar livre) |
| Despesas fixas - vendaval para concessionárias (inclusive veículos ao ar livre) | Despesas Fixas - Ampla · Lucros cessantes - vendaval · Lucros cessantes - vendaval para bens ao ar livre · Lucros cessantes - vendaval para concessionárias (exceto veículos ao ar livre) · Lucros cessantes - vendaval para concessionárias (inclusive veículos ao ar livre) · Despesas fixas - vendaval · Despesas fixas - vendaval para bens ao ar livre · Despesas fixas - vendaval para concessionárias (exceto veículos ao ar livre) |
| Lucros cessantes - danos elétricos | Despesas Fixas - Ampla |
| Lucros cessantes - vendaval | Despesas Fixas - Ampla · Lucros cessantes - vendaval para bens ao ar livre · Lucros cessantes - vendaval para concessionárias (exceto veículos ao ar livre) · Lucros cessantes - vendaval para concessionárias (inclusive veículos ao ar livre) · Despesas fixas - vendaval · Despesas fixas - vendaval para bens ao ar livre · Despesas fixas - vendaval para concessionárias (exceto veículos ao ar livre) · Despesas fixas - vendaval para concessionárias (inclusive veículos ao ar livre) |
| Lucros cessantes - vendaval para bens ao ar livre | Despesas Fixas - Ampla · Lucros cessantes - vendaval · Lucros cessantes - vendaval para concessionárias (exceto veículos ao ar livre) · Lucros cessantes - vendaval para concessionárias (inclusive veículos ao ar livre) · Despesas fixas - vendaval · Despesas fixas - vendaval para bens ao ar livre · Despesas fixas - vendaval para concessionárias (exceto veículos ao ar livre) · Despesas fixas - vendaval para concessionárias (inclusive veículos ao ar livre) |
| Lucros cessantes - vendaval para concessionárias (exceto veículos ao ar livre) | Despesas Fixas - Ampla · Lucros cessantes - vendaval · Lucros cessantes - vendaval para bens ao ar livre · Lucros cessantes - vendaval para concessionárias (inclusive veículos ao ar livre) · Despesas fixas - vendaval · Despesas fixas - vendaval para bens ao ar livre · Despesas fixas - vendaval para concessionárias (exceto veículos ao ar livre) · Despesas fixas - vendaval para concessionárias (inclusive veículos ao ar livre) |
| Lucros cessantes - vendaval para concessionárias (inclusive veículos ao ar livre) | Despesas Fixas - Ampla · Lucros cessantes - vendaval · Lucros cessantes - vendaval para bens ao ar livre · Lucros cessantes - vendaval para concessionárias (exceto veículos ao ar livre) · Despesas fixas - vendaval · Despesas fixas - vendaval para bens ao ar livre · Despesas fixas - vendaval para concessionárias (exceto veículos ao ar livre) · Despesas fixas - vendaval para concessionárias (inclusive veículos ao ar livre) |
| Responsabilidade civil - guarda de veículos - compreensiva | Responsabilidade Civil - Guarda de Veículo - Incêndio e Roubo |

Resumo prático:

- **Vendaval**: só um entre `Vendaval, Furacão, Ciclone, Tornado, Granizo e Impacto de Veículos`,
  `Vendaval para concessionárias (exceto…)` e `Vendaval para concessionárias (inclusive…)`.
  O "para Bens Ao Ar Livre" pode ficar junto.
- **Despesas Fixas / Lucros Cessantes por vendaval**: só **uma** das 8 variantes (DF-vendaval,
  DF-vendaval bens ao ar livre, DF-vendaval concessionárias exceto/inclusive e as 4 de LC). E
  nenhuma delas com `Despesas Fixas - Ampla`.
- **Incêndio**: `Despesas Fixas - Ampla`, `Despesas Fixas - Incêndio` e `Lucros Cessantes -
  Incêndio` são mutuamente excludentes: escolha uma só.
- **RC - Operações × RC Pet Shop**: confirmado na homologação ("Cobertura selecionada
  Responsabilidade Civil - Operações Pet Shop e/ou Clínica Veterinária, cancela a contratação da
  cobertura Responsabilidade Civil - Operações"). Com RC Pet Shop, as RC que exigem
  "RC Operações ou Estabelecimento de Ensino" (bicicletas, bullying, alimentos na escola) só
  entram se houver `RC - operações estabelecimento de ensino`.

## Pontos a confirmar na fonte (evite em massa válida; pergunte se o pedido exigir)

- `Responsabilidade Civil - Operações`: a coluna de código exclui só a RC Pet Shop (512), mas a
  descrição também cita "Estabelecimento de Ensino". Numa massa válida, **não** junte RC -
  Operações com RC - operações estabelecimento de ensino.
- `Lucros Cessantes - Incêndio`: coluna "Até % das demais coberturas" = 5, sem cobertura de
  referência indicada.
- A linha do código 526 vem com o nome "Lucros Cessantes - Vendaval para Bens ao Ar Livre", mas
  pelo código e pela cobertura exigida (535) é `Lucros cessantes - vendaval para concessionárias
  (exceto veículos ao ar livre)`. Foi mapeada assim.
