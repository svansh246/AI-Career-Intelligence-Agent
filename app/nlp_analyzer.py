import spacy


# Load English spaCy model
nlp = spacy.load("en_core_web_sm")


# Entities that are generally useful for resume analysis
USEFUL_ENTITY_LABELS = {
    "PERSON",
    "ORG",
    "GPE",
    "LOC",
    "FAC",
    "DATE",
    "CARDINAL"
}


def analyze_resume(text):

    doc = nlp(text)

    entities = []

    for ent in doc.ents:

        entity_text = ent.text.strip()
        entity_label = ent.label_

        # Ignore empty entities
        if not entity_text:
            continue

        # Ignore very short noisy entities
        if len(entity_text) < 2:
            continue

        # Ignore obvious resume noise
        ignored_terms = {
            "profile",
            "internship",
            "intern",
            "experience",
            "education",
            "skills",
            "projects",
            "data",
            "ai",
            "ml",
            "aff",
            "cbse",
            "crud",
            "gui",
            "team",
            "critical",
            "effective"
        }

        if entity_text.lower().strip() in ignored_terms:
            continue

        if entity_label not in USEFUL_ENTITY_LABELS:
            continue

        entities.append({
            "text": entity_text,
            "label": entity_label
        })

    # Remove duplicates
    unique_entities = []

    seen = set()

    for entity in entities:

        key = (
            entity["text"].lower(),
            entity["label"]
        )

        if key not in seen:

            seen.add(key)
            unique_entities.append(entity)

    return unique_entities


def get_entities_by_type(entities, label):

    return [
        entity["text"]
        for entity in entities
        if entity["label"] == label
    ]