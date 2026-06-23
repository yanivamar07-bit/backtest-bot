#!/usr/bin/env python3
"""Parse 11_corriges_detailles.md and output JS data for Annales section."""
import re, json

with open("11_corriges_detailles.md", encoding="utf-8") as f:
    raw = f.read()

def clean(s):
    s = re.sub(r'\*\*(.+?)\*\*', r'\1', s)
    s = s.replace('**', '').replace('*', '')
    s = re.sub(r'`(.+?)`', r'\1', s)
    return s.strip()

def extract_word(sentence):
    m = re.search(r'\*\*(.+?)\*\*', sentence)
    return m.group(1) if m else ""

def parse_questions(content):
    """Parse Q blocks from a content section."""
    q_blocks = re.split(r'### Q\d+', content)
    questions = []
    for q_block in q_blocks[1:]:
        lines = q_block.strip().split('\n')
        if not lines:
            continue
        sentence_line = lines[0].strip().lstrip('—').strip()
        sentence_clean = clean(sentence_line)
        word = extract_word(sentence_line)

        # Find correct answer
        correct_text = ""
        for l in lines:
            m = re.search(r'✅.+?[אבגד]\) (.+)', l)
            if m:
                correct_text = clean(m.group(1))
                break

        # Find options from table (2+ columns or single column)
        opts = []
        correct_opt_idx = -1
        for l in lines:
            m = re.match(r'\|\s*\*?\*?([אבגד])\)\s*\*?\*?(.+?)\*?\*?\s*\|', l)
            if m:
                opt_text = clean(m.group(2).split('|')[0])
                opts.append(opt_text)
                if correct_text and (correct_text in opt_text or opt_text in correct_text):
                    correct_opt_idx = len(opts) - 1

        # Explanation from blockquote
        exp = ""
        for l in lines:
            if l.startswith('> '):
                exp = clean(l[2:])
                break

        if opts and len(opts) >= 2 and correct_opt_idx >= 0:
            questions.append({
                "s": sentence_clean,
                "w": word,
                "opts": opts,
                "ans": correct_opt_idx,
                "exp": exp
            })
    return questions

# Split by exam
exam_splits = re.split(r'# EXAMEN BLANC N°(\d+)', raw)
exams_raw = []
i = 1
while i < len(exam_splits):
    num = exam_splits[i]
    content = exam_splits[i+1] if i+1 < len(exam_splits) else ""
    exams_raw.append((num, content))
    i += 2

exams_out = []

for exam_num, exam_content in exams_raw:
    exam_data = {"exam": f"Examen Blanc N°{exam_num}", "sections": []}

    # Try splitting by SECTION headers
    sections = re.split(r'## SECTION ([A-C])[^\n]*\n', exam_content)

    if len(sections) > 1:
        # Has explicit section headers
        si = 1
        sec_names = {"A": "Section A — Vocabulaire", "B": "Section B — Complétion de texte", "C": "Section C — Compréhension"}
        while si < len(sections):
            sec_letter = sections[si]
            sec_content = sections[si+1] if si+1 < len(sections) else ""
            si += 2
            qs = parse_questions(sec_content)
            if qs:
                exam_data["sections"].append({
                    "name": sec_names.get(sec_letter, f"Section {sec_letter}"),
                    "questions": qs
                })
    else:
        # No section headers — treat all as Section A
        qs = parse_questions(exam_content)
        if qs:
            exam_data["sections"].append({
                "name": "Section A — Vocabulaire",
                "questions": qs
            })

    if exam_data["sections"]:
        exams_out.append(exam_data)

total_q = sum(len(s['questions']) for e in exams_out for s in e['sections'])
print(f"// Parsed {total_q} questions from {len(exams_out)} exams", flush=True)
for e in exams_out:
    for s in e["sections"]:
        print(f"//   {e['exam']} — {s['name']}: {len(s['questions'])} questions")

print("const ANNALES_DATA =", json.dumps(exams_out, ensure_ascii=False, indent=2), ";")
