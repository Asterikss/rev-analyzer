import spacy

ner = spacy.load("en_core_web_sm")

def compute_ner(input: str):
    # ents = ner(input).ents
    works_of_art = []
    people = []
    for ent in ner(input).ents:
        print(ent.text, ent.label_)

        if ent.label_ == "WORK_OF_ART":
            works_of_art.append(ent.text)
        elif ent.label_ == "PERSON":
            people.append(ent.text)


    return works_of_art, people
    # i = 0
    # for ent in doc.ents:
        # print(ent.text, ent.label_)
    # for token in doc:
    #     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)
    #     i += 1
    #     if i == 13:
    #         break


