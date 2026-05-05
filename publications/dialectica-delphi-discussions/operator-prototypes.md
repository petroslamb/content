# Delphi Operator Prototypes

This is the package index for the end-to-end operator prototype.

The point of the prototype is to show how Delphi sessions can become structured expert-network memory. Each worked session follows the same path:

```text
raw session sources
  -> session record
  -> claim map
  -> artifact map
  -> give/get follow-up actions
  -> data model instance
```

The three worked examples are intentionally different. That is the proof of the pattern. AI ROI is an operating-truth room. Claude Mythos is a reactive sensemaking room. Hormuz is a multidisciplinary crisis teardown. The same operator workflow can process all three without flattening them into generic summaries.

## Worked Packets

| Session | Format | Packet | What It Proves |
| :--- | :--- | :--- | :--- |
| AI ROI | Operating-truth discovery | [`ai-roi/operator-prototype/`](ai-roi/operator-prototype/README.md) | Delphi can convert private operator comparison into ROI metrics, governance artifacts, and targeted CTO follow-up. |
| Claude Mythos | Reactive sensemaking | [`claude-mythos/operator-prototype/`](claude-mythos/operator-prototype/README.md) | Delphi can respond to a fast-moving AI-security event with board, CISO, and practitioner outputs. |
| Hormuz Fallout | Multidisciplinary crisis teardown | [`hormuz-fallout/operator-prototype/`](hormuz-fallout/operator-prototype/README.md) | Delphi can map a cross-domain crisis into defense, insurance, treasury, energy, and supply-chain follow-ups. |

## Canonical Packet Shape

Each packet contains:

- `session-record.md`: the reviewed session object and operating read
- `claim-map.md`: normalized claims with confidence, sensitivity, allowed audience, and next review
- `artifact-map.md`: candidate outputs by audience
- `give-get-actions.md`: follow-up offers, asks, channels, owners, and success signals
- `data-model-instance.yaml`: a concrete instance of the proposed expert/session memory model

## What This Demonstrates

The prototype demonstrates the first thin operator workflow:

1. Keep raw transcripts and chat stable.
2. Extract reviewed claims, questions, disagreements, and participant signals.
3. Separate internal, attendee, client-safe, and public-safe artifact layers.
4. Convert session insight into give/get actions.
5. Write the outcome back into expert and topic state.

This is the practical version of the data-to-engagement idea. The email or community surface is not the core product. The core product is the modeled state that knows what an expert contributed, what they are likely to value, what can be reused, and what action should happen next.

## What Is Still Missing

This is a content and data-model prototype, not a software prototype.

The next technical step would be a small operator console that can ingest a session bundle, create these objects, and push approved actions into existing email or journey tooling. Before that can be safely built, the discovery phase needs access to the real expert data model, CRM or expert-management system, email tooling, Zoom exports, compliance constraints, and existing analytics or dbt models.
