from dotenv import load_dotenv
import os

load_dotenv()

import spacy
model = os.getenv("SPACY_MODEL")
try:
    nlp = spacy.load(model)
except:
    import spacy.cli
    spacy.cli.download(model)
    nlp = spacy.load(model)

from spacy import displacy

def analyze(text):
    doc = nlp(text)
    svg = displacy.render(doc, style="dep", jupyter=False)
    return [(token.text, token.pos_, token.dep_, token.head.text, token.head.pos_) for token in doc], svg

