# Give/Get Actions: Claude Mythos

## Follow-Up Principle

Participants should receive a concrete readiness artifact before being asked for deeper AI-security detail. The exchange should make clear that responses are aggregated or no-attribution unless explicit consent is granted.

## Candidate Actions

| ID | Segment | Give | Get | Channel | Owner | Success Signal |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| MYTHOS-A01 | CISOs and security leaders | AI-security readiness checklist | Top preparedness gap | Email follow-up | Delphi operator | Gap taxonomy created |
| MYTHOS-A02 | Board-facing leaders | Board-language risk memo | Hardest internal translation problem | Email follow-up | Operator / Pere | Board-risk segment identified |
| MYTHOS-A03 | Technical practitioners | Exposure-management follow-up invite | Willingness to join practitioner circle | Personal invite | Pere / operator | 6-10 qualified participants |
| MYTHOS-A04 | Insurance/risk participants | AI-risk underwriting prompt | Which controls insurers are likely to ask for | Email / call | Operator | Insurance-pressure notes |
| MYTHOS-A05 | Mid-market operators | Public-safe readiness teaser and checklist | Whether they lack access to guidance or tools | Email follow-up | Operator | Mid-market needs validated |

## Draft Follow-Up Prompt

Subject: Mythos follow-up: what readiness gap matters most?

```text
Thank you for joining the Delphi session on Claude Mythos and AI-security readiness.

We are preparing a short no-attribution recap and checklist for participants. The strongest theme was that Mythos-class capability changes the operating environment even for organizations that never deploy the tool themselves.

If useful, reply with the readiness gap that feels most urgent in your organization:

1. Exposure visibility
2. Patch and remediation speed
3. Agent permissions and identity
4. Shadow AI usage
5. Board reporting
6. Cyber insurance or client assurance
7. Security budget for AI-era defense

We will use responses only in aggregated form unless you explicitly agree otherwise.
```

## State Updates

Every completed action should update:

- readiness_gap_tag
- board_translation_interest
- technical_controls_interest
- practitioner_circle_opt_in
- consent_for_aggregated_reuse
