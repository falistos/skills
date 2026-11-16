# Design anti-patterns

For tiers 1, 2 and 6. Report only project-specific harm; repo standards and recorded exceptions override this
catalog.

## Architecture and layering

- **God class/service:** unrelated responsibilities, high churn and dependency fan-in; 500+ lines/30+
  methods/15+ fields are signals, not verdicts. Split by responsibility.
- **Static/global state:** hidden dependencies through `getInstance()`, static collections or config; inject
  dependencies. Truly global immutable services may fit when the framework offers no lifecycle scope.
- **Hidden coupling:** shared files/statics create links absent from imports; make collaborators/events
  explicit.
- **Cycles:** extract a shared concept, invert an edge or merge what is one module.
- **Hub dependency:** most importers need different parts; split by responsibility.
- **Ball of mud:** mixed domain/persistence/commands with no boundaries is Critical; move natural slices
  incrementally.
- **Misplaced concern:** framework/SQL/presentation owns domain logic or vice versa; fix painful leaks,
  calibrated to size.
- **Missing boundary:** replaceable implementation details contaminate many callers; isolate only a boundary
  that matters, not Bukkit ports for a small plugin.
- **Half migration:** old/new patterns stalled in one module is Major; finish or justify both and freeze
  legacy.

## Domain and abstractions

- **Anemic model:** repeated/missed invariants across services; put behavior/validation on entities/value
  objects and leave orchestration/IO to services. For JPA/Spring report the trend, not each entity.
- **Primitive obsession:** introduce value records for real rules/semantics or swapped-argument risk, not
  plain counts.
- **Data clumps:** 3+ repeated parameter groups suggest a missing record concept.
- **Long parameters:** 5+ or mixed flags/data/dependencies; group data, type flags/split methods,
  constructor-inject dependencies.
- **Feature envy:** move repeated getter-based work to the object owning the data; multiple envious classes
  suggest an under-modeled owner.
- **Train wreck:** move deep chained operations to the data owner; chains on value objects/records are fine.
- **Speculative generality:** one implementation/variant with no next consumer, fake generics or unused
  extension points; collapse until a real second case.
- **Useless wrapper:** delete pure pass-through services/classes.
- **Inheritance for reuse:** without is-a, favor composition/delegation or a helper/strategy.
- **Type dispatch:** open set → polymorphism; closed set → sealed records and exhaustive switch.
- **Golden hammer:** remove patterns/libraries from contexts without benefit.
- **Reinvention:** reuse JDK and framework primitives before hand-rolling one.

## Errors

Expected absence/failure and loop exits use values (`Optional`/Result), unless the repo rules say otherwise;
exceptions represent exceptional failures.
