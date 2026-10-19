# PRD — Shipment Exception Management

## Status and evidence
Independent portfolio simulation, not a Shiprocket product. All shipments are fictional. Rules are illustrative and require seller/carrier validation. No measured business improvement is claimed.

## Problem hypothesis
Sellers managing several shipments may struggle to identify which delivery exceptions need action, understand the last available event, and track ownership across follow-ups.

## Users and jobs
- Seller: identify affected orders and prepare accurate customer updates.
- Support: investigate evidence and own unresolved cases.
- Operations lead: review backlog and ownership.

## Discovery plan
Interview 5–8 sellers about their last delayed shipment. Ask for the timeline, information checked, handoffs, workarounds and outcome. Do not lead with the dashboard solution. Validate scan thresholds, timezones and permitted actions with carrier operations. No interviews have yet been conducted.

## Journey
Order created → pickup scheduled → pickup completed → in transit → out for delivery → delivered.
Branches: missed pickup; stale scan; failed attempt → retry or return. Returned shipments require a separate reconciliation workflow, out of this MVP.

## Prototype scope
Exception queue, priority/status filters, detail inspection, recommended next action, simulated owner/status updates, message drafts and CSV exports. Session-only audit trail. No persistence across refresh/session loss, authorization, external integrations, real notifications, bulk actions or predictions.

## Illustrative rules
Frozen clock: 2026-10-19 12:00 demo-local time; timestamps share that clock.
1. Delivered/returned: suppress active alerts.
2. Future scan: flag invalid data, P1, do not recommend a customer promise.
3. Failed delivery: P1; inspect reason and recipient availability.
4. Pickup pending past scheduled pickup: P2.
5. In transit without a scan for at least 48 hours: P2.
6. An already detected exception past promised delivery becomes P1.
Precedence is the order above: one exception per shipment. These are not universal carrier SLAs. Production needs configurable contractual rules, null handling, UTC storage, event-time ordering and ingestion-lag checks.

## User stories and acceptance criteria
- As a seller I want a prioritized queue so I can act on urgent cases. Given a nonterminal shipment meets a documented rule, queue refresh includes one row with its last scan and rule category.
- As an operator I want to assign ownership. Saving an owner changes the session record and appends an audit entry.
- As a support agent I want resolution evidence. Resolving without a nonblank note fails validation; resolving with a note records the previous and new status.
- As a seller I want a safe customer update. Drafts must not claim delivery guarantees; the UI explicitly says no message was sent.
- As a reviewer I want closed cases distinguishable from active ones. Resolved cases remain available in the queue but are excluded from unresolved counts. Source rule and case status remain separate.

## Edge cases and production backlog
Duplicate scans: deduplicate by carrier event ID. Conflicting statuses: reconcile carrier event time and authority, not arrival order. Missing scans or invalid timestamps: data-quality queue, never silently label delivered. Terminal statuses: suppress active alert, retain history. Reopened issue: create new incident generation while preserving old resolution. Concurrent edits: optimistic locking. PII: minimize fields, role-based access and retention limits. These production behaviors are requirements, not implemented claims.

## Measurement
Primary: median elapsed time from first rule detection to evidence-backed resolution, per incident, not shipment. Segment by category, severity and carrier. Exclude unresolved cases only with explicit censoring disclosure; show open-case age and unresolved proportion alongside the median to prevent gaming.
Guardrails: false-alert rate from sampled human review; duplicate-alert rate; reopen rate within seven days; contact rate per 100 affected shipments; message error rate. Baselines and targets await operational data. The prototype has no detection/resolution timestamp pipeline and does not calculate these outcomes.

## Rollout and responsibilities
PM validates problem/rules and defines success; design validates queue/task usability; engineering builds ingestion, idempotent incidents, persistence and access controls; operations labels alerts and owns playbooks; support approves message templates.
1. Shadow mode on approved data; review false positives.
2. Small opt-in seller pilot; manual message approval and rollback switch.
3. Expand only after agreed data-quality and safety thresholds pass.
Rollback: disable notifications/actions while retaining read-only queue and audit history.
