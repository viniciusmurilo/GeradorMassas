#!/usr/bin/env python3
"""
Preenche N massas (uma por linha) nos templates novos de Empresarial/Residencial
(aba "Exportation", cabecalho na linha 2, dados a partir da linha 3).

Uso:
    python3 preencher_massa.py entrada.json saida.xlsx template.xlsx

Formato do JSON de entrada:
    {"ramo": "empresarial" | "residencial",
     "massas": [
       {
         "campos": {"Corretor": "COI", "Tipo Pessoa": "#cpf", "Cep Risco": "#cep"},
         "combos": {"Tipo de Construção": "Superior", "Objeto Segurado": "Prédio",
                    "Assistência 24h": "Assistência Empresarial Plano Superior"},
         "texto": {"Atividade": "Academias", "Valor em Risco - Danos Materiais": 10000000,
                   "Lucros Cessantes": 10000},
         "bool": ["Benefícios Bike"],
         "grupos": {"Existem equipamentos de proteção contra incêndio?": ["Extintores"]},
         "coberturas": [{"nome": "Danos Elétricos", "valor": 200000}]
       }
     ]}

O script LE o cabecalho (linha 2) do template em tempo de execucao e classifica cada
coluna (campo direto, combo, texto, bool, grupo RDB/CHK, cobertura, periodo indenitario).
Nunca escreve por posicao: tudo e pareado pelo nome exato do cabecalho (comparacao
tolerante a acento/caixa/pontuacao). Chave nao encontrada = erro, nunca "chute".
"""

import json
import re
import sys
import unicodedata
from copy import copy

import openpyxl
from openpyxl.utils import get_column_letter

ABA = "Exportation"
LINHA_CABECALHO = 2
LINHA_DADOS = 3
SIM = "sim"
IGNORAR = "<IGNORE>"

# Pares SIM/NAO tratados como grupo de escolha unica mesmo quando o prefixo do
# cabecalho e "CHK" (o template nao e consistente entre os dois ramos aqui).
OPCOES_UNICO_FORCADO = {"SIM", "NÃO", "NAO"}


def normalizar(texto):
    t = unicodedata.normalize("NFKD", str(texto))
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r"[^a-zA-Z0-9]+", " ", t)
    return " ".join(t.lower().split())


def formatar_valor_br(v):
    """Numero (ou string tolerante) -> string BR com milhar/decimal: 200000 -> '200.000,00'."""
    if isinstance(v, (int, float)):
        num = float(v)
    else:
        s = str(v).strip()
        s = re.sub(r"(?i)^r\$\s*", "", s)
        s = re.sub(r"[^\d,.]", "", s)
        if "," in s:
            s = s.replace(".", "").replace(",", ".")
        elif s.count(".") == 1 and len(s.split(".")[1]) in (1, 2):
            pass
        else:
            s = s.replace(".", "")
        if not s:
            raise ValueError("valor vazio ou nao numerico")
        num = float(s)
    texto = f"{num:,.2f}"
    return texto.translate(str.maketrans({",": "", ".": ","})).replace("", ".")


def classificar(header):
    h = str(header).strip()
    m = re.match(r'^(RDB|CHK)\s+"([^"]+)"\s+(.*)$', h)
    if m:
        prefixo, opcao, resto = m.groups()
        if resto.endswith("Valor da Cobertura"):
            return {"tipo": "cobertura", "chave": opcao}
        return {"tipo": "grupo", "prefixo": prefixo, "grupo": resto, "opcao": opcao}
    m = re.match(r"^(RDB|CHK)\s+([A-ZÀ-Ú][A-ZÀ-Ú]*)\s+(.*)$", h)
    if m:
        prefixo, opcao, resto = m.groups()
        return {"tipo": "grupo", "prefixo": prefixo, "grupo": resto, "opcao": opcao}
    m = re.match(r"^CHK\s+(.*)$", h)
    if m:
        return {"tipo": "bool", "chave": m.group(1)}
    m = re.match(r'^TXT\s+"([^"]+)"\s+Valor da Cobertura$', h)
    if m:
        return {"tipo": "cobertura", "chave": m.group(1)}
    m = re.match(r'^TXT\s+"([^"]+)"\s+Per[ií]odo Indenit[aá]rio$', h)
    if m:
        return {"tipo": "periodo", "chave": m.group(1)}
    m = re.match(r"^CBO\s+(.*)$", h)
    if m:
        return {"tipo": "combo", "chave": m.group(1)}
    m = re.match(r"^TXT\s+(.*)$", h)
    if m:
        return {"tipo": "texto", "chave": m.group(1)}
    return {"tipo": "direto", "chave": h}


def montar_mapa(ws):
    """Le a linha de cabecalho e devolve estrutura classificada por coluna."""
    campos, combos, textos, bools = {}, {}, {}, {}
    coberturas, periodos = {}, {}
    grupos = {}  # grupo_nome -> {"prefixo":..., "opcoes": {opcao: col_letter}}

    for c in range(1, ws.max_column + 1):
        header = ws.cell(row=LINHA_CABECALHO, column=c).value
        if header in (None, ""):
            continue
        col = get_column_letter(c)
        info = classificar(header)
        tipo = info["tipo"]
        if tipo == "direto":
            campos[info["chave"]] = col
        elif tipo == "combo":
            combos[info["chave"]] = col
        elif tipo == "texto":
            textos[info["chave"]] = col
        elif tipo == "bool":
            bools[info["chave"]] = col
        elif tipo == "cobertura":
            coberturas[info["chave"]] = col
        elif tipo == "periodo":
            periodos[info["chave"]] = col
        elif tipo == "grupo":
            g = grupos.setdefault(info["grupo"], {"prefixo": info["prefixo"], "opcoes": {}})
            g["opcoes"][info["opcao"]] = col
            # se o grupo tiver SIM/NAO, forca escolha unica independente do prefixo do cabecalho
            if set(g["opcoes"]) & OPCOES_UNICO_FORCADO:
                g["prefixo"] = "RDB"

    return {
        "campos": campos, "combos": combos, "textos": textos, "bools": bools,
        "coberturas": coberturas, "periodos": periodos, "grupos": grupos,
    }


def _indice(nomes):
    return {normalizar(n): n for n in nomes}


def preencher_linha(ws, linha, massa, mapa):
    # --- campos diretos + combos + texto: obrigatorios, sem default ---
    diretos = {}
    diretos.update(massa.get("campos", {}))
    diretos.update(massa.get("combos", {}))
    diretos.update(massa.get("texto", {}))

    esperados = set(mapa["campos"]) | set(mapa["combos"]) | set(mapa["textos"])
    faltando = esperados - set(diretos)
    if faltando:
        raise ValueError(f"linha {linha}: campos obrigatorios ausentes: {sorted(faltando)}")
    sobrando = set(diretos) - esperados
    if sobrando:
        raise ValueError(f"linha {linha}: campos inexistentes no template: {sorted(sobrando)}")

    for nome, valor in diretos.items():
        col = mapa["campos"].get(nome) or mapa["combos"].get(nome) or mapa["textos"].get(nome)
        if nome in mapa["textos"] and isinstance(valor, (int, float)):
            ws[f"{col}{linha}"] = valor
        else:
            ws[f"{col}{linha}"] = valor

    # --- bool independentes ---
    marcados_bool = set(massa.get("bool", []))
    invalidos = marcados_bool - set(mapa["bools"])
    if invalidos:
        raise ValueError(f"linha {linha}: campo bool inexistente: {sorted(invalidos)}")
    for nome, col in mapa["bools"].items():
        ws[f"{col}{linha}"] = SIM if nome in marcados_bool else IGNORAR

    # --- grupos RDB/CHK ---
    grupos_pedidos = massa.get("grupos", {})
    invalidos = set(grupos_pedidos) - set(mapa["grupos"])
    if invalidos:
        raise ValueError(f"linha {linha}: grupo inexistente: {sorted(invalidos)}")
    for grupo_nome, ginfo in mapa["grupos"].items():
        selecionadas = grupos_pedidos.get(grupo_nome, [])
        idx_opcoes = _indice(ginfo["opcoes"])
        canon_selecionadas = []
        for opc in selecionadas:
            canon = idx_opcoes.get(normalizar(opc))
            if canon is None:
                raise ValueError(
                    f"linha {linha}: opcao '{opc}' nao existe no grupo '{grupo_nome}' "
                    f"(opcoes validas: {sorted(ginfo['opcoes'])})"
                )
            canon_selecionadas.append(canon)
        if ginfo["prefixo"] == "RDB" and len(canon_selecionadas) > 1:
            raise ValueError(
                f"linha {linha}: grupo '{grupo_nome}' e de escolha unica, "
                f"recebeu {canon_selecionadas}"
            )
        marcadas = set(canon_selecionadas)
        for opcao, col in ginfo["opcoes"].items():
            ws[f"{col}{linha}"] = SIM if opcao in marcadas else IGNORAR

    # --- coberturas + periodo indenitario ---
    idx_cob = _indice(mapa["coberturas"])
    idx_per = _indice(mapa["periodos"])
    solicitadas = {}
    periodos_dados = {}
    for item in massa.get("coberturas", []):
        canon = idx_cob.get(normalizar(item["nome"]))
        if canon is None:
            raise ValueError(f"linha {linha}: cobertura nao existe no template: {item['nome']!r}")
        if canon in solicitadas:
            raise ValueError(f"linha {linha}: cobertura duplicada: {canon!r}")
        solicitadas[canon] = formatar_valor_br(item["valor"])
        if item.get("periodo_indenitario") is not None:
            canon_per = idx_per.get(normalizar(item["nome"]))
            if canon_per is None:
                raise ValueError(
                    f"linha {linha}: cobertura {canon!r} nao tem coluna de periodo indenitario"
                )
            periodos_dados[canon_per] = item["periodo_indenitario"]

    for nome, col in mapa["coberturas"].items():
        ws[f"{col}{linha}"] = solicitadas.get(nome, IGNORAR)
    for nome, col in mapa["periodos"].items():
        ws[f"{col}{linha}"] = periodos_dados.get(nome, IGNORAR)

    return solicitadas


def preencher(dados, caminho_template, caminho_saida):
    wb = openpyxl.load_workbook(caminho_template)
    ws = wb[ABA]
    mapa = montar_mapa(ws)

    # captura o estilo da primeira linha de dados original (ja formatada) p/ replicar
    estilos = {}
    for c in range(1, ws.max_column + 1):
        cel = ws.cell(row=LINHA_DADOS, column=c)
        estilos[c] = {
            "font": copy(cel.font), "alignment": copy(cel.alignment),
            "border": copy(cel.border), "fill": copy(cel.fill),
            "number_format": cel.number_format,
        }

    resumo = []
    for i, massa in enumerate(dados.get("massas", [])):
        linha = LINHA_DADOS + i
        solicitadas = preencher_linha(ws, linha, massa, mapa)
        resumo.append((linha, solicitadas))

    max_col = ws.max_column
    for i in range(len(resumo)):
        linha = LINHA_DADOS + i
        for c in range(1, max_col + 1):
            cel = ws.cell(row=linha, column=c)
            est = estilos[c]
            cel.font = est["font"]
            cel.alignment = est["alignment"]
            cel.border = est["border"]
            cel.fill = est["fill"]
            cel.number_format = est["number_format"]

    wb.save(caminho_saida)
    return resumo


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)
    entrada, saida, template = sys.argv[1], sys.argv[2], sys.argv[3]

    with open(entrada, encoding="utf-8") as f:
        dados = json.load(f)

    resumo = preencher(dados, template, saida)
    print(f"{saida}: {len(resumo)} massas gravadas.")
    for linha, marcadas in resumo:
        print(f"  linha {linha}: {len(marcadas)} coberturas -> {sorted(marcadas)}")


if __name__ == "__main__":
    main()
