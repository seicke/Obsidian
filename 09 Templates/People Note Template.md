``<%*
moment.locale("en");
let filename = tp.file.title;

const match = filename.match(/^(?<surname>[A-Za-zÄÖÜäöüß\-]+),\s?(?<forname>[A-Za-zÄÖÜäöüß\-]+)/);
console.log(match);
if (match) {
	filename = `${match.groups.surname}, ${match.groups.forname}`;
	if (tp.file.title !== filename) await tp.file.rename(filename);
}
%>---
company:
email:
aliases:
birthday:
title:
created:
updated:
---
# <% filename %>

## Notes
<% tp.file.cursor() %>

## Meetings