---
created: 2026-07-20 06:37:20
updated: 2026-07-20 06:40:37
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
