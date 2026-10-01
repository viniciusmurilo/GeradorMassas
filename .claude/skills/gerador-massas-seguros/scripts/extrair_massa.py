#!/usr/bin/env python3
"""
Le uma planilha de massa ja preenchida (aba "Exportation", cabecalho na linha 2, dados a partir
da linha 3) e devolve o JSON de entrada do preencher_massa.py, uma massa por linha.

Uso:
    python3 extrair_massa.py planilha.xlsx saida.json

O ramo e detectado pelo cabecalho ("Cep Risco" -> empresarial, "Tipo de Residência" ->
residencial). Valores em formato BR ("1.000,00") viram numero; "<IGNORE>" fica de fora
(coberturas, periodos, grupos e bools) ou e mantido como "<IGNORE>" (campos de texto).
"""

import json
import re
import sys

import openpyxl

from preencher_massa import ABA, IGNORAR, LINHA_DADOS, montar_mapa, normalizar


def valor_numero(v):
    if isinstance(v, (int, float)):
        return v
    s = str(v).strip()
    if re.fullmatch(r"[\d.]+,\d{1,2}|\d+(\.\d+)?", s):
        n = float(s.replace(".", "").replace(",", ".")) if "," in s else float(s)
        return int(n) if n == int(n) else n
    return s


def marcado(v):
    return v is not None and normalizar(v) in ("sim", "s", "x", "true", "1")


def extrair(caminho):
    ws = openpyxl.load_workbook(caminho, data_only=True)[ABA]
    mapa = montar_mapa(ws)
    ramo = "empresarial" if "Cep Risco" in mapa["campos"] else "residencial"
    colunas = [mapa["campos"], mapa["combos"], mapa["textos"], mapa["bools"],
               mapa["coberturas"], mapa["periodos"]]
    todas = [c for d in colunas for c in d.values()]
    todas += [c for g in mapa["grupos"].values() for c in g["opcoes"].values()]

    massas = []
    for linha in range(LINHA_DADOS, ws.max_row + 1):
        if all(ws[f"{c}{linha}"].value in (None, "", IGNORAR) for c in todas):
            continue
        cel = lambda col: ws[f"{col}{linha}"].value
        massa = {
            "campos": {n: cel(c) for n, c in mapa["campos"].items()},
            "combos": {n: cel(c) for n, c in mapa["combos"].items()},
            "bool": [n for n, c in mapa["bools"].items() if marcado(cel(c))],
            "grupos": {g: [o for o, c in info["opcoes"].items() if marcado(cel(c))]
                       for g, info in mapa["grupos"].items()},
            "coberturas": [],
        }
        if mapa["textos"]:
            massa["texto"] = {}
            for n, c in mapa["textos"].items():
                v = cel(c)
                massa["texto"][n] = v if c not in mapa["colunas_valor"] or v in (None, IGNORAR) \
                    else valor_numero(v)
        periodos = {normalizar(n): cel(c) for n, c in mapa["periodos"].items()}
        for n, c in mapa["coberturas"].items():
            v = cel(c)
            if v in (None, "", IGNORAR):
                continue
            item = {"nome": n, "valor": valor_numero(v)}
            p = periodos.get(normalizar(n))
            if p not in (None, "", IGNORAR):
                item["periodo_indenitario"] = valor_numero(p)
            massa["coberturas"].append(item)
        # residencial nao tem bools fora do catalogo; empresarial nunca usa o CHK orfao
        if ramo == "empresarial":
            massa["bool"] = []
        massas.append(massa)
    return {"ramo": ramo, "massas": massas}


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    dados = extrair(sys.argv[1])
    json.dump(dados, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{sys.argv[2]}: {dados['ramo']}, {len(dados['massas'])} massas extraídas.")


if __name__ == "__main__":
    main()
