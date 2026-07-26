<%*
moment.locale("en");
let filename = tp.file.title;
let day = null

const match = filename.match(/^(?<date>\d{4}-\d{2})/);
if (match) {
	today = moment();
	month = moment(match.groups.date, 'YYYY-MM');
} else {
	today = moment();
	month = today.clone();
}

month_before = week.clone().subtract(1, 'month');
month_after = week.clone().add(7, 'month');

month_start = today.clone().startOf('month');
month_end = today.clone().endOf('month');

planning_day = month_start.clone().subtract(1, 'day').day(0);
review_day = month_end.clone().day(0);

filename = month.format('YYYY-MM MMMM');
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
tR += `- [ ] Weekly Planning 🔺➕ ${today.format('YYYY-MM-DD')} ⏳ ${planning_day.format('YYYY-MM-DD')} 📅 ${planning_day.format('YYYY-MM-DD')}\n`;
%>

> [!todo]- Tasks
> ```tasks
> not done
> filter by function !(task.scheduled.moment ?? task.due.moment) ? false : !(task.scheduled.moment ?? task.due.moment).isValid() ? false : !!(task.scheduled.moment ?? task.due.moment).isBetween( moment("<% week.format('gggg-MM-DD') %>").startOf('isoWeek'), moment("<% week.format('gggg-MM-DD') %>").endOf('isoWeek'), 'day', '[]' )
> group by function (task.scheduled.moment ?? task.due.moment)?.format("YYYY-MM-DD dddd") ?? "No date"
> sort by function task.scheduled.moment?.valueOf() ?? task.due.moment?.valueOf() ?? Infinity
> sort by priority
> hide created date
> path does not include StudentTasks.md
> ```

## Review
<%*
tR += `- [ ] [[${week.format('[01 Journal]/gggg/gggg [W]WW')}|Weekly Review]] 🔺➕ ${today.format('YYYY-MM-DD')} ⏳ ${review_day.format('YYYY-MM-DD')} 📅 ${review_day.clone().add(2, 'day').format('YYYY-MM-DD')}\n`;
%>