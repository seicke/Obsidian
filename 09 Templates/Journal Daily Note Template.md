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
<%* // ❮❮ YYYY-MM-DD dddd | YYYY | MMMM YYYY | W[WW] gggg | YYYY-MM-DD dddd  ❯❯
%>❮❮ [[<% day_before.format('[01 Journal]/YYYY/YYYY-MM MMMM/YYYY-MM-DD dddd|YYYY-MM-DD dddd') %>]] | [[<% day.format('[01 Journal]/YYYY/YYYY|YYYY') %>]] | [[<% day.format('[01 Journal]/YYYY/YYYY-MM MMMM/YYYY-MM MMMM|MMMM YYYY') %>]] | [[<% day.format('[01 Journal]/gggg/gggg [W]WW|[W]WW gggg') %>]] | [[<% day_after.format('[01 Journal]/YYYY/YYYY-MM MMMM/YYYY-MM-DD dddd|YYYY-MM-DD dddd') %>]] ❯❯

> [!todo]- Tasks Today
>```tasks
>not done
>(due before <% day.format('YYYY-MM-DD') %>) OR (due on <% day.format('YYYY-MM-DD') %>) OR (scheduled before <% day.format('YYYY-MM-DD') %>) OR (scheduled on <% day.format('YYYY-MM-DD') %>)
>sort by due, priority
>hide created date
>path does not include StudentTasks.md
>```

<%*
if (day.isSame(today, 'day') || day.isAfter(today)) {
	if ((tp.user.computername() || require('os').hostname()).toLowerCase().includes('nbespel')) {
		if ([1,2,3,4,5].includes(day.isoWeekday())
			&& [2025,2026].includes(day.year())) { 
			tR += `- [ ] [[Railway-X]] Stunden buchen: [Aufwandabschätzung_Railway-X.xlsx](https://harting.sharepoint.com/:x:/r/sites/Railway-X/Freigegebene%20Dokumente/General/Aufw%C3%A4nde/Aufwandsch%C3%A4tzung_Railway-X.xlsx?d=wec9022baf9184e1cbbecc0054bd1b2c2&csf=1&web=1&e=1pSzDy) 🔽 ➕ ${day.format('YYYY-MM-DD')} 📅 ${day.format('YYYY-MM-DD')}\n`;
			tR += `- [ ] [[2026 English Course]] Vocabulary lernen ➕ ${day.format('YYYY-MM-DD')} 📅 ${day.format('YYYY-MM-DD')}\n`;
		}
		if ([3].includes(day.isoWeekday())) {
			tR += `- [ ] MX-Talk Stuff checken [MX-Talk Videos](https://www.plattform-i40.de/SiteGlobals/IP/Forms/Listen/Downloads/DE/Downloads_Formular.html?cl2Categories_Typ_name=video) / [MX-Talk Veröffentlichungen](https://www.plattform-i40.de/SiteGlobals/IP/Forms/Listen/Downloads/DE/Downloads_Formular.html?cl2Categories_Typ_name=veroeffentlichung) ➕ ${day.format('YYYY-MM-DD')}  📅 ${day.format('YYYY-MM-DD')}\n`
			tR += `- [ ] [internen Stellenanzeigen](https://hcm55.sapsf.eu/sf/careers/jobsearch?bplte_company=hartingsti&_s.crb=aaT2Y5495AbWrHakbBpKEqRo7JfaY3q2dsKpCIQixzE%3d) checken ➕ ${day.format('YYYY-MM-DD')}  📅 ${day.format('YYYY-MM-DD')}\n`;
		}
		if ([5].includes(day.isoWeekday())) {
			tR += `- [ ] 00 Inbox leeren ⏫ ➕ ${day.format('YYYY-MM-DD')}  📅 ${day.format('YYYY-MM-DD')}\n`;
		}
	}
}
%>- <% tp.file.cursor() %>