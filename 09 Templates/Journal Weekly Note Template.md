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

week_start = week = today.clone().startOf('isoWeek');
week_end = today.clone().endOf('isoWeek');

planning_day = week_start.clone().subtract(3, 'day');

filename = week.format('gggg [W]WW');
if (tp.file.title !== filename) await tp.file.rename(filename);
%>---
aliases:
  - <% week.format('gggg [W]WW') %>
  - <% week.format('[W]WW gggg') %>
created:
updated:
---
# <% filename %>
<%* // ❮❮ gggg [W]WW | gggg | MMMM gggg | gggg [W]WW  ❯❯
%>❮❮ [[<% week_before.format('[01 Journal]/gggg/gggg [W]WW|gggg [W]WW') %>]] | [[<% week.format('[01 Journal]/gggg/gggg|gggg') %>]] | [[<% week.format('[01 Journal]/gggg/gggg-MM MMMM/gggg-MM MMMM|MMMM gggg') %>]] | [[<% week_after.format('[01 Journal]/gggg/gggg [W]WW|gggg [W]WW') %>]] ❯❯

## Planning
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
%>

## Review


```tasks
> not done
> (due this week) OR (scheduled this week)
> group by function (task.due.moment ?? task.scheduled.moment)?.format("YYYY-MM-DD dddd") ?? "No date"
> sort by function task.due.moment?.valueOf() ?? task.scheduled.moment?.valueOf() ?? Infinity
> sort by priority
> hide created date
> path does not include StudentTasks.md
> ```
- <% tp.file.cursor() %>