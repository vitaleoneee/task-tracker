# SQL Tasks

## Tables

- tasks (*id, name, status, project_id*)
- projects (*id, name*)

---

### Query 1 - get all statuses, not repeating, alphabetically ordered

```postgresql
SELECT DISTINCT status
FROM tasks
ORDER BY status
```

---

### Query 2 - get the count of all tasks in each project, order by tasks count descending

```postgresql
SELECT project_id, COUNT(*) AS tasks_count
FROM tasks
GROUP BY project_id
ORDER BY tasks_count DESC
```

---

### Query 3 - get the count of all tasks in each project, order by projects names

```postgresql
SELECT p.name, COUNT(t.id) AS tasks_count
FROM projects p
LEFT JOIN tasks t ON p.id = t.project_id
GROUP BY p.name
ORDER BY p.name
```

---

### Query 4 - get the tasks for all projects having the name beginning with "N" letter

```postgresql
SELECT t.*
FROM projects p
JOIN tasks t ON p.id = t.project_id
WHERE p.name LIKE 'N%'
```

---

### Query 5 - get the list of all projects containing the 'a' letter in the middle of the name, and show the tasks count near each project. Mention that there can exist projects without tasks and tasks with project_id = NULL

```postgresql
SELECT p.name, COUNT(t.id) AS tasks_count
FROM projects p
LEFT JOIN tasks t ON p.id = t.project_id
WHERE p.name ILIKE '_%a%_'
GROUP BY p.name
```

---

### Query 6 - get the list of tasks with duplicate names. Order alphabetically

```postgresql
SELECT name, COUNT(*) AS duplicates_count
FROM tasks
GROUP BY name
HAVING COUNT(*) > 1
ORDER BY name
```

---

### Query 7 - get the list of tasks having several exact matches of both name and status, from the project 'Delivery'. Order by matches count

```postgresql
SELECT t.name, t.status, COUNT(*) AS matches_count
FROM projects p
JOIN tasks t ON p.id = t.project_id
WHERE p.name = 'Delivery'
GROUP BY t.name, t.status
HAVING COUNT(*) > 1
ORDER BY matches_count DESC
```

---

### Query 8 - get the list of project names having more than 10 tasks in status 'completed'. Order by project_id

```postgresql
SELECT p.name
FROM projects p
         JOIN tasks t ON t.project_id = p.id
WHERE t.status = 'completed'
GROUP BY p.id, p.name
HAVING COUNT(*) > 10
ORDER BY p.id
```