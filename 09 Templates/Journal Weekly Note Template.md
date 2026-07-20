---
created: 2026-07-20 06:37:20
updated: 2026-07-20 06:45:11
---
<%*
moment.locale("en");
let filename = tp.file.title;
let day = null

const match = filename.match(/^(?<date>\d{4} W\d{2})/);
if (match) {
	today = moment();
	week = moment(match.groups.date, 'gggg [W]WW');
} else {
	today = moment();
	week = today.clone();
}

week_before = week.clone().subtract(7, 'day');
week_after = week.clone().add(7, 'day');

filename = week.format('gggg [W]WW');
if (tp.file.title !== filename) await tp.file.rename(filename);
%>---
aliases:
---
# <% filename %>
<%* // ❮❮ gggg [W]WW | gggg | MMMM gggg | gggg [W]WW  ❯❯
%>❮❮ [[<% week_before.format('[01 Journal]/gggg/gggg [W]WW') %>]] | [[<% week.format('[01 Journal]/gggg/gggg|gggg') %>]] | [[<% day.format('[01 Journal]/gggg/gggg-MM MMMM/gggg-MM MMMM|MMMM gggg') %>]] | [[<% week_after.format('[01 Journal]/gggg/gggg [W]WW') %>]] ❯❯