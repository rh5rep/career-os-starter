# Bounded City Search

## Copy/paste prompt

Search for current opportunities in **{{CITY/REGION}}** for these approved role families: **{{ROLE_FAMILIES}}**. Apply these hard constraints: **{{CONSTRAINTS}}**. Use live employer/ATS postings as the verification source when available.

Bound the search: maximum **{{MAX_WAVES, default 3}}** search waves and maximum **{{MAX_ROLES, default 20}}** returned roles. First discover broadly; then verify only the strongest plausible candidates. Do not start application tailoring, evidence mapping, or artifact creation in this search.

For each returned role give company, exact title, location/work arrangement, authoritative URL, live-status confidence, seniority signal, role family, one-sentence reason it may fit, and any obvious blocker. Deduplicate within the board. If time/tool limits are reached, return verified partial results rather than continuing indefinitely. End with explicit `SEARCH STOPPED` reason and what should move to consolidation/deep triage.
