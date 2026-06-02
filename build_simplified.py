#!/usr/bin/env python3
"""Παράγει το AE007/index.html από το ριζικό index.html (AE007: χωρίς κεφαλαιαγορά, χωρίς μεσίτη, με πράκτορα + Unit Linked).

Μετά από αλλαγές στο ριζικό index.html που πρέπει να φανούν στο AE007: τρέξτε πάντα
  python3 AE007/build_simplified.py
από τη ρίζα του repo. Μην βασίζεστε σε χειροκίνητες επεξεργασίες μόνο του AE007/index.html.

Αν αλλάξουν κείμενα/nav/HTML σχόλια γύρω από s-yli ή τα tabs, ελέγξτε ότι τα
remove_between / replace παρακάτω ταιριάζουν ακόμα — δες AE007/README.md.

Για δεδομένα ύλης στο AE007 χρειάζεται μόνο ο φάκελος insurance_agent_yli/ (όχι insurance_yli/ του μεσίτη)."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "index.html"
SRC = ROOT / "index.html"


def strip_js_function_block(text: str, start_marker: str, end_before: str) -> str:
    i = text.find(start_marker)
    if i < 0:
        return text
    j = text.find(end_before, i)
    if j < 0:
        raise SystemExit(f"Δεν βρέθηκε τέλος μπλοκ μετά από: {start_marker[:40]}...")
    return text[:i] + text[j:]


def remove_const_object(text: str, name: str) -> str:
    marker = f"const {name}="
    i = text.find(marker)
    if i < 0:
        return text
    brace = text.find("{", i)
    if brace < 0:
        return text
    depth = 0
    k = brace
    while k < len(text):
        c = text[k]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                k += 1
                while k < len(text) and text[k] in " \t":
                    k += 1
                if k < len(text) and text[k] == ";":
                    k += 1
                if k < len(text) and text[k] == "\n":
                    k += 1
                return text[:i] + text[k:]
        k += 1
    return text


def remove_between(text: str, start: str, end: str) -> str:
    i = text.find(start)
    if i < 0:
        return text
    j = text.find(end, i)
    if j < 0:
        raise SystemExit(f"remove_between: λείπει τέλος μετά από {start[:50]!r}")
    return text[:i] + text[j:]


def main() -> None:
    text = SRC.read_text(encoding="utf-8")

    # --- Quiz UL: όχι «Εργαστήριο αναλυτικών λύσεων» (σύνδεμο εκτός AE007)· αυτόνομο upload GitHub ---
    text = re.sub(
        r"\n\s*<a\b[^>]*\bid\s*=\s*\"quizAnalytikesLyseisLabLink\"[\s\S]*?</a>",
        "",
        text,
        count=1,
    )

    # --- HTML: αφαίρεση οθόνης s-yli (κεφαλαιαγορά) — πριν το μπλοκ μεσίτη (υπάρχει μόνο στο πλήρες index) ---
    text = remove_between(
        text,
        "\n<!-- Τράπεζα θεμάτων κεφαλαιαγοράς:",
        "\n<!-- Ύλη μεσίτη ασφαλίσεων",
    )

    # --- HTML: αφαίρεση μεσίτη (κάρτα quiz, επιλογές quiz, κάρτα αρχικής, οθόνη s-mesiti) ---
    text = remove_between(
        text,
        '      <div id="quizModeCardMesiti"',
        '      <div id="quizModeCardPraktoras"',
    )
    text = remove_between(
        text,
        '    <div id="qMesitiOpts"',
        '    <div id="qPraktorasOpts"',
    )
    text = remove_between(
        text,
        '    <div class="card" style="cursor:pointer;min-width:0;border-color:rgba(24,95,165,0.35)" onclick="go(\'mesiti\')"',
        '    <div class="card" style="cursor:pointer;min-width:0;border-color:rgba(186,117,23,0.4)" onclick="go(\'praktoras\')"',
    )
    text = remove_between(
        text,
        "\n<!-- Ύλη μεσίτη ασφαλίσεων",
        "\n<!-- Ύλη ασφαλιστικού πράκτορα",
    )

    # --- Nav: μία καρτέλα (χωρίς τράπεζα κεφαλαιαγοράς) ---
    text = text.replace(
        '<button class="nav-tab active" onclick="go(\'quiz\')">Αρχική</button>\n'
        '    <button class="nav-tab" onclick="go(\'yli\')" title="Τράπεζα θεμάτων κεφαλαιαγοράς (ΤτΕ)">Τράπεζα θεμάτων κεφαλαιαγοράς</button>',
        '<button class="nav-tab active" onclick="go(\'quiz\')">Αρχική</button>',
    )
    text = text.replace(
        '<button class="nav-tab active" onclick="go(\'quiz\')">Αρχική</button>\n'
        '    <button class="nav-tab" onclick="go(\'yli\')">Ύλη</button>',
        '<button class="nav-tab active" onclick="go(\'quiz\')">Αρχική</button>',
    )

    # --- Κείμενο αρχικής (AE007: Unit Linked + πράκτορας, όχι μεσίτης) ---
    text = text.replace(
        "Οι τέσσερις ενότητες οργανώνουν την ύλη και τα κεφάλαια· το <strong>Quiz</strong> (tab Αρχική) περιλαμβάνει Unit Linked ΤτΕ και τις τράπεζες ασφαλίσεων (μεσίτης, πράκτορας). Η καρτέλα <strong>Τράπεζα θεμάτων κεφαλαιαγοράς</strong> περιέχει μόνο την ύλη κεφαλαιαγοράς (αρχεία ΤτΕ).</p>",
        "Οι τέσσερις ενότητες οργανώνουν την ύλη και τα κεφάλαια· το <strong>Quiz</strong> (tab Αρχική) περιλαμβάνει Unit Linked ΤτΕ και την τράπεζα <strong>ασφαλιστικού πράκτορα</strong>.</p>",
    )
    text = text.replace(
        "Οι τέσσερις ενότητες οργανώνουν την ύλη και τα κεφάλαια· το <strong>Quiz</strong> (tab Αρχική) περιλαμβάνει Unit Linked ΤτΕ και τις τράπεζες ασφαλίσεων (μεσίτης, πράκτορας). Η <strong>Ύλη</strong> = μόνο κεφαλαιαγορά.",
        "Οι τέσσερις ενότητες οργανώνουν την ύλη και τα κεφάλαια· το <strong>Quiz</strong> (tab Αρχική) περιλαμβάνει Unit Linked ΤτΕ και την τράπεζα <strong>ασφαλιστικού πράκτορα</strong>.",
    )
    text = text.replace(
        '<div style="font-size:11px;color:var(--muted)">608 θέματα · κείμενο όπως στην τράπεζα ΤτΕ (Unit Linked FINAL)</div></div>',
        '<div style="font-size:11px;color:var(--muted)">608 θέματα · Τράπεζα ΤτΕ</div></div>',
        1,
    )
    text = text.replace(
        "Τράπεζα θεμάτων για το πιστοποιητικό επαγγελματικών γνώσεων <strong>ασφαλιστικού πράκτορα</strong> (ΤτΕ). Ξεχωριστή από τη τράπεζα μεσίτη και από την ύλη κεφαλαιαγοράς. Οι 600 ερωτήσεις",
        "Τράπεζα θεμάτων για το πιστοποιητικό επαγγελματικών γνώσεων <strong>ασφαλιστικού πράκτορα</strong> (ΤτΕ). Οι 600 ερωτήσεις",
    )

    # --- CSS: αφαίρεση κανόνων μεσίτη (AE007 — μόνο πράκτορας / Unit Linked) ---
    text = text.replace(
        "#mesCatMount .citem.yli-mesitis-unit .ctitle,\n"
        "#qmCatMount .citem.yli-mesitis-unit .ctitle,\n"
        "#praCatMount .citem.yli-mesitis-unit .ctitle,\n"
        "#qmPraCatMount .citem.yli-mesitis-unit .ctitle{font-size:16px;font-weight:600;line-height:1.35}",
        "#praCatMount .citem.yli-agent-unit .ctitle,\n"
        "#qmPraCatMount .citem.yli-agent-unit .ctitle{font-size:16px;font-weight:600;line-height:1.35}",
    )
    text = text.replace(
        ".quiz-mode-card.mesiti{border-color:rgba(24,95,165,0.35)}\n"
        ".quiz-mode-card.mesiti:hover{border-color:var(--blue2);background:rgba(24,95,165,0.1)}\n",
        "",
    )
    text = text.replace(
        ".quiz-mode-card.quiz-mode-selected-mesiti{border-color:rgba(55,138,221,0.85);\n"
        "  box-shadow:\n"
        "    0 8px 28px rgba(0,0,0,0.32),\n"
        "    0 2px 10px rgba(0,0,0,0.2),\n"
        "    0 0 0 2px rgba(24,95,165,0.55),\n"
        "    inset 0 1px 0 rgba(255,255,255,0.08)}\n"
        ".quiz-mode-card.mesiti.quiz-mode-selected-mesiti:hover{border-color:rgba(55,138,221,0.95);background:rgba(24,95,165,0.12)}\n",
        "",
    )
    text = text.replace(
        "#qMesitiOpts.quiz-options-accent-mesiti #qmBrowse{\n"
        "  padding:14px 16px 16px;\n"
        "  border-radius:14px;\n"
        "  border:1px solid rgba(55,138,221,0.55);\n"
        "  background:rgba(24,95,165,0.1);\n"
        "  box-shadow:\n"
        "    0 8px 28px rgba(0,0,0,0.32),\n"
        "    0 2px 10px rgba(0,0,0,0.2),\n"
        "    0 0 0 2px rgba(24,95,165,0.38),\n"
        "    inset 0 1px 0 rgba(255,255,255,0.08)}\n",
        "",
    )
    text = text.replace(
        "#qMesitiOpts.quiz-options-accent-mesiti #qmMesitiFooter{\n"
        "  margin-top:12px;\n"
        "  padding:14px 16px;\n"
        "  border-radius:14px;\n"
        "  border:1px solid rgba(55,138,221,0.5);\n"
        "  background:rgba(24,95,165,0.08);\n"
        "  box-shadow:\n"
        "    0 4px 18px rgba(0,0,0,0.22),\n"
        "    0 0 0 1px rgba(24,95,165,0.22),\n"
        "    inset 0 1px 0 rgba(255,255,255,0.06)}\n",
        "",
    )
    text = text.replace(
        "#qmMesUnitMenu .quiz-chapter-menu-row .quiz-chapter-done-cb,\n"
        "#mesUnitMenu .quiz-chapter-menu-row .quiz-chapter-done-cb{accent-color:var(--blue2)}\n",
        "",
    )
    text = text.replace(
        "#mesUnitMenu .quiz-chapter-item.yli-mesitis-unit,\n"
        "#qmMesUnitMenu .quiz-chapter-item.yli-mesitis-unit,\n"
        "#praUnitMenu .quiz-chapter-item.yli-mesitis-unit,\n"
        "#qmPraUnitMenu .quiz-chapter-item.yli-mesitis-unit{font-size:15px;font-weight:600;line-height:1.35}",
        "#praUnitMenu .quiz-chapter-item.yli-agent-unit,\n"
        "#qmPraUnitMenu .quiz-chapter-item.yli-agent-unit{font-size:15px;font-weight:600;line-height:1.35}",
    )
    text = text.replace(
        'html[data-time-theme="day"] .quiz-mode-card.mesiti:hover{border-color:var(--blue2);background:rgba(24,95,165,0.08)}\n',
        "",
    )
    text = text.replace(
        'html[data-time-theme="day"] .quiz-mode-card.quiz-mode-selected-mesiti{\n'
        "  box-shadow:\n"
        "    0 6px 22px rgba(30,50,40,0.1),\n"
        "    0 2px 8px rgba(30,50,40,0.06),\n"
        "    0 0 0 2px rgba(24,95,165,0.42),\n"
        "    inset 0 1px 0 rgba(255,255,255,0.75)}\n",
        "",
    )
    text = text.replace(
        'html[data-time-theme="day"] #qMesitiOpts.quiz-options-accent-mesiti #qmBrowse{\n'
        "  border-color:rgba(55,138,221,0.45);\n"
        "  background:rgba(24,95,165,0.06);\n"
        "  box-shadow:\n"
        "    0 6px 22px rgba(30,50,40,0.09),\n"
        "    0 2px 8px rgba(30,50,40,0.06),\n"
        "    0 0 0 2px rgba(24,95,165,0.32),\n"
        "    inset 0 1px 0 rgba(255,255,255,0.75)}\n",
        "",
    )
    text = text.replace(
        'html[data-time-theme="day"] #qMesitiOpts.quiz-options-accent-mesiti #qmMesitiFooter{\n'
        "  border-color:rgba(55,138,221,0.42);\n"
        "  background:rgba(24,95,165,0.05);\n"
        "  box-shadow:0 2px 10px rgba(30,50,40,0.06),0 0 0 1px rgba(24,95,165,0.16),inset 0 1px 0 rgba(255,255,255,0.65)}\n",
        "",
    )

    # --- JS: loadYliManifestIfNeeded — μόνο insurance_agent_yli ---
    text = re.sub(
        r"async function loadYliManifestIfNeeded\(\)\{[\s\S]*?\n\}\n\nfunction insuranceBankExpandRows",
        """async function loadYliManifestIfNeeded(){
  const errEl=document.getElementById(yliAct.ids.loadErr);
  if(errEl){errEl.style.display="none";errEl.textContent="";}
  const shared=YLI_CTX_AGENT.manifest||YLI_CTX_AGENT_QUIZ.manifest;
  if(shared){
    syncAgentManifestRef(shared);
    yliAct.manifest=shared;
    renderYliCategories();
    return;
  }
  try{
    const r=await fetch(yliAct.basePath+yliFetchPath("manifest.json"));
    if(!r.ok)throw new Error(r.status+" "+r.statusText);
    const data=await r.json();
    syncAgentManifestRef(data);
    yliAct.manifest=data;
    renderYliCategories();
  }catch(e){
    if(errEl){
      errEl.innerHTML=yliAct.errManifestHtml;
      errEl.style.display="block";
    }
  }
}

function insuranceBankExpandRows""",
        text,
        count=1,
    )

    # --- JS: renderYliCategories — μόνο πράκτορας ---
    text = re.sub(
        r"function renderYliCategories\(\)\{[\s\S]*?\n\}\n\nfunction formatMesitisQuestionCount",
        """function renderYliCategories(){
  const ctx=yliAct;
  const mount=document.getElementById(ctx.ids.catMount);
  if(!mount||!ctx.manifest||!ctx.manifest.categories){
    if(insuranceAgentCtx(ctx)&&ctx.pick){
      const pp=document.getElementById(ctx.pick.panel);
      if(pp)pp.style.display="none";
    }
    return;
  }
  const flat=[];
  for(const cat of ctx.manifest.categories){
    for(const r of yliBrowseRowsForCategory(ctx,cat))flat.push(yliBrowseRowHtml(r));
  }
  mount.innerHTML=`<div class="cgrid agent-cat-flat">${flat.join("")}</div>`;
  populatePraktorasUnitPicker();
}

function formatAgentQuestionCount""",
        text,
        count=1,
    )

    # --- JS: αφαίρεση συναρτήσεων μεσίτη / MES ---
    text = strip_js_function_block(
        text,
        "function resetQuizMesitiBrowseState(){",
        "function resetQuizPraktorasBrowseState(){",
    )
    text = strip_js_function_block(
        text,
        "function cancelMesitiQuizOpts(){",
        "function cancelPraktorasQuizOpts(){",
    )
    text = strip_js_function_block(
        text,
        "function startMesitiMode(){",
        "function startPraktorasMode(){",
    )
    text = strip_js_function_block(
        text,
        "function setMesUnitCountForIndex(i,pick){",
        "function syncMesUnitTriggerLabel(pick){",
    )
    text = strip_js_function_block(
        text,
        "function syncMesUnitTriggerLabel(pick){",
        "function refreshMesUnitAriaSelected(pick){",
    )
    text = strip_js_function_block(
        text,
        "function refreshMesUnitAriaSelected(pick){",
        "const MES_PICK_BIND=",
    )
    text = strip_js_function_block(
        text,
        "function initMesitisUnitPicker(){",
        "function findMesitis601File(manifest){",
    )
    text = strip_js_function_block(
        text,
        "function findMesitis601File(manifest){",
        "function findPraktoras600File(manifest){",
    )
    text = strip_js_function_block(
        text,
        "function populateMesitisUnitPicker(){",
        "function openMesitisSelectedFromPicker(which){",
    )
    text = strip_js_function_block(
        text,
        "function openMesitisSelectedFromPicker(which){",
        "function flattenYliPayload(data){",
    )
    text = strip_js_function_block(
        text,
        "function mesUnitReadMap(){",
        "function praUnitReadMap(){",
    )
    text = strip_js_function_block(
        text,
        "function mesUnitSetRead(title,on){",
        "function praUnitSetRead(title,on){",
    )
    text = strip_js_function_block(
        text,
        "function mesUnitIsRead(title){",
        "function praUnitIsRead(title){",
    )

    text = text.replace("let MESITIS_UNIT_PICK_ROWS=[];\n", "")
    text = text.replace(
        "const MES_PICK_BIND=[YLI_CTX_INS.pick,YLI_CTX_INS_QUIZ.pick];\n", ""
    )

    text = remove_const_object(text, "YLI_CTX_INS_QUIZ")
    text = remove_const_object(text, "YLI_CTX_INS")

    text = re.sub(
        r"\nfunction syncInsuranceManifestRef\(data\)\{[^\}]+\}\n",
        "\n",
        text,
    )
    text = re.sub(
        r"\nfunction insuranceMesCtx\(ctx\)\{[^\}]+\}\n",
        "\n",
        text,
    )
    text = text.replace(
        "function insuranceAuxCtx(ctx){\n  return insuranceMesCtx(ctx)||insuranceAgentCtx(ctx);\n}",
        "function insuranceAuxCtx(ctx){\n  return insuranceAgentCtx(ctx);\n}",
    )

    text = text.replace(
        "function insuranceQuizYliExit(){\n"
        "  if(yliAct!==YLI_CTX_INS_QUIZ&&yliAct!==YLI_CTX_AGENT_QUIZ)return;",
        "function insuranceQuizYliExit(){\n  if(yliAct!==YLI_CTX_AGENT_QUIZ)return;",
    )
    # Μετά το strip του TTS δεν υπάρχουν yliTtsPlaying / ttsUserStopYli — αφαίρεση αναφορών
    text = text.replace(
        "function insuranceQuizYliExit(){\n"
        "  if(yliAct!==YLI_CTX_AGENT_QUIZ)return;\n"
        "  if(!confirm(\"Θέλεις να τερματίσεις την εξάσκηση; Θα επιστρέψεις στην επιλογή ενότητας.\"))return;\n"
        "  yliTtsChainActive=false;\n"
        "  if(yliTtsPlaying){ttsUserStopYli();yliTtsPlaying=false;}\n"
        "  yliBackToBrowse();\n"
        "}\n",
        "function insuranceQuizYliExit(){\n"
        "  if(yliAct!==YLI_CTX_AGENT_QUIZ)return;\n"
        "  if(!confirm(\"Θέλεις να τερματίσεις την εξάσκηση; Θα επιστρέψεις στην επιλογή ενότητας.\"))return;\n"
        "  yliBackToBrowse();\n"
        "}\n",
    )

    text = text.replace(
        "  if(yliAct===YLI_CTX_INS_QUIZ){\n"
        "    const foot=document.getElementById(\"qmMesitiFooter\");\n"
        "    if(foot)foot.style.display=\"flex\";\n"
        "  }\n"
        "  if(yliAct===YLI_CTX_AGENT_QUIZ){",
        "  if(yliAct===YLI_CTX_AGENT_QUIZ){",
    )

    text = text.replace(
        "      let sid=\"mes\";\n"
        "      if(ctx===YLI_CTX_INS_QUIZ)sid=\"qmMes\";\n"
        "      else if(ctx===YLI_CTX_AGENT_QUIZ)sid=\"qmPra\";\n"
        "      else if(ctx===YLI_CTX_AGENT)sid=\"pra\";",
        "      let sid=\"pra\";\n"
        "      if(ctx===YLI_CTX_AGENT_QUIZ)sid=\"qmPra\";",
    )

    text = text.replace(
        "    if(ctx===YLI_CTX_INS_QUIZ){\n"
        "      const g=document.querySelector(\"#s-quiz .quiz-mode-grid\");\n"
        "      if(g)g.style.display=\"none\";\n"
        "      const foot=document.getElementById(\"qmMesitiFooter\");\n"
        "      if(foot)foot.style.display=\"none\";\n"
        "    }\n"
        "    if(ctx===YLI_CTX_AGENT_QUIZ){",
        "    if(ctx===YLI_CTX_AGENT_QUIZ){",
    )

    text = text.replace(
        "  if(ctx===YLI_CTX_INS_QUIZ||ctx===YLI_CTX_AGENT_QUIZ){",
        "  if(ctx===YLI_CTX_AGENT_QUIZ){",
    )
    text = text.replace(
        "if(yliAct===YLI_CTX_INS_QUIZ||yliAct===YLI_CTX_AGENT_QUIZ)updateQuizHomeCheckedFooters();",
        "if(yliAct===YLI_CTX_AGENT_QUIZ)updateQuizHomeCheckedFooters();",
    )
    text = text.replace(
        """  const mesFoot=document.getElementById("quizMesCheckedFooter");
  if(mesFoot&&MESITIS_UNIT_PICK_ROWS&&MESITIS_UNIT_PICK_ROWS.length){
    const mm=mesUnitReadMap();
    const tot=insuranceBankTotalQuestionCount(MESITIS_UNIT_PICK_ROWS);
    const checked=insuranceBankCheckedQuestionSum(MESITIS_UNIT_PICK_ROWS,mm);
    mesFoot.textContent="Τσεκαρισμένες ερωτήσεις · "+checked+" / "+tot;
  }
""",
        "",
    )

    SET_QUIZ_MODE = """function setQuizModeSelection(mode){
  const ul=document.getElementById("quizModeCardUl");
  const pr=document.getElementById("quizModeCardPraktoras");
  const catOpts=document.getElementById("qCatOpts");
  const praOpts=document.getElementById("qPraktorasOpts");
  if(catOpts){
    catOpts.classList.remove("quiz-options-accent-ul");
  }
  if(praOpts){
    praOpts.classList.remove("quiz-options-accent-praktoras");
  }
  if(ul){
    ul.classList.remove("quiz-mode-selected-ul");
    ul.setAttribute("aria-pressed","false");
  }
  if(pr){
    pr.classList.remove("quiz-mode-selected-praktoras");
    pr.setAttribute("aria-pressed","false");
  }
  if(mode==="ul"&&ul){
    ul.classList.add("quiz-mode-selected-ul");
    ul.setAttribute("aria-pressed","true");
    if(catOpts)catOpts.classList.add("quiz-options-accent-ul");
  }
  if(mode==="praktoras"&&pr){
    pr.classList.add("quiz-mode-selected-praktoras");
    pr.setAttribute("aria-pressed","true");
    if(praOpts)praOpts.classList.add("quiz-options-accent-praktoras");
  }
}"""
    text = re.sub(
        r"function setQuizModeSelection\(mode\)\{[\s\S]*?\n\}\n\nfunction cancelQuizCatOpts",
        SET_QUIZ_MODE + "\n\nfunction cancelQuizCatOpts",
        text,
        count=1,
    )

    text = text.replace(
        "function showQuizStart(){\n  ttsStop();\n  quizTtsPlaying=false;\n  quizTtsContinuous=false;\n  ttsQuizToken++;\n  "
        'document.getElementById("qStart").style.display="block";\n'
        '  document.getElementById("qRun").style.display="none";\n'
        '  document.getElementById("qRes").style.display="none";\n'
        '  document.getElementById("qCatOpts").style.display="none";\n'
        '  document.getElementById("qMesitiOpts").style.display="none";\n'
        '  document.getElementById("qPraktorasOpts").style.display="none";\n'
        "  resetQuizMesitiBrowseState();\n"
        "  resetQuizPraktorasBrowseState();\n"
        "  setQuizModeSelection(null);\n"
        "}",
        "function showQuizStart(){\n"
        '  document.getElementById("qStart").style.display="block";\n'
        '  document.getElementById("qRun").style.display="none";\n'
        '  document.getElementById("qRes").style.display="none";\n'
        '  document.getElementById("qCatOpts").style.display="none";\n'
        '  document.getElementById("qPraktorasOpts").style.display="none";\n'
        "  resetQuizPraktorasBrowseState();\n"
        "  setQuizModeSelection(null);\n"
        "}",
    )

    text = text.replace(
        "function startQuizMode(){\n"
        '  document.getElementById("qMesitiOpts").style.display="none";\n'
        '  document.getElementById("qPraktorasOpts").style.display="none";\n'
        "  resetQuizMesitiBrowseState();\n"
        "  resetQuizPraktorasBrowseState();\n"
        "  setQuizModeSelection(\"ul\");\n"
        '  document.getElementById("qCatOpts").style.display="block";\n'
        "  updateCatChapterCount();\n"
        "}",
        "function startQuizMode(){\n"
        '  document.getElementById("qPraktorasOpts").style.display="none";\n'
        "  resetQuizPraktorasBrowseState();\n"
        "  setQuizModeSelection(\"ul\");\n"
        '  document.getElementById("qCatOpts").style.display="block";\n'
        "  updateCatChapterCount();\n"
        "}",
    )

    text = text.replace(
        "function startPraktorasMode(){\n"
        '  setQuizModeSelection("praktoras");\n'
        '  document.getElementById("qCatOpts").style.display="none";\n'
        '  document.getElementById("qMesitiOpts").style.display="none";\n'
        '  document.getElementById("qPraktorasOpts").style.display="block";\n'
        "  yliAct=YLI_CTX_AGENT_QUIZ;\n"
        "  loadYliManifestIfNeeded();\n"
        "}",
        "function startPraktorasMode(){\n"
        '  setQuizModeSelection("praktoras");\n'
        '  document.getElementById("qCatOpts").style.display="none";\n'
        '  document.getElementById("qPraktorasOpts").style.display="block";\n'
        "  yliAct=YLI_CTX_AGENT_QUIZ;\n"
        "  loadYliManifestIfNeeded();\n"
        "}",
    )

    text = text.replace(
        '["home","chapters","chapter","calc","quiz","yli","mesiti","praktoras"].forEach',
        '["home","chapters","chapter","calc","quiz","praktoras"].forEach',
    )
    text = text.replace("const map={quiz:0,yli:1};", "const map={quiz:0};")
    text = text.replace(
        'if(name==="yli"){yliAct=YLI_CTX_CAP;showYliBrowse();loadYliManifestIfNeeded();}\n  ',
        "",
    )
    text = text.replace(
        'if(name==="mesiti"){yliAct=YLI_CTX_INS;showYliBrowse();loadYliManifestIfNeeded();}\n  ',
        "",
    )

    # --- CSS: αχρησιμοποίητα TTS (προαιρετικό καθάρισμα) ---
    text = re.sub(
        r"\.qtts-bar\{[^}]+\}[^\n]*\n"
        r"\.qtts-bar \.tts-auto\{[^}]+\}[^\n]*\n"
        r"\.qtts-bar \.tts-auto input\{[^}]+\}[^\n]*\n"
        r"\.qtts-hint\{[^}]+\}[^\n]*\n",
        "",
        text,
    )

    # --- Μεταβλητές quiz (χωρίς TTS) ---
    text = text.replace(
        "let QBANK=null,qIdx=0,qScore=0,qAns=false,qList=[],qTimerId=null,qTimerMins=0,qTimerSecs=0,qAnsByIdx={},qTimerPaused=false,qLastWrongList=[],qShuffleQuestionOrder=false,qShuffleAnswers=false,qOptOrderByIdx={},ttsQuizToken=0,ttsYliToken=0,qTtsExplain=false,quizInlineExpl=false,quizTtsPlaying=false,quizTtsContinuous=false,yliTtsPlaying=false,yliTtsChainActive=false,yliInlineExpl=false;",
        "let QBANK=null,qIdx=0,qScore=0,qAns=false,qList=[],qTimerId=null,qTimerMins=0,qTimerSecs=0,qAnsByIdx={},qTimerPaused=false,qLastWrongList=[],qShuffleQuestionOrder=false,qShuffleAnswers=false,qOptOrderByIdx={};",
    )

    text = remove_const_object(text, "YLI_CTX_CAP")
    text = text.replace("let yliAct=YLI_CTX_CAP;", "let yliAct=YLI_CTX_AGENT;")

    text = text.replace(
        "function showQuizStart(){\n  ttsStop();\n  quizTtsPlaying=false;\n  quizTtsContinuous=false;\n  ttsQuizToken++;\n  ",
        "function showQuizStart(){\n  ",
    )
    text = text.replace(
        "  qShuffleAnswers=!!document.getElementById(\"catShuffleAns\").checked;\n"
        "  quizInlineExpl=!!(localStorage.getItem(\"catTtsExplain\")===\"1\"||localStorage.getItem(\"ttsQuizExplPlus\")===\"1\");\n"
        "  qTtsExplain=quizInlineExpl;\n"
        "  quizTtsPlaying=false;\n"
        "  quizTtsContinuous=false;\n"
        "  const copy=filtered.slice();",
        "  qShuffleAnswers=!!document.getElementById(\"catShuffleAns\").checked;\n"
        "  const copy=filtered.slice();",
    )
    text = text.replace(
        "qIdx=0;qScore=0;qAns=false;qAnsByIdx={};qOptOrderByIdx={};qTimerPaused=false;quizTtsContinuous=false;",
        "qIdx=0;qScore=0;qAns=false;qAnsByIdx={};qOptOrderByIdx={};qTimerPaused=false;",
    )
    text = text.replace(
        "function finishQuiz(){\n"
        "  clearUlQuizState();\n"
        "  if(qTimerId){clearInterval(qTimerId);qTimerId=null;}\n"
        "  ttsStop();\n"
        "  quizTtsPlaying=false;\n"
        "  quizTtsContinuous=false;\n"
        "  ttsQuizToken++;\n"
        "  ",
        "function finishQuiz(){\n"
        "  clearUlQuizState();\n"
        "  if(qTimerId){clearInterval(qTimerId);qTimerId=null;}\n"
        "  ",
    )
    text = text.replace(
        "function renderQ(){\n"
        "  if(qIdx>=qList.length){finishQuiz();return;}\n"
        "  ttsQuizToken++;\n"
        "  ttsStop();\n"
        "  const q=qList[qIdx];\n"
        "  quizInlineExpl=!!(localStorage.getItem(\"catTtsExplain\")===\"1\"||localStorage.getItem(\"ttsQuizExplPlus\")===\"1\");\n"
        "  qTtsExplain=quizInlineExpl;\n"
        "  const orderKeys=optionKeysForQuestion(q,qIdx);",
        "function renderQ(){\n"
        "  if(qIdx>=qList.length){finishQuiz();return;}\n"
        "  const q=qList[qIdx];\n"
        "  const orderKeys=optionKeysForQuestion(q,qIdx);",
    )
    text = text.replace(
        '      <div class="qmeta-tts-inline">${quizTtsInlineRowHtml()}</div>',
        '      <div class="qmeta-tts-inline"></div>',
    )
    text = text.replace(
        "function quizPrev(){\n"
        "  if(quizTtsPlaying){ttsUserStopQuiz();quizTtsPlaying=false;}\n"
        "  quizTtsContinuous=false;\n"
        "  if(qIdx<=0)return;",
        "function quizPrev(){\n  if(qIdx<=0)return;",
    )
    text = text.replace(
        "function quizNext(){\n"
        "  if(quizTtsPlaying){ttsUserStopQuiz();quizTtsPlaying=false;}\n"
        "  quizTtsContinuous=false;\n"
        "  if(qIdx>=qList.length-1){finishQuiz();return;}",
        "function quizNext(){\n  if(qIdx>=qList.length-1){finishQuiz();return;}",
    )
    text = text.replace(
        "function showYliBrowse(){\n"
        "  ttsStop();\n"
        "  yliTtsChainActive=false;\n"
        "  yliTtsPlaying=false;\n"
        "  ttsYliToken++;\n"
        "  const id=yliAct.ids;",
        "function showYliBrowse(){\n  const id=yliAct.ids;",
    )

    text = text.replace(
        "/* ——— Ύλη · κοινή μηχανή (κεφαλαιαγορά: yli/ · μεσίτης: insurance_yli/ · πράκτορας: insurance_agent_yli/) ——— */",
        "/* ——— Ασφαλιστικός πράκτορας: insurance_agent_yli/ (AE007) ——— */",
    )

    # Αφαίρεση όλου του μπλοκ TTS πριν το initTtsUi
    text = strip_js_function_block(text, "function ttsStop(){", "function initTtsUi(){")
    text = text.replace(
        "function initTtsUi(){\n"
        "  if(window.speechSynthesis)speechSynthesis.getVoices();\n"
        "  const explOn=localStorage.getItem(\"catTtsExplain\")===\"1\"||localStorage.getItem(\"ttsQuizExplPlus\")===\"1\";\n"
        "  quizInlineExpl=explOn;\n"
        "  qTtsExplain=quizInlineExpl;\n"
        "}",
        "function initTtsUi(){}",
    )

    text = text.replace(
        "function renderYliQ(){\n"
        "  ttsYliToken++;\n"
        "  ttsStop();\n"
        "  const ctx=yliAct;",
        "function renderYliQ(){\n  const ctx=yliAct;",
    )
    text = text.replace(
        '    }else{\n      sub+=" (με τη σειρά των φύλλων). Οι επιλογές δεν ανακατεύτηκαν.";\n    }',
        "    }",
    )
    text = text.replace(
        "  const q=ctx.list[ctx.idx];\n"
        "  quizInlineExpl=!!(localStorage.getItem(\"catTtsExplain\")===\"1\"||localStorage.getItem(\"ttsQuizExplPlus\")===\"1\");\n"
        "  const order=yliOptOrder(q,ctx.idx);",
        "  const q=ctx.list[ctx.idx];\n  const order=yliOptOrder(q,ctx.idx);",
    )
    text = text.replace(
        '      <div class="qmeta-tts-inline">${yliTtsInlineRowHtml(id.area)}</div>',
        '      <div class="qmeta-tts-inline"></div>',
    )
    text = text.replace(
        "function yliPrev(){\n"
        "  const ctx=yliAct;\n"
        "  if(ctx.idx<=0)return;\n"
        "  yliTtsChainActive=false;\n"
        "  if(yliTtsPlaying){ttsUserStopYli();yliTtsPlaying=false;}\n"
        "  ctx.idx--;",
        "function yliPrev(){\n  const ctx=yliAct;\n  if(ctx.idx<=0)return;\n  ctx.idx--;",
    )
    text = text.replace(
        "function yliNext(){\n"
        "  const ctx=yliAct;\n"
        "  yliTtsChainActive=false;\n"
        "  if(yliTtsPlaying){ttsUserStopYli();yliTtsPlaying=false;}\n"
        "  if(ctx.idx>=ctx.list.length-1){",
        "function yliNext(){\n  const ctx=yliAct;\n  if(ctx.idx>=ctx.list.length-1){",
    )

    text = text.replace(
        'window.addEventListener("load",()=>{\n'
        "  initTtsUi();\n"
        '  if(window.speechSynthesis)speechSynthesis.addEventListener("voiceschanged",()=>speechSynthesis.getVoices());\n'
        "  initThemeControls();",
        'window.addEventListener("load",()=>{\n  initTtsUi();\n  initThemeControls();',
    )

    # Σχόλια Στυλιανός (διάσπαρτα)
    text = text.replace(
        "<script>\nconst CHAPS=[",
        "<script>\n"
        "/* Στυλιανός — AE007: έκδοση επίδειξης· Unit Linked + πράκτορας (χωρίς μεσίτη / χωρίς ύλη κεφαλαιαγοράς). */\n"
        "const CHAPS=[",
        1,
    )
    text = text.replace(
        "function go(name){\n  if(name===\"appendices\")name=\"calc\";",
        "function go(name){\n"
        "  /* Στυλιανός — εναλλαγή οθονών (χωρίς καρτέλα «Ύλη» κεφαλαιαγοράς). */\n"
        "  if(name===\"appendices\")name=\"calc\";",
        1,
    )
    text = text.replace(
        "async function loadYliManifestIfNeeded(){\n  const errEl=",
        "async function loadYliManifestIfNeeded(){\n"
        "  /* Στυλιανός — μόνο insurance_agent_yli. */\n"
        "  const errEl=",
        1,
    )
    text = text.replace(
        "function renderYliQ(){\n  const ctx=yliAct;",
        "function renderYliQ(){\n"
        "  /* Στυλιανός — ερώτηση πράκτορα / εξάσκησης, χωρίς εκφώνηση. */\n"
        "  const ctx=yliAct;",
        1,
    )
    text = text.replace(
        "function launchCategories(){\n  if(!QBANK){loadQuestionBank();setTimeout(launchCategories,500);return;}",
        "function launchCategories(){\n"
        "  /* Στυλιανός — εκκίνηση quiz Unit Linked από επιλεγμένο κεφάλαιο. */\n"
        "  if(!QBANK){loadQuestionBank();setTimeout(launchCategories,500);return;}",
        1,
    )
    text = text.replace(
        'window.addEventListener("load",()=>{\n  initTtsUi();\n  initThemeControls();',
        'window.addEventListener("load",()=>{\n'
        "  /* Στυλιανός — αρχικοποίηση· το TTS αφαιρέθηκε σκόπιμα σε αυτή την έκδοση. */\n"
        "  initTtsUi();\n  initThemeControls();",
        1,
    )

    text = text.replace(
        'function htmlEsc(s){\n  return String(s??"").replace(/&/g,"&amp;")',
        'function htmlEsc(s){\n'
        '  /* Stylianos — ασφαλής εμφάνιση κειμένου στο HTML */\n'
        '  return String(s??"").replace(/&/g,"&amp;")',
        1,
    )

    # --- JS: ουδέτερα ονόματα (χωρίς μεσίτη / mesitis στο UI) ---
    text = text.replace("formatMesitisQuestionCount", "formatAgentQuestionCount")
    # Οι σταθερές LS_MES_* ήταν για τον μεσίτη· ο σχετικός κώδικας αφαιρείται — όχι μετονομασία σε LS_PRA (θα έκανε διπλή δήλωση με τα LS_PRA του πράκτορα).
    text = text.replace(
        'const LS_MES_UNIT_READ="axiaXronou_mesitis_unit_read_v1";\n'
        'const LS_MES_UNIT_LAST_IDX="axiaXronou_mesitis_unit_last_idx_v1";\n',
        "",
    )
    text = text.replace("yli-mesitis-unit", "yli-agent-unit")
    text = text.replace("mesitis-picker-full", "agent-picker-full")
    text = text.replace("mesitisUnit", "unitChapter")
    text = text.replace("mes-cat-flat", "agent-cat-flat")

    # CSS: γραμμές που αφορούσαν μόνο TTS / banner ακρόασης
    filtered: list[str] = []
    for line in text.splitlines(keepends=True):
        s = line.lstrip()
        if s.startswith(".q-tts-inline{") or s.startswith(".q-tts-pp{") or s.startswith(
            ".q-tts-pp:hover"
        ):
            continue
        if s.startswith(".q-tts-pick,.q-tts-plus{") or s.startswith(".q-tts-pick:hover"):
            continue
        if s.startswith(".q-tts-pick.is-on") or s.startswith(".q-tts-plus:hover"):
            continue
        if s.startswith(".q-tts-plus{") or s.startswith(".q-tts-warn{"):
            continue
        if s.startswith('html[data-time-theme="day"] .q-tts'):
            continue
        if s.startswith(".qmeta-tts-inline"):
            continue
        if s.startswith(".listen-banner{") or s.startswith(
            'html[data-time-theme="day"] .listen-banner{'
        ):
            continue
        filtered.append(line)
    text = "".join(filtered)

    # AE007: χωρίς analytikes-lab — αφαίρεση CSS της κάρτας-συνδέσμου (νεκρό μετά το strip του anchor)
    text = text.replace(
        """.quiz-lab-link-card{
  display:block;
  text-decoration:none;
  color:inherit;
  cursor:pointer;
  background:linear-gradient(135deg,var(--navy2) 0%,rgba(18,34,52,0.98) 100%);
  border:1px solid rgba(255,94,121,0.38);
  border-radius:14px;
  padding:20px;
  transition:border-color .25s,background .25s,box-shadow .25s;
  min-width:0;
  box-shadow:0 8px 28px rgba(0,0,0,0.28),0 0 0 1px rgba(255,77,106,0.08),inset 0 1px 0 rgba(255,255,255,0.05);
}
.quiz-lab-link-card:hover{border-color:rgba(255,120,148,0.55);background:rgba(255,77,106,0.09);box-shadow:0 8px 28px rgba(0,0,0,0.3),0 0 26px -6px rgba(255,56,92,0.35),inset 0 1px 0 rgba(255,255,255,0.06)}
.quiz-lab-link-card:focus-visible{outline:2px solid var(--teal2);outline-offset:2px}
.quiz-lab-link-card h3{font-size:14px;margin:0;color:var(--white);font-weight:600;letter-spacing:0.01em}
html[data-time-theme="day"] .quiz-lab-link-card{
  background:linear-gradient(135deg,var(--navy2) 0%,#f8fafc 8%);
  box-shadow:
    0 6px 22px rgba(30,50,40,0.09),
    0 2px 8px rgba(30,50,40,0.06),
    0 0 0 1px rgba(255,106,138,0.2),
    inset 0 1px 0 rgba(255,255,255,0.75);
}
html[data-time-theme="day"] .quiz-lab-link-card:hover{
  border-color:rgba(255,106,138,0.5);
  background:rgba(255,77,106,0.06);
}
""",
        "",
    )

    # Έλεγχοι υπολοίπων αναφορών TTS (με \\b ώστε να μην ταιριάζει yliTts μέσα σε yliTtsInlineRowHtml κ.λπ.)
    for bad in (
        "speechSynthesis",
        "ttsStop",
        "quizTts",
        "yliTts",
        "ttsQuiz",
        "ttsYli",
        "quizInlineExpl",
        "qTtsExplain",
        "yliTtsChain",
    ):
        if re.search(rf"\b{re.escape(bad)}\b", text):
            raise SystemExit(f"Υπολείπεται αναφορά σε: {bad}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")

    # --- Δεδομένα αυτόνομης λειτουργίας (GitHub)· χωρίς εξάρτηση από γονικό AxiaXronou ---
    QBANK_SRC = ROOT / "questions_bank.json"
    QBANK_DST = OUT.parent / "questions_bank.json"
    if QBANK_SRC.is_file():
        shutil.copy2(QBANK_SRC, QBANK_DST)
        print("Αντίγραφο:", QBANK_DST)
    else:
        print("Προειδοποίηση: δεν υπήρχε", QBANK_SRC)

    THEORIA_SRC = ROOT / "theoria"
    THEORIA_DST = OUT.parent / "theoria"
    if THEORIA_SRC.is_dir():
        if THEORIA_DST.exists():
            shutil.rmtree(THEORIA_DST)
        shutil.copytree(THEORIA_SRC, THEORIA_DST)
        print("Αντίγραφο:", THEORIA_DST)
    else:
        print("Προειδοποίηση: δεν υπήρχε φάκελος", THEORIA_SRC)

    print("Έγραψε:", OUT)


if __name__ == "__main__":
    main()
