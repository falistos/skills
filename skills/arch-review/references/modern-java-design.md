# Modern Java as design tools

For tiers 5/7. Report visible gains in valid-state modeling, exhaustiveness, immutability or intent, not
syntax alone. Respect the configured Java target and the repo's Java rules.

## Modeling

- **Records:** value objects, DTOs/events/payloads, final-field boilerplate or unused setters. Keep identity
  entities and mutating private state as classes; validate in compact constructors, use static
  factories/interfaces where needed.
- **Sealed hierarchies:** finite settled variants, status-dependent fields, enum-as-sum-type or a type tag.
  Keep SPI/third-party and unsettled extension sets open. Sealed records plus exhaustive switch make invalid
  combinations unrepresentable and force consumers to handle new variants.
- **Pattern switch/record patterns:** replace long instanceof/cast chains or Visitor for closed models. A
  nonsealed parent/default throw loses exhaustiveness.
- **Other syntax:** instanceof binding, switch expressions, text blocks and var matter only when repeated
  changes improve clarity. Keep small concatenations; use var only when the type is evident.

## State/concurrency

Use the repo's IO/ownership, threading and persistence conventions where it has them. Review guessed fixed IO pools and callback contortions caused by pool scarcity; distinguish
IO from CPU work.

Structured concurrency can clarify sibling failure/cancellation and raw-thread lifetimes. Check preview status
on the project's JDK; keep suggestions Minor/forward-looking unless preview is already enabled.

## Collections and expressions

- Prefer transformation pipelines, ordinary loops for side effects; flag single-element streams, side-effect
  forEach and long map lambdas only when clarity suffers.
- Method references/lambdas can replace single-method anonymous classes.
- Expected absence follows the team's Optional/value rule; review unchecked get and Optional parameters/fields
  as modeling smells.
- Immutable factories/copies simplify defensive-copy boilerplate and prevent exposing mutable internals.
- Sequenced getFirst/getLast is Minor unless pervasive.
