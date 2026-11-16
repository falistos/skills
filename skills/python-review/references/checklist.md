# Review checklist

Use for issues beyond enabled lint/type checks; let repo policy override smells. Async and modernization have
sibling references.

## Runtime/security

- Check semantic traps static tools miss: falsey versus None, iterator consumed twice, mutation during
  iteration, bounds, runtime validation stripped by -O, broad catches hiding failures and cleanup tied to
  GC/happy paths.
- Trace real untrusted input into shell, SQL, eval/exec/pickle, YAML loaders and filesystem paths; verify
  parameterization, safe loading and resolved containment where relevant.
- Review weak hashes in auth/integrity/signing (cache fingerprints are fine), timing-safe secret comparison,
  TLS bypass and logs containing secrets/PII. Linters cover literal syntax, not end-to-end trust.

## Architecture

- God-class/module size (~500/~1000 lines) is a signal; split responsibilities, not line counts.
- DB/HTTP in domain logic suggests an IO adapter/Protocol; consistent anemic models can be intentional,
  persistence-heavy domain models deserve review.
- Libraries need explicit stable exports/public types; review cycles, star imports and package re-exports
  against actual callers.
- Avoid one-implementation ABCs without a concrete need; around three implementations may justify one.
  Complete half migrations or document the driver/deadline.
- Keep high-level abstractions above adapters, or document accepted coupling.
- Centralize scattered getenv configuration in startup Pydantic Settings passed explicitly.
- Use a typed domain error vocabulary and one expected-outcome shape per layer; generic boundary
  ValueError/RuntimeError forces callers to inspect internals.
- Hardcoded clock/client/random/path dependencies remove test seams; identify the seam rather than prescribing
  monkey patches.

## Type design

- Public Any infects callers; internal Any may fit. Bare generics are acceptable in scripts, not library
  contracts.
- Narrow concrete requirements to Protocols when useful; runtime_checkable verifies names, not signatures, and
  belongs at genuinely dynamic boundaries.
- Audit override validity, blanket ignores, casts hiding missing runtime validation and typing-only imports
  beyond configured checker/linter coverage.

## Performance/polish beyond tooling

- Trace quadratic membership/concatenation, eagerly evaluated expensive log arguments, per-request HTTP
  clients losing pooling, avoidable whole-file loading, dataframe row iteration and repeated regex work on hot
  paths.
- Review ambiguous public names and error messages for a usable correction. Log levels reflect actual failure,
  degraded recovery, lifecycle/business events or debugging.
- Identify dead/commented code, ownerless TODOs and library diagnostic print calls; normal CLI stdout is fine.
