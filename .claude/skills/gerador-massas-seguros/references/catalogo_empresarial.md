# Catálogo de Colunas — Empresarial (`templates/template_empresarial.xlsx`)

Uma linha = uma massa completa (identificação + risco + questionário/proteções + coberturas).
Cabeçalho na **linha 2**, dados a partir da **linha 3**. O script (`scripts/preencher_massa.py`)
lê o cabeçalho em tempo de execução e casa cada campo pelo **nome exato**, nunca por posição —
não precisa (nem deve) calcular letra de coluna na mão.

## Campos diretos (obrigatórios em toda massa) — chave `campos`

| Cabeçalho | Conteúdo |
|---|---|
| `Corretor` | Nome do corretor (texto livre, ex.: `COI`) |
| `Tipo Pessoa` | CPF/CNPJ do segurado — ver "Tokens de aleatoriedade" abaixo |
| `Cep Risco` | CEP do risco — ver "Tokens de aleatoriedade" abaixo |

## Combos (obrigatórios) — chave `combos`

| Cabeçalho | Valores válidos |
|---|---|
| `Tipo de Construção` | `Superior` · `Sólida` · `Mista` · `Inferior` |
| `Objeto Segurado` | `Prédio e Conteúdo` · `Prédio` · `Conteúdo` |
| `Assistência 24h` | `Assistência Empresarial Plano Superior` · `Assistência Empresarial Plano Intermediário` · `Assistência Empresarial Plano Básico` · `Não Contratado` |

**Atenção**: `Mista` e `Inferior` não têm aceitação comercial na HDI (ver `references/normas_empresarial.md` §Tipo de Construção). Só use esses dois valores quando o pedido for **testar** essa rejeição — nunca em massa "normal"/válida.

## Texto (obrigatórios) — chave `texto`

| Cabeçalho | Conteúdo | Formato |
|---|---|---|
| `Atividade` | uma das 439 atividades de `references/atividades.txt` | texto exato do catálogo |
| `Valor em Risco - Danos Materiais` | valor do risco | **número puro** (ex.: `10000000`), nunca string formatada |
| `Lucros Cessantes` | valor de lucros cessantes | **número puro** |

## Coluna órfã — nunca preencher

`CHK Residencial Benefícios Essenciais` (coluna G) existe no arquivo mas é um campo do ramo
Residencial vazado no template Empresarial. Sempre fica `<IGNORE>` — o script já faz isso
sozinho quando a massa não menciona nada em `bool`; **nunca** inclua esse nome em `bool` para
uma massa empresarial.

## Grupos de escolha (questionário/proteção) — chave `grupos`, **os 3 abaixo são obrigatórios**

Cada grupo vira um conjunto de colunas `sim`/`<IGNORE>`. Passe só os nomes das opções marcadas;
o script grava `<IGNORE>` nas demais automaticamente. Nome de grupo e de opção têm que bater com
a lista abaixo (comparação tolera acento/caixa, mas não invente opção).

Os 3 grupos a seguir são **obrigatórios em toda massa** — o script recusa se algum não aparecer
em `grupos` (mesmo que vazio não vale; tem que ter uma opção escolhida). Se o usuário não disser
nada sobre proteção/indenização, use o padrão indicado em cada um.

### `Deseja contratar indenização a valor de novo?` — escolha única, obrigatório
Opções: `SIM` · `NÃO`. Padrão quando o usuário não especificar: `["NÃO"]`.

### `Existem equipamentos de proteção contra incêndio?` — escolha única, obrigatório
Opções: `Extintores` · `Extintores e Hidrantes` · `Extintores, hidrantes e sistema de detecção ou alarme de incêndio` · `Extintores, hidrantes e sprinklers` · `Não informado sistema de proteção contra incêndio`.
Padrão: `["Não informado sistema de proteção contra incêndio"]`.

### `Existem equipamentos de proteção contra roubo?` — múltipla escolha, obrigatório
Opções: `Sistema de alarme contra roubo` · `Grades de proteção e fechaduras tipo tetra` · `Vigilância armada ou desarmada com cobertura exclusiva 24 horas` · `Edificação comercial com elevador e controle de acesso por porteiro 24 horas` · `Não informado sistema de proteção contra roubo`.
Padrão: `["Não informado sistema de proteção contra roubo"]`.

Pode marcar mais de uma opção (ex.: alarme + grades), **exceto** `Não informado...`, que é
exclusiva — o script recusa se ela vier junto com qualquer outra opção do grupo.

Ver `references/normas_empresarial.md` §Protecionais Mínimos para atividades que **exigem**
proteção mínima de incêndio/roubo acima de determinado valor — numa massa válida, respeite esse
mínimo quando a atividade/cobertura pedida estiver na lista.

## Coberturas — chave `coberturas`

96 coberturas com coluna `TXT "<nome>" Valor da Cobertura`. Valor aceito no JSON: número (o
script formata sozinho para string BR `"200.000,00"`, igual ao padrão observado no template).
Cobertura pedida fora desta lista = erro do script → confira grafia aqui antes de perguntar ao
usuário se não achar.

4 delas também têm coluna `TXT "<nome>" Período Indenitário` — some `"periodo_indenitario": N`
(meses) no item de cobertura só quando o usuário pedir; sem isso a coluna fica `<IGNORE>`.

**Coberturas com período indenitário**: `Perda Ou Pagamento de Aluguel a Terceiros` ·
`Despesas Fixas - Ampla` · `Despesas Fixas - Incêndio` · `Lucros Cessantes - Incêndio`

**Lista completa (96):**

Alagamento · Anúncios Luminosos · Benefícios fiscais · Bens depositados em guarda volumes ·
Bens do segurado em locais especificados · Bens do segurado em locais não especificados ·
Bens do segurado em locais não especificados - ampla · Danos Elétricos · Danos à fabricação ·
Danos à mercadoria por quebra de vidro · Demolição e Remoção de Entulho ·
Derrame Ou Vazamento de Chuveiros Automáticos (sprinklers) · Derrame de material em estado de fusão ·
Desmoronamento · Despesas Fixas - Ampla · Despesas Fixas - Incêndio ·
Despesas com instalação em novo local · Despesas extraordinárias · Despesas fixas - danos elétricos ·
Despesas fixas - vendaval · Despesas fixas - vendaval para bens ao ar livre ·
Despesas fixas - vendaval para concessionárias (exceto veículos ao ar livre) ·
Despesas fixas - vendaval para concessionárias (inclusive veículos ao ar livre) ·
Deterioração de Mercadorias Em Ambientes Frigorificados ·
Deterioração de Vacinas para Pet Shop, Consultório, Agropecuária e Veterinário ·
Deterioração de flores em câmaras frias · Equipamentos Eletrônicos · Equipamentos Estacionários ·
Equipamentos Móveis · Equipamentos cinematográficos, fotográficos e de vídeo ·
Equipamentos e/ou objetos portáteis · Equipamentos em exposição · Escritório Em Casa de Funcionário ·
Fidelidade de empregados · Honorários de peritos contábeis ·
Incêndio, Queda de Raio, Queda de Aeronaves, Implosão, Explosão e Fumaça ·
Lucros Cessantes - Incêndio · Lucros cessantes - danos elétricos · Lucros cessantes - quebra de máquinas ·
Lucros cessantes - vendaval · Lucros cessantes - vendaval para bens ao ar livre ·
Lucros cessantes - vendaval para concessionárias (exceto veículos ao ar livre) ·
Lucros cessantes - vendaval para concessionárias (inclusive veículos ao ar livre) ·
Moldes e matrizes · Movimentação interna · Obras de arte ·
Operações de carga, descarga, içamento e descida · Pequenas obras de engenharia ·
Perda Ou Pagamento de Aluguel a Terceiros · Pátio - Até 100 Km · Pátio - Até 200 Km ·
Pátio - Até 300 Km · Quebra de Vidros · Quebra de máquinas · Quebra de vidro de utensílio de cozinha ·
Queimadas em zonas rurais · Recomposição de Registros e Documentos ·
Responsabilidade Civil - Danos Morais · Responsabilidade Civil - Empregador ·
Responsabilidade Civil - Guarda de Veículo - Incêndio e Roubo · Responsabilidade Civil - Operações ·
Responsabilidade civil - alimentos distribuídos pela escola · Responsabilidade civil - banho e tosa ·
Responsabilidade civil - contingentes de veículos · Responsabilidade civil - dog walker ·
Responsabilidade civil - guarda de bicicletas · Responsabilidade civil - guarda de embarcações de terceiros ·
Responsabilidade civil - guarda de veículos - compreensiva · Responsabilidade civil - hotel pet ·
Responsabilidade civil - movimentação de carga e descarga ·
Responsabilidade civil - ocorrência de bullying em escolas ·
RESPONSABILIDADE CIVIL - BARES E RESTAURANTES ·
Responsabilidade civil - operações clubes, agremiações e associações recreativas ·
Responsabilidade civil - operações concessionárias até 100 km ·
Responsabilidade civil - operações concessionárias até 200 km ·
Responsabilidade civil - operações concessionárias até 300 km ·
Responsabilidade civil - operações estabelecimento de ensino ·
Responsabilidade civil - operações hotéis e pousadas ·
Responsabilidade civil - operações pet shop e/ou clínica veterinária ·
Responsabilidade civil - operações salões de beleza · Responsabilidade civil - produtos ·
Responsabilidade civil - serviços de manobrista · Responsabilidade civil - taxi dog ·
Roubo E/ou Furto Qualificado de Bens · Roubo E/ou Furto Qualificado de Bens de Hóspedes ·
Roubo de Valores Em Mãos de Portadores · Roubo de Valores No Interior do Estabelecimento ·
Roubo de valores e/ou bens de clientes · Terremoto, tremor de terra e maremoto ·
Tumultos, Greves e Lockout · Tumultos, Greves e Lockout - Atos Dolosos ·
Vazamento de Tanques e Ruptura de Tubulações · Vendaval para concessionárias (exceto veículos ao ar livre) ·
Vendaval para concessionárias (inclusive veículos ao ar livre) ·
Vendaval, Furacão, Ciclone, Tornado, Granizo e Impacto de Veículos ·
Vendaval, Furacão, Ciclone, Tornado, Granizo e Impacto de Veículos - para Bens Ao Ar Livre

### Regras de desambiguação (nomes parecidos — pare e pergunte se não estiver claro)

- **Despesas Fixas / Lucros Cessantes**: existem duas famílias por peril. A "principal" (Título
  Case, com Período Indenitário): `Despesas Fixas - Ampla`, `Despesas Fixas - Incêndio`,
  `Lucros Cessantes - Incêndio`. A "por peril adicional" (minúsculas, sem período):
  `Despesas fixas - danos elétricos`, `Despesas fixas - vendaval[...]`,
  `Lucros cessantes - danos elétricos`, `Lucros cessantes - quebra de máquinas`,
  `Lucros cessantes - vendaval[...]`. São coberturas **diferentes** — não troque uma pela outra.
- **Vendaval**: "...e Impacto de Veículos" (bens em geral) ≠ "...e Impacto de Veículos - para
  Bens Ao Ar Livre". Só "vendaval" no pedido → pergunte.
- **Roubo/Furto Qualificado de Bens**: sem "de Hóspedes" é a geral; "de Hóspedes" só com menção
  explícita a hóspedes/hotel/pousada.
- **Roubo de Valores**: "Em Mãos de Portadores" (trânsito) ≠ "No Interior do Estabelecimento"
  (cofre/caixa) ≠ "e/ou Bens de Clientes".
- **Pátio**: 100 / 200 / 300 Km. Sem distância → pergunte.
- **Responsabilidade Civil**: mais de 25 variantes (Operações, Empregador, Danos Morais, Produtos,
  Taxi Dog, Dog Walker, Banho e Tosa, Hotel Pet, etc.). Só "RC" no pedido → pergunte qual.
- **Equipamentos**: "Eletrônicos" ≠ "Estacionários" ≠ "Móveis" ≠ "cinematográficos, fotográficos
  e de vídeo" ≠ "e/ou objetos portáteis" ≠ "em exposição".
- **Bens do segurado em locais...**: "especificados" ≠ "não especificados" ≠ "não especificados -
  ampla". Coberturas distintas.
- **Deterioração**: "de Mercadorias Em Ambientes Frigorificados" ≠ "de Vacinas para Pet Shop,
  Consultório, Agropecuária e Veterinário" ≠ "de flores em câmaras frias".
- **"Danos Elétricos" ≠ "Equipamentos Eletrônicos"** — coberturas diferentes.

## Tokens de aleatoriedade (`Tipo Pessoa` / `Cep Risco`)

Quando o pedido for por CPF/CNPJ/CEP **aleatórios**, grave o token literal — um robô externo
substitui pelo valor real depois. Nunca gere CPF/CNPJ/CEP você mesmo nesse caso.

| Token | Significado |
|---|---|
| `#cpf` | CPF aleatório |
| `#cnpj` | CNPJ aleatório (numérico) |
| `#cnpjalfa` | CNPJ alfanumérico aleatório |
| `#cep` | CEP aleatório |

Se o usuário informar um CPF/CNPJ/CEP **específico**, grave o valor literal (só dígitos, sem
pontuação/traço) em vez do token.

## Overlap com Residencial

7 nomes de cobertura existem nos dois catálogos com grafia idêntica: `Alagamento`,
`Danos Elétricos`, `Desmoronamento`, `Quebra de Vidros`, `Responsabilidade Civil - Danos Morais`,
`Roubo E/ou Furto Qualificado de Bens`, `Tumultos, Greves e Lockout`.
Os demais são exclusivos de cada ramo — **nunca misture os catálogos**. Em particular,
`Vendaval, Furacão, Ciclone, Tornado, Granizo e Impacto de Veículos - para Bens Ao Ar Livre` é
**só do empresarial**: existia por engano também no template residencial e foi removida de lá
(ver `catalogo_residencial.md` §Correção do template) — não use esse nome numa massa residencial.
