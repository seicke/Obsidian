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
created:
updated:
---
# <% filename %>
<%* // ❮❮ YYYY-MM-DD dddd | YYYY | MMMM YYYY | YYYY-MM-DD dddd  ❯❯
%>❮❮ [[<% day_before.format('[01 Journal]/YYYY/YYYY-MM MMMM/YYYY-MM-DD dddd|YYYY-MM-DD dddd') %>]] | [[<% day.format('[01 Journal]/YYYY/YYYY|YYYY') %>]] | [[<% day.format('[01 Journal]/YYYY/YYYY-MM MMMM/YYYY-MM MMMM|MMMM YYYY') %>]] | [[<% day_after.format('[01 Journal]/YYYY/YYYY-MM MMMM/YYYY-MM-DD dddd|YYYY-MM-DD dddd') %>]] ❯❯

> [!todo] Today
>```tasks
>not done
>(due before <% day_before.format('YYYY-MM-DD') %>) OR (due on <% day_before.format('YYYY-MM-DD') %>) OR (scheduled on <% day_before.format('YYYY-MM-DD') %>)
>sort by due, priority
>hide due date
>hide created date
>path does not include StudentTasks.md
>```

<%*
if (day.isSame(today, 'day') || day.isAfter(today)) {
	if ([1,2,3,4,5].includes(day.isoWeekday())
		&& [2025,2026].includes(day.year())) {
		tR += `- [ ] [[Railway-X]] Stunden buchen: [Aufwandabschätzung_Railway-X.xlsx](https://harting.sharepoint.com/:x:/r/sites/Railway-X/Freigegebene%20Dokumente/General/Aufw%C3%A4nde/Aufwandsch%C3%A4tzung_Railway-X.xlsx?d=wec9022baf9184e1cbbecc0054bd1b2c2&csf=1&web=1&e=1pSzDy) ➕ ${day.format('YYYY-MM-DD')} 📅 ${day.format('YYYY-MM-DD')}\n`;
		tR += `- [ ] #Blockbrain Daily Assistant testen ➕ ${day.format('YYYY-MM-DD')} 📅 ${day.format('YYYY-MM-DD')}\n`;
		tR += `- [ ] [[2026 English Course]] Vocabulary lernen ➕ ${day.format('YYYY-MM-DD')} 📅 ${day.format('YYYY-MM-DD')}\n`;
	}
	if ([5].includes(day.isoWeekday())) {
		tR += `- [ ] Weekly Review ➕ ${day.format('YYYY-MM-DD')} 📅 ${day.format('YYYY-MM-DD')}\n`;
	}
}
%>- <% tp.file.cursor() %>