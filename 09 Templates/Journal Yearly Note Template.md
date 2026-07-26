<%*
moment.locale("en");
let filename = tp.file.title;
let year = null;

const match = filename.match(/^(?<date>\d{4})/);
if (match) {
	year = moment(match.groups.date, 'YYYY');
} else {
	year = moment();
}

const prev_year = year.clone().subtract(1, 'year');
const next_year = year.clone().add(1, 'year');

filename = year.format('YYYY');
if (tp.file.title !== filename) await tp.file.rename(filename);
%>---
aliases:
  - 
created:
updated:
---
# <% filename %>
<%* // ❮❮ YYYY-- | YYYY++  ❯❯
%>❮❮ [[<% prev_year.format('[1 Journal]/YYYY|YYYY') %>]] | [[<% next_year.format('[1 Journal]/YYYY|YYYY') %>]] ❯❯

- <% tp.file.cursor() %>

## Planning
1. Was möchte ich 2026 erreichen? Was nehme ich mir vor?
	- 
2. Wie stelle ich mir 2026 vor?
	-

## Review
1. Was hat dieses Jahr zu einem guten Jahr gemacht?
	-
2. Welche Nachricht hat mich in diesem Jahr am meisten berührt?
	-
3. Was ist mir jetzt klar, was ich vor einem Jahr noch nicht wusstest?
	-
4. Wer oder was bestimmt derzeit am stärksten, was „Erfolg“ für mich ist?
	-
5. Was hat mich beschäftigt, aber nicht erfüllt?
	-
6. Welche neue Seite habe ich an mir entdeckt?
	-
7. Worin bin ich besser geworden?
	-
8. Mit wem habe ich mich in diesem Jahr am lebendigsten gefühlt?
	-
9. Womit bin ich mir und anderen auf die Nerven gegangen?
	-
10. Welche Frage nehme ich mit ins neue Jahr?
	-
11. Was möchte ich loslassen?
	-