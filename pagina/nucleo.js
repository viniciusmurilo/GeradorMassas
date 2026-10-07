/*
 * Núcleo do Gerador de Massas no navegador: porta para JavaScript (ExcelJS) dos scripts da
 * skill gerador-massas-seguros (preencher_massa.py, extrair_massa.py, validar_massa.py).
 * Mesmas regras, mesmo formato de JSON de entrada e mesmo Excel de saída.
 *
 * Funciona no navegador (global `Nucleo`, com `ExcelJS` global) e no Node (require), onde é
 * testado contra os scripts Python por pagina/teste_paridade.js.
 */
(function (raiz, fabrica) {
  if (typeof module === "object" && module.exports) module.exports = fabrica(require("exceljs"), require("jszip"));
  else raiz.Nucleo = fabrica(raiz.ExcelJS, raiz.JSZip);
})(typeof self !== "undefined" ? self : this, function (ExcelJS, JSZip) {
  "use strict";

  const ABA = "Exportation";
  const LINHA_CABECALHO = 2;
  const LINHA_DADOS = 3;
  const SIM = "sim";
  const IGNORAR = "<IGNORE>";

  // ---------------------------------------------------------------- regras de preenchimento
  const REGRAS_GRUPO = {
    "Deseja contratar indenização a valor de novo?": { modo: "unico", obrigatorio: true, nao_informado: null },
    "Existem equipamentos de proteção contra incêndio?": {
      modo: "unico", obrigatorio: true, nao_informado: "Não informado sistema de proteção contra incêndio" },
    "Existem equipamentos de proteção contra roubo?": {
      modo: "multiplo", obrigatorio: true, nao_informado: "Não informado sistema de proteção contra roubo" },
    "Equipamentos de Proteção": { modo: "multiplo", obrigatorio: true, nao_informado: "Não informado" },
    "Deseja contratar indenização a valor de novo? Condominio": { modo: "unico", obrigatorio: false, nao_informado: null },
    "Quantidade de Pavimentos (incluindo térreo, garagem e subsolos)?": {
      modo: "unico", obrigatorio: true, nao_informado: "Não informado" },
    "Qual a idade do Condomínio?": { modo: "unico", obrigatorio: true, nao_informado: null },
  };
  const REGRA_GRUPO_PADRAO = { modo: "multiplo", obrigatorio: true, nao_informado: null };
  const PERGUNTAS_CONDICIONAIS = {
    "Qual a quantidade de elevadores?": ["O Condomínio possui elevador?", "sim"],
  };
  const ESTILOS = {
    padrao: { marcado: SIM, desmarcado: IGNORAR, vazio: IGNORAR, valor: "br", desmarcado_grupo: {} },
    condominio: {
      marcado: "Sim", desmarcado: IGNORAR, vazio: IGNORAR, valor: "numero",
      desmarcado_grupo: { "Deseja contratar indenização a valor de novo? Condominio": "Não" },
    },
  };
  // Bloco de proposta: igual em todos os templates e no template_proposta.xlsx.
  const PREFIXOS_PROPOSTA = ["proponente", "endereco proponente", "contato ", "proposta "];
  const OPCOES_PROPOSTA = {
    "Proponente PF - Tipo Documento": ["RG", "RNE"],
    "Contato - Tipo Telefone": ["Celular", "Residencial", "Comercial"],
    "Proposta - Forma Pagamento": ["Carnê", "Débito", "Cartão de Crédito"],
    "Proposta - Quantidade Parcelas": ["1 + 1", "1 + 2", "0 + 1"],
    "Proposta Débito - Proponente Titular": ["Sim", "Não"],
  };
  const estiloDoRamo = (ramo) => ESTILOS[String(ramo).startsWith("condominio") ? "condominio" : "padrao"];

  // ---------------------------------------------------------------- utilidades
  const semAcento = (s) => String(s).normalize("NFKD").replace(/[̀-ͯ]/g, "");
  /** normalizar() do preencher_massa.py: sem acento, só letras/dígitos, minúsculo. */
  const normalizar = (s) => semAcento(s).replace(/[^a-zA-Z0-9]+/g, " ").toLowerCase().trim().replace(/\s+/g, " ");
  /** norm() do validar_massa.py: sem acento, minúsculo, espaços colapsados. */
  const norm = (s) => semAcento(s).toLowerCase().trim().replace(/\s+/g, " ");
  const vazio = (v) => v === null || v === undefined || v === "" || v === IGNORAR;

  function brl(v) {
    const [int, dec] = Math.abs(v).toFixed(2).split(".");
    return (v < 0 ? "-" : "") + int.replace(/\B(?=(\d{3})+(?!\d))/g, ".") + "," + dec;
  }

  /** Número ou string tolerante -> número (mesmas regras do formatar_valor_br do Python). */
  function paraNumero(v) {
    if (typeof v === "number") return v;
    let s = String(v).trim().replace(/^r\$\s*/i, "").replace(/[^\d,.]/g, "");
    if (s.includes(",")) s = s.replace(/\./g, "").replace(",", ".");
    else if ((s.match(/\./g) || []).length === 1 && [1, 2].includes(s.split(".")[1].length)) { /* decimal com ponto */ }
    else s = s.replace(/\./g, "");
    if (!s) throw new Error("valor vazio ou não numérico: " + JSON.stringify(v));
    return parseFloat(s);
  }
  const formatarValorBr = (v) => brl(paraNumero(v));
  const numeroInteiro = (v) => { const n = Math.round(paraNumero(v) * 100) / 100; return n; };

  /** num() do validador: número, string BR, ou null para vazio/<IGNORE>. */
  function num(v) {
    if (vazio(v)) return null;
    if (typeof v === "number") return v;
    let s = String(v).trim().replace("R$", "").trim();
    if (s.includes(",")) s = s.replace(/\./g, "").replace(",", ".");
    const n = parseFloat(s);
    if (Number.isNaN(n)) throw new Error("valor não numérico: " + JSON.stringify(v));
    return n;
  }

  /** Valor de célula ExcelJS -> valor simples (texto rico, fórmula, hyperlink). */
  function valorCelula(v) {
    if (v === null || v === undefined) return null;
    if (typeof v === "object") {
      if (v instanceof Date) return v;
      if (Array.isArray(v.richText)) return v.richText.map((t) => t.text).join("");
      if ("result" in v) return valorCelula(v.result);
      if ("text" in v) return v.text;
      if ("error" in v) return null;
    }
    return v;
  }

  const fmtPct = (p) => String(Number(p));
  const listaPy = (xs) => "[" + xs.map((x) => "'" + x + "'").join(", ") + "]";

  // ---------------------------------------------------------------- leitura do template
  function classificar(header) {
    const h = String(header).trim();
    let m = h.match(/^(RDB|CHK)\s+"([^"]+)"\s+(.*)$/);
    if (m) {
      const [, prefixo, opcao, resto] = m;
      if (resto.endsWith("Valor da Cobertura")) return { tipo: "cobertura", chave: opcao };
      return { tipo: "grupo", prefixo, grupo: resto, opcao };
    }
    m = h.match(/^(RDB|CHK)\s+([A-ZÀ-Ú][A-ZÀ-Ú]*)\s+(.*)$/);
    if (m) return { tipo: "grupo", prefixo: m[1], grupo: m[3], opcao: m[2] };
    m = h.match(/^CHK\s+(.*)$/);
    if (m) return { tipo: "bool", chave: m[1] };
    m = h.match(/^TXT\s+"([^"]+)"\s+Valor da Cobertura$/i);
    if (m) return { tipo: "cobertura", chave: m[1] };
    m = h.match(/^TXT\s+"([^"]+)"\s+Per[ií]odo Indenit[aá]rio$/);
    if (m) return { tipo: "periodo", chave: m[1] };
    m = h.match(/^TXT\s+"\s*([^"]+?)\s*"\s+(.+)$/);
    if (m) {
      const [, a, b] = m;
      if (normalizar(a) === "periodo indenitario") return { tipo: "periodo", chave: b };
      if (normalizar(a) === "valor da cobertura") return { tipo: "cobertura", chave: b };
      if (normalizar(a) === "qt de vidas") return { tipo: "qt_vidas", chave: b };
      return { tipo: "cobertura", chave: a };
    }
    m = h.match(/^CBO\s+(.*)$/);
    if (m) return { tipo: "combo", chave: m[1] };
    m = h.match(/^TXT\s+(.*)$/);
    if (m) return { tipo: "texto", chave: m[1] };
    if (PREFIXOS_PROPOSTA.some((p) => normalizar(h).startsWith(p))) return { tipo: "proposta", chave: h };
    if (h.endsWith("?")) return { tipo: "pergunta", chave: h };
    return { tipo: "direto", chave: h };
  }

  function abaDados(wb) {
    return wb.getWorksheet(ABA) || wb.worksheets[0];
  }

  function ultimaColuna(ws) {
    let max = 0;
    ws.getRow(LINHA_CABECALHO).eachCell({ includeEmpty: false }, (_c, col) => { if (col > max) max = col; });
    return Math.max(max, ws.columnCount || 0);
  }

  /** montar_mapa(): cabeçalho da linha 2 classificado. Colunas são números (1 = A). */
  function montarMapa(ws) {
    const mapa = { campos: {}, combos: {}, textos: {}, bools: {}, perguntas: {}, proposta: {}, coberturas: {},
      periodos: {}, qt_vidas: {}, grupos: {}, duplicadas: [], colunas_valor: new Set() };
    const maxCol = ultimaColuna(ws);
    for (let c = 1; c <= maxCol; c++) {
      const header = valorCelula(ws.getCell(LINHA_CABECALHO, c).value);
      if (header === null || header === "") continue;
      const info = classificar(header);
      const t = info.tipo;
      if (t === "direto") mapa.campos[info.chave] = c;
      else if (t === "combo") mapa.combos[info.chave] = c;
      else if (t === "texto") mapa.textos[info.chave] = c;
      else if (t === "pergunta") mapa.perguntas[info.chave] = c;
      else if (t === "proposta") mapa.proposta[info.chave] = c;
      else if (t === "bool") mapa.bools[info.chave] = c;
      else if (t === "cobertura" || t === "periodo" || t === "qt_vidas") {
        const destino = { cobertura: mapa.coberturas, periodo: mapa.periodos, qt_vidas: mapa.qt_vidas }[t];
        if (info.chave in destino) mapa.duplicadas.push([destino[info.chave], c]);
        else destino[info.chave] = c;
      } else if (t === "grupo") {
        (mapa.grupos[info.grupo] = mapa.grupos[info.grupo] || { opcoes: {} }).opcoes[info.opcao] = c;
      }
    }
    for (const [nome, col] of Object.entries(mapa.textos)) if (normalizar(nome) !== "atividade") mapa.colunas_valor.add(col);
    for (const col of Object.values(mapa.coberturas)) mapa.colunas_valor.add(col);
    for (const [nome, col] of Object.entries(mapa.combos)) if (normalizar(nome).startsWith("valor em risco")) mapa.colunas_valor.add(col);
    for (const [p, d] of mapa.duplicadas) if (mapa.colunas_valor.has(p)) mapa.colunas_valor.add(d);
    mapa.maxCol = maxCol;
    return mapa;
  }

  const indice = (nomes) => Object.fromEntries(Object.keys(nomes).map((n) => [normalizar(n), n]));

  /**
   * O ExcelJS expande cada validação de dados célula a célula: uma lista em "N3:N1048576" (como
   * no template do Amplo) trava o navegador. Antes de abrir, corta essas faixas na linha LIMITE.
   */
  const LIMITE_LINHAS = 1000;
  async function sanear(buffer) {
    const zip = await JSZip.loadAsync(buffer);
    let mudou = false;
    for (const nome of Object.keys(zip.files).filter((n) => /^xl\/worksheets\/[^/]+\.xml$/.test(n))) {
      const xml = await zip.file(nome).async("string");
      const novo = xml.replace(/sqref="([^"]*)"/g, (_m, refs) => 'sqref="' +
        refs.replace(/([A-Z]+)(\d+)/g, (r, col, lin) => (Number(lin) > LIMITE_LINHAS ? col + LIMITE_LINHAS : r)) + '"');
      if (novo !== xml) { zip.file(nome, novo); mudou = true; }
    }
    return mudou ? zip.generateAsync({ type: "uint8array" }) : buffer;
  }

  async function abrir(buffer) {
    const wb = new ExcelJS.Workbook();
    await wb.xlsx.load(await sanear(buffer));
    return wb;
  }

  // ---------------------------------------------------------------- preencher
  function preencherLinha(ws, linha, massa, mapa, estilo) {
    const { marcado: MARCADO, desmarcado: DESMARCADO, vazio: VAZIO } = estilo;
    const fmtValor = estilo.valor === "br" ? formatarValorBr : numeroInteiro;
    const set = (col, v) => { ws.getCell(linha, col).value = v === undefined ? null : v; };

    const diretos = Object.assign({}, massa.campos || {}, massa.combos || {}, massa.texto || {});
    const esperados = new Set([...Object.keys(mapa.campos), ...Object.keys(mapa.combos), ...Object.keys(mapa.textos)]);
    const faltando = [...esperados].filter((n) => !(n in diretos)).sort();
    if (faltando.length) throw new Error(`linha ${linha}: campos obrigatórios ausentes: ${listaPy(faltando)}`);
    const sobrando = Object.keys(diretos).filter((n) => !esperados.has(n)).sort();
    if (sobrando.length) throw new Error(`linha ${linha}: campos inexistentes no template: ${listaPy(sobrando)}`);
    for (const [nome, valor0] of Object.entries(diretos)) {
      const col = mapa.campos[nome] || mapa.combos[nome] || mapa.textos[nome];
      let valor = valor0;
      if (mapa.colunas_valor.has(col) && valor !== IGNORAR && !vazio(valor)) valor = fmtValor(valor);
      set(col, valor);
    }

    const idxProp = indice(mapa.proposta), dadosProp = {};
    for (const [nome, valor] of Object.entries(massa.proposta || {})) {
      const canon = idxProp[normalizar(nome)];
      if (!canon) throw new Error(`linha ${linha}: coluna de proposta inexistente no template: '${nome}'`);
      dadosProp[canon] = valor;
    }
    for (const [nome, col] of Object.entries(mapa.proposta)) {
      const v = dadosProp[nome];
      set(col, v === undefined || v === null || v === "" ? IGNORAR : v);
    }

    const marcadosBool = new Set(massa.bool || []);
    const invalidosBool = [...marcadosBool].filter((n) => !(n in mapa.bools));
    if (invalidosBool.length) throw new Error(`linha ${linha}: campo bool inexistente: ${listaPy(invalidosBool)}`);
    for (const [nome, col] of Object.entries(mapa.bools)) set(col, marcadosBool.has(nome) ? MARCADO : DESMARCADO);

    const perguntas = Object.assign({}, massa.perguntas || {});
    const gruposPedidos = Object.assign({}, massa.grupos || {});
    for (const nome of Object.keys(mapa.perguntas)) {
      if (!(nome in perguntas) && nome in gruposPedidos) {
        const op = gruposPedidos[nome]; delete gruposPedidos[nome];
        perguntas[nome] = op.length === 1 ? op[0] : "";
      }
    }
    for (const [nome, col] of Object.entries(mapa.perguntas)) {
      let resp = perguntas[nome];
      if (normalizar(nome).startsWith("deseja contratar indenizacao")) {
        const chave = vazio(resp) ? "nao" : normalizar(resp);
        if (chave !== "sim" && chave !== "nao") throw new Error(`linha ${linha}: '${nome}' aceita só sim/não, recebeu ${JSON.stringify(resp)}`);
        resp = chave === "sim" ? "sim" : IGNORAR;
      } else if (nome in PERGUNTAS_CONDICIONAIS &&
          normalizar(perguntas[PERGUNTAS_CONDICIONAIS[nome][0]] || "") !== PERGUNTAS_CONDICIONAIS[nome][1]) {
        resp = VAZIO;
      } else if (vazio(resp)) {
        throw new Error(`linha ${linha}: pergunta '${nome}' sem resposta`);
      }
      set(col, resp);
    }
    const perguntasSobrando = Object.keys(perguntas).filter((n) => !(n in mapa.perguntas));
    if (perguntasSobrando.length) throw new Error(`linha ${linha}: pergunta inexistente no template: ${listaPy(perguntasSobrando)}`);

    const gruposInvalidos = Object.keys(gruposPedidos).filter((n) => !(n in mapa.grupos));
    if (gruposInvalidos.length) throw new Error(`linha ${linha}: grupo inexistente: ${listaPy(gruposInvalidos)}`);
    const ausentes = Object.keys(mapa.grupos).filter((n) => (REGRAS_GRUPO[n] || REGRA_GRUPO_PADRAO).obrigatorio && !(n in gruposPedidos));
    if (ausentes.length) throw new Error(`linha ${linha}: questionário obrigatório não respondido: ${listaPy(ausentes.sort())}`);
    for (const [grupo, ginfo] of Object.entries(mapa.grupos)) {
      const regra = REGRAS_GRUPO[grupo] || REGRA_GRUPO_PADRAO;
      const idx = indice(ginfo.opcoes);
      const canon = (gruposPedidos[grupo] || []).map((opc) => {
        const c = idx[normalizar(opc)];
        if (!c) throw new Error(`linha ${linha}: opção '${opc}' não existe no questionário '${grupo}' (opções válidas: ${listaPy(Object.keys(ginfo.opcoes).sort())})`);
        return c;
      });
      if (regra.obrigatorio && !canon.length) throw new Error(`linha ${linha}: questionário '${grupo}' sem resposta — marque pelo menos uma opção (opções válidas: ${listaPy(Object.keys(ginfo.opcoes).sort())})`);
      if (regra.modo === "unico" && canon.length > 1) throw new Error(`linha ${linha}: questionário '${grupo}' é de escolha única, recebeu ${listaPy(canon)}`);
      if (regra.nao_informado && canon.includes(regra.nao_informado) && canon.length > 1)
        throw new Error(`linha ${linha}: questionário '${grupo}': '${regra.nao_informado}' é exclusiva, não pode vir com outras opções (${listaPy(canon)})`);
      const desmarcado = grupo in estilo.desmarcado_grupo ? estilo.desmarcado_grupo[grupo] : DESMARCADO;
      for (const [opcao, col] of Object.entries(ginfo.opcoes)) set(col, canon.includes(opcao) ? MARCADO : desmarcado);
    }

    const idxCob = indice(mapa.coberturas), idxPer = indice(mapa.periodos), idxVid = indice(mapa.qt_vidas);
    const solicitadas = {}, periodos = {}, vidas = {};
    for (const item of massa.coberturas || []) {
      const canon = idxCob[normalizar(item.nome)];
      if (!canon) throw new Error(`linha ${linha}: cobertura não existe no template: '${item.nome}'`);
      if (canon in solicitadas) throw new Error(`linha ${linha}: cobertura duplicada: '${canon}'`);
      solicitadas[canon] = fmtValor(item.valor);
      if (item.periodo_indenitario !== undefined && item.periodo_indenitario !== null && item.periodo_indenitario !== "") {
        const cp = idxPer[normalizar(item.nome)];
        if (!cp) throw new Error(`linha ${linha}: cobertura '${canon}' não tem coluna de período indenitário`);
        periodos[cp] = item.periodo_indenitario;
      }
      if (item.qt_vidas !== undefined && item.qt_vidas !== null && item.qt_vidas !== "") {
        const cv = idxVid[normalizar(item.nome)];
        if (!cv) throw new Error(`linha ${linha}: cobertura '${item.nome}' não tem coluna de Qt de vidas`);
        vidas[cv] = item.qt_vidas;
      }
    }
    for (const [nome, col] of Object.entries(mapa.coberturas)) set(col, nome in solicitadas ? solicitadas[nome] : VAZIO);
    for (const [nome, col] of Object.entries(mapa.periodos)) set(col, nome in periodos ? periodos[nome] : VAZIO);
    for (const [nome, col] of Object.entries(mapa.qt_vidas)) set(col, nome in vidas ? vidas[nome] : VAZIO);
    for (const [principal, repetida] of mapa.duplicadas) set(repetida, ws.getCell(linha, principal).value);
    return solicitadas;
  }

  /** preencher(): JSON {ramo, massas} + buffer do template -> {buffer, resumo}. */
  async function preencher(dados, templateBuffer) {
    const wb = await abrir(templateBuffer);
    const ws = abaDados(wb);
    const mapa = montarMapa(ws);
    const estilo = estiloDoRamo(dados.ramo);
    const estilos = {};
    for (let c = 1; c <= mapa.maxCol; c++) estilos[c] = JSON.parse(JSON.stringify(ws.getCell(LINHA_DADOS, c).style || {}));

    const resumo = [];
    (dados.massas || []).forEach((massa, i) => {
      const linha = LINHA_DADOS + i;
      resumo.push({ linha, coberturas: Object.keys(preencherLinha(ws, linha, massa, mapa, estilo)) });
    });
    for (const { linha } of resumo) {
      for (let c = 1; c <= mapa.maxCol; c++) {
        const cel = ws.getCell(linha, c);
        const st = JSON.parse(JSON.stringify(estilos[c]));
        if (mapa.colunas_valor.has(c) && estilo.valor === "br") st.numFmt = "@";
        cel.style = st;
      }
    }
    const ultimaLinha = Math.max(ws.rowCount, ws.actualRowCount || 0);
    for (let linha = LINHA_DADOS + resumo.length; linha <= ultimaLinha; linha++)
      for (let c = 1; c <= mapa.maxCol; c++) ws.getCell(linha, c).value = null;

    const buffer = await wb.xlsx.writeBuffer();
    return { buffer, resumo };
  }

  // ---------------------------------------------------------------- extrair
  function valorNumero(v) {
    if (typeof v === "number") return v;
    const s = String(v).trim();
    if (/^[\d.]+,\d{1,2}$/.test(s) || /^\d+(\.\d+)?$/.test(s)) {
      const n = s.includes(",") ? parseFloat(s.replace(/\./g, "").replace(",", ".")) : parseFloat(s);
      return n;
    }
    return s;
  }
  const marcadoCel = (v) => v !== null && v !== undefined && ["sim", "s", "x", "true", "1"].includes(normalizar(v));

  function detectarRamo(mapa) {
    if ("Numero Cotacao" in mapa.campos) return "proposta";
    if ("Tipo de Condomínio" in mapa.combos) {
      const trad = Object.keys(mapa.coberturas).some((n) => normalizar(n).startsWith("incendio queda de raio"));
      return trad ? "condominio_tradicional" : "condominio_amplo";
    }
    return "Cep Risco" in mapa.campos ? "empresarial" : "residencial";
  }

  /** extrair(): buffer de uma planilha preenchida -> {ramo, massas}. */
  async function extrair(buffer) {
    const wb = await abrir(buffer);
    const ws = abaDados(wb);
    const mapa = montarMapa(ws);
    const ramo = detectarRamo(mapa);
    const limpar = (v) => (typeof v === "string" ? v.replace(/ /g, " ").trim() : v);
    const todas = [mapa.campos, mapa.combos, mapa.textos, mapa.bools, mapa.perguntas, mapa.coberturas, mapa.periodos]
      .flatMap((d) => Object.values(d))
      .concat(Object.values(mapa.grupos).flatMap((g) => Object.values(g.opcoes)));
    const massas = [];
    const ultimaLinha = Math.max(ws.rowCount, ws.actualRowCount || 0);
    for (let linha = LINHA_DADOS; linha <= ultimaLinha; linha++) {
      const cel = (col) => limpar(valorCelula(ws.getCell(linha, col).value));
      if (todas.every((c) => vazio(cel(c)))) continue;
      const massa = {
        campos: Object.fromEntries(Object.entries(mapa.campos).map(([n, c]) => [n, cel(c)])),
        combos: Object.fromEntries(Object.entries(mapa.combos).map(([n, c]) => {
          const v = cel(c);
          return [n, mapa.colunas_valor.has(c) && !vazio(v) ? valorNumero(v) : v];
        })),
        bool: ramo === "empresarial" ? [] : Object.entries(mapa.bools).filter(([, c]) => marcadoCel(cel(c))).map(([n]) => n),
        perguntas: Object.fromEntries(Object.entries(mapa.perguntas).map(([n, c]) => {
          const v = cel(c);
          return [n, normalizar(n).startsWith("deseja contratar indenizacao") && vazio(v) ? "não" : v];
        })),
        grupos: Object.fromEntries(Object.entries(mapa.grupos).map(([g, info]) =>
          [g, Object.entries(info.opcoes).filter(([, c]) => marcadoCel(cel(c))).map(([o]) => o)])),
        coberturas: [],
      };
      if (Object.keys(mapa.textos).length) {
        massa.texto = Object.fromEntries(Object.entries(mapa.textos).map(([n, c]) => {
          const v = cel(c);
          return [n, !mapa.colunas_valor.has(c) || vazio(v) ? v : valorNumero(v)];
        }));
      }
      const proposta = Object.fromEntries(Object.entries(mapa.proposta).map(([n, c]) => [n, cel(c)]).filter(([, v]) => !vazio(v)));
      if (Object.keys(proposta).length) massa.proposta = proposta;
      const periodos = Object.fromEntries(Object.entries(mapa.periodos).map(([n, c]) => [normalizar(n), cel(c)]));
      for (const [n, c] of Object.entries(mapa.coberturas)) {
        const v = cel(c);
        if (vazio(v)) continue;
        const item = { nome: n, valor: valorNumero(v) };
        const vidas = n in mapa.qt_vidas ? cel(mapa.qt_vidas[n]) : null;
        if (!vazio(vidas)) item.qt_vidas = valorNumero(vidas);
        const p = periodos[normalizar(n)];
        if (!vazio(p)) item.periodo_indenitario = valorNumero(p);
        massa.coberturas.push(item);
      }
      massas.push(massa);
    }
    return { ramo, massas };
  }

  /** Estrutura do template para montar formulário e prompt. */
  async function estruturaTemplate(buffer) {
    const wb = await abrir(buffer);
    const mapa = montarMapa(abaDados(wb));
    return {
      campos: Object.keys(mapa.campos), combos: Object.keys(mapa.combos), textos: Object.keys(mapa.textos),
      bools: Object.keys(mapa.bools), perguntas: Object.keys(mapa.perguntas), proposta: Object.keys(mapa.proposta),
      grupos: Object.fromEntries(Object.entries(mapa.grupos).map(([g, i]) =>
        [g, { opcoes: Object.keys(i.opcoes), ...(REGRAS_GRUPO[g] || REGRA_GRUPO_PADRAO) }])),
      coberturas: Object.keys(mapa.coberturas), periodos: Object.keys(mapa.periodos), qt_vidas: Object.keys(mapa.qt_vidas),
    };
  }

  // ---------------------------------------------------------------- validar
  const PADRAO_GRUPO = {
    "Deseja contratar indenização a valor de novo?": "NÃO",
    "Existem equipamentos de proteção contra incêndio?": "Não informado sistema de proteção contra incêndio",
    "Existem equipamentos de proteção contra roubo?": "Não informado sistema de proteção contra roubo",
    "Equipamentos de Proteção": "Não informado",
    "Quantidade de Pavimentos (incluindo térreo, garagem e subsolos)?": "Não informado",
  };
  const GRUPOS_COND = ["Quantidade de Pavimentos (incluindo térreo, garagem e subsolos)?", "Qual a idade do Condomínio?"];
  const GRUPOS_RAMO = {
    empresarial: ["Existem equipamentos de proteção contra incêndio?", "Existem equipamentos de proteção contra roubo?"],
    residencial: ["Equipamentos de Proteção"],
    condominio_amplo: GRUPOS_COND, condominio_tradicional: GRUPOS_COND,
  };
  const PERGUNTAS_COND = {
    "O condomínio está legalmente constituído?": null,
    "O Condomínio possui elevador?": null,
    "O Condomínio Possui Central Telefônica e/ou equipamentos de segurança e/ou monitoramento?": null,
  };
  const PERGUNTAS_RAMO = {
    empresarial: { "Deseja contratar indenização a valor de novo?": "não" },
    residencial: { "Deseja contratar indenização a valor de novo?": "não" },
    condominio_amplo: PERGUNTAS_COND, condominio_tradicional: PERGUNTAS_COND,
  };

  class Massa {
    constructor(dados, regras) {
      this.d = dados; this.r = regras;
      this.idx = Object.fromEntries(Object.keys(regras.coberturas).map((n) => [norm(n), n]));
      this.cob = new Map(); this.desconhecidas = [];
      for (const item of dados.coberturas || []) {
        const canon = this.idx[norm(item.nome)];
        if (canon === undefined) this.desconhecidas.push(item.nome); else this.cob.set(canon, item);
      }
    }
    v(nome) { const it = this.cob.get(nome); return it ? num(it.valor) : null; }
    tem(nome) { return this.cob.has(nome) && (this.v(nome) || 0) > 0; }
    remover(nome) {
      const it = this.cob.get(nome);
      if (it) { this.cob.delete(nome); this.d.coberturas.splice(this.d.coberturas.indexOf(it), 1); }
    }
    definir(nome, valor) {
      if (this.cob.has(nome)) this.cob.get(nome).valor = valor;
      else { const it = { nome, valor }; (this.d.coberturas = this.d.coberturas || []).push(it); this.cob.set(nome, it); }
    }
  }

  function tetoEfetivo(m, nome, regra, maxCorretor, basicaV) {
    const tetos = [];
    if (maxCorretor !== null && maxCorretor !== undefined) tetos.push([Number(maxCorretor), `máximo do corretor ${brl(maxCorretor)}`]);
    const pct = regra.pct_basica;
    if (pct && nome !== m.r.basica && basicaV) tetos.push([basicaV * pct / 100, `${fmtPct(pct)}% da básica`]);
    const pex = regra.pct_max_da_exigida;
    if (pex && regra.exige_uma_de)
      for (const e of regra.exige_uma_de) if (m.tem(e)) tetos.push([m.v(e) * pex / 100, `${fmtPct(pex)}% de ${e}`]);
    if (!tetos.length) return [null, null];
    return tetos.reduce((a, b) => (b[0] < a[0] ? b : a));
  }

  /** Bloco de proposta (opcional): valores das listas do template. */
  function validarProposta(massa, corrigir, erro, fix) {
    const proposta = massa.proposta || {};
    for (const [nome, opcoes] of Object.entries(OPCOES_PROPOSTA)) {
      const v = proposta[nome];
      if (vazio(v) || opcoes.includes(v)) continue;
      const chave = (x) => norm(x).replace(/ /g, "");
      const canon = opcoes.find((o) => chave(o) === chave(v));
      if (canon && corrigir) { proposta[nome] = canon; fix(`proposta '${nome}': '${v}' → '${canon}'`); }
      else if (canon) erro(`proposta '${nome}': use '${canon}' (recebeu '${v}')`);
      else erro(`proposta '${nome}': '${v}' não existe na lista ${listaPy(opcoes)}`);
    }
  }

  /** validar(): devolve [[nivel, mensagem]]; com corrigir=true altera a massa no lugar. */
  function validar(massa, regras, corrigir = false) {
    const ramo = regras.ramo;
    const m = new Massa(massa, regras);
    const out = [];
    const erro = (s) => out.push(["ERRO", s]), aviso = (s) => out.push(["AVISO", s]), fix = (s) => out.push(["CORRIGIDO", s]);

    validarProposta(massa, corrigir, erro, fix);
    if (ramo === "proposta") {
      const campos = (massa.campos = massa.campos || {});
      if (!campos.Perfil) {
        if (corrigir) { campos.Perfil = "Corretor"; fix("Perfil vazio → 'Corretor'"); }
        else erro("campo 'Perfil' vazio (ex.: 'Corretor')");
      }
      if (vazio(campos["Numero Cotacao"])) erro("campo 'Numero Cotacao' vazio (número da cotação a que a proposta se refere)");
      return out;
    }

    for (const n of m.desconhecidas) aviso(`cobertura '${n}' sem regra cadastrada para ${ramo} (não validada)`);
    const combos = massa.combos || {};
    const texto = massa.texto || {};
    const tipoRes = combos["Tipo de Residência"];

    const campos = (massa.campos = massa.campos || {});
    if (!campos.Perfil) {
      if (corrigir) { campos.Perfil = "Corretor"; fix("Perfil vazio → 'Corretor'"); }
      else erro("campo 'Perfil' vazio (ex.: 'Corretor')");
    }

    const perguntas = (massa.perguntas = massa.perguntas || {});
    const gruposAntigos = massa.grupos || {};
    for (const [g, padrao] of Object.entries(PERGUNTAS_RAMO[ramo])) {
      if (!perguntas[g] && gruposAntigos[g] && gruposAntigos[g].length) {
        perguntas[g] = String(gruposAntigos[g][0]).toLowerCase().replace("nao", "não"); delete gruposAntigos[g];
      }
      if (!perguntas[g] || perguntas[g] === IGNORAR) {
        if (corrigir && padrao !== null) { perguntas[g] = padrao; fix(`pergunta '${g}' sem resposta → '${padrao}'`); }
        else erro(`pergunta '${g}' sem resposta`);
      }
    }
    for (const [g, [mae, habilita]] of Object.entries(PERGUNTAS_CONDICIONAIS)) {
      if (g in perguntas || ramo.startsWith("condominio"))
        if (norm(perguntas[mae] || "") === habilita && vazio(perguntas[g])) erro(`pergunta '${g}' sem resposta ('${mae}' = ${perguntas[mae]})`);
    }

    const grupos = (massa.grupos = massa.grupos || {});
    for (const g of GRUPOS_RAMO[ramo]) {
      if (!grupos[g] || !grupos[g].length) {
        if (corrigir && g in PADRAO_GRUPO) { grupos[g] = [PADRAO_GRUPO[g]]; fix(`questionário '${g}' sem resposta → '${PADRAO_GRUPO[g]}'`); }
        else erro(`questionário '${g}' sem resposta`);
      }
    }

    if (ramo === "empresarial") {
      const ativ = texto.Atividade, constr = combos["Tipo de Construção"];
      const soSolida = regras.atividades_so_solida.includes(ativ);
      if (regras.tipo_construcao_sem_aceitacao.includes(constr) || (soSolida && constr !== "Sólida")) {
        const novo = soSolida ? "Sólida" : "Superior";
        if (corrigir) { combos["Tipo de Construção"] = novo; fix(`tipo de construção '${constr}' → '${novo}'`); }
        else erro(`tipo de construção '${constr}' não aceito` + (soSolida ? ` (atividade '${ativ}' só aceita Sólida)` : ""));
      }
      if (regras.atividades_so_predio.includes(ativ) && combos["Objeto Segurado"] !== "Prédio") {
        if (corrigir) { combos["Objeto Segurado"] = "Prédio"; fix(`objeto segurado → 'Prédio' (atividade '${ativ}')`); }
        else erro(`atividade '${ativ}' só aceita Objeto Segurado = Prédio`);
      }
      const vr = num(texto["Valor em Risco - Danos Materiais"]);
      const lim = regras.valor_em_risco;
      if (vr !== null && !(lim.min <= vr && vr <= lim.max)) erro(`Valor em Risco ${brl(vr)} fora de ${brl(lim.min)} a ${brl(lim.max)}`);
    }
    if (ramo === "residencial" && (regras.objeto_so_predio || []).includes(tipoRes) && combos["Objeto Segurado"] !== "Prédio") {
      if (corrigir) { combos["Objeto Segurado"] = "Prédio"; fix(`objeto segurado → 'Prédio' (${tipoRes})`); }
      else erro(`${tipoRes} exige Objeto Segurado = Prédio`);
    }

    const maxPorTipo = (tipoRes && (regras.max_corretor_por_tipo || {})[tipoRes]) || {};
    const maxCorretor = (nome) => (nome in maxPorTipo ? maxPorTipo[nome] : regras.coberturas[nome].max);

    const jaReportadas = new Set();
    for (const nome of [...m.cob.keys()]) {
      const regra = regras.coberturas[nome];
      if (regra.sem_aceitacao || maxCorretor(nome) === 0) {
        const motivo = regra.sem_aceitacao ? "sem aceitação comercial" : `indisponível para ${tipoRes}`;
        if (corrigir) { m.remover(nome); fix(`removida '${nome}' (${motivo})`); }
        else { erro(`'${nome}' ${motivo}`); jaReportadas.add(nome); }
      }
    }
    const tipoCond = combos["Tipo de Condomínio"];
    for (const nome of [...m.cob.keys()]) {
      const proib = (regras.coberturas[nome].proibida_para_tipo_condominio || []).map(norm);
      if (tipoCond && proib.includes(norm(tipoCond))) {
        if (corrigir) { m.remover(nome); fix(`removida '${nome}' (não aceita para '${tipoCond}')`); }
        else { erro(`'${nome}' não é aceita para '${tipoCond}'`); jaReportadas.add(nome); }
      }
    }

    const basica = regras.basica;
    let basicaV = null;
    if (regras.basica_campo) {
      basicaV = num(combos[regras.basica_campo]);
      const lim = regras.basica_limites;
      if (!basicaV) erro(`'${regras.basica_campo}' vazio (base dos percentuais)`);
      else if (!(lim.min <= basicaV && basicaV <= lim.max)) erro(`'${regras.basica_campo}' ${brl(basicaV)} fora de ${brl(lim.min)} a ${brl(lim.max)}`);
    } else if (!m.tem(basica)) erro(`falta a cobertura básica '${basica}' (base dos percentuais)`);

    const pares = new Set();
    for (const nome of [...m.cob.keys()]) {
      if (!m.cob.has(nome)) continue;
      for (const outra of regras.coberturas[nome].exclui || []) {
        const chave = [nome, outra].sort().join("\u0000");
        if (m.cob.has(outra) && !pares.has(chave)) {
          pares.add(chave);
          if (corrigir) { m.remover(outra); fix(`removida '${outra}' (excludente com '${nome}')`); }
          else erro(`'${nome}' e '${outra}' são excludentes`);
        }
      }
    }
    for (const [a, b] of regras.avisos_par_excludente || [])
      if (m.cob.has(a) && m.cob.has(b)) aviso(`'${a}' com '${b}': a fonte indica exclusão (ponto a confirmar)`);

    if (ramo === "empresarial") {
      let vrLc = num(texto["Lucros Cessantes"]);
      const basicasLc = regras.lucros_cessantes_basicas, limitadas = regras.limitadas_pelo_vr_lucros_cessantes;
      if (vrLc) {
        if (!basicasLc.some((b) => m.tem(b))) {
          if (corrigir) {
            const valor = Math.min(vrLc, m.v(basica) || vrLc);
            m.definir(basicasLc[0], valor);
            fix(`VR Lucros Cessantes sem LC/DF básica → adicionada '${basicasLc[0]}' com ${brl(valor)}`);
          } else erro("VR Lucros Cessantes preenchido exige 'Lucros Cessantes - Incêndio' ou 'Despesas Fixas - Incêndio'");
        }
      } else {
        const presentes = regras.proibidas_sem_vr_lucros_cessantes.filter((n) => m.tem(n));
        if (presentes.length) {
          const maiores = limitadas.filter((n) => m.tem(n)).map((n) => m.v(n));
          if (corrigir && maiores.length) {
            vrLc = Math.max(...maiores); texto["Lucros Cessantes"] = vrLc;
            fix(`VR Lucros Cessantes vazio com ${listaPy(presentes)} → VR = ${brl(vrLc)}`);
          } else if (corrigir) {
            for (const n of presentes) { m.remover(n); fix(`removida '${n}' (sem VR Lucros Cessantes)`); }
          } else erro(`sem VR Lucros Cessantes não pode ter ${listaPy(presentes)}`);
        }
      }
      if (vrLc) for (const n of limitadas) {
        if (m.tem(n) && m.v(n) > vrLc) {
          if (corrigir) { m.definir(n, vrLc); fix(`'${n}' reduzida para o VR Lucros Cessantes ${brl(vrLc)}`); }
          else erro(`'${n}' ${brl(m.v(n))} maior que o VR Lucros Cessantes ${brl(vrLc)}`);
        }
      }
    }

    let mudou = true;
    while (mudou) {
      mudou = false;
      for (const nome of [...m.cob.keys()]) {
        const exige = regras.coberturas[nome].exige_uma_de;
        if (exige && !exige.some((e) => m.tem(e))) {
          if (corrigir) { m.remover(nome); fix(`removida '${nome}' (exige uma de: ${listaPy(exige)})`); mudou = true; }
          else erro(`'${nome}' exige uma de: ${listaPy(exige)}`);
        }
      }
    }

    const chaveOrdem = (n) => (n !== basica ? 1 : 0) * 2 + (regras.coberturas[n].exige_uma_de ? 1 : 0);
    const ordem = [...m.cob.keys()].map((n, i) => [n, i]).sort((a, b) => chaveOrdem(a[0]) - chaveOrdem(b[0]) || a[1] - b[1]).map((x) => x[0]);
    for (const nome of ordem) {
      if (!m.cob.has(nome) || jaReportadas.has(nome)) continue;
      const regra = regras.coberturas[nome];
      let val = m.v(nome);
      if (val === null) continue;
      const minimo = regra.min || 0;
      const [teto, motivo] = tetoEfetivo(m, nome, regra, maxCorretor(nome), regras.basica_campo ? basicaV : m.v(basica));
      if (regra.valor_fixo && val !== minimo) {
        if (corrigir) { m.definir(nome, minimo); fix(`'${nome}' ${brl(val)} → valor fixo ${brl(minimo)}`); }
        else erro(`'${nome}' tem valor fixo ${brl(minimo)} (recebeu ${brl(val)})`);
        continue;
      }
      const analise = regra.acima_max === "analise";
      if (teto !== null && val > teto) {
        const soCorretor = motivo.startsWith("máximo do corretor");
        if (analise && soCorretor) aviso(`'${nome}' ${brl(val)} acima do ${motivo} → vai para análise técnica`);
        else if (corrigir) {
          if (teto < minimo) { m.remover(nome); fix(`removida '${nome}': teto ${brl(teto)} (${motivo}) abaixo do mínimo ${brl(minimo)}`); continue; }
          const novo = Math.trunc(teto * 100) / 100;
          m.definir(nome, novo); fix(`'${nome}' ${brl(val)} → ${brl(novo)} (${motivo})`); val = novo;
        } else erro(`'${nome}' ${brl(val)} acima do teto ${brl(teto)} (${motivo})`);
      }
      if (val < minimo) {
        if (corrigir) { m.definir(nome, minimo); fix(`'${nome}' ${brl(val)} → mínimo ${brl(minimo)}`); }
        else erro(`'${nome}' ${brl(val)} abaixo do mínimo ${brl(minimo)}`);
      }
    }

    let somaRc = 0;
    if (ramo === "empresarial") { for (const n of m.cob.keys()) if (norm(n).startsWith("responsabilidade civil")) somaRc += m.v(n) || 0; }
    else for (const n of regras.rc_soma || []) if (m.tem(n)) somaRc += m.v(n);
    if (regras.soma_rc_max && somaRc > regras.soma_rc_max)
      erro(`soma das RC ${brl(somaRc)} acima de ${brl(regras.soma_rc_max)} (ajuste manual: reduza as RC)`);
    if (ramo === "residencial") {
      let lmg = 0; for (const n of regras.compoem_lmg) if (m.tem(n)) lmg += m.v(n);
      if (lmg > regras.lmg_max) erro(`LMG ${brl(lmg)} acima de ${brl(regras.lmg_max)}`);
    }

    if (ramo === "empresarial") {
      for (const [n, lim] of Object.entries(regras.inspecao)) if (m.tem(n) && m.v(n) > lim) aviso(`'${n}' acima de ${brl(lim)} exige inspeção de risco`);
    } else if (ramo === "residencial" && tipoRes in regras.inspecao_roubo) {
      const n = "Roubo E/ou Furto Qualificado de Bens", lim = regras.inspecao_roubo[tipoRes];
      if (m.tem(n) && m.v(n) > lim) aviso(`Roubo acima de ${brl(lim)} em ${tipoRes} exige inspeção de risco`);
    }
    return out;
  }

  const copia = (x) => JSON.parse(JSON.stringify(x));

  /**
   * validarLote(): mesmo comportamento do main() do validar_massa.py.
   * Devolve {dados (corrigidos, se corrigir), relatorio: [{massa, linha, problemas:[[nivel,msg]]}], erros}.
   */
  function validarLote(dados, regras, corrigir = false) {
    const saida = copia(dados);
    const relatorio = [];
    let erros = 0;
    saida.massas.forEach((massa, i) => {
      const alvo = corrigir ? massa : copia(massa);
      let problemas = validar(alvo, regras, corrigir);
      if (corrigir) {
        problemas = problemas.filter((p) => p[0] !== "ERRO").concat(validar(copia(massa), regras).filter((p) => p[0] === "ERRO"));
      }
      erros += problemas.filter((p) => p[0] === "ERRO").length;
      relatorio.push({ massa: i + 1, linha: i + LINHA_DADOS, problemas });
    });
    return { dados: saida, relatorio, erros };
  }

  return {
    IGNORAR, LINHA_DADOS, OPCOES_PROPOSTA, normalizar, norm, brl, num, classificar, montarMapa, abrir, abaDados,
    preencher, extrair, estruturaTemplate, validar, validarLote, detectarRamo, REGRAS_GRUPO,
  };
});
