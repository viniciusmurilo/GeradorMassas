# Catálogo de Coberturas — Residencial (20 nomes utilizáveis)

Anfitrião
Bicicletas
Carro Na Garagem
Danos Elétricos
Equipamentos Eletrônicos e Eletrodomésticos
Equipamentos de Energia Solar e Fotovoltaico
Escritório Em Residência
Impacto de Veículos
Perda Ou Pagamento de Aluguel (pi = 12 Meses)
Quebra de Vidros
Responsabilidade Civil - Danos Morais
Responsabilidade Civil - Empregados Domésticos
Responsabilidade Civil - Familiar
Responsabilidade Civil - Prática de Esporte
Roubo E/ou Furto Qualificado de Bens
Roubo E/ou Furto Qualificado de Bicicleta Fora da Residência
Ruptura de Tubulações e Vazamento Acidental
Tumultos, Greves e Lockout
Vendaval, Furacão, Ciclone, Tornado, Granizo e Fumaça para Bens Ao Ar Livre
Vendaval, Furacão, Ciclone, Tornado, Granizo, Neve e Geada

## Defeito conhecido do template residencial

`Microempreendedor Em Residência` tem coluna CHK (**AA**) mas **não tem coluna TXT**. O arquivo tem
41 colunas (número ímpar: 21 CHK e 20 TXT). Consequências:

- Essa cobertura **nunca pode ser marcada como `sim`** — não há onde gravar o valor. Sua coluna CHK
  recebe `<IGNORE>` em todas as linhas.
- O `TXT "Escritório Em Residência"` ocupa a coluna AB, ao lado do CHK do Microempreendedor. Se na
  origem a AB deveria ser do Microempreendedor, os valores de Escritório estão indo para a coluna
  errada. **Só se resolve corrigindo o template na origem** — não é algo para o agente consertar.

O agente deve **tolerar** o CHK órfão (tratar como não-selecionável), nunca criar a coluna faltante.
Os scripts (`preencher_cobertura_multi.py`) já fazem isso automaticamente.

## Sobreposição entre os ramos

Apenas 6 nomes existem nos dois catálogos: Danos Elétricos, Quebra de Vidros, Responsabilidade
Civil - Danos Morais, Roubo E/ou Furto Qualificado de Bens, Tumultos Greves e Lockout, e
Vendaval...Fumaça para Bens Ao Ar Livre. Os demais são exclusivos de cada ramo. **Nunca misture os
catálogos** — uma cobertura só empresarial não pode ir para uma massa residencial e vice-versa.
