# LMI por Cobertura — Empresarial (base "Coberturas x LMI", aba `Empresarial`)

Complementa `normas_empresarial.md`. Onde as duas fontes divergem, **vale o valor mais
restritivo**. Os tetos absolutos desta planilha batem com a tabela de limites da norma; o que é
novo aqui é o **mínimo**, o **teto percentual** e as regras de dependência/exclusão.

## Como aplicar numa massa válida

Cada cobertura tem **três** limites que valem ao mesmo tempo:

1. **Mínimo** (R$).
2. **Máximo absoluto** (R$).
3. **Máximo percentual** — % do LMI de outra cobertura, quase sempre a básica
   `Incêndio, Queda de Raio, Queda de Aeronaves, Implosão, Explosão e Fumaça` ("básica" na
   tabela).

Teto efetivo = **o menor** entre o máximo absoluto e o percentual × LMI da cobertura de
referência. Por isso:

- Toda massa com cobertura adicional precisa ter a **cobertura básica (Incêndio)** com valor.
  Defina a básica primeiro (coerente com `Valor em Risco - Danos Materiais`) e calcule as demais.
- Cobertura cuja referência é outra cobertura (RC - Operações, Lucros Cessantes - Incêndio,
  RC Operações Pet Shop...) exige essa cobertura na massa.
- Ex.: básica = 1.000.000 → Danos Elétricos ≤ min(5.000.000; 60% × 1.000.000) = **600.000**;
  Quebra de Vidros ≤ min(1.000.000; 20%) = **200.000**.

## Campos de risco

| Campo (`texto`) | Mín (R$) | Máx (R$) |
|---|---:|---:|
| `Valor em Risco - Danos Materiais` | 55.000,00 | 150.000.000,00 |

`Despesas Fixas - Ampla`, `Despesas Fixas - Incêndio` e `Lucros Cessantes - Incêndio` não podem
passar do valor informado em `Lucros Cessantes` (campo de texto) — numa massa com qualquer uma
delas, preencha `Lucros Cessantes` com valor ≥ ao LMI dessas coberturas.

## Tabela de LMI

Nomes na grafia do template (`catalogo_empresarial.md`).

| Cobertura | Mín (R$) | Máx (R$) | Máx % | Observação |
|---|---:|---:|---|---|
| Danos Elétricos | 1.000,00 | 5.000.000,00 | 60% da básica |  |
| Roubo E/ou Furto Qualificado de Bens | 1.000,00 | 500.000,00 | 30% da básica |  |
| Equipamentos Eletrônicos | 1.000,00 | 3.000.000,00 | 20% da básica |  |
| Quebra de Vidros | 1.000,00 | 1.000.000,00 | 20% da básica |  |
| Vendaval, Furacão, Ciclone, Tornado, Granizo e Impacto de Veículos | 5.000,00 | 7.500.000,00 | 50% da básica |  |
| Alagamento | 1.000,00 | 500.000,00 | 20% da básica |  |
| Anúncios Luminosos | 1.000,00 | 1.000.000,00 | 20% da básica |  |
| Demolição e Remoção de Entulho | 5.000,00 | 30.000.000,00 | 100% da básica |  |
| Derrame Ou Vazamento de Chuveiros Automáticos (sprinklers) | 5.000,00 | 5.000.000,00 | 20% da básica |  |
| Desmoronamento | 5.000,00 | 1.000.000,00 | 40% da básica |  |
| Responsabilidade Civil - Danos Morais | 1.000,00 | 1.000.000,00 | — | ≤ LMI da básica · exige uma RC Operações (ver §Dependências) |
| Responsabilidade Civil - Operações | 1.000,00 | 3.000.000,00 | 50% da básica |  |
| Despesas Fixas - Ampla | 5.000,00 | 20.000.000,00 | — | ≤ Valor em Risco de `Lucros Cessantes` · excludente com DF-Incêndio (ver §Excludentes) |
| Despesas Fixas - Incêndio | 5.000,00 | 20.000.000,00 | 100% da básica | ≤ Valor em Risco de `Lucros Cessantes` · excludente com DF-Ampla |
| Deterioração de Mercadorias Em Ambientes Frigorificados | 1.000,00 | 500.000,00 | 10% da básica |  |
| Deterioração de Vacinas para Pet Shop, Consultório, Agropecuária e Veterinário | 1.000,00 | 50.000,00 | 10% da básica |  |
| Equipamentos Estacionários | 1.000,00 | 3.000.000,00 | 20% da básica |  |
| Equipamentos Móveis | 1.000,00 | 3.000.000,00 | 20% da básica |  |
| Escritório Em Casa de Funcionário | 1.000,00 | 50.000,00 | 10% da básica |  |
| Lucros Cessantes - Incêndio | 5.000,00 | 20.000.000,00 | 100% da básica | ≤ Valor em Risco de `Lucros Cessantes` · excludente com DF-Ampla |
| Pátio - Até 100 Km | 5.000,00 | 10.000.000,00 | 70% da básica | excludente com Pátio 200 Km |
| Pátio - Até 200 Km | 5.000,00 | 10.000.000,00 | 70% da básica | excludente com Pátio 100/300 Km |
| Pátio - Até 300 Km | 5.000,00 | 10.000.000,00 | 70% da básica | excludente com Pátio 200 Km |
| Recomposição de Registros e Documentos | 1.000,00 | 5.000.000,00 | 10% da básica |  |
| Responsabilidade Civil - Empregador | 1.000,00 | 3.000.000,00 | 100% de Responsabilidade Civil - Operações | exige RC - Operações |
| Responsabilidade Civil - Guarda de Veículo - Incêndio e Roubo | 1.000,00 | 500.000,00 | 10% da básica |  |
| Roubo de Valores Em Mãos de Portadores | 1.000,00 | 50.000,00 | 10% da básica |  |
| Roubo de Valores No Interior do Estabelecimento | 1.000,00 | 50.000,00 | 10% da básica |  |
| Roubo E/ou Furto Qualificado de Bens de Hóspedes | 1.000,00 | 100.000,00 | — | ≤ LMI da básica |
| Tumultos, Greves e Lockout | 1.000,00 | 4.000.000,00 | 50% da básica | excludente com TGL - Atos Dolosos |
| Tumultos, Greves e Lockout - Atos Dolosos | 1.000,00 | 4.000.000,00 | 50% da básica | excludente com TGL |
| Vazamento de Tanques e Ruptura de Tubulações | 1.000,00 | 1.000.000,00 | 50% da básica |  |
| Perda Ou Pagamento de Aluguel a Terceiros | 1.000,00 | 15.000.000,00 | 50% da básica |  |
| Benefícios fiscais | 1.000,00 | 999.999.999,99 | 1% da básica |  |
| Bens depositados em guarda volumes | 1.000,00 | 20.000,00 | 20% da básica |  |
| Bens do segurado em locais especificados | 1.000,00 | 999.999.999,99 | 5% da básica |  |
| Bens do segurado em locais não especificados | 1.000,00 | 0,00 | 5% da básica | máximo **0,00** na fonte — trate como não contratável (ver §Pontos a confirmar) |
| Bens do segurado em locais não especificados - ampla | 1.000,00 | 999.999.999,99 | 5% da básica |  |
| Danos à fabricação | 5.000,00 | 500.000,00 | 50% da básica |  |
| Danos à mercadoria por quebra de vidro | 1.000,00 | 50.000,00 | 10% da básica |  |
| Derrame de material em estado de fusão | 5.000,00 | 500.000,00 | 50% da básica |  |
| Despesas com instalação em novo local | 5.000,00 | 12.000.000,00 | 100% da básica |  |
| Despesas extraordinárias | 5.000,00 | 2.000.000,00 | 10% de Lucros Cessantes - Incêndio | exige Lucros Cessantes - Incêndio |
| Despesas fixas - danos elétricos | 1.000,00 | 1.000.000,00 | 20% da básica |  |
| Despesas fixas - vendaval | 1.000,00 | 3.000.000,00 | 50% da básica | excludente com DF-Vendaval bens ao ar livre |
| Despesas fixas - vendaval para bens ao ar livre | 1.000,00 | 3.000.000,00 | 50% da básica | excludente com DF-Vendaval |
| Despesas fixas - vendaval para concessionárias (exceto veículos ao ar livre) | 5.000,00 | 3.000.000,00 | 50% da básica | exige `Vendaval para concessionárias (exceto veículos ao ar livre)` · excludente com DF-Vendaval bens ao ar livre |
| Despesas fixas - vendaval para concessionárias (inclusive veículos ao ar livre) | 5.000,00 | 3.000.000,00 | — | ≤ LMI da básica · exige `Vendaval para concessionárias (inclusive veículos ao ar livre)` · excludente com DF-Vendaval concessionárias (exceto) |
| Deterioração de flores em câmaras frias | 1.000,00 | 100.000,00 | 20% da básica |  |
| Equipamentos cinematográficos, fotográficos e de vídeo | 1.000,00 | 200.000,00 | 20% da básica |  |
| Equipamentos e/ou objetos portáteis | 1.000,00 | 100.000,00 | 20% da básica |  |
| Equipamentos em exposição | 1.000,00 | 1.000.000,00 | 20% da básica |  |
| Fidelidade de empregados | 1.000,00 | 250.000,00 | 10% da básica |  |
| Honorários de peritos contábeis | 1.000,00 | 500.000,00 | — | ≤ LMI da básica |
| Lucros cessantes - danos elétricos | 5.000,00 | 3.000.000,00 | 20% da básica |  |
| Lucros cessantes - quebra de máquinas | 5.000,00 | 999.999.999,99 | 50% da básica | fonte: "verificar, não aparece os valores em tela" |
| Lucros cessantes - vendaval | 5.000,00 | 3.000.000,00 | 50% da básica | exige `Vendaval, Furacão, Ciclone, Tornado, Granizo e Impacto de Veículos` |
| Lucros cessantes - vendaval para bens ao ar livre | 5.000,00 | 3.000.000,00 | 50% da básica | excludente com LC-Vendaval |
| Lucros cessantes - vendaval para concessionárias (exceto veículos ao ar livre) | 5.000,00 | 3.000.000,00 | 50% da básica | excludente com LC-Vendaval bens ao ar livre |
| Lucros cessantes - vendaval para concessionárias (inclusive veículos ao ar livre) | 5.000,00 | 3.000.000,00 | — | ≤ LMI da básica · exige `Vendaval para concessionárias (inclusive veículos ao ar livre)` |
| Moldes e matrizes | 1.000,00 | 20.000,00 | 10% da básica |  |
| Movimentação interna | 1.000,00 | 500.000,00 | 50% da básica |  |
| Obras de arte | 500,00 | 999.999.999,99 | 20% da básica |  |
| Operações de carga, descarga, içamento e descida | 1.000,00 | 500.000,00 | 50% da básica |  |
| Pequenas obras de engenharia | 5.000,00 | 1.000.000,00 | 5% da básica |  |
| Quebra de máquinas | 5.000,00 | 300.000,00 | 50% da básica |  |
| Quebra de vidro de utensílio de cozinha | 1.000,00 | 50.000,00 | 10% da básica |  |
| Queimadas em zonas rurais | 5.000,00 | 0,00 | 100% da básica | máximo **0,00** na fonte — trate como não contratável (ver §Pontos a confirmar) |
| Responsabilidade civil - alimentos distribuídos pela escola | 1.000,00 | 50.000,00 | 20% de Responsabilidade Civil - Operações | exige RC - Operações |
| Responsabilidade civil - banho e tosa | 1.000,00 | 50.000,00 | — | ≤ LMI da básica · exige RC Operações Pet Shop |
| Responsabilidade civil - contingentes de veículos | 1.000,00 | 3.000.000,00 | 100% de Responsabilidade Civil - Operações | exige RC - Operações |
| Responsabilidade civil - dog walker | 1.000,00 | 50.000,00 | — | ≤ LMI da básica · exige RC Operações Pet Shop |
| Responsabilidade civil - guarda de bicicletas | 1.000,00 | 50.000,00 | 20% de Responsabilidade Civil - Operações | exige RC - Operações |
| Responsabilidade civil - guarda de embarcações de terceiros | 1.000,00 | 999.999.999,99 | 50% da básica | **sem aceitação comercial** (CB18.26008) |
| Responsabilidade civil - guarda de veículos - compreensiva | 1.000,00 | 500.000,00 | — | excludente com RC Guarda de Veículo - Incêndio e Roubo |
| Responsabilidade civil - hotel pet | 1.000,00 | 50.000,00 | — | ≤ LMI da básica · exige RC Operações Pet Shop |
| Responsabilidade civil - movimentação de carga e descarga | 1.000,00 | 999.999.999,99 | 50% da básica | fonte repete a mensagem de "sem aceitação" da Guarda de Embarcações (ver §Pontos a confirmar) |
| Responsabilidade civil - ocorrência de bullying em escolas | 1.000,00 | 50.000,00 | 20% de Responsabilidade Civil - Operações | ≤ LMI da básica · exige RC Operações ou RC Operações Estabelecimento de Ensino |
| RESPONSABILIDADE CIVIL - BARES E RESTAURANTES | 1.000,00 | 3.000.000,00 | 50% da básica | CB18.26053 |
| Responsabilidade civil - operações clubes, agremiações e associações recreativas | 1.000,00 | 3.000.000,00 | 50% da básica | CB18.26054 |
| Responsabilidade civil - operações concessionárias até 100 km | 1.000,00 | 3.000.000,00 | 70% da básica | CB18.26055 · excludente com RC Concessionárias 200 km |
| Responsabilidade civil - operações concessionárias até 200 km | 1.000,00 | 3.000.000,00 | 70% da básica | excludente com RC Concessionárias 100/300 km |
| Responsabilidade civil - operações concessionárias até 300 km | 1.000,00 | 3.000.000,00 | 70% da básica | CB18.26057 · excludente com RC Concessionárias 200 km |
| Responsabilidade civil - operações estabelecimento de ensino | 1.000,00 | 3.000.000,00 | 50% da básica |  |
| Responsabilidade civil - operações hotéis e pousadas | 1.000,00 | 3.000.000,00 | 50% da básica |  |
| Responsabilidade civil - operações pet shop e/ou clínica veterinária | 1.000,00 | 1.000.000,00 | 50% da básica | excludente com RC - Operações |
| Responsabilidade civil - operações salões de beleza | 1.000,00 | 1.000.000,00 | 50% da básica |  |
| Responsabilidade civil - produtos | 1.000,00 | 999.999.999,99 | 50% da básica | **sem aceitação comercial** (por `normas_empresarial.md`) |
| Responsabilidade civil - serviços de manobrista | 1.000,00 | 200.000,00 | — | ≤ LMI da básica · exige RC Guarda de Veículos - Compreensiva |
| Responsabilidade civil - taxi dog | 1.000,00 | 50.000,00 | 20% de Responsabilidade Civil - Operações Pet Shop e/ou Clínica Veterinária | exige RC Operações Pet Shop |
| Roubo de valores e/ou bens de clientes | 1.000,00 | 20.000,00 | 20% da básica | CB18.26072 |
| Terremoto, tremor de terra e maremoto | 1.000,00 | 999.999.999,99 | 20% da básica |  |
| Vendaval, Furacão, Ciclone, Tornado, Granizo e Impacto de Veículos - para Bens Ao Ar Livre | 5.000,00 | 1.000.000,00 | 10% da básica | fonte também lista como "... e Fumaça para Bens Ao Ar Livre" (mesmos limites) |
| Vendaval para concessionárias (exceto veículos ao ar livre) | 5.000,00 | 7.500.000,00 | 50% da básica | excludente com `Vendaval, Furacão, Ciclone, Tornado, Granizo e Impacto de Veículos` |
| Indenização a valor de novo (LMI) | 0,01 | 999.999.999,99 | ≤ LMI da básica | só se aplica quando o grupo `Deseja contratar indenização a valor de novo?` = `SIM` |

A cobertura básica `Incêndio, Queda de Raio, Queda de Aeronaves, Implosão, Explosão e Fumaça` não
tem linha própria na fonte — use como teto o `Valor em Risco - Danos Materiais` da massa.

## Dependências (cobertura X exige cobertura Y na mesma massa)

| Se incluir… | …precisa incluir pelo menos uma de |
|---|---|
| Responsabilidade Civil - Danos Morais | Responsabilidade Civil - Operações · RC - operações pet shop e/ou clínica veterinária · RC - operações concessionárias até 100/200/300 km · RC - operações salões de beleza · RC - operações estabelecimento de ensino · RC - operações hotéis e pousadas · RC - operações clubes, agremiações e associações recreativas · RESPONSABILIDADE CIVIL - BARES E RESTAURANTES |
| Responsabilidade civil - banho e tosa / dog walker / hotel pet / taxi dog | Responsabilidade civil - operações pet shop e/ou clínica veterinária |
| Responsabilidade civil - ocorrência de bullying em escolas | Responsabilidade Civil - Operações · Responsabilidade civil - operações estabelecimento de ensino |
| Responsabilidade civil - serviços de manobrista | Responsabilidade civil - guarda de veículos - compreensiva |
| Lucros cessantes - vendaval | Vendaval, Furacão, Ciclone, Tornado, Granizo e Impacto de Veículos |
| Despesas fixas - vendaval para concessionárias (exceto veículos ao ar livre) | Vendaval para concessionárias (exceto veículos ao ar livre) |
| Despesas fixas - vendaval para concessionárias (inclusive veículos ao ar livre) | Vendaval para concessionárias (inclusive veículos ao ar livre) |
| Lucros cessantes - vendaval para concessionárias (inclusive veículos ao ar livre) | Vendaval para concessionárias (inclusive veículos ao ar livre) |
| RC - Empregador / alimentos distribuídos pela escola / contingentes de veículos / guarda de bicicletas | Responsabilidade Civil - Operações (base do %) |
| Despesas extraordinárias | Lucros Cessantes - Incêndio (base do %) |

## Excludentes ("cobertura X cancela a cobertura Y" — nunca as duas na mesma massa)

Além da lista de `Despesas Fixas - Ampla` já documentada em `normas_empresarial.md`:

- `Despesas Fixas - Incêndio` × `Despesas Fixas - Ampla`
- `Lucros Cessantes - Incêndio` × `Despesas Fixas - Ampla`
- `Pátio - Até 100 Km` × `Pátio - Até 200 Km` × `Pátio - Até 300 Km` (escolha uma só)
- `Tumultos, Greves e Lockout` × `Tumultos, Greves e Lockout - Atos Dolosos`
- `Despesas fixas - vendaval` × `Despesas fixas - vendaval para bens ao ar livre`
- `Despesas fixas - vendaval para concessionárias (exceto veículos ao ar livre)` × `Despesas fixas - vendaval para bens ao ar livre`
- `Despesas fixas - vendaval para concessionárias (inclusive veículos ao ar livre)` × `Despesas fixas - vendaval para concessionárias (exceto veículos ao ar livre)`
- `Lucros cessantes - vendaval para bens ao ar livre` × `Lucros cessantes - vendaval`
- `Lucros cessantes - vendaval para concessionárias (exceto veículos ao ar livre)` × `Lucros cessantes - vendaval para bens ao ar livre`
- `Responsabilidade civil - guarda de veículos - compreensiva` × `Responsabilidade Civil - Guarda de Veículo - Incêndio e Roubo`
- `Responsabilidade civil - operações concessionárias até 100 km` × `... até 200 km` × `... até 300 km` (escolha uma só)
- `Vendaval para concessionárias (exceto veículos ao ar livre)` × `Vendaval, Furacão, Ciclone, Tornado, Granizo e Impacto de Veículos`
- `Responsabilidade civil - operações pet shop e/ou clínica veterinária` × `Responsabilidade Civil - Operações`
  (erro observado na homologação: "Cobertura selecionada Responsabilidade Civil - Operações Pet
  Shop e/ou Clínica Veterinária, cancela a contratação da cobertura Responsabilidade Civil -
  Operações"). Consequência: numa massa com RC Pet Shop, **não** inclua RC - Empregador,
  RC - alimentos distribuídos pela escola, RC - contingentes de veículos nem RC - guarda de
  bicicletas (todas dependem de RC - Operações); `Responsabilidade Civil - Danos Morais`
  continua válida porque a própria RC Pet Shop satisfaz a dependência dela.

## Coberturas sem aceitação comercial (nunca usar em massa válida)

- `Responsabilidade civil - guarda de embarcações de terceiros` (CB18.26008)
- `Responsabilidade civil - produtos` (já em `normas_empresarial.md`)

## Pontos a confirmar na fonte (evite em massa válida; pergunte se o pedido exigir)

- `Bens do segurado em locais não especificados` e `Queimadas em zonas rurais`: máximo **0,00**
  na planilha — provavelmente não contratáveis.
- `Responsabilidade civil - movimentação de carga e descarga`: a mensagem de erro é cópia da de
  Guarda de Embarcações ("não possui aceitação comercial") — pode ser erro de digitação na fonte.
- `Lucros cessantes - quebra de máquinas`: fonte anota "verificar, não aparece os valores em tela".
