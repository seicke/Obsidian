---
created: 2026-07-10 09:09:51
updated: 2026-07-29 08:14:28
---

>[!todo] Today
>```tasks
>not done
>(due before today) OR (due on today) OR (scheduled on today)  OR (scheduled before today) 
>sort by due, priority
>hide due date
>hide created date
>path does not include StudentTasks.md
>```

> [!todo]- Tomorrow
> ```tasks
> not done
> (due on tomorrow) OR (scheduled on tomorrow)
> sort by due, priority
> hide due date
> hide created date
> path does not include StudentTasks.md 
> ``` 

> [!todo]- This Week
> ```tasks
> not done
> (due this week) OR (scheduled this week)
> group by function (task.scheduled.moment ?? task.due.moment)?.format("YYYY-MM-DD dddd") ?? "No date"
> sort by function task.scheduled.moment?.valueOf() ?? task.due.moment?.valueOf() ?? Infinity
> sort by priority
> hide created date
> path does not include StudentTasks.md
> ``` 

>[!info]- Student Tasks
>```tasks
>not done
>sort by due, priority
>hide created date
>path includes Student Tasks
>```
^0219ae

>[!example]- Backlog
>```tasks
>not done
>no due date
>no scheduled date
>hide created date
>path does not include 09 Templates
>path does not include StudentTasks.md
>path does not include Student Tasks
>```