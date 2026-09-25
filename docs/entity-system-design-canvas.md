# Hermes Entity System — Design Canvas

> **Status:** Working document, not a final architecture.
>
> This canvas separates the logical model, physical storage, and computational implementation. It is meant to support incremental architectural decisions rather than prescribe the entire system at once.

## Contents

1. [Entity](#1-entity)
2. [Entity Identity](#2-entity-identity)
3. [Identifiers](#3-identifiers)
4. [Aliases](#4-aliases)
5. [Observations](#5-observations)
6. [Entity Resolution](#6-entity-resolution)
7. [Resolution Evidence](#7-resolution-evidence)
8. [Canonicalization](#8-canonicalization)
9. [Entity Registry](#9-entity-registry)
10. [Relationships](#10-relationships)
11. [Entity Graph](#11-entity-graph)
12. [Provenance](#12-provenance)
13. [Temporal / Historical Identity](#13-temporal--historical-identity)
14. [Storage](#14-storage)
15. [APIs](#15-apis)
16. [Python ↔ Rust Boundary](#16-python--rust-boundary)
17. [Scale](#17-scale)
18. [Open Design Questions](#18-open-design-questions)

## Important Distinctions

The term **canonical entity** currently combines three different ideas:

1. The real-world referent.
2. Hermes's identity assignment.
3. The current best-known projection of that entity.

These can diverge. A stable identity should not be confused with the latest name, the current attributes, or the current source consensus.

Two operations should also remain separate:

- **Normalization for comparison:** preparing values to be compared.
- **Canonicalization of managed knowledge:** choosing versioned current or historical projections.

A useful provisional vocabulary is:

```text
Observation              = source-bound record or extracted fact
Entity identity          = stable Hermes identity for a referent
Canonical projection     = versioned current view derived from evidence
Identifier assertion     = scoped external identifier claim
Resolution decision      = comparison outcome with evidence
Relationship assertion   = source-bound relationship claim
Entity graph             = queryable view over identities and relationships
```

These labels are provisional. They are not final class or table names.

---

## 1. Entity

### Currently known

- An Entity represents a real-world thing.
- Multiple source records may refer to one Entity.
- Hermes must support arbitrary domains.
- The initial sketch includes names, identifiers, aliases, attributes, metadata, and relationships.

### Major questions

- Does “Entity” mean a physical thing, legal person, organization, conceptual object, event, document, or role?
- Are roles such as CEO, owner, issuer, or commander entities, or relationships?
- Are events entities, or only observations and assertions?
- Is `entity_type` immutable, time-varying, provisional, or multi-valued?
- Can an Entity exist without a canonical name?
- What is the minimum identity information required?

### Decisions needed

- Whether `Entity` means the referent itself or a Hermes-managed identity record.
- Whether facts, labels, and relationships are embedded or separate logical records.
- How entity types are asserted and versioned.
- Which domain concepts are universally first-class and which remain extensions.

### Defer

- Complete ontology.
- Class hierarchy.
- Universal property catalog.
- Final physical entity schema.

### Challenge

Putting `relationships` directly inside an Entity makes the Entity look authoritative while hiding the relationships' sources, times, and conflicts.

Not everything deserves entity identity. An economic-indicator value, a CEO role, or a source-document mention may be better represented as an observation or relationship unless traversal requires it to be a node.

---

## 2. Entity Identity

### Currently known

- Hermes IDs such as `HRM-CMP-...` represent canonical identity.
- External identifiers are not Hermes identity.
- Identity should survive name and attribute changes where appropriate.

### Major questions

- When is an ID minted?
- Can an unresolved observation have an Entity ID?
- Is an ID global across all entity types?
- What happens when an entity's apparent type changes?
- How are mergers, splits, reincorporations, and erroneous merges represented?
- Can a merge be reversed or challenged later?

### Decisions needed

- Whether IDs are opaque and immutable.
- Whether IDs are ever reused.
- Whether type prefixes are semantic or merely display conventions.
- How old IDs remain resolvable after lifecycle events.
- Whether a registry permits reopening prior identity decisions.

### Defer

- UUID, ULID, or custom ID syntax.
- Distributed ID allocation.
- Cryptographic identity mechanisms.

### Challenge

An Entity ID stabilizes a decision; it does not prove that the decision was correct. If erroneous merges cannot be reversed, the registry will fossilize mistakes.

A typed prefix such as `CMP` is convenient, but should not be the actual identity mechanism if type classification can be disputed or change.

---

## 3. Identifiers

### Currently known

- Entities can have many external identifiers.
- Identifier schemes have different scopes and semantics.
- Identifiers need provenance and historical handling.

### Major questions

- Which identifier schemes are supported?
- What is the namespace, issuer, scope, and version of each scheme?
- Can one identifier be reused?
- Can an identifier be shared by multiple entities?
- Are identifiers asserted, verified, rejected, or merely observed?
- How are conflicting identifier claims handled?
- Which identifier types are sensitive and access-controlled?

### Decisions needed

- Identifiers should be separate logical records rather than fields on Entity.
- Each identifier assertion should preserve scheme, value, scope, provenance, status, and validity where known.
- Exact identifier equality should be scoped, not global.
- Identifier matching should produce evidence, not silently establish identity.

### Defer

- A universal external identifier registry.
- Canonical URI syntax.
- Identifier-matching infrastructure beyond the initial implementation.

### Challenge

The example containing `Apple`, `AAPL`, `US0378331005`, and CIK `320193` mixes different identity levels.

Typically:

- `AAPL` identifies an exchange-scoped trading symbol.
- An ISIN identifies a financial instrument.
- A CIK identifies an issuer or company.

Those should not automatically resolve to one Entity. The security may be related to the issuer, but they are not necessarily the same thing.

---

## 4. Aliases

### Currently known

- Entities can have names, former names, translations, abbreviations, and source-local labels.
- Aliases are evidence about labels, not identity by themselves.

### Major questions

- Is an alias one concept or a family of label assertions?
- Are names, translations, former names, and colloquialisms different alias types?
- Are aliases language- and script-aware?
- Are aliases valid over time?
- Can an alias be source-specific or context-specific?
- Can one alias apply to many entities?

### Decisions needed

- Keep aliases logically separate from the identity record.
- Preserve provenance and validity for aliases.
- Allow aliases to be disputed or superseded.
- Treat the current canonical name as a selected presentation value, not identity.

### Defer

- Multilingual alias taxonomies.
- Global fuzzy-alias indexes.
- Automatic transliteration and translation policies.

### Challenge

Aliases must not become globally unique keys. “Apple,” “AC,” or “The Bank” can refer to multiple things depending on type, language, place, and time.

A source-specific label should not silently become a global canonical name.

---

## 5. Observations

### Currently known

- An SEC filing saying “Apple Inc., CIK 320193” is an observation.
- Connectors produce source-bound data.
- Existing Hermes `Dataset`, `Source`, `Lineage`, and provenance concepts should be reused.

### Major questions

- Is an Observation:
  - a raw source record,
  - a normalized record,
  - an extracted claim,
  - or a bundle of claims?
- Can one observation refer to multiple entities?
- Can one observation support multiple relationships?
- How are corrections and superseding records represented?
- What is the observation's stable identity?
- How much interpretation belongs inside the observation?

### Decisions needed

- Preserve source artifacts and source-bound observations.
- Keep observations immutable; corrections should create new evidence.
- Allow unresolved entity references.
- Reuse existing Hermes source and lineage concepts rather than creating a parallel source model.
- Support field-level or claim-level evidence where needed.

### Defer

- A universal claim/assertion grammar.
- Event sourcing for all observations.
- A final physical representation for raw payloads.

### Challenge

If Observation is only a row, field-level provenance is lost. If every field becomes a separate universal assertion, volume and complexity may become unreasonable.

Also distinguish a source document from a document entity. A filing can be a source artifact, a real-world document, or both; those are different roles.

---

## 6. Entity Resolution

### Currently known

The conceptual pipeline is:

```text
profiling
→ field identification
→ canonicalization
→ blocking
→ candidate generation
→ comparison
→ scoring
→ decision
```

Python orchestrates; Rust can implement expensive kernels.

### Major questions

- Is the comparison unit an Observation, an extracted record, a canonical Entity, or a relationship assertion?
- How are pairwise comparison and dataset-level clustering related?
- How are blocking keys selected and versioned?
- How do schemas influence candidate generation?
- How are type constraints and incompatible schemas handled?
- How are negative and missing values treated?
- How are thresholds configured?
- How are human decisions incorporated?
- How are clusters updated when new evidence contradicts an old match?

### Decisions needed

Separate:

- candidate generation,
- pairwise comparison,
- policy decision,
- observation-to-entity assignment,
- cluster maintenance.

Treat `MATCH`, `NON_MATCH`, and `UNCERTAIN` as policy outcomes with evidence.

Make batch resolution produce a run artifact, assignments, unresolved cases, and diagnostics. Avoid silent mutation of canonical entities.

Define `NON_MATCH` as evidence of distinctness, not merely lack of evidence.

### Defer

- Embeddings.
- Learned matching models.
- Distributed resolution.
- A universal clustering algorithm.

### Challenge

Pairwise matching is not enough to establish dataset identity. If `A ≈ B` and `B ≈ C`, it does not automatically follow that `A ≈ C`. Naive union-find can create irreversible over-merging.

Schema inference is also not the same operation as entity resolution. `resolve_data()` must expose what it inferred about columns and records rather than pretending the meaning was known.

---

## 7. Resolution Evidence

### Currently known

- Decisions must be explainable.
- Sources, comparisons, scores, and policies must remain distinguishable.
- Human review may be needed later.

### Major questions

- What exactly is evidence: a source assertion, a normalized value, a feature, a comparison, or a model output?
- Should evidence be stored per field, per candidate pair, or per cluster assignment?
- How are negative and missing signals represented?
- How are correlated sources handled?
- How are policy, algorithm, and model versions recorded?
- How are human decisions distinguished from automated decisions?

### Decisions needed

Preserve at least these distinctions:

```text
evidence
→ score
→ policy decision
→ outcome
```

A single scalar `confidence` is insufficient. It may mean source trust, match probability, score strength, or policy margin.

Evidence should include enough information to reproduce the decision: compared values, normalization version, comparator, feature values, policy version, and source references.

### Defer

- Vector storage for evidence.
- A fixed evidence schema.
- A review UI.

### Challenge

Confidence is not automatically probability. A score of `0.92` has no statistical meaning until the scoring process is calibrated against representative data.

Absence of evidence should not be treated as evidence of non-match.

---

## 8. Canonicalization

### Currently known

- Hermes needs canonical names and attributes.
- Sources may disagree.
- Canonical data must preserve provenance and history.

### Major questions

- Is canonicalization:
  1. normalization for comparison, or
  2. construction of a current Entity projection?
- Should both happen?
- Which source wins for each field?
- Are source-precedence rules global, type-specific, field-specific, or time-specific?
- How are conflicts represented in the current view?
- Can users override a value without destroying evidence?
- Is the current projection rebuildable?

### Decisions needed

- Separate comparison normalization from canonical knowledge projection.
- Preserve all source assertions even when a current value is selected.
- Make canonical values versioned and rebuildable.
- Treat manual overrides as explicit, provenance-bearing decisions.
- Define “current” separately from “historically valid.”

### Defer

- Universal source-authority rules.
- Default conflict-resolution policies.
- Attribute-level embeddings or learned canonicalization.

### Challenge

“Canonical” does not mean “true.” A selected value can be useful for display or querying while remaining contested.

A single mutable `Entity` row containing the latest name, status, headquarters, and CEO will eventually hide conflicts and historical changes.

---

## 9. Entity Registry

### Currently known

- Hermes needs persistent identity across repeated ingestion.
- Entity IDs and lifecycle need durable management.
- The registry may be logical rather than a service.

### Major questions

- What exactly does the registry own?
- Does it own only IDs and lifecycle, or also canonical projections?
- How are unresolved candidates represented?
- How are merges, splits, retirements, and reactivations recorded?
- Can historical IDs point to current identities?
- Is there one registry or multiple domain registries?
- Who can perform lifecycle operations?

### Decisions needed

- Treat the registry as the authority for identity and lifecycle.
- Keep it separate from evidence and relationship storage.
- Record lifecycle events rather than destructively rewriting identity history.
- Avoid hard deletion; distinguish disappearance, dissolution, and deletion policy.
- Decide whether placeholder entities are allowed and when they are promoted.

### Defer

- Service boundary.
- Database choice.
- Global versus domain-specific registry topology.

### Challenge

If the registry stores every fact, it duplicates the evidence system and becomes a bottleneck. If it stores only `id → name`, it cannot explain merges, uncertainty, or historical continuity.

The registry should be authoritative about **which identity exists**, not about every fact ever learned about it.

---

## 10. Relationships

### Currently known

- Relationships connect canonical entities.
- Relationships may have provenance, confidence, validity, and attributes.
- Relationship data can be represented independently of a graph database.

### Major questions

- Is a relationship a source assertion, a canonical fact, or a derived edge?
- Which relationship types are universal?
- Which are domain-specific?
- Are relationships always pairwise?
- How are roles and qualifiers represented?
- Can a relationship have multiple sources with conflicting claims?
- What is the identity of a relationship record?
- Can relationships point to unresolved observations?

### Decisions needed

- Preserve source relationship assertions separately from derived or accepted graph relationships.
- Make relationships first-class logical records rather than only nested Entity fields.
- Support provenance, confidence/status, validity intervals, and qualifiers.
- Allow derived relationships to reference the assertions and resolution decisions that produced them.
- Preserve conflicting claims instead of overwriting them.

### Defer

- A complete relationship ontology.
- Automatic inverse relationships.
- A universal edge schema.
- Rules for inferring ownership, control, or succession.

### Challenge

A simple edge such as:

```text
Apple --issues--> AAPL
```

may hide important distinctions: issuance event, instrument type, time, market, and legal role. A graph edge without qualifiers may be visually elegant but semantically too weak.

Source claims should not be lost by waiting until after entity resolution to create relationships.

---

## 11. Entity Graph

### Currently known

- The graph is a logical view over entities and relationships.
- Physical graph storage is not required.
- Graph queries and traversal are future capabilities.

### Major questions

- Does the graph contain:
  - canonical entities only,
  - accepted relationships,
  - all source assertions,
  - or some combination?
- How are uncertain relationships represented?
- How do temporal traversal and snapshots work?
- What does a path mean when edges have different provenance and confidence?
- Is the provenance graph separate from the entity graph?
- How are graph versions identified?

### Decisions needed

- Define the graph as a projection over canonical identities and relationship records.
- Distinguish entity edges from provenance links.
- Define current, historical, and uncertain traversal semantics.
- Keep graph APIs independent of graph databases.

### Defer

- Neo4j or another graph database.
- Cypher or another query language.
- Materialized graph snapshots.
- Distributed graph serving.

### Challenge

Calling any relationship table “the graph” hides whether its edges are asserted, accepted, inferred, current, or merely observed.

A graph database would add infrastructure before the project has established that graph-specific traversal or indexing is the bottleneck.

---

## 12. Provenance

### Currently known

Hermes already has concepts for:

```text
Source
Dataset
Provenance
Lineage
```

The entity system should integrate with them.

### Major questions

- At what granularity is provenance recorded?
- Does provenance attach to:
  - source artifacts,
  - observations,
  - fields,
  - assertions,
  - canonical values,
  - resolution decisions,
  - relationships,
  - derived graph edges?
- How are transformations and extraction models recorded?
- How are source trust and factual confidence represented?
- What retention and deletion policies apply?

### Decisions needed

- Reuse existing provenance and lineage concepts.
- Attach provenance to evidence-bearing records, not only to Entity aggregates.
- Record computational provenance for automated resolution and canonicalization.
- Keep provenance separate from confidence and truth.
- Support sensitivity/access classifications for government IDs and personal data.

### Defer

- Full W3C PROV adoption.
- A general-purpose lineage service.
- Distributed provenance infrastructure.

### Challenge

Entity-level provenance is insufficient. If five sources contributed conflicting attributes, Hermes must be able to explain which source supported which value and when it was observed.

---

## 13. Temporal / Historical Identity

### Currently known

Entities change over time:

```text
names
attributes
identifiers
relationships
ownership
status
```

Identity may also change through mergers, splits, renames, acquisitions, dissolution, and reincorporation.

### Major questions

- Is `observed_at` different from `valid_from` and `valid_to`?
- Which times are supplied by sources?
- What happens when validity is unknown?
- How are historical names and identifiers preserved?
- How are predecessor and successor relationships represented?
- What does a merger do to old IDs?
- What does a split do to the old ID?
- Does a reincorporated company continue the same identity?

### Decisions needed

- Preserve historical assertions rather than overwriting them.
- Distinguish observation time from factual validity where possible.
- Keep IDs stable across renames and ordinary attribute changes when policy permits.
- Represent mergers and splits as lifecycle events, not merely aliases.
- Preserve old IDs as historical references.

### Defer

- Full bitemporal storage.
- Temporal database requirements.
- A universal event-sourcing model.
- Exact legal-continuation rules for every jurisdiction.

### Challenge

A rename may preserve identity. A merger may combine two previously distinct legal identities. A split cannot safely reuse one old ID for several descendants without an explicit policy.

Generic `same_as` and `alias` relationships are insufficient for these cases.

---

## 14. Storage

### Currently known

Possible physical representations include:

```text
Parquet
Arrow
DuckDB
Postgres
graph databases
```

The project has limited hardware and should remain local-first.

### Major questions

- Which workload is primary:
  - bulk analytical scans,
  - transactional identity updates,
  - point lookups,
  - graph traversal,
  - or evidence append?
- Can the registry be rebuilt from immutable data?
- What requires strong consistency?
- How are snapshots and indexes versioned?
- What is the update and compaction policy?
- How are sensitive fields protected?

### Decisions needed

- Keep logical records independent of storage adapters.
- Prefer simple local storage initially.
- Treat evidence and provenance as append-oriented.
- Allow current projections and indexes to be rebuilt.
- Use transactional storage only where identity lifecycle demands it.

### Defer

- Production database choice.
- Distributed storage.
- Graph database adoption.
- A universal index architecture.

### Challenge

`entities.parquet`, `identifiers.parquet`, and `relationships.parquet` are not automatically a coherent data system. Referential integrity, snapshot consistency, mutation, index rebuilding, and recovery still need definitions.

Parquet is strong for immutable analytical data but weak as a transactional identity registry. DuckDB can query files but is not automatically the authoritative write path.

---

## 15. APIs

### Currently known

Intended APIs include:

```python
hr.resolve(left, right)
hr.resolve_data(data)
```

Input may eventually include Polars, Arrow, pandas, or SQL-backed data.

### Major questions

- Are `left` and `right` observations, records, or canonical entities?
- What does a resolution result contain?
- Does resolution mutate the registry?
- How are schema hints and policies supplied?
- How are unresolved and ambiguous records returned?
- How are runs versioned and reproduced?
- What is the separate operation for applying approved links?

### Decisions needed

- Return a structured result, not only a boolean.
- Include outcome, evidence, score components, candidate-generation reason, policy/model version, and diagnostics.
- Make `resolve_data()` return assignments plus unresolved cases and interpretation warnings.
- Separate “calculate resolution” from “apply identity changes.”
- Define a logical tabular input contract before optimizing for a particular DataFrame library.

### Defer

- Exact SDK signatures.
- Configuration language.
- Async API.
- Graph query language.
- Human-review API details.

### Challenge

`resolve_data(data)` cannot reliably infer semantics from column names alone. It may assist with inference, but it must expose uncertainty rather than hide it.

A schema mismatch or incomparable record should not automatically become `NON_MATCH`. That would confuse “different” with “not enough information to compare.”

---

## 16. Python ↔ Rust Boundary

### Currently known

- Python orchestrates workflows.
- Rust handles computationally expensive operations through PyO3.
- The system targets Python and Rust, not heavyweight ML infrastructure.

### Major questions

- Which operations are actually bottlenecks?
- Should Rust own normalization, blocking, comparison, or only selected kernels?
- What is the cost of crossing the PyO3 boundary?
- Should kernels operate on Python objects or columnar batches?
- How will algorithm versions be exposed?
- Which logic must remain policy-driven in Python?

### Decisions needed

- Python owns I/O, configuration, provenance, lifecycle, policy, and orchestration.
- Rust should initially own deterministic, batch-friendly computational kernels where profiling justifies it.
- Likely candidates for later measurement:
  - distance calculations,
  - phonetic methods,
  - n-gram processing,
  - blocking-key generation,
  - candidate scoring,
  - selected Arrow/columnar operations.
- Keep domain semantics and policy thresholds out of low-level Rust kernels.

### Defer

- Full Rust-side pipeline.
- GPU inference.
- Rust-specific ML runtime.
- Fine-grained Python-to-Rust calls for every string.

### Challenge

Moving orchestration into Rust too early creates a second framework and makes policy changes harder.

Fine-grained PyO3 calls may also be slower than Python-level vectorized or standard-library operations for small datasets.

---

## 17. Scale

### Currently known

The potential range is:

```text
thousands
→ millions
→ hundreds of millions
→ billions
```

The initial machine has approximately 8 GB RAM and four CPU cores.

### Major questions

- What is the real cardinality and latency target?
- What block sizes are acceptable?
- How will candidate recall be measured?
- How are new observations matched against existing entities?
- How are clusters revised when evidence changes?
- How are large blocks prevented from exhausting memory?
- How are high-cardinality identifiers and common names handled?
- What can be processed incrementally?

### Decisions needed

- Never make all-pairs comparison the default.
- Use blocking and persistent candidate indexes.
- Preserve observation-to-entity assignments across ingestion runs.
- Support bounded batches, external sorting, and partitionable inputs.
- Partition or index by type, namespace, source, and time where appropriate.
- Design evidence storage so reprocessing does not destroy prior decisions.

### Defer

- Distributed execution.
- Spark, Ray, or Kubernetes.
- Vector databases.
- Billion-record guarantees before measuring workloads.

### Challenge

“Supports billions” is not a useful first requirement without data distributions, latency targets, and acceptable error rates.

Rust can make comparison faster, but it cannot fix poor blocking or uncontrolled candidate growth.

---

## 18. Open Design Questions

The highest-leverage decisions, in order, appear to be:

1. Does `Entity` mean a stable referent identity, a mutable canonical record, or both?
2. What is the minimum identity payload, and when is an ID minted?
3. Is an Observation a source record, an extracted claim, or a bundle of claims?
4. Which things qualify as entities: roles, events, documents, measurements, brands, securities, legal entities?
5. How are entity types modeled and revised?
6. How are identifier namespaces and identifier status represented?
7. What exactly does a pairwise resolution result mean?
8. How does dataset resolution move from pairwise matches to clusters?
9. What lifecycle semantics apply to merges, splits, renames, and reincorporations?
10. What minimum temporal model is required from the beginning?
11. Are source relationship assertions separate from accepted graph edges?
12. How are conflicting sources selected for current projections?
13. What does human review change, and how is it audited?
14. What privacy and access controls are needed for personal identifiers?
15. What is the smallest useful local storage implementation?
16. Which operations genuinely need Rust?
17. What scale workload should drive the first optimization work?

### Things not to decide yet

- A complete universal ontology.
- Neo4j or another graph database.
- Embeddings or machine-learned matching.
- Distributed infrastructure.
- A sophisticated graph query language.
- A complex event-sourcing architecture.
- A permanent ID syntax.
- A large domain-specific class hierarchy.

### Suggested discussion order

```text
Entity semantics
→ Observation/claim boundaries
→ Identity and registry lifecycle
→ Resolution contracts
→ Temporal and provenance rules
→ Relationships and graph semantics
→ Storage
→ Python/Rust optimization
```

## First Discussion Question

My provisional position is:

```text
Entity = stable identity for a referent
Current name/attributes = versioned projection
Observations = source-bound evidence
Relationships = separate provenance-bearing records
```

The first decision is:

> When Hermes says two things are the same Entity, should continuity mean the same real-world referent, the same legal or organizational identity, or a type-specific continuation policy?

A renamed company, an acquired subsidiary, a reused brand, and a security versus its issuer may require different answers.
