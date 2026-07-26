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
  - <% month.format('YYYY-MM') %>
  - <% month.format('YYYY MMMM') %>
  - <% month.format('MMMM YYYY') %>
created:
updated:
---
# <% filename %>
<%* // ❮❮ YYYY MMMM | YYYY | YYYY MMMM  ❯❯
%>❮❮ [[<% month_before.format('[01 Journal]/YYYY/YYYY MMMM|YYYY MMMM') %>]] | [[<% month.format('[01 Journal]/YYYY/YYYY|YYYY') %>]] | [[<% month_after.format('[01 Journal]/YYYY/YYYY MMMM|YYYY MMMM') %>]] ❯❯

- <% tp.file.cursor() %>

## Planning
<%*
tR += `- [ ] Monthly Planning 🔺➕ ${today.format('YYYY-MM-DD')} ⏳ ${planning_day.format('YYYY-MM-DD')} 📅 ${planning_day.format('YYYY-MM-DD')}\n`;
%>

## Review
<%*
tR += `- [ ] [[${month.format('[01 Journal]/YYYY/YYYY MMMM')}|Weekly Review]] 🔺➕ ${today.format('YYYY-MM-DD')} ⏳ ${review_day.format('YYYY-MM-DD')} 📅 ${review_day.clone().add(2, 'day').format('YYYY-MM-DD')}\n`;
%>