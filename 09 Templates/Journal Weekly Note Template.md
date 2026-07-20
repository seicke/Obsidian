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
review_day = week.clone().isoWeekday(5);

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

- <% tp.file.cursor() %>

## Planning
<%*
tR += `- [ ] Weekly Planning ➕ ${today.format('YYYY-MM-DD')} ⏳ ${planning_day.format('YYYY-MM-DD')} 📅 ${planning_day.format('YYYY-MM-DD')}\n`;
%>

```tasks
not done
filter by function (function() { const ref = moment("<% week.format('gggg-MM-DD') %>"); const date = task.due.moment ?? task.scheduled.moment; if (!date) return false; const start = ref.clone().startOf('isoWeek'); const end = ref.clone().endOf('isoWeek'); return date.isBetween(start, end, 'day', '[]'); })()
group by function (task.due.moment ?? task.scheduled.moment)?.format("YYYY-MM-DD dddd") ?? "No date"
sort by function task.due.moment?.valueOf() ?? task.scheduled.moment?.valueOf() ?? Infinity
sort by priority
hide created date
path does not include StudentTasks.md
```

## Review
<%*
tR += `- [ ] Weekly Review ➕ ${today.format('YYYY-MM-DD')} ⏳ ${review_day.format('YYYY-MM-DD')} 📅 ${review_day.clone().add(2, 'day').format('YYYY-MM-DD')}\n`;
%>