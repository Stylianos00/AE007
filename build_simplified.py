#!/usr/bin/env python3
"""Παράγει το AE007/index.html από το ριζικό index.html (απλοποίηση AE007)."""
from __future__ import annotations

import re
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


def main() -> None:
    text = SRC.read_text(encoding="utf-8")

    # --- HTML: αφαίρεση οθόνης s-yli (κεφαλαιαγορά) ---
    text = re.sub(
        r"\n<!-- Ύλη: τράπεζα ΤτΕ.*?</div>\n</div>\n\n(?=<!-- Ύλη μεσίτη)",
        "\n",
        text,
        flags=re.DOTALL,
    )

    # --- Nav: μία καρτέλα ---
    text = text.replace(
        '<button class="nav-tab active" onclick="go(\'quiz\')">Αρχική</button>\n'
        '    <button class="nav-tab" onclick="go(\'yli\')">Ύλη</button>',
        '<button class="nav-tab active" onclick="go(\'quiz\')">Αρχική</button>',
    )

    # --- Κείμενο αρχικής ---
    text = text.replace(
        "Οι τέσσερις ενότητες οργανώνουν την ύλη και τα κεφάλαια· το <strong>Quiz</strong> (tab Αρχική) είναι Unit Linked ΤτΕ. Η <strong>Ύλη</strong> = μόνο κεφαλαιαγορά. Ο <strong>μεσίτης ασφαλίσεων</strong> φαίνεται δίπλα στο Quiz και <strong>στην πρώτη οθόνη του Ερωτηματολογίου</strong> (πλαίσιο με το 🛡️).",
        "Οι τέσσερις ενότητες οργανώνουν την ύλη και τα κεφάλαια· το <strong>Quiz</strong> (tab Αρχική) είναι Unit Linked ΤτΕ. Ο <strong>μεσίτης ασφαλίσεων</strong> είναι στην <strong>κάρτα Μεσίτης</strong> και <strong>στην πρώτη οθόνη του Ερωτηματολογίου</strong> (πλαίσιο με το 🛡️).",
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
    text = text.replace("let yliAct=YLI_CTX_CAP;", "let yliAct=YLI_CTX_INS;")

    text = text.replace(
        '["home","chapters","chapter","calc","quiz","yli","mesiti"].forEach',
        '["home","chapters","chapter","calc","quiz","mesiti"].forEach',
    )
    text = text.replace("const map={quiz:0,yli:1};", "const map={quiz:0};")
    text = text.replace(
        'if(name==="yli"){yliAct=YLI_CTX_CAP;showYliBrowse();loadYliManifestIfNeeded();}\n  ',
        "",
    )

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
        "  if(qTimerId){clearInterval(qTimerId);qTimerId=null;}\n"
        "  ttsStop();\n"
        "  quizTtsPlaying=false;\n"
        "  quizTtsContinuous=false;\n"
        "  ttsQuizToken++;\n"
        "  ",
        "function finishQuiz(){\n  if(qTimerId){clearInterval(qTimerId);qTimerId=null;}\n  ",
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
        "  if(!confirm(\"Θέλεις να τερματίσεις την εξάσκηση; Θα επιστρέψεις στην επιλογή ενότητας.\"))return;\n"
        "  yliTtsChainActive=false;\n"
        "  if(yliTtsPlaying){ttsUserStopYli();yliTtsPlaying=false;}\n"
        "  yliBackToBrowse();",
        "  if(!confirm(\"Θέλεις να τερματίσεις την εξάσκηση; Θα επιστρέψεις στην επιλογή ενότητας.\"))return;\n"
        "  yliBackToBrowse();",
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

    # loadYliManifestIfNeeded — μόνο insurance_yli
    old_load = """async function loadYliManifestIfNeeded(){
  const errEl=document.getElementById(yliAct.ids.loadErr);
  if(errEl){errEl.style.display="none";errEl.textContent="";}
  if(yliAct.basePath==="insurance_yli/"){
    const shared=YLI_CTX_INS.manifest||YLI_CTX_INS_QUIZ.manifest;
    if(shared){
      syncInsuranceManifestRef(shared);
      yliAct.manifest=shared;
      renderYliCategories();
      return;
    }
  }else if(yliAct.manifest){
    renderYliCategories();
    return;
  }
  try{
    const r=await fetch(yliAct.basePath+yliFetchPath("manifest.json"));
    if(!r.ok)throw new Error(r.status+" "+r.statusText);
    const data=await r.json();
    if(yliAct.basePath==="insurance_yli/")syncInsuranceManifestRef(data);
    yliAct.manifest=data;
    renderYliCategories();
  }catch(e){
    if(errEl){
      errEl.innerHTML=yliAct.errManifestHtml;
      errEl.style.display="block";
    }
  }
}"""
    new_load = """async function loadYliManifestIfNeeded(){
  const errEl=document.getElementById(yliAct.ids.loadErr);
  if(errEl){errEl.style.display="none";errEl.textContent="";}
  const shared=YLI_CTX_INS.manifest||YLI_CTX_INS_QUIZ.manifest;
  if(shared){
    syncInsuranceManifestRef(shared);
    yliAct.manifest=shared;
    renderYliCategories();
    return;
  }
  try{
    const r=await fetch(yliAct.basePath+yliFetchPath("manifest.json"));
    if(!r.ok)throw new Error(r.status+" "+r.statusText);
    const data=await r.json();
    syncInsuranceManifestRef(data);
    yliAct.manifest=data;
    renderYliCategories();
  }catch(e){
    if(errEl){
      errEl.innerHTML=yliAct.errManifestHtml;
      errEl.style.display="block";
    }
  }
}"""
    if old_load not in text:
        raise SystemExit("loadYliManifestIfNeeded: δεν ταιριάζει το αναμενόμενο μπλοκ")
    text = text.replace(old_load, new_load)

    old_render_cat = """function renderYliCategories(){
  const ctx=yliAct;
  const mount=document.getElementById(ctx.ids.catMount);
  if(!mount||!ctx.manifest||!ctx.manifest.categories){
    if(insuranceMesCtx(ctx)&&ctx.pick){
      const pp=document.getElementById(ctx.pick.panel);
      if(pp)pp.style.display="none";
    }
    return;
  }
  const pfx=ctx.pidPrefix;
  if(insuranceMesCtx(ctx)){
    const flat=[];
    for(const cat of ctx.manifest.categories){
      for(const r of yliBrowseRowsForCategory(ctx,cat))flat.push(yliBrowseRowHtml(r));
    }
    mount.innerHTML=`<div class="cgrid mes-cat-flat">${flat.join("")}</div>`;
  }else{
    mount.innerHTML=ctx.manifest.categories.map((cat,ci)=>{
      const pid=pfx+ci;
      const nq=cat.files.reduce((s,f)=>s+(f.questionCount||0),0);
      const browseRows=yliBrowseRowsForCategory(ctx,cat);
      const nFiles=(cat.files||[]).length;
      const expanded=browseRows.length>nFiles;
      const metaLabel=expanded
        ? (browseRows.length===25&&nFiles===1&&nq===601
          ? "πλήρες + 24 ενότητες · 601 ερωτήσεις"
          : `${browseRows.length} επιλογές · ${nq} ερωτήσεις`)
        : `${nFiles} αρχεία · ${nq} ερωτήσεις`;
      const rows=browseRows.map(r=>yliBrowseRowHtml(r)).join("");
      const subTail=expanded?metaLabel:`${metaLabel} · ${nq} ερωτήσεις`;
      return `<div class="psec yli-cat"><div class="phdr" onclick="toggleP('${pid}')"><div class="phdr-left"><div class="pnum teal">${ci+1}</div><div><div class="phdr-title">${yliEsc(cat.title)}</div><div class="phdr-sub">${subTail}</div></div></div><div class="parr" id="arr-${pid}">›</div></div><div class="cgrid" id="${pid}">${rows}</div></div>`;
    }).join("");
  }
  if(insuranceMesCtx(ctx))populateMesitisUnitPicker();
  else{
    const h1=document.getElementById(YLI_CTX_INS.pick.panel);
    const h2=document.getElementById(YLI_CTX_INS_QUIZ.pick.panel);
    if(h1)h1.style.display="none";
    if(h2)h2.style.display="none";
  }
}"""
    new_render_cat = """function renderYliCategories(){
  const ctx=yliAct;
  const mount=document.getElementById(ctx.ids.catMount);
  if(!mount||!ctx.manifest||!ctx.manifest.categories){
    if(insuranceMesCtx(ctx)&&ctx.pick){
      const pp=document.getElementById(ctx.pick.panel);
      if(pp)pp.style.display="none";
    }
    return;
  }
  const flat=[];
  for(const cat of ctx.manifest.categories){
    for(const r of yliBrowseRowsForCategory(ctx,cat))flat.push(yliBrowseRowHtml(r));
  }
  mount.innerHTML=`<div class="cgrid mes-cat-flat">${flat.join("")}</div>`;
  populateMesitisUnitPicker();
}"""
    if old_render_cat not in text:
        raise SystemExit("renderYliCategories: δεν ταιριάζει")
    text = text.replace(old_render_cat, new_render_cat)

    text = text.replace(
        "/* ——— Ύλη · κοινή μηχανή (κεφαλαιαγορά: yli/ · μεσίτης: insurance_yli/) ——— */",
        "/* ——— Μεσίτης / εξάσκηση: insurance_yli/ (AE007) ——— */",
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
        "/* Στυλιανός — AE007: έκδοση επίδειξης· απλούστερη από την πλήρη εφαρμογή. */\n"
        "const CHAPS=[",
        1,
    )
    text = text.replace(
        "function go(name){\n  if(name===\"appendices\")name=\"calc\";",
        "function go(name){\n"
        "  /* Στυλιανός — εδώ γίνεται η εναλλαγή οθονών (χωρίς καρτέλα «Ύλη» κεφαλαιαγοράς). */\n"
        "  if(name===\"appendices\")name=\"calc\";",
        1,
    )
    text = text.replace(
        "async function loadYliManifestIfNeeded(){\n  const errEl=",
        "async function loadYliManifestIfNeeded(){\n"
        "  /* Στυλιανός — μόνο insurance_yli· δεν φορτώνει yli/ κεφαλαιαγοράς. */\n"
        "  const errEl=",
        1,
    )
    text = text.replace(
        "function renderYliQ(){\n  const ctx=yliAct;",
        "function renderYliQ(){\n"
        "  /* Στυλιανός — κοινή απόδοση ερώτησης μεσίτη / εξάσκησης, χωρίς εκφώνηση. */\n"
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

    # Έλεγχοι υπολοίπων αναφορών TTS
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
        if bad in text:
            raise SystemExit(f"Υπολείπεται αναφορά σε: {bad}")

    OUT.write_text(text, encoding="utf-8")
    print("Έγραψε:", OUT)


if __name__ == "__main__":
    main()
