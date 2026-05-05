# Claim Map: AI ROI

This is a normalized operator claim map. It preserves the substance of the session without treating every raw utterance as ready for reuse.

| ID | Claim | Evidence Basis | Confidence | Sensitivity | Allowed Audience | Next Review |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| AIROI-C01 | AI-written code percentage is a weak proxy for business productivity. | Repeated session framing around high AI involvement in code generation versus smaller cycle-time improvement. | High | Medium | Internal, attendee recap, anonymized executive memo | Verify any numeric examples before external use. |
| AIROI-C02 | The missing ROI often sits in delivery process: review, QA, security, deployment, compliance, and adoption. | Session analysis notes repeated discussion of delivery lifecycle bottlenecks. | High | Low | Internal, attendee recap, client-safe synthesis | Convert into a process-bottleneck checklist. |
| AIROI-C03 | Early AI adoption can slow teams if people use AI for tasks where manual execution is faster. | Session analysis notes adoption phase where perceived speed and measured delivery diverged. | Medium | Medium | Internal, attendee recap | Source-check before publication. |
| AIROI-C04 | AI review plus human review may reduce review wait states more concretely than generic code generation. | Session analysis notes movement from two human reviewers toward one AI reviewer plus one human reviewer. | Medium | Medium | Internal, technical follow-up | Validate against actual practice and risk controls. |
| AIROI-C05 | QA has to move earlier and become more continuous as AI increases output volume. | Session analysis around CI/CD, automated checks, security checks, and earlier QA. | High | Low | Internal, attendee recap, client-safe synthesis | Turn into SDLC pattern. |
| AIROI-C06 | Token spend is a governance issue, especially when non-engineers use stronger models without usage discipline. | Session analysis notes spend jumps, model choice, and non-engineer iteration behavior. | High | Medium | Internal, CTO/CFO memo | Create budget-guardrail template. |
| AIROI-C07 | Buy-versus-build still favors buying non-core tools because security, maintenance, certification, and UX costs remain. | Session analysis notes CTO stance: prefer buy unless core IP. | High | Low | Internal, attendee recap, client-safe synthesis | Map to Delphi build-versus-buy choices. |
| AIROI-C08 | Adoption is the real ROI gate: a quickly built tool fails if it does not change business behavior. | Session analysis notes usage, maintainability, workflow change, and business behavior. | High | Low | Internal, attendee recap, client-safe synthesis | Connect to Delphi metrics. |
| AIROI-C09 | Distribution, trust, and launch channels become more valuable when building gets easier. | Session analysis captures market point around distribution becoming bottleneck. | Medium | Low | Internal, public-safe essay | Use as broader market observation. |
| AIROI-C10 | Context discipline is more durable than temporary model choice. | Chat/session analysis notes model race and context engineering. | Medium | Low | Internal, technical follow-up | Pair with AI workflow architecture. |

## Disagreement And Uncertainty

The main disagreement is not whether AI is useful. The tension is where to locate ROI. Some claims point to developer acceleration. The stronger session synthesis points to process redesign, adoption, and governance.

The unresolved question is measurement. The session implies that teams should compare against their own baselines, but the operator workflow still needs a clean metric taxonomy and a way to distinguish reported experience from measured evidence.

## Derived Artifact Hooks

The strongest reusable hook is:

```text
AI compresses code production before it compresses the organization around code.
```

This is suitable for an internal memo or anonymized public-safe teaser after source review.
