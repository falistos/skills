# Patterns catalog

For tiers 3–4. Repo standards override this catalog; prefer a pattern only for a concrete variation or
boundary.

| Pattern | Fits / missing signal | Abuse / smaller Java form |
|---|---|---|
| Strategy | Runtime/config variation; long type/mode branches, each new mode edits central logic | One variant/non-variation; use Function/method reference or behavior record, sealed switch for a closed set |
| Registry | Dynamic handlers/providers/actions; hand name/id dispatch or scattered reflection | Fixed tiny set/global mutable registry; Map or passed factory suffices, ServiceLoader/SPI across jars |
| Builder | Many optional fields, stepwise creation; telescoping constructors, 6+ similar positional args, setter sequences | Two-field record/all fields always set; static factory/copy-with or nested sealed config records |
| Factory | Distinct semantics, opaque constructors, runtime subtype; caller helpers around new | Pure new wrapper; named static factory beside validated record constructor |
| Composition/delegation | Reuse without is-a or runtime swap; template bases, narrow subclass overrides | Value-free forwarding; expose inner object; sealed records may remove inheritance |
| Observer/event bus | Open-ended multiple reactions; producer edits for every new consumer, cross-cutting work tangled in business logic | One fixed subscriber, sync control flow, Object payloads; reuse platform bus, typed event records |
| Visitor | Fixed types, frequently added operations | On Java 21+, prefer sealed record-pattern switch with exhaustiveness |
| Adapter | Mismatched APIs; third-party types spread into internals | Pass-through wrapper |
| Decorator | Orthogonal logging/cache/retry/metrics repeated across many classes | Deep chains or replacing a strategy |
| Template method | Fixed sequence/varying steps; repeated scaffolding | Deep protected-hook inheritance; prefer Strategy/composition or Function/Consumer argument |
| Singleton/locator | Truly global immutable service; small-app locator only if repo permits | Mutable globals, hidden method-body lookups, god locator; constructor injection, no enterprise DI unless project scale warrants it |
| Repository | Domain-shaped persistence; SQL/ORM leaks into domain, repeated queries | Many findBy combinations → query/spec object; generic BaseRepository without domain contract |
| Specification/predicate | Composable rules/queries; repeated conditions or long conjunctions | Predicate.and/or/negate often suffices |
| Chain of responsibility | Configurable short-circuiting pipeline; new step edits a central chain | One step, or choosing one handler (registry) |
| State machine | Finite states with transitions; scattered status/action assignments or silently invalid transitions | Sealed states, record payloads and pattern-matched transitions |

A framework's own composition, injection and state rules outrank the generic singleton/locator exceptions here.
