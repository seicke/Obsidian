<%*
moment.locale("en");
let filename = tp.file.title;
let day = null

const match = filename.match(/^(?<date>\d{4}-\d{2})/);
console.log(match)
if (match) {
	today = moment();
	month = moment(match.groups.date, 'YYYY-MM');
} else {
	today = moment();
	month = today.clone();
}

month_before = month.clone().subtract(1, 'month');
month_after = month.clone().add(1, 'month');

month_start = month.clone().startOf('month');
month_end = month.clone().endOf('month');

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
tR += `- [ ] [[${month.format('[01 Journal]/YYYY/YYYY MMMM')}|Monthly Planning]] 🔺➕ ${today.format('YYYY-MM-DD')} ⏳ ${planning_day.format('YYYY-MM-DD')} 📅 ${planning_day.format('YYYY-MM-DD')}\n`;
%>

<%*
if (!(tp.user.computername() || require('os').hostname()).toLowerCase().includes('nbespel')) {
	tR += `- Was ist mir in diesem Monat wichtig?\n`;
	tR += `- Wie sieht ein perfekter Monat für mich aus?\n`;
}
%>

## Review
<%*
tR += `- [ ] [[${month.format('[01 Journal]/YYYY/YYYY MMMM')}|Monthly Review]] 🔺➕ ${today.format('YYYY-MM-DD')} ⏳ ${review_day.format('YYYY-MM-DD')} 📅 ${review_day.clone().format('YYYY-MM-DD')}\n`;
%>