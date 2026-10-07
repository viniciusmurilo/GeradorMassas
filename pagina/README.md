# Página do Gerador de Massas

Versão no navegador da skill `gerador-massas-seguros`, com quatro abas:

1. **Corrigir planilha**: sobe um .xlsx de massas, valida, corrige e devolve o Excel corrigido.
2. **Gerar por texto**: descreve as massas como no chat, o Claude monta e valida, a página gera o Excel.
3. **Formulário**: monta a massa campo a campo, com validação ao vivo.
4. **Templates**: baixa os templates originais.

- `nucleo.js`: porta em JavaScript (ExcelJS) do `preencher_massa.py`, do `extrair_massa.py` e do
  `validar_massa.py`. Dá o mesmo resultado dos scripts Python (testado nas 30 planilhas de teste).
- `ui.html`: a página.
- `montar.py`: gera `dist/gerador_massas.html`, um arquivo único que embute o núcleo, os templates,
  as regras e as referências da skill.

Depois de mudar uma regra, um template ou a página, rode `python3 pagina/montar.py` e publique
de novo o `dist/gerador_massas.html`.
