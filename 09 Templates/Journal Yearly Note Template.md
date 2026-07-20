---
created: 2026-07-13 06:56:28
updated: 2026-07-20 06:50:59
---
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