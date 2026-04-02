from dotenv import load_dotenv
import os

load_dotenv()

import spacy
model = os.getenv("SPACY_MODEL", "ru_core_news_sm")
try:
    nlp = spacy.load(model)
except Exception:
    import spacy.cli
    spacy.cli.download(model)
    nlp = spacy.load(model)

from spacy import displacy

def analyze(text):
    doc = nlp(text)
    svgs = [displacy.render(i, style="dep", jupyter=False) for i in doc.sents]
    syntactic_analysis = [(token.text, token.pos_, token.dep_, token.head.text, token.head.pos_) for token in doc]
    semantic_analysis = [(entity.text, entity.label_) for entity in doc.ents]
    return syntactic_analysis, svgs, semantic_analysis

