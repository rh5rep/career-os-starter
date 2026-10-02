# Template Setup

Career Search OS does not force one resume design across industries or candidates.

During onboarding, provide or choose what you want the system to use:

- **Primary resume template** — recommended if you already have a format you like.
- **Optional CV template** — only if your field/geography benefits from a separate CV.
- **Optional cover-letter template** — if you actually use one.
- **Optional logos/media** — only if your document format genuinely uses them.

Put user-supplied assets under `assets/user_templates/` or make them available to the connected workspace. The system records the approved asset in `canonical/TEMPLATE_REGISTRY.yaml`; you should not edit that file manually.

If your existing resume format is good, preserve it. The system should tailor content to the target without replacing the visual identity merely because the framework has its own internal examples.

A template is considered registered only after you confirm which asset should be used and for what purpose. Missing templates may stay `NOT_REGISTERED` without blocking profile setup.

For a DOCX, registration records the exact file hash, a machine-readable structural fingerprint, and an approved rendered reference. The fingerprint captures page/section geometry, header/footer parts, paragraph styles and layout-control order, tab stops, drawings and image relationships, tables, text boxes, and fields. It does not freeze variable wording or paragraph counts. The system generates it with `python3 scripts/audit_docx_structure.py path/to/template.docx --fingerprint-out path/to/fingerprint.json`; the candidate need not inspect XML. A changed source hash requires a new fingerprint and canary.

Missing templates also do not block discovery or triage. They do block automatic creation of a final application artifact: the system must pause and ask you to register or explicitly approve a format first. It must not silently create an “approved” design.
