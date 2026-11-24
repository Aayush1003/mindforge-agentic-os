# Near-Term Research Frontiers: A Human-and-AI Scout

This companion helps a person or research agent find an important, timely, and realistically approachable research question. It is a research-selection guide, not a claim that any project below is novel or likely to win a Nobel Prize.

## Important expectation

No one can reliably identify a future Nobel Prize-winning project in advance. Nobel Prizes recognize exceptional discoveries and contributions, often years after the work; they are not a practical project-selection target. Choose a question because it matters, can be investigated responsibly, and may produce evidence others can use. A small project can contribute useful data, replication, a tool, or a clearly scoped result without claiming to solve the whole problem.

## How a research agent should find what is being studied now

Before recommending a project, browse the live web and record the search date. Do not rely on model memory for claims about current research. Search in this order:

1. **Authoritative problem assessments:** recent reports from organizations such as the IPCC, WHO, IEA, national public-health agencies, and national science agencies. Use these to establish the scale, urgency, and affected populations.
2. **Recent research:** review articles and systematic reviews first, then papers and preprints from roughly the last three years. Search scholarly indexes such as PubMed, Crossref, OpenAlex, or Google Scholar. Check publication dates and distinguish peer-reviewed work from preprints.
3. **Open research gaps:** inspect the limitations and future-work sections of recent reviews, unresolved questions in registered study protocols, and replication or benchmark results. A paper's authors' proposed next step is a lead, not proof that the gap remains open.
4. **Existing efforts:** look for active projects, public datasets, standards, and local organizations already addressing the issue. Prefer complementing them over duplicating work.
5. **Independent verification:** confirm important claims in at least two independent, high-quality sources. Follow citations to the original study; do not treat headlines, search snippets, or AI summaries as evidence.

For every proposed research direction, provide links and publication dates, summarize what is known, identify uncertainty and disagreement, and say what the sources do *not* establish. Include at least one source that could challenge the recommendation.

### Copyable research-agent prompt

```text
Find high-priority research problems people may be able to make a useful contribution to in the next 1–5 years. Browse the web; do not present remembered information as a current literature review.

For each candidate:
- State a precise, answerable question and who benefits if it is answered.
- Summarize current work using dated links to primary studies and recent reviews or authoritative assessments.
- Identify the specific unresolved gap and verify it is not already solved or actively covered by another project.
- Describe a safe, ethical, low-cost first study a person or small team could do, with a measurable outcome and a reproducible method.
- Explain what would make the result useful to practitioners or researchers, and what it could not establish.
- Assess feasibility, expected impact, time to useful evidence, cost, data access, safety/ethics, and risk of duplication.
- Include counterevidence, uncertainty, and at least one competing candidate.
- Do not promise novelty, a cure, policy change, or a Nobel Prize. Separate verified facts from your judgment.

Rank candidates using the rubric in this document. State the date the web search was performed and provide enough source details for a human to verify every key claim.
```

## Candidate-ranking rubric

Score each item from 1 (weak) to 5 (strong), with a short evidence-based justification. Do not let a high impact score compensate for an unsafe or unanswerable project.

| Criterion | What to check |
| --- | --- |
| Human need | Is the problem important to people, and is the affected group clear? |
| Near-term usefulness | Could credible evidence or a practical tool help within 1–5 years? |
| Evidence of a real gap | Do recent sources support that this question remains unresolved? |
| Small-team feasibility | Can the first study be done with accessible skills, equipment, and data? |
| Measurability | Is there a defined outcome, comparison, and way to report uncertainty? |
| Safety and ethics | Can the work avoid unnecessary risk, sensitive data, and unreviewed human-subject research? |
| Reproducibility and openness | Can methods, code, and non-sensitive data be shared for independent checking? |
| Duplication risk | Are existing groups already doing the same work, and can this project complement them? |

A strong recommendation should explain the tradeoffs, not just announce a winner. Recheck the literature before starting and before making public claims.

## Recommended starter direction: local heat-risk and shade audit

**Why consider it:** Extreme heat is a near-term health and infrastructure concern, while shade, cooling access, and neighborhood conditions are locally actionable. A small team may be able to produce a useful, transparent map or audit without attempting medical research. This is a starting hypothesis to validate against current local evidence—not a live review proving that a particular neighborhood has an unmet need.

**Starter question:** In one clearly bounded neighborhood, do publicly available heat observations and a repeatable, non-invasive shade audit identify places where people may have limited access to shaded walking routes or public cooling locations?

**Low-risk first study:**

1. Define one small area and the exact question before collecting observations.
2. Check local public-health guidance, heat-risk reports, existing maps, and community organizations; ask whether the proposed work duplicates or could support ongoing efforts.
3. Use public weather, land-cover, and cooling-location data where available. Record source, date, spatial resolution, and known limitations.
4. If conducting an outdoor shade audit, use a written observation protocol at safe times, avoid collecting images or identifying information about people, and do not enter private property.
5. Compare a small number of routes or sites using a predeclared measure, such as shaded segments per route or distance to a verified public cooling location. Repeat observations and report conditions and uncertainty.
6. Share a methods note and non-sensitive results with a local community or public-health partner for review before drawing conclusions.

**Safety and limits:** Avoid heat exposure as an experimental condition; stop if conditions are unsafe and follow local heat advisories. Do not recruit participants, collect health information, or make individual medical-risk predictions. Public maps can be outdated or incomplete, and a shade audit does not establish health outcomes or prove that an intervention works.

**What would make a contribution stronger:** A documented gap confirmed by local partners, a repeatable protocol, validated data, transparent uncertainty, independent replication, and evidence that the result helps a decision-maker. If those conditions are absent, revise the question or choose another candidate.

## Research record for each candidate

```text
Search date:
Question:
Who benefits and how:
Current evidence (dated links):
Evidence against or competing explanation:
Specific unresolved gap:
Existing projects or partners checked:
Smallest useful study:
Outcome and comparison:
Cost, time, and required skills:
Safety and ethics review:
Data, code, and reproducibility plan:
Limitations and uncertainty:
Ranking and rationale:
Next verification step:
```

## Sources to begin a live search

These are discovery starting points, not endorsements or evidence for any specific local claim. Verify the current page, date, and underlying references when using them.

- IPCC reports: https://www.ipcc.ch/reports/
- WHO climate change and health: https://www.who.int/news-room/fact-sheets/detail/climate-change-and-health
- WHO heat and health: https://www.who.int/news-room/fact-sheets/detail/climate-change-heat-and-health
- PubMed: https://pubmed.ncbi.nlm.nih.gov/
- OpenAlex: https://openalex.org/
- Crossref: https://search.crossref.org/

The best project is not necessarily the most fashionable or prestigious one. It is a well-supported question where careful work can produce a useful, honest, and independently checkable contribution.
