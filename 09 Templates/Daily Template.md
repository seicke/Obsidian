<%*
moment.locale("en");
let filename = tp.file.title;
let day = null

const match = filename.match(/^(?<date>\d{4}-\d{2}-\d{2})/);
if (match) {
	today = moment();
	day = moment(match.groups.date, 'YYYY-MM-DD');
} else {
	today = moment();
	day = today.clone();
}

day_before = day.clone().subtract(1, 'day');
day_after = day.clone().add(1, 'day');

filename = day.format('YYYY-MM-DD dddd');
if (tp.file.title !== filename) await tp.file.rename(filename);
%>---
aliases:
  - <% day.format('DD.MM.YYYY') %>
  - <% day.format('YYYY-MM-DD') %>
  - <% day.format('dddd DD.MM.YYYY') %>
  - <% day.format('dddd DD. MMMM YYYY') %>
  - <% day.clone().locale("de").format('dddd DD.MM.YYYY') %>
  - <% day.clone().locale("de").format('dddd DD. MMMM YYYY') %>
---
# <% filename %>
<%* // ❮❮ YYYY-MM-DD dddd-- | YYYY | MMMM YYYY | YYYY-MM-DD dddd++  ❯❯
%>❮❮ [[<% day_before.format('[1 Journal]/YYYY/YYYY-MM MMMM/YYYY-MM-DD dddd|YYYY-MM-DD dddd') %>]] | [[<% day.format('[1 Journal]/YYYY/YYYY|YYYY') %>]] | [[<% day.format('[1 Journal]/YYYY/YYYY-MM MMMM/YYYY-MM MMMM|MMMM YYYY') %>]] | [[<% day_after.format('[1 Journal]/YYYY/YYYY-MM MMMM/YYYY-MM-DD dddd|YYYY-MM-DD dddd') %>]] ❯❯

<%*
//if (day.isSame(today, 'day') || day.isAfter(today)) {
//	if ([1,2,3,4,5].includes(day.isoWeekday())
//		&& [2025,2026].includes(day.year())) {
//		tR += `- [ ] ... ➕ ${day.format('YYYY-MM-DD')} 📅 ${day.format('YYYY-MM-DD')}\n`;
//	}
//}
%>- <% tp.file.cursor() %>
