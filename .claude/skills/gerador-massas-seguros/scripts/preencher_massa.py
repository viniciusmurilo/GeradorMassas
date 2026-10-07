#!/usr/bin/env python3
"""
Preenche N massas (uma por linha) nos templates novos de Empresarial/Residencial
(aba "Exportation", cabecalho na linha 2, dados a partir da linha 3).

Uso:
    python3 preencher_massa.py entrada.json saida.xlsx [template.xlsx]

Sem o 3o argumento, usa o template embutido na skill:
templates/template_<ramo>.xlsx (ao lado da pasta scripts/).

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
         "grupos": {
           "Deseja contratar indenização a valor de novo?": ["NÃO"],
           "Existem equipamentos de proteção contra incêndio?": ["Extintores"],
           "Existem equipamentos de proteção contra roubo?": ["Sistema de alarme contra roubo"]
         },
         "coberturas": [{"nome": "Danos Elétricos", "valor": 200000}],
         "proposta": {"Contato - Tipo Telefone": "Celular"}   # opcional
       }
     ]}

O script LE o cabecalho (linha 2) do template em tempo de execucao e classifica cada
coluna (campo direto, combo, texto, bool, grupo RDB/CHK, cobertura, periodo indenitario).
Nunca escreve por posicao: tudo e pareado pelo nome exato do cabecalho (comparacao
tolerante a acento/caixa/pontuacao). Chave nao encontrada = erro, nunca "chute".

Os 3-4 questionarios de grupo (indenizacao a valor de novo, protecao contra incendio,
protecao contra roubo/equipamentos de protecao) sao OBRIGATORIOS: tem que aparecer em
"grupos" em toda massa, mesmo que so com a opcao padrao ("NÃO" / "Não informado...").
O modo de cada grupo (escolha unica vs multipla) e a exclusividade da opcao "Não
informado" sao fixados em REGRAS_GRUPO — nao dependem do prefixo RDB/CHK do cabecalho,
que nao e consistente entre os dois ramos.
"""

import json
import os
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

# O prefixo do cabecalho (RDB/CHK) NAO indica de forma confiavel se o grupo e de
# escolha unica ou multipla (confirmado com o dono do produto): o grupo "Equipamentos
# de Protecao" do residencial e RDB no cabecalho mas e multipla escolha na pratica, e
# "protecao contra roubo" do empresarial e CHK mas tem opcao exclusiva. Por isso o modo
# de cada grupo e fixado explicitamente aqui, por nome de grupo, em vez de inferido.
#
# modo="unico": no maximo 1 opcao marcada.
# modo="multiplo": varias opcoes podem ser marcadas juntas.
# nao_informado: se preenchido, essa opcao e exclusiva dentro do grupo — quando
#   selecionada, nenhuma outra opcao do grupo pode vir junto.
# obrigatorio: o grupo tem que aparecer em "grupos" no JSON de entrada (mesmo que so
#   com a opcao padrao/"nao informado") — nunca fica implicitamente de fora.
REGRAS_GRUPO = {
    "Deseja contratar indenização a valor de novo?": {
        "modo": "unico", "obrigatorio": True, "nao_informado": None,
    },
    "Existem equipamentos de proteção contra incêndio?": {
        "modo": "unico", "obrigatorio": True,
        "nao_informado": "Não informado sistema de proteção contra incêndio",
    },
    "Existem equipamentos de proteção contra roubo?": {
        "modo": "multiplo", "obrigatorio": True,
        "nao_informado": "Não informado sistema de proteção contra roubo",
    },
    "Equipamentos de Proteção": {
        "modo": "multiplo", "obrigatorio": True, "nao_informado": "Não informado",
    },
    # condominio: so existe a opcao SIM; sem marcar = nao contrata
    "Deseja contratar indenização a valor de novo? Condominio": {
        "modo": "unico", "obrigatorio": False, "nao_informado": None,
    },
    "Quantidade de Pavimentos (incluindo térreo, garagem e subsolos)?": {
        "modo": "unico", "obrigatorio": True, "nao_informado": "Não informado",
    },
    "Qual a idade do Condomínio?": {
        "modo": "unico", "obrigatorio": True, "nao_informado": None,
    },
}

# perguntas de coluna unica que so se aplicam conforme a resposta de outra
# (pergunta -> (pergunta_mae, resposta_que_habilita)); fora disso a coluna vai <IGNORE>
PERGUNTAS_CONDICIONAIS = {
    "Qual a quantidade de elevadores?": ("O Condomínio possui elevador?", "sim"),
}


# Formato de preenchimento por ramo. Empresarial/residencial: opcao marcada "sim", resto e
# cobertura nao contratada "<IGNORE>", valores em texto BR ("10.000,00"). Condominios (pelas
# linhas de exemplo dos templates do usuario): marcada "Sim", desmarcada e cobertura nao
# contratada "<IGNORE>", valores como numero. "desmarcado_grupo" sobrepoe por grupo.
ESTILOS = {
    "padrao": {"marcado": SIM, "desmarcado": IGNORAR, "vazio": IGNORAR, "valor": "br",
               "desmarcado_grupo": {}},
    "condominio": {"marcado": "Sim", "desmarcado": IGNORAR, "vazio": IGNORAR, "valor": "numero",
                   # indenizacao do condominio (so tem a opcao SIM): nao contratar = "Não"
                   "desmarcado_grupo": {
                       "Deseja contratar indenização a valor de novo? Condominio": "Não"}},
}


def estilo_do_ramo(ramo):
    return ESTILOS["condominio" if str(ramo).startswith("condominio") else "padrao"]


def numero(v):
    """'1.000,00' / 1000 -> 1000 (int quando inteiro)."""
    n = float(formatar_valor_br(v).replace(".", "").replace(",", "."))
    return int(n) if n == int(n) else n


def aba_dados(wb):
    """Aba de dados: 'Exportation' (empresarial/residencial) ou a primeira (condominios)."""
    return wb[ABA] if ABA in wb.sheetnames else wb.worksheets[0]
# grupo novo que aparecer no template sem regra propria: tambem e obrigatorio (todo
# questionario precisa de pelo menos uma resposta).
REGRA_GRUPO_PADRAO = {"modo": "multiplo", "obrigatorio": True, "nao_informado": None}


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


# Colunas do bloco de proposta, iguais em todos os templates e no template_proposta.xlsx.
PREFIXOS_PROPOSTA = ("proponente", "endereco proponente", "contato ", "proposta ")
# Opcoes das listas do bloco de proposta (template_proposta.xlsx, linhas 3 a 5).
OPCOES_PROPOSTA = {
    "Proponente PF - Tipo Documento": ["RG", "RNE"],
    "Contato - Tipo Telefone": ["Celular", "Residencial", "Comercial"],
    "Proposta - Forma Pagamento": ["Carnê", "Débito", "Cartão de Crédito"],
    "Proposta - Quantidade Parcelas": ["1 + 1", "1 + 2", "0 + 1"],
    "Proposta Débito - Proponente Titular": ["Sim", "Não"],
}


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
    m = re.match(r'^TXT\s+"([^"]+)"\s+Valor da Cobertura$', h, re.IGNORECASE)
    if m:
        return {"tipo": "cobertura", "chave": m.group(1)}
    m = re.match(r'^TXT\s+"([^"]+)"\s+Per[ií]odo Indenit[aá]rio$', h)
    if m:
        return {"tipo": "periodo", "chave": m.group(1)}
    # formatos dos templates de condominio: TXT "<A>" <B>
    m = re.match(r'^TXT\s+"\s*([^"]+?)\s*"\s+(.+)$', h)
    if m:
        a, b = m.groups()
        if normalizar(a) == "periodo indenitario":
            return {"tipo": "periodo", "chave": b}
        if normalizar(a) == "valor da cobertura":
            return {"tipo": "cobertura", "chave": b}
        if normalizar(a) == "qt de vidas":
            return {"tipo": "qt_vidas", "chave": b}
        # ex.: TXT "Roubo E/ou Furto Qualificado de Bens Dos Condôminos" Roubo de Valores
        return {"tipo": "cobertura", "chave": a}
    m = re.match(r"^CBO\s+(.*)$", h)
    if m:
        return {"tipo": "combo", "chave": m.group(1)}
    m = re.match(r"^TXT\s+(.*)$", h)
    if m:
        return {"tipo": "texto", "chave": m.group(1)}
    if normalizar(h).startswith(PREFIXOS_PROPOSTA):
        # bloco de proposta (proponente, contato, pagamento, debito): opcional, chave "proposta"
        return {"tipo": "proposta", "chave": h}
    if h.endswith("?"):
        # pergunta de coluna unica (ex.: "Deseja contratar indenização a valor de novo?"),
        # respondida com o texto da resposta ("sim"/"não"...)
        return {"tipo": "pergunta", "chave": h}
    return {"tipo": "direto", "chave": h}


def montar_mapa(ws):
    """Le a linha de cabecalho e devolve estrutura classificada por coluna."""
    campos, combos, textos, bools, perguntas, proposta = {}, {}, {}, {}, {}, {}
    coberturas, periodos, qt_vidas = {}, {}, {}
    duplicadas = []  # (coluna_principal, coluna_repetida): mesmo cabecalho em 2 colunas
    grupos = {}  # grupo_nome -> {"opcoes": {opcao: col_letter}} (modo/obrigatoriedade: ver REGRAS_GRUPO)

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
        elif tipo == "pergunta":
            perguntas[info["chave"]] = col
        elif tipo == "proposta":
            proposta[info["chave"]] = col
        elif tipo == "bool":
            bools[info["chave"]] = col
        elif tipo in ("cobertura", "periodo", "qt_vidas"):
            destino = {"cobertura": coberturas, "periodo": periodos, "qt_vidas": qt_vidas}[tipo]
            if info["chave"] in destino:
                duplicadas.append((destino[info["chave"]], col))
            else:
                destino[info["chave"]] = col
        elif tipo == "grupo":
            g = grupos.setdefault(info["grupo"], {"opcoes": {}})
            g["opcoes"][info["opcao"]] = col

    # campos de texto que sao valor em R$ (Valor em Risco, Lucros Cessantes...): tudo que
    # nao e a Atividade. Gravados como texto BR, igual as coberturas.
    colunas_valor = {col for nome, col in textos.items() if normalizar(nome) != "atividade"}
    colunas_valor |= set(coberturas.values())
    colunas_valor |= {col for nome, col in combos.items()
                      if normalizar(nome).startswith("valor em risco")}
    colunas_valor |= {d for p, d in duplicadas if p in colunas_valor}

    return {
        "campos": campos, "combos": combos, "textos": textos, "bools": bools,
        "perguntas": perguntas, "proposta": proposta,
        "coberturas": coberturas, "periodos": periodos, "grupos": grupos,
        "qt_vidas": qt_vidas, "duplicadas": duplicadas,
        "colunas_valor": colunas_valor,
    }


def _indice(nomes):
    return {normalizar(n): n for n in nomes}


def preencher_linha(ws, linha, massa, mapa, estilo=ESTILOS["padrao"]):
    MARCADO, DESMARCADO, VAZIO = estilo["marcado"], estilo["desmarcado"], estilo["vazio"]
    fmt_valor = formatar_valor_br if estilo["valor"] == "br" else numero
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
        if col in mapa["colunas_valor"] and valor != IGNORAR:
            # mesmo formato das coberturas (texto BR "10.000.000,00" ou numero, conforme o ramo)
            valor = fmt_valor(valor)
        ws[f"{col}{linha}"] = valor

    # --- bloco de proposta: opcional; coluna sem valor fica <IGNORE> ---
    proposta = massa.get("proposta") or {}
    idx_prop = _indice(mapa["proposta"])
    dados_prop = {}
    for nome, valor in proposta.items():
        canon = idx_prop.get(normalizar(nome))
        if canon is None:
            raise ValueError(f"linha {linha}: coluna de proposta inexistente no template: {nome!r}")
        dados_prop[canon] = valor
    for nome, col in mapa["proposta"].items():
        valor = dados_prop.get(nome)
        ws[f"{col}{linha}"] = IGNORAR if valor in (None, "") else valor

    # --- bool independentes ---
    marcados_bool = set(massa.get("bool", []))
    invalidos = marcados_bool - set(mapa["bools"])
    if invalidos:
        raise ValueError(f"linha {linha}: campo bool inexistente: {sorted(invalidos)}")
    for nome, col in mapa["bools"].items():
        ws[f"{col}{linha}"] = MARCADO if nome in marcados_bool else DESMARCADO

    # --- perguntas de coluna unica: obrigatorias, com resposta ---
    perguntas = dict(massa.get("perguntas", {}))
    grupos_pedidos = dict(massa.get("grupos", {}))
    for nome in mapa["perguntas"]:
        # compatibilidade: indenizacao a valor de novo ja foi grupo RDB SIM/NAO
        if nome not in perguntas and nome in grupos_pedidos:
            opcoes = grupos_pedidos.pop(nome)
            perguntas[nome] = opcoes[0] if len(opcoes) == 1 else ""
    for nome, col in mapa["perguntas"].items():
        resp = perguntas.get(nome)
        if normalizar(nome).startswith("deseja contratar indenizacao"):
            # coluna unica: "sim" = contrata; "<IGNORE>" = NAO contrata
            chave = normalizar(resp) if resp not in (None, "", IGNORAR) else "nao"
            if chave not in ("sim", "nao"):
                raise ValueError(f"linha {linha}: '{nome}' aceita só sim/não, recebeu {resp!r}")
            resp = "sim" if chave == "sim" else IGNORAR
        elif nome in PERGUNTAS_CONDICIONAIS and normalizar(
                perguntas.get(PERGUNTAS_CONDICIONAIS[nome][0], "")) != PERGUNTAS_CONDICIONAIS[nome][1]:
            resp = VAZIO  # nao se aplica (ex.: sem elevador -> sem quantidade)
        elif resp in (None, "", IGNORAR):
            raise ValueError(f"linha {linha}: pergunta '{nome}' sem resposta")
        ws[f"{col}{linha}"] = resp
    sobrando = set(perguntas) - set(mapa["perguntas"])
    if sobrando:
        raise ValueError(f"linha {linha}: pergunta inexistente no template: {sorted(sobrando)}")

    # --- grupos RDB/CHK (modo/obrigatoriedade fixados em REGRAS_GRUPO, nao no cabecalho) ---
    invalidos = set(grupos_pedidos) - set(mapa["grupos"])
    if invalidos:
        raise ValueError(f"linha {linha}: grupo inexistente: {sorted(invalidos)}")
    obrigatorios_ausentes = [
        nome for nome in mapa["grupos"]
        if REGRAS_GRUPO.get(nome, REGRA_GRUPO_PADRAO)["obrigatorio"] and nome not in grupos_pedidos
    ]
    if obrigatorios_ausentes:
        raise ValueError(
            f"linha {linha}: questionario obrigatorio nao respondido: {sorted(obrigatorios_ausentes)}"
        )
    for grupo_nome, ginfo in mapa["grupos"].items():
        regra = REGRAS_GRUPO.get(grupo_nome, REGRA_GRUPO_PADRAO)
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
        if regra["obrigatorio"] and not canon_selecionadas:
            raise ValueError(
                f"linha {linha}: questionario '{grupo_nome}' sem resposta — marque pelo menos "
                f"uma opcao (opcoes validas: {sorted(ginfo['opcoes'])})"
            )
        if regra["modo"] == "unico" and len(canon_selecionadas) > 1:
            raise ValueError(
                f"linha {linha}: grupo '{grupo_nome}' e de escolha unica, "
                f"recebeu {canon_selecionadas}"
            )
        if (
            regra["nao_informado"] and regra["nao_informado"] in canon_selecionadas
            and len(canon_selecionadas) > 1
        ):
            raise ValueError(
                f"linha {linha}: grupo '{grupo_nome}': '{regra['nao_informado']}' e exclusiva, "
                f"nao pode vir com outras opcoes ({canon_selecionadas})"
            )
        marcadas = set(canon_selecionadas)
        desmarcado = estilo["desmarcado_grupo"].get(grupo_nome, DESMARCADO)
        for opcao, col in ginfo["opcoes"].items():
            ws[f"{col}{linha}"] = MARCADO if opcao in marcadas else desmarcado

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
        solicitadas[canon] = fmt_valor(item["valor"])
        if item.get("periodo_indenitario") is not None:
            canon_per = idx_per.get(normalizar(item["nome"]))
            if canon_per is None:
                raise ValueError(
                    f"linha {linha}: cobertura {canon!r} nao tem coluna de periodo indenitario"
                )
            periodos_dados[canon_per] = item["periodo_indenitario"]

    for nome, col in mapa["coberturas"].items():
        ws[f"{col}{linha}"] = solicitadas.get(nome, VAZIO)
    for nome, col in mapa["periodos"].items():
        ws[f"{col}{linha}"] = periodos_dados.get(nome, VAZIO)

    # quantidade de vidas (plano de vida dos condominios), junto da cobertura
    vidas = {}
    for item in massa.get("coberturas", []):
        if item.get("qt_vidas") is not None:
            canon = _indice(mapa["qt_vidas"]).get(normalizar(item["nome"]))
            if canon is None:
                raise ValueError(f"linha {linha}: cobertura {item['nome']!r} nao tem coluna de Qt de vidas")
            vidas[canon] = item["qt_vidas"]
    for nome, col in mapa["qt_vidas"].items():
        ws[f"{col}{linha}"] = vidas.get(nome, VAZIO)

    # cabecalho repetido no template (ex.: bloco de plano de vida em dobro): mesma resposta
    for principal, repetida in mapa["duplicadas"]:
        ws[f"{repetida}{linha}"] = ws[f"{principal}{linha}"].value

    return solicitadas


def preencher(dados, caminho_template, caminho_saida):
    wb = openpyxl.load_workbook(caminho_template)
    ws = aba_dados(wb)
    mapa = montar_mapa(ws)
    estilo = estilo_do_ramo(dados.get("ramo"))

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
        solicitadas = preencher_linha(ws, linha, massa, mapa, estilo)
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
            if get_column_letter(c) in mapa["colunas_valor"] and estilo["valor"] == "br":
                cel.number_format = "@"

    # O template original tem linhas de exemplo ja preenchidas (referencia de formato)
    # que podem ir alem do numero de massas pedidas agora. Sem isso, a copia de saida
    # ficaria com "massas fantasma" do exemplo original misturadas com as geradas.
    primeira_linha_sobrando = LINHA_DADOS + len(resumo)
    for linha in range(primeira_linha_sobrando, ws.max_row + 1):
        for c in range(1, max_col + 1):
            ws.cell(row=linha, column=c).value = None

    wb.save(caminho_saida)
    return resumo


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    entrada, saida = sys.argv[1], sys.argv[2]

    with open(entrada, encoding="utf-8") as f:
        dados = json.load(f)

    if len(sys.argv) >= 4:
        template = sys.argv[3]
    else:
        pasta_skill = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        template = os.path.join(pasta_skill, "templates", f"template_{dados.get('ramo')}.xlsx")
    if not os.path.isfile(template):
        sys.exit(f"ERRO: template nao encontrado: {template}")

    resumo = preencher(dados, template, saida)
    print(f"{saida}: {len(resumo)} massas gravadas.")
    for linha, marcadas in resumo:
        print(f"  linha {linha}: {len(marcadas)} coberturas -> {sorted(marcadas)}")


if __name__ == "__main__":
    main()
