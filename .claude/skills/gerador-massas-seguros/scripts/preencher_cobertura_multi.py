#!/usr/bin/env python3
"""
Preenche N massas (uma por linha) reusando a logica de preencher_cobertura.py.

Uso:
    python3 preencher_cobertura_multi.py entrada_multi.json saida.xlsx template.xlsx

Formato:
    {"massas": [{"coberturas": [{"nome": "...", "valor": 200000}, ...]}, ...]}

Mesmas regras do script original: pareamento CHK/TXT pelo nome do cabecalho,
nome fora do catalogo e erro, ausentes viram <IGNORE>. Muda apenas a linha destino.
"""

import json
import sys

import openpyxl
from openpyxl.styles import Alignment

import re

from openpyxl.utils import get_column_letter

from preencher_cobertura import (
    ABA,
    IGNORAR,
    LINHA_CABECALHO,
    LINHA_DADOS,
    SIM,
    formatar_valor,
    normalizar,
)


def mapear_colunas_tolerante(ws):
    """Igual ao original, mas CHK sem TXT vira 'orfao' em vez de erro.

    Nao altera o template: a cobertura orfa simplesmente nao pode ser marcada,
    e sua coluna CHK recebe <IGNORE> em todas as linhas.
    """
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

    sem_chk = sorted(set(txt) - set(chk))
    if sem_chk:
        raise ValueError(f"Coluna de valor sem coluna de check: {sem_chk}")

    pares = {n: {"chk": chk[n], "txt": txt[n]} for n in chk if n in txt}
    orfas = {n: chk[n] for n in chk if n not in txt}
    return pares, orfas


def preencher_multi(dados, caminho_template, caminho_saida):
    wb = openpyxl.load_workbook(caminho_template)
    ws = wb[ABA]
    colunas, orfas = mapear_colunas_tolerante(ws)
    if orfas:
        print(f"AVISO: sem coluna de valor no template, nao podem ser marcadas: {sorted(orfas)}")
    indice = {normalizar(n): n for n in colunas}

    resumo = []
    for i, massa in enumerate(dados.get("massas", [])):
        linha = LINHA_DADOS + i
        solicitadas = {}
        for item in massa.get("coberturas", []):
            canonico = indice.get(normalizar(item["nome"]))
            if canonico is None:
                raise ValueError(
                    f"massa {i + 1}: cobertura nao existe no template: {item['nome']!r}"
                )
            if canonico in solicitadas:
                raise ValueError(f"massa {i + 1}: cobertura duplicada: {canonico!r}")
            solicitadas[canonico] = formatar_valor(item["valor"])

        for nome, cols in colunas.items():
            marcada = nome in solicitadas
            ws[f"{cols['chk']}{linha}"] = SIM if marcada else IGNORAR
            ws[f"{cols['txt']}{linha}"] = solicitadas[nome] if marcada else IGNORAR

        for col in orfas.values():
            ws[f"{col}{linha}"] = IGNORAR

        resumo.append((linha, solicitadas))

    # uniformiza o alinhamento das linhas de dados (a linha 2 vem centralizada do template)
    for linha_ws in ws.iter_rows(min_row=LINHA_DADOS, max_row=ws.max_row):
        for celula in linha_ws:
            celula.alignment = Alignment()

    wb.save(caminho_saida)
    return resumo, len(colunas)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    entrada, saida = sys.argv[1], sys.argv[2]
    template = sys.argv[3] if len(sys.argv) > 3 else "template_cobertura.xlsx"

    with open(entrada, encoding="utf-8") as f:
        dados = json.load(f)

    resumo, total = preencher_multi(dados, template, saida)
    print(f"{saida}: {len(resumo)} massas gravadas (catalogo de {total} coberturas).")
    for linha, marcadas in resumo:
        print(f"  linha {linha}: {len(marcadas)} coberturas")
        for nome, valor in sorted(marcadas.items()):
            print(f"      - {nome}: {valor}")


if __name__ == "__main__":
    main()
