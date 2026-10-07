#!/usr/bin/env python3
"""Monta a página do Gerador de Massas num HTML único (pagina/dist/gerador_massas.html).

Embute no pagina/ui.html:
  - pagina/nucleo.js (validação, extração e preenchimento em JavaScript);
  - os templates, as regras_*.json, os .md de referência, o SKILL.md e as atividades da skill.

Rode sempre que mudar uma regra, um template ou a página:
    python3 pagina/montar.py
"""
import base64
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.join(AQUI, "..", ".claude", "skills", "gerador-massas-seguros")
RAMOS = ["empresarial", "residencial", "condominio_amplo", "condominio_tradicional"]


def ler(*partes):
    with open(os.path.join(*partes), encoding="utf-8") as f:
        return f.read()


def main():
    refs_dir = os.path.join(SKILL, "references")
    dados = {
        "templates": {},
        "regras": {},
        "refs": {"SKILL.md": ler(SKILL, "SKILL.md")},
        "atividades": [a.strip() for a in ler(refs_dir, "atividades.txt").splitlines() if a.strip()],
    }
    for ramo in RAMOS:
        with open(os.path.join(SKILL, "templates", f"template_{ramo}.xlsx"), "rb") as f:
            dados["templates"][ramo] = base64.b64encode(f.read()).decode()
        dados["regras"][ramo] = json.loads(ler(refs_dir, f"regras_{ramo}.json"))
    for nome in sorted(os.listdir(refs_dir)):
        if nome.endswith(".md"):
            dados["refs"][nome] = ler(refs_dir, nome)

    html = ler(AQUI, "ui.html")
    # "</" dentro de <script> fecharia a tag: escapa a barra no JSON e no JS embutidos.
    dados_js = json.dumps(dados, ensure_ascii=False).replace("</", "<\\/")
    nucleo = ler(AQUI, "nucleo.js").replace("</script", "<\\/script")
    assert "/*NUCLEO*/" in html and "/*DADOS*/null" in html
    html = html.replace("/*NUCLEO*/", nucleo).replace("/*DADOS*/null", dados_js)

    os.makedirs(os.path.join(AQUI, "dist"), exist_ok=True)
    saida = os.path.join(AQUI, "dist", "gerador_massas.html")
    with open(saida, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"{saida}: {len(html.encode()) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
