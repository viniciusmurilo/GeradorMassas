#!/usr/bin/env python3
"""Monta a página do Gerador de Massas num HTML único (pagina/dist/gerador_massas.html).

O arquivo abre com dois cliques no navegador, sem servidor e sem internet. Embute no pagina/ui.html:
  - as bibliotecas ExcelJS e JSZip (pagina/vendor);
  - pagina/nucleo.js (validação, extração e preenchimento em JavaScript);
  - os templates, as regras_*.json e as atividades da skill.

Rode sempre que mudar uma regra, um template ou a página:
    python3 pagina/montar.py
"""
import base64
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.join(AQUI, "..", ".claude", "skills", "gerador-massas-seguros")
RAMOS = ["empresarial", "residencial", "condominio_amplo", "condominio_tradicional", "proposta"]


def ler(*partes):
    with open(os.path.join(*partes), encoding="utf-8") as f:
        return f.read()


def main():
    refs_dir = os.path.join(SKILL, "references")
    dados = {
        "templates": {},
        "regras": {},
        "atividades": [a.strip() for a in ler(refs_dir, "atividades.txt").splitlines() if a.strip()],
    }
    for ramo in RAMOS:
        with open(os.path.join(SKILL, "templates", f"template_{ramo}.xlsx"), "rb") as f:
            dados["templates"][ramo] = base64.b64encode(f.read()).decode()
        dados["regras"][ramo] = json.loads(ler(refs_dir, f"regras_{ramo}.json"))

    html = ler(AQUI, "ui.html")
    # "</" dentro de <script> fecharia a tag: escapa a barra no JSON e no JS embutidos.
    dados_js = json.dumps(dados, ensure_ascii=False).replace("</", "<\\/")
    nucleo = ler(AQUI, "nucleo.js").replace("</script", "<\\/script")
    assert "/*NUCLEO*/" in html and "/*DADOS*/null" in html
    html = html.replace("/*NUCLEO*/", nucleo).replace("/*DADOS*/null", dados_js)

    # Bibliotecas dentro do arquivo no lugar do CDN: funciona offline.
    libs = "".join(
        "<script>\n" + ler(AQUI, "vendor", nome).replace("</script", "<\\/script") + "\n</script>\n"
        for nome in ("exceljs-4.4.0.min.js", "jszip-3.10.2.min.js"))
    i, j = html.index("<!--LIBS-->"), html.index("<!--/LIBS-->") + len("<!--/LIBS-->")
    html = html[:i] + libs + html[j:]

    # Documento completo: o arquivo é aberto direto no navegador.
    html = ('<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<style>body{margin:0}[hidden]{display:none!important}</style>\n</head>\n<body>\n'
            + html + '\n</body>\n</html>\n')

    os.makedirs(os.path.join(AQUI, "dist"), exist_ok=True)
    saida = os.path.join(AQUI, "dist", "gerador_massas.html")
    with open(saida, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"{saida}: {len(html.encode()) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
