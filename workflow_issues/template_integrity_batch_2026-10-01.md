# Template structure can silently diverge while ATS text passes

Status: addressed in portable controls; next live canary remains to validate.

Observed failure: a surviving inline alignment tab preceded newly appended header text, and a second tab preceded right metadata. All outputs in a batch shared the defect. Parser success and contact-sheet consistency did not reveal it.

Control: fingerprint the candidate-approved source DOCX at registration; populate placeholders in place or deliberately rebuild paragraphs; compare final OOXML structural semantics to the exact source; run separate ATS, semantic, and individual-page visual gates; bind each gate to final file hashes; approve a canary before fan-out after any material build-path change.

Verification: `python3 scripts/test_docx_structure.py`, `python3 scripts/test_portable_invariants.py`, and one real canary for each newly registered template profile.
