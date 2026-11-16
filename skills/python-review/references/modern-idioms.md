# Python modernization

For tier 6/tooling recommendations. Respect the repo's Python/dependency target: 3.12+ is a baseline, not
permission to upgrade pinned projects. Generic syntax changes belong to configured ruff UP/PTH/DTZ/TC checks,
not duplicate review findings.

## Version-sensitive design

- Check supported-version gains rather than dates: type parameters/aliases and override (3.12), default type
  parameters (3.13), lazy annotation evaluation/free-threaded build/t-strings (3.14).
- Public generics, Self/fluent returns, LiteralString boundaries and Unpack[TypedDict] kwargs matter when they
  improve contracts; prefer structural Protocol where useful.
- Keep future annotations on ≤3.13 for forward references/cycles; existing use on 3.14+ is harmless, not an
  urgent removal.
- Dataclass slots/frozen/kw-only, match for tagged/tree dispatch, timezone-aware timestamps and async
  sibling/timeout APIs are design leads, not mandatory rewrites. Two-branch conditions stay simple.

## Pydantic v2 review leads

| v1 surface | v2 surface to verify against installed version |
|---|---|
| Inner Config | model_config / ConfigDict (same enum/arbitrary-type options) |
| allow_population_by_field_name | populate_by_name |
| dict/json | model_dump/model_dump_json |
| parse_obj/parse_raw | model_validate/model_validate_json |
| schema | model_json_schema |
| validator / pre=True | field_validator / mode="before" |
| root_validator | model_validator(mode="after") |
| Field env | pydantic-settings Field alias |

Review reusable Annotated constraints, computed_field for serialized derived values, pydantic-settings
BaseSettings/SettingsConfigDict and SecretStr, after-validation on typed data versus before-validation for raw
input, and strict domain validation where coercion is undesirable.

## Tooling recommendations

Recommend concrete pyproject snippets fitted to the repo: Python metadata, backend, ruff and strict
mypy/pyright, pytest and lockfile. The main skill names baseline lint categories; extend only for demonstrated
gaps (PERF/FURB/C4/TID/PIE/RET/SLF/TC etc.).

Prefer uv for environment/dependency/lock management; apps commit uv.lock, libraries may lock dev tooling.
Hatchling fits dynamic/VCS metadata, uv_build simple pure Python, setuptools C extensions. Libraries use src
layout to avoid cwd imports and force installation before tests; small apps may stay flat. Centralize
metadata/tool config in pyproject rather than setup.py/setup.cfg.
