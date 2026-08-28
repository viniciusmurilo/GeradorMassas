#!/usr/bin/env python3
"""
Preenche a planilha de cobertura empresarial a partir de um JSON de extracao.

Uso:
    python preencher_cobertura.py entrada.json saida.xlsx [template.xlsx]

Formato do JSON de entrada:
    {
      "coberturas": [
        {"nome": "Danos Eletricos", "valor": 200000},
        {"nome": "Alagamento", "valor": 300000}
      ]
    }

Regras aplicadas:
  - Cobertura presente no JSON  -> CHK = "sim", TXT = valor
  - Cobertura ausente do JSON   -> CHK = "<IGNORE>", TXT = "<IGNORE>"

O pareamento CHK/TXT e feito pelo NOME lido no cabecalho, nunca por posicao:
5 dos 34 pares nao sao colunas adjacentes neste template.
"""

import json
import re
import sys
import unicodedata

import openpyxl
from openpyxl.utils import get_column_letter

ABA = "Exportation"
LINHA_CABECALHO = 1
LINHA_DADOS = 2
SIM = "sim"
IGNORAR = "<IGNORE>"


def normalizar(texto):
    """Minusculas, sem acento, sem pontuacao, espacos colapsados."""
    t = unicodedata.normalize("NFKD", str(texto))
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r"[^a-zA-Z0-9]+", " ", t)
    return " ".join(t.lower().split())


def mapear_colunas(ws):
    """Le a linha de cabecalho e devolve {nome_canonico: {'chk': col, 'txt': col}}."""
    chk, txt = {}, {}
    for c in range(1, ws.max_column + 1):
        cabecalho = ws.cell(row=LINHA_CABECALHO, column=c).value
        if not cabecalho:
            continue
        cabecalho = str(cabecalho).strip()
        col = get_column_letter(c)
        if cabecalho.startswith("CHK "):
            chk[cabecalho[4:].strip()] = col
        else:
            m = re.match(r'TXT\s+"(.+)"\s+Valor da Cobertura', cabecalho)
            if m:
                txt[m.group(1).strip()] = col

    faltando_txt = set(chk) - set(txt)
    faltando_chk = set(txt) - set(chk)
    if faltando_txt or faltando_chk:
        raise ValueError(
            f"Cabecalho inconsistente. Sem coluna de valor: {sorted(faltando_txt)}. "
            f"Sem coluna de check: {sorted(faltando_chk)}."
        )

    return {nome: {"chk": chk[nome], "txt": txt[nome]} for nome in chk}


def formatar_valor(v):
    """Normaliza para string inteira sem separador: 200000 / '200.000' / 'R$ 200 mil' -> '200000'."""
    if isinstance(v, (int, float)):
        return str(int(round(v)))
    s = str(v).strip()
    s = re.sub(r"(?i)^r\$\s*", "", s)
    s = re.sub(r"[^\d,.]", "", s)
    if "," in s:                      # padrao BR: 200.000,50
        s = s.replace(".", "").replace(",", ".")
    elif s.count(".") == 1 and len(s.split(".")[1]) in (1, 2):
        pass                          # 1500.50 -> decimal
    else:
        s = s.replace(".", "")        # 200.000 -> milhar
    if not s:
        raise ValueError("valor vazio ou nao numerico")
    return str(int(round(float(s))))


def preencher(dados, caminho_template, caminho_saida):
    wb = openpyxl.load_workbook(caminho_template)
    ws = wb[ABA]
    colunas = mapear_colunas(ws)
    indice = {normalizar(n): n for n in colunas}

    solicitadas = {}
    for item in dados.get("coberturas", []):
        nome_bruto = item["nome"]
        canonico = indice.get(normalizar(nome_bruto))
        if canonico is None:
            raise ValueError(
                f"Cobertura nao existe no template: {nome_bruto!r}. "
                "O extrator deve devolver apenas nomes do catalogo."
            )
        if canonico in solicitadas:
            raise ValueError(f"Cobertura duplicada na entrada: {canonico!r}")
        solicitadas[canonico] = formatar_valor(item["valor"])

    for nome, cols in colunas.items():
        if nome in solicitadas:
            ws[f"{cols['chk']}{LINHA_DADOS}"] = SIM
            ws[f"{cols['txt']}{LINHA_DADOS}"] = solicitadas[nome]
        else:
            ws[f"{cols['chk']}{LINHA_DADOS}"] = IGNORAR
            ws[f"{cols['txt']}{LINHA_DADOS}"] = IGNORAR

    wb.save(caminho_saida)
    return solicitadas, len(colunas)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    entrada, saida = sys.argv[1], sys.argv[2]
    template = sys.argv[3] if len(sys.argv) > 3 else "template_cobertura.xlsx"

    with open(entrada, encoding="utf-8") as f:
        dados = json.load(f)

    marcadas, total = preencher(dados, template, saida)
    print(f"{saida}: {len(marcadas)} de {total} coberturas marcadas como '{SIM}'.")
    for nome, valor in sorted(marcadas.items()):
        print(f"  - {nome}: {valor}")


if __name__ == "__main__":
    main()
