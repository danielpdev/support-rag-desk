# Pregătire pentru interviu — Support RAG Desk

Roluri țintă: Applied AI Engineer / RAG Engineer.

## Prezentare de 90 de secunde

1. Explică problema concretă și cine folosește rezultatul.
2. Rulează `make demo` sau fluxul din UI.
3. Arată testul pentru un caz de eșec, apoi explică mecanismul din cod.
4. Spune ce limite are demonstrația și ce ai construi pentru producție.

Decizia de explicat: Workspace filtering happens before ranking and before any prompt is built. Fixture mode returns a source extract; local mode combines MiniLM retrieval and a Qwen answer. Unsupported queries create a review ticket.

## Cinci întrebări

1. Unde aplici filtrarea pe tenant?
2. Ce măsoară retrieval versus answer quality?
3. Cum tratezi o citare inventată?
4. De ce prompt injection nu se rezolvă doar printr-un prompt?
5. Când escaladezi la un om?

## Exercițiu înainte de a aplica

Bind workspace identity to a verified session and add a larger adversarial groundedness dataset.

Alege o parte mică a acestei modificări, implementeaz-o personal, adaugă un test care verifică comportamentul și descrie rezultatul într-un commit real. Nu declara că ai înțeles sau construit singur o parte pe care nu o poți explica.

## Checklist personal

- [ ] Pot porni proiectul dintr-un checkout curat.
- [ ] Pot urmări cererea până la rezultatul salvat.
- [ ] Pot explica diferența dintre fixture și model local.
- [ ] Pot demonstra un eșec și recuperarea lui.
- [ ] Am făcut o modificare proprie și o pot explica în engleză.

Aceste puncte necesită review-ul tău; nu au fost bifate automat.
