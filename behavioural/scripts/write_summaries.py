#!/usr/bin/env python3
"""Regenerate behavioural/runs/*/summary.md from the run logs.

Run from the repo root after any new sampling run. Needs no GPU and no keys:
it only reads the .jsonl files.

    python behavioural/scripts/write_summaries.py
"""
import json,glob,collections,re,os,hashlib,pathlib
FOLDER_COND={'baseline':'baseline','expert':'expert_role','urgency':'objective_emphasis','CoT':'cot',
 'hallucination':'anti_hallucination','encourage':'encouragement','nomistakes':'error_avoidance',
 'threat':'threat','substrate':'substrate_llama_v3','correct':'correct_answer'}
FILE={'baseline':'baseline.txt','expert_role':'benchmark_expert.txt','objective_emphasis':'benchmark_urgency.txt',
 'cot':'benchmark_CoT.txt','anti_hallucination':'benchmark_hallucination.txt','encouragement':'benchmark_encourage.txt',
 'error_avoidance':'benchmark_nomistakes.txt','threat':'benchmark_threat.txt',
 'substrate_llama_v3':'substrate.txt (system) + baseline.txt (user)','correct_answer':'benchmark_correct.txt'}
def act(t):
    t=t or ''
    m=re.match(r'\s*[\*\_"\'\#\-\s]*\b(walk|drive)\w*\b',t,re.I)
    if m: return m.group(1).lower()
    ms=re.findall(r'\b(walk|drive)\w*\b',t,re.I); return ms[-1].lower() if ms else None
def state(v):
    d=sum(1 for x in v if x=='drive')
    return d,len(v),('RC' if d==len(v) else ('RI' if d==0 else 'NR'))
for folder,cond in FOLDER_COND.items():
    files=sorted(glob.glob(f'behavioural/runs/{folder}/*.jsonl'))
    rows={}; errs=collections.Counter(); reissued=collections.Counter(); shas=set(); sys_shas=set()
    for f in files:
        for ln in open(f):
            if not ln.strip(): continue
            d=json.loads(ln)
            if str(d.get('error'))!='None': errs[str(d['error'])[:60]]+=1; continue
            arm='local' if d.get('backend')=='local' else 'hosted'
            k=(d['model_label'],arm,str(d['sample_index']))
            if k in rows: reissued[d['model_label']]+=1  # same arm, same sample
            if k not in rows or d['timestamp']>rows[k]['timestamp']: rows[k]=d
            if d.get('prompt_sha256'): shas.add(d['prompt_sha256'][:8])
            if d.get('system_sha256') and d['system_sha256']!='NONE': sys_shas.add(d['system_sha256'][:8])
    by=collections.defaultdict(list)
    for (m,arm,i),d in rows.items():
        by[(m,arm)].append(act(d.get('response_text')))
    L=[f"# {cond}\n"]
    L.append(f"`prompts/{FILE[cond]}`. {len(files)} files, {len(rows)} usable rows, "
             f"{len(by)} models, R=10, temperature 1.0.\n")
    L.append(f"Sent-text digest: `{'`, `'.join(sorted(shas))}`"
             + (f"; system `{'`, `'.join(sorted(sys_shas))}`" if sys_shas else "") + ".\n")
    tally=collections.Counter()
    L.append("| model | intended actions | state |")
    L.append("|---|---|---|")
    for m,arm in sorted(by):
        d,n,s=state(by[(m,arm)]); tally[s]+=1
        label=f"{m} ({arm})" if (m,'local' if arm=='hosted' else 'hosted') in by else m
        L.append(f"| {label} | {d}/{n} | {s} |")
    L.append("")
    L.append(f"RC {tally['RC']} · NR {tally['NR']} · RI {tally['RI']} "
             f"(over all {len(by)} model arms present in this folder, hosted and local counted separately).\n")
    notes=[]
    if errs:
        for e,n in errs.items(): notes.append(f"- {n} rows carry `{e}` and produce no response; excluded above.")
    if reissued:
        for m,n in reissued.items(): notes.append(f"- {m}: {n} sample(s) reissued; the later timestamp is used.")
    if notes:
        L.append("## Notes\n"); L+=notes; L.append("")
    pathlib.Path(f'behavioural/runs/{folder}/summary.md').write_text("\n".join(L))
    print(f"  {folder:16} {len(rows):>4} rows  {len(by):>2} models  RC{tally['RC']} NR{tally['NR']} RI{tally['RI']}")
