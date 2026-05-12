# Issue 12 - Guardrails, Query Intelligence, and Agent Tools

## Goal
Add reliable answer behavior, adaptive retrieval strategy, and safe agent actions.

## Scope
- In: grounded-answer guardrails, query classification, strategy routing, tool-calling agent with action logging and confirmations.
- Out: multi-agent orchestration.

## Deliverables
- Guardrailed prompting and confidence behavior
- Query type classifier + strategy policies
- Agent tools (`search`, `read`, `summarize`, `create_note`, etc.) with safety checks

## Implementation Tasks
1. Enforce strict grounded-answer prompt policy.
2. Add unsupported-evidence behavior and conflict handling.
3. Implement query classification and strategy router.
4. Implement agent tool set with audit logs.
5. Add confirmation gates for destructive actions.

## Tests
- Unit: query classifier routing.
- Unit: guardrail response policy (unknown/conflict/fake citation rejection).
- Integration: agent tool call trace with citations.
- Security test: destructive action requires explicit confirmation.

## Definition of Done
- Assistant never fabricates citations in test suite.
- Query strategy adapts by question type.
- Agent actions are auditable and safely gated.

## Success Metrics
- `fake_citation_rate = 0` in regression suite.
- `strategy_selection_accuracy >= 0.85` on labeled queries.
- `destructive_action_without_confirmation = 0`.

## Deployment
- Release tag: `v0.12.0-guardrails-agent`
- Production checklist from roadmap fully mappable to shipped capabilities.
