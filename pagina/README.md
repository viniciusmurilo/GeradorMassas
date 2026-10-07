# Gerador de Massas (página HTML)

`dist/gerador_massas.html` é um arquivo único: dê dois cliques e ele abre no navegador. Funciona
sem servidor, sem login e sem internet, e qualquer pessoa pode usar.

Abas:

1. **Corrigir planilha**: sobe um .xlsx de massas, valida, corrige o que dá e devolve o Excel corrigido.
   O que não dá para corrigir sozinho aparece como ERRO, para ajuste manual.
2. **Montar massa**: formulário campo a campo, com as regras conferidas enquanto você digita. Junta
   várias massas e baixa tudo num Excel.
3. **Templates**: baixa os templates originais da skill.

Arquivos:

- `nucleo.js`: porta em JavaScript (ExcelJS) do `preencher_massa.py`, do `extrair_massa.py` e do
  `validar_massa.py`. Dá o mesmo resultado dos scripts Python (testado nas 30 planilhas de teste).
- `ui.html`: a página.
- `vendor/`: ExcelJS 4.4.0 e JSZip 3.10.2 (licença MIT), embutidos no HTML final.
- `montar.py`: gera `dist/gerador_massas.html` com tudo dentro (bibliotecas, núcleo, templates, regras).

Depois de mudar uma regra ou um template da skill, rode `python3 pagina/montar.py` e distribua de
novo o `dist/gerador_massas.html`.
