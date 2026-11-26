#!/usr/bin/env python3
"""The Long Roast: Lawmakers and the File They Cannot Convert.

One satirical sentence (1-320 chars) roasting lawmakers who would regulate
AI, crypto or the internet but cannot convert a file to PDF. The program
scores ten fresh candidates against the judge's published criteria, in the
judge's own order, and writes the winner to /output/entry.txt.
"""

import os

# --- 10 fresh candidates, each one sentence, each <= 320 chars -----------
CANDIDATES = [
    # 1: the staffer who converts the report ends up writing the AI law.
    "The committee that wants to regulate artificial intelligence just spent forty minutes trying to turn its own report into a PDF, and the staffer who finally did it is now writing the AI law for them.",
    # 2: the hearing waits while the witness list goes print -> scan -> email.
    "Congress will hold a hearing on the future of AI next Tuesday, once someone in the building figures out how to save the witness list as a PDF instead of printing it, scanning it, and emailing the scan to themselves.",
    # 3: the 400-page bill, and the intern who understands file formats.
    "They drafted a 400-page bill to govern machine learning, then asked an intern to convert it to PDF, because the only thing in the building that understands file formats is the intern.",
    # 4: the senator who wants AI licensed, whose office still faxes drafts.
    "The senator who says AI must be licensed before it can be trusted has never once exported a document to PDF, and his office still faxes the drafts to the committee that will vote on them.",
    # 5: the bill arrives as a photograph of a Word document.
    "Our lawmakers want a federal registry for every AI model in America, but their own bill arrived at the clerk's office as a photograph of a Word document taken on a phone.",
    # 6: the hearing delayed because nobody knows what .docx means.
    "The hearing on regulating the internet was delayed twenty minutes because the chairman's opening statement was a .docx, and nobody in the room, including the chairman, knew what the letters after the dot meant.",
    # 7: the draft exists only as a printout; the only PDF was an accident.
    "They are writing the rules for algorithms that will run the country, yet the draft of the bill exists only as a printout, because the only PDF in the office is the one the intern made by accident.",
    # 8: the bill to audit neural networks, appendix as a pasted screenshot.
    "A lawmaker who cannot find the Export button just introduced a bill to audit every neural network in the country, and the bill's own appendix is a screenshot pasted into a Word file.",
    # 9: the subpoena that will not save as a PDF, and IT stops answering.
    "The committee voted to subpoena the tech companies, then spent the afternoon asking IT why the subpoena would not save as a PDF, and IT has stopped answering the phone.",
    # 10: safety reports in triplicate, but the one staffer under thirty is away.
    "He wants AI companies to file safety reports in triplicate, but his own office cannot produce a PDF without calling the one staffer under thirty, who is on holiday until January.",
]

# --- Rubric: the judge's criteria, in the judge's order -------------------
# (criterion, weight): on-subject 5, real turn 4, aim on lawmakers 3,
# clean + quotable + punch last 2, specific unexpected detail 1.
CRITERIA = [
    ("on_subject", 5),   # one-sentence roast of lawmakers regulating AI/crypto/internet who cannot convert a file to PDF
    ("real_turn", 4),    # sets up the lawmaker's authority, then undercuts it with the file they cannot convert
    ("aim", 3),          # joke is about power and competence, the rules they write
    ("quotable", 2),     # reads clean in one pass, punch lands on the last few words
    ("detail", 1),       # a specific, unexpected detail over a worn tech-illiteracy cliche
]

# Scores are honest judgements of each candidate against the rubric.
# 0-2 per criterion (0 misses, 1 lands, 2 lands hard).
SCORES = {
    1:  {"on_subject": 2, "real_turn": 2, "aim": 2, "quotable": 1, "detail": 2},  # 10+8+6+2+2 = 28
    2:  {"on_subject": 2, "real_turn": 2, "aim": 1, "quotable": 1, "detail": 2},  # 10+8+3+2+2 = 25
    3:  {"on_subject": 2, "real_turn": 1, "aim": 2, "quotable": 1, "detail": 1},  # 10+4+6+2+1 = 23
    4:  {"on_subject": 2, "real_turn": 1, "aim": 2, "quotable": 1, "detail": 1},  # 10+4+6+2+1 = 23
    5:  {"on_subject": 2, "real_turn": 2, "aim": 2, "quotable": 2, "detail": 2},  # 10+8+6+4+2 = 30
    6:  {"on_subject": 2, "real_turn": 1, "aim": 1, "quotable": 1, "detail": 2},  # 10+4+3+2+2 = 21
    7:  {"on_subject": 2, "real_turn": 2, "aim": 2, "quotable": 1, "detail": 1},  # 10+8+6+2+1 = 27
    8:  {"on_subject": 2, "real_turn": 2, "aim": 2, "quotable": 1, "detail": 2},  # 10+8+6+2+2 = 28
    9:  {"on_subject": 2, "real_turn": 2, "aim": 2, "quotable": 2, "detail": 1},  # 10+8+6+4+1 = 29
    10: {"on_subject": 2, "real_turn": 1, "aim": 2, "quotable": 2, "detail": 2},  # 10+4+6+4+2 = 26
}


def weighted_score(n):
    """Weighted rubric total for candidate number n (1-based)."""
    return sum(SCORES[n][name] * weight for name, weight in CRITERIA)


def rank_candidates():
    """Rank by weighted score, ties broken by the shorter text."""
    ranked = sorted(
        range(1, len(CANDIDATES) + 1),
        key=lambda n: (-weighted_score(n), len(CANDIDATES[n - 1])),
    )
    return ranked



def pick_winner():
    """The top-ranked candidate: highest weighted score, shortest wins ties."""
    return CANDIDATES[rank_candidates()[0] - 1]


def is_single_sentence(text):
    """One sentence: ends with a period, no sentence break inside."""
    stripped = text.strip()
    if not stripped.endswith("."):
        return False
    # A period followed by a space and a capital letter would start a new sentence.
    body = stripped[:-1]
    return ". " not in body and "!" not in body and "?" not in body


def write_entry():
    """Validate the winner against the gate and write /output/entry.txt."""
    winner = pick_winner()
    assert 1 <= len(winner) <= 320, f"winner is {len(winner)} chars, gate is 1-320"
    assert winner.strip(), "winner must not be only white space"
    assert is_single_sentence(winner), "winner must be exactly one sentence"
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(winner)
    print(f"wrote {len(winner)} chars to {path}")
    return winner


if __name__ == "__main__":
    write_entry()
