#!/usr/bin/env python3
"""
Valida (e opcionalmente corrige) massas no formato JSON de entrada do preencher_massa.py,
usando as regras de references/regras_<ramo>.json.

Uso:
    python3 validar_massa.py entrada.json                    # so relatorio
    python3 validar_massa.py entrada.json --corrigir saida.json

Relatorio: uma linha por problema, "ERRO" (o sistema rejeita) ou "AVISO" (passa, mas cai em
analise tecnica / inspecao / ponto a confirmar). Sai com codigo 1 se houver ERRO.

--corrigir aplica so correcoes mecanicas e seguras e registra cada uma no relatorio:
  - remove coberturas sem aceitacao comercial, e as indisponiveis para o tipo de residencia;
  - remove a cobertura que exige outra ausente, e a segunda de um par excludente;
  - VR Lucros Cessantes: com VR e sem LC/DF basica, adiciona LC-Incendio; sem VR e com
    LC/DF, preenche o VR com o maior LMI delas;
  - ajusta valores para dentro de [minimo, teto efetivo] (teto = menor entre maximo do corretor,
    % da basica e % da cobertura exigida); se o teto ficar abaixo do minimo, remove a cobertura;
  - tipo de construcao sem aceitacao -> Superior (ou Solida se a atividade exigir);
    objeto segurado restrito -> Predio; questionario vazio -> opcao padrao.
O que nao da para decidir sozinho (ex.: soma de RC acima do limite) fica como ERRO no relatorio.
"""

import json
import os
import sys
import unicodedata
from copy import deepcopy

AQUI = os.path.dirname(os.path.abspath(__file__))
REFS = os.path.join(AQUI, "..", "references")
IGNORAR = "<IGNORE>"

PADRAO_GRUPO = {
    "Deseja contratar indenização a valor de novo?": "NÃO",
    "Existem equipamentos de proteção contra incêndio?": "Não informado sistema de proteção contra incêndio",
    "Existem equipamentos de proteção contra roubo?": "Não informado sistema de proteção contra roubo",
    "Equipamentos de Proteção": "Não informado",
}
GRUPOS_RAMO = {
    "empresarial": [
        "Existem equipamentos de proteção contra incêndio?",
        "Existem equipamentos de proteção contra roubo?",
    ],
    "residencial": ["Equipamentos de Proteção"],
}
# perguntas de coluna unica (chave "perguntas" no JSON) e resposta padrao
PERGUNTAS_RAMO = {
    "empresarial": {"Deseja contratar indenização a valor de novo?": "não"},
    "residencial": {"Deseja contratar indenização a valor de novo?": "não"},
}


def norm(s):
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(s.lower().split())


def num(v):
    """Numero de JSON ou string BR ('1.000,00') -> float. None para vazio/<IGNORE>."""
    if v is None or v == "" or v == IGNORAR:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace("R$", "").strip()
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    return float(s)


def brl(v):
    return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


class Massa:
    """Visao sobre um item de 'massas' com coberturas indexadas pelo nome canonico das regras."""

    def __init__(self, dados, regras):
        self.d = dados
        self.r = regras
        self.idx = {norm(n): n for n in regras["coberturas"]}
        self.cob = {}  # nome canonico -> item original
        self.desconhecidas = []
        for item in dados.get("coberturas", []):
            canon = self.idx.get(norm(item["nome"]))
            if canon is None:
                self.desconhecidas.append(item["nome"])
            else:
                self.cob[canon] = item

    def v(self, nome):
        item = self.cob.get(nome)
        return num(item["valor"]) if item else None

    def tem(self, nome):
        return nome in self.cob and (self.v(nome) or 0) > 0

    def remover(self, nome):
        item = self.cob.pop(nome, None)
        if item is not None:
            self.d["coberturas"].remove(item)

    def definir(self, nome, valor):
        if nome in self.cob:
            self.cob[nome]["valor"] = valor
        else:
            item = {"nome": nome, "valor": valor}
            self.d.setdefault("coberturas", []).append(item)
            self.cob[nome] = item


def teto_efetivo(m, nome, regra, max_corretor, basica_v):
    """Menor entre maximo do corretor, % da basica e % da(s) cobertura(s) exigida(s) presentes."""
    tetos = []
    if max_corretor is not None:
        tetos.append((float(max_corretor), f"máximo do corretor {brl(max_corretor)}"))
    pct = regra.get("pct_basica")
    if pct and nome != m.r["basica"] and basica_v:
        tetos.append((basica_v * pct / 100, f"{pct:g}% da básica"))
    pct_ex = regra.get("pct_max_da_exigida")
    if pct_ex and regra.get("exige_uma_de"):
        presentes = [(m.v(e), e) for e in regra["exige_uma_de"] if m.tem(e)]
        for val, e in presentes:
            tetos.append((val * pct_ex / 100, f"{pct_ex:g}% de {e}"))
    if not tetos:
        return None, None
    return min(tetos, key=lambda t: t[0])


def validar(dados_massa, regras, corrigir=False):
    """Devolve lista de (nivel, mensagem). Com corrigir=True altera dados_massa no lugar."""
    ramo = regras["ramo"]
    m = Massa(dados_massa, regras)
    out = []

    def erro(msg):
        out.append(("ERRO", msg))

    def aviso(msg):
        out.append(("AVISO", msg))

    def fix(msg):
        out.append(("CORRIGIDO", msg))

    for n in m.desconhecidas:
        erro(f"cobertura '{n}' não existe nas regras/template do {ramo}")

    combos = dados_massa.get("combos", {})
    texto = dados_massa.get("texto", {})
    tipo_res = combos.get("Tipo de Residência")

    # --- perfil ---
    campos = dados_massa.setdefault("campos", {})
    if not campos.get("Perfil"):
        if corrigir:
            campos["Perfil"] = "Corretor"
            fix("Perfil vazio → 'Corretor'")
        else:
            erro("campo 'Perfil' vazio (ex.: 'Corretor')")

    # --- perguntas de coluna unica (aceita o formato antigo em "grupos") ---
    perguntas = dados_massa.setdefault("perguntas", {})
    grupos_antigos = dados_massa.get("grupos", {})
    for g, padrao in PERGUNTAS_RAMO[ramo].items():
        if not perguntas.get(g) and grupos_antigos.get(g):
            perguntas[g] = grupos_antigos.pop(g)[0].lower().replace("nao", "não")
        if not perguntas.get(g) or perguntas[g] == IGNORAR:
            if corrigir:
                perguntas[g] = padrao
                fix(f"pergunta '{g}' sem resposta → '{padrao}'")
            else:
                erro(f"pergunta '{g}' sem resposta")

    # --- questionarios ---
    grupos = dados_massa.setdefault("grupos", {})
    for g in GRUPOS_RAMO[ramo]:
        if not grupos.get(g):
            if corrigir:
                grupos[g] = [PADRAO_GRUPO[g]]
                fix(f"questionário '{g}' sem resposta → '{PADRAO_GRUPO[g]}'")
            else:
                erro(f"questionário '{g}' sem resposta")

    # --- caracteristicas de risco (empresarial) ---
    if ramo == "empresarial":
        ativ = texto.get("Atividade")
        constr = combos.get("Tipo de Construção")
        so_solida = ativ in regras["atividades_so_solida"]
        if constr in regras["tipo_construcao_sem_aceitacao"] or (so_solida and constr != "Sólida"):
            novo = "Sólida" if so_solida else "Superior"
            if corrigir:
                combos["Tipo de Construção"] = novo
                fix(f"tipo de construção '{constr}' → '{novo}'")
            else:
                erro(f"tipo de construção '{constr}' não aceito"
                     + (f" (atividade '{ativ}' só aceita Sólida)" if so_solida else ""))
        if ativ in regras["atividades_so_predio"] and combos.get("Objeto Segurado") != "Prédio":
            if corrigir:
                combos["Objeto Segurado"] = "Prédio"
                fix(f"objeto segurado → 'Prédio' (atividade '{ativ}')")
            else:
                erro(f"atividade '{ativ}' só aceita Objeto Segurado = Prédio")
        vr = num(texto.get("Valor em Risco - Danos Materiais"))
        lim = regras["valor_em_risco"]
        if vr is not None and not (lim["min"] <= vr <= lim["max"]):
            erro(f"Valor em Risco {brl(vr)} fora de {brl(lim['min'])} a {brl(lim['max'])}")

    if ramo == "residencial" and tipo_res in regras["objeto_so_predio"] \
            and combos.get("Objeto Segurado") != "Prédio":
        if corrigir:
            combos["Objeto Segurado"] = "Prédio"
            fix(f"objeto segurado → 'Prédio' ({tipo_res})")
        else:
            erro(f"{tipo_res} exige Objeto Segurado = Prédio")

    max_por_tipo = regras.get("max_corretor_por_tipo", {}).get(tipo_res, {}) if tipo_res else {}

    def max_corretor(nome):
        return max_por_tipo.get(nome, regras["coberturas"][nome]["max"])

    # --- sem aceitacao / indisponivel para o tipo ---
    ja_reportadas = set()
    for nome in list(m.cob):
        regra = regras["coberturas"][nome]
        if regra.get("sem_aceitacao") or max_corretor(nome) == 0:
            motivo = "sem aceitação comercial" if regra.get("sem_aceitacao") \
                else f"indisponível para {tipo_res}"
            if corrigir:
                m.remover(nome)
                fix(f"removida '{nome}' ({motivo})")
            else:
                erro(f"'{nome}' {motivo}")
                ja_reportadas.add(nome)

    # --- basica ---
    basica = regras["basica"]
    if not m.tem(basica):
        erro(f"falta a cobertura básica '{basica}' (base dos percentuais)")

    # --- excludentes (mantem a primeira que aparece na massa) ---
    pares = set()
    for nome in list(m.cob):
        if nome not in m.cob:
            continue
        for outra in regras["coberturas"][nome].get("exclui", []):
            if outra in m.cob and frozenset((nome, outra)) not in pares:
                pares.add(frozenset((nome, outra)))
                if corrigir:
                    m.remover(outra)
                    fix(f"removida '{outra}' (excludente com '{nome}')")
                else:
                    erro(f"'{nome}' e '{outra}' são excludentes")
    for a, b in regras.get("avisos_par_excludente", []):
        if a in m.cob and b in m.cob:
            aviso(f"'{a}' com '{b}': a fonte indica exclusão (ponto a confirmar)")

    # --- VR Lucros Cessantes (empresarial, nos dois sentidos) ---
    if ramo == "empresarial":
        vr_lc = num(texto.get("Lucros Cessantes"))
        basicas_lc = regras["lucros_cessantes_basicas"]
        limitadas = regras["limitadas_pelo_vr_lucros_cessantes"]
        if vr_lc:
            if not any(m.tem(b) for b in basicas_lc):
                if corrigir:
                    valor = min(vr_lc, m.v(basica) or vr_lc)
                    m.definir(basicas_lc[0], valor)
                    fix(f"VR Lucros Cessantes sem LC/DF básica → adicionada '{basicas_lc[0]}' "
                        f"com {brl(valor)}")
                else:
                    erro("VR Lucros Cessantes preenchido exige 'Lucros Cessantes - Incêndio' "
                         "ou 'Despesas Fixas - Incêndio'")
        else:
            presentes = [n for n in regras["proibidas_sem_vr_lucros_cessantes"] if m.tem(n)]
            if presentes:
                maiores = [m.v(n) for n in limitadas if m.tem(n)]
                if corrigir and maiores:
                    texto["Lucros Cessantes"] = max(maiores)
                    vr_lc = max(maiores)
                    fix(f"VR Lucros Cessantes vazio com {presentes} → VR = {brl(vr_lc)}")
                elif corrigir:
                    for n in presentes:
                        m.remover(n)
                        fix(f"removida '{n}' (sem VR Lucros Cessantes)")
                else:
                    erro(f"sem VR Lucros Cessantes não pode ter {presentes}")
        if vr_lc:
            for n in limitadas:
                if m.tem(n) and m.v(n) > vr_lc:
                    if corrigir:
                        m.definir(n, vr_lc)
                        fix(f"'{n}' reduzida para o VR Lucros Cessantes {brl(vr_lc)}")
                    else:
                        erro(f"'{n}' {brl(m.v(n))} maior que o VR Lucros Cessantes {brl(vr_lc)}")

    # --- dependencias (exige) ---
    mudou = True
    while mudou:
        mudou = False
        for nome in list(m.cob):
            exige = regras["coberturas"][nome].get("exige_uma_de")
            if exige and not any(m.tem(e) for e in exige):
                if corrigir:
                    m.remover(nome)
                    fix(f"removida '{nome}' (exige uma de: {exige})")
                    mudou = True
                else:
                    erro(f"'{nome}' exige uma de: {exige}")

    # --- valores: minimo e teto efetivo (basica primeiro, dependentes por ultimo) ---
    ordem = sorted(m.cob, key=lambda n: (n != basica,
                                         bool(regras["coberturas"][n].get("exige_uma_de"))))
    for nome in ordem:
        if nome not in m.cob or nome in ja_reportadas:
            continue
        regra = regras["coberturas"][nome]
        val = m.v(nome)
        if val is None:
            continue
        minimo = regra.get("min") or 0
        teto, motivo = teto_efetivo(m, nome, regra, max_corretor(nome), m.v(basica))
        analise = regra.get("acima_max") == "analise"
        if teto is not None and val > teto:
            so_corretor = motivo.startswith("máximo do corretor")
            if analise and so_corretor:
                aviso(f"'{nome}' {brl(val)} acima do {motivo} → vai para análise técnica")
            elif corrigir:
                if teto < minimo:
                    m.remover(nome)
                    fix(f"removida '{nome}': teto {brl(teto)} ({motivo}) abaixo do mínimo {brl(minimo)}")
                    continue
                novo = int(teto * 100) / 100
                m.definir(nome, novo)
                fix(f"'{nome}' {brl(val)} → {brl(novo)} ({motivo})")
                val = novo
            else:
                erro(f"'{nome}' {brl(val)} acima do teto {brl(teto)} ({motivo})")
        if val < minimo:
            if corrigir:
                m.definir(nome, minimo)
                fix(f"'{nome}' {brl(val)} → mínimo {brl(minimo)}")
            else:
                erro(f"'{nome}' {brl(val)} abaixo do mínimo {brl(minimo)}")

    # --- somas ---
    if ramo == "empresarial":
        soma_rc = sum(m.v(n) for n in m.cob if norm(n).startswith("responsabilidade civil"))
    else:
        soma_rc = sum(m.v(n) for n in regras["rc_soma"] if m.tem(n))
    if soma_rc > regras["soma_rc_max"]:
        erro(f"soma das RC {brl(soma_rc)} acima de {brl(regras['soma_rc_max'])} "
             "(ajuste manual: reduza as RC)")
    if ramo == "residencial":
        lmg = sum(m.v(n) for n in regras["compoem_lmg"] if m.tem(n))
        if lmg > regras["lmg_max"]:
            erro(f"LMG {brl(lmg)} acima de {brl(regras['lmg_max'])}")

    # --- avisos de inspecao ---
    if ramo == "empresarial":
        for n, lim in regras["inspecao"].items():
            if m.tem(n) and m.v(n) > lim:
                aviso(f"'{n}' acima de {brl(lim)} exige inspeção de risco")
    elif tipo_res in regras["inspecao_roubo"]:
        n = "Roubo E/ou Furto Qualificado de Bens"
        lim = regras["inspecao_roubo"][tipo_res]
        if m.tem(n) and m.v(n) > lim:
            aviso(f"Roubo acima de {brl(lim)} em {tipo_res} exige inspeção de risco")

    return out


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    entrada = sys.argv[1]
    saida = None
    if "--corrigir" in sys.argv:
        saida = sys.argv[sys.argv.index("--corrigir") + 1]

    dados = json.load(open(entrada, encoding="utf-8"))
    ramo = dados["ramo"]
    regras = json.load(open(os.path.join(REFS, f"regras_{ramo}.json"), encoding="utf-8"))
    corrigido = deepcopy(dados)

    total_erros = 0
    for i, massa in enumerate(corrigido["massas"]):
        alvo = massa if saida else deepcopy(massa)
        problemas = validar(alvo, regras, corrigir=bool(saida))
        if saida:
            # segunda passada sobre a massa ja corrigida: os ERROs que sobraram
            problemas = [p for p in problemas if p[0] != "ERRO"]
            problemas += [p for p in validar(deepcopy(massa), regras) if p[0] == "ERRO"]
        rotulo = f"massa {i + 1} (linha {i + 3})"
        if not problemas:
            print(f"{rotulo}: OK")
        for nivel, msg in problemas:
            print(f"{rotulo}: {nivel}: {msg}")
        total_erros += sum(1 for p in problemas if p[0] == "ERRO")

    if saida:
        json.dump(corrigido, open(saida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"JSON corrigido gravado em {saida}")
    sys.exit(1 if total_erros else 0)


if __name__ == "__main__":
    main()
