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

from preencher_massa import IGNORAR, LINHA_DADOS, aba_dados, montar_mapa, normalizar


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
    ws = aba_dados(openpyxl.load_workbook(caminho, data_only=True))
    mapa = montar_mapa(ws)
    if "Numero Cotacao" in mapa["campos"]:
        ramo = "proposta"  # template de proposta, comum a todos os produtos
    elif "Tipo de Condomínio" in mapa["combos"]:
        # o Tradicional tem a basica de Incendio; o Amplo nao
        tradicional = any(normalizar(n).startswith("incendio queda de raio")
                          for n in mapa["coberturas"])
        ramo = "condominio_tradicional" if tradicional else "condominio_amplo"
    else:
        ramo = "empresarial" if "Cep Risco" in mapa["campos"] else "residencial"
    # celulas de exemplo do template as vezes vem com espaco duro no fim ("Sólida\xa0")
    limpar = lambda v: v.replace("\xa0", " ").strip() if isinstance(v, str) else v
    colunas = [mapa["campos"], mapa["combos"], mapa["textos"], mapa["bools"], mapa["perguntas"],
               mapa["coberturas"], mapa["periodos"]]
    todas = [c for d in colunas for c in d.values()]
    todas += [c for g in mapa["grupos"].values() for c in g["opcoes"].values()]

    massas = []
    for linha in range(LINHA_DADOS, ws.max_row + 1):
        if all(ws[f"{c}{linha}"].value in (None, "", IGNORAR) for c in todas):
            continue
        cel = lambda col: limpar(ws[f"{col}{linha}"].value)
        massa = {
            "campos": {n: cel(c) for n, c in mapa["campos"].items()},
            "combos": {n: (valor_numero(cel(c)) if c in mapa["colunas_valor"]
                           and cel(c) not in (None, IGNORAR) else cel(c))
                       for n, c in mapa["combos"].items()},
            "bool": [n for n, c in mapa["bools"].items() if marcado(cel(c))],
            # indenizacao a valor de novo: "<IGNORE>" na coluna significa "não"
            "perguntas": {n: ("não" if normalizar(n).startswith("deseja contratar indenizacao")
                              and cel(c) in (None, "", IGNORAR) else cel(c))
                          for n, c in mapa["perguntas"].items()},
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
            vidas = cel(mapa["qt_vidas"][n]) if n in mapa["qt_vidas"] else None
            if vidas not in (None, "", IGNORAR):
                item["qt_vidas"] = valor_numero(vidas)
            p = periodos.get(normalizar(n))
            if p not in (None, "", IGNORAR):
                item["periodo_indenitario"] = valor_numero(p)
            massa["coberturas"].append(item)
        # bloco de proposta: so as colunas preenchidas
        proposta = {n: cel(c) for n, c in mapa["proposta"].items() if cel(c) not in (None, "", IGNORAR)}
        if proposta:
            massa["proposta"] = proposta
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
