# Company List Search

## Copy/paste prompt

Search only these companies: **{{COMPANIES}}**. Inspect their current careers boards for roles plausibly matching **{{ROLE_FAMILIES}}** and **{{CONSTRAINTS}}**. Do not search replacement companies.

For each company, inspect at most **{{MAX_PLAUSIBLE_ROLES_PER_COMPANY, default 5}}** plausible openings after an initial board scan. Record strongest role(s), materially relevant alternatives, and why others are too senior/weak/duplicative. Use authoritative posting links when available. Stop after the listed companies are completed or tool/time limits are reached, and return partial verified results rather than broadening scope.
