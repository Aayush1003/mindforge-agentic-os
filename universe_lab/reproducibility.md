# Human-Reproducibility Verifier

A practical, human-led checklist for deciding whether a study or computational claim provides enough evidence to review and attempt independently. This is a decision aid, not proof of correctness or a replacement for expert scientific judgment.

## Problem

Experimental and computational claims are often difficult to verify when the report omits methods, data, code, uncertainty, negative results, or independent reproduction.

## Evidence checklist

Mark each item as **confirmed** only after a person verifies the underlying source.

| Evidence item | Status | Human review needed |
|---|---|---|
| Methods | Unconfirmed | Can another person reconstruct the procedure? |
| Data | Unconfirmed | Is the relevant data accessible, intact, and sufficiently documented? |
| Code | Unconfirmed | Can the analysis be run from a clear, recorded starting point? |
| Uncertainty | Unconfirmed | Are error bounds, limitations, and alternative explanations reported? |
| Negative results | Unconfirmed | Were failed or contrary outcomes disclosed? |
| Independent reproduction | Unconfirmed | Has an unrelated team or environment repeated the result? |

## Status rules

- **Complete:** All six evidence items are confirmed.
- **Partially complete:** Four or five items are confirmed.
- **Insufficient:** Fewer than four items are confirmed.

Missing items do not prove that a claim is false. They mean that independent confidence is not yet justified.

## Human workflow

1. Inspect the original study, not only summaries or news articles.
2. Record where each method, dataset, code file, uncertainty estimate, and negative result is found.
3. Mark a checklist item only when the evidence is accessible and understandable.
4. Attempt an independent reproduction under explicitly stated assumptions.
5. Record failures, unexpected discrepancies, and what remains unknown.
6. Have a qualified reviewer adjudicate ambiguous evidence.

## Measurable outcome

A useful benchmark is agreement between the checklist and expert audit labels across chemistry, biology, physics, medicine, and software studies. It should reduce fabricated confidence and hidden unsupported links while preserving legitimate uncertainty.

## Simulation scenario

Consider a claim with the following evidence:

```json
{
  "methods": true,
  "data": true,
  "code": false,
  "uncertainty": true,
  "negative_results": false,
  "independent_reproduction": false
}
```

**Result:** Partially complete, with 3 of 6 essential items confirmed.

**Missing evidence:** Code, negative results, and independent reproduction.

**Human judgment:** Do not accept or reject the claim solely from this checklist. Inspect the data and methods, request the code, check for unpublished contradictions, and attempt independent reproduction.

## Limitations

- A completed checklist does not establish causation or truth.
- False claims can still contain accurate-looking documentation.
- Reproduction may be impossible for privacy, safety, cost, or security reasons.
- Experts must define which evidence is necessary for a particular field.

## Source context

This exercise supports the **Create a reproducibility and uncertainty verifier** problem in `universe_lab/open_problems/ai_grand_challenges_22nd_century_and_recommended_solutions.md`.
