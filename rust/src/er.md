## Hermes ER — Entity Resolution

**Purpose:** Identify records that refer to the same real-world entity, link them with evidence, and preserve the original data.

### 1. Pipeline

```text
Input Data
    ↓
1. Ingestion
    ↓
2. Normalization
    ↓
3. Candidate Generation
    ↓
4. Comparison & Scoring
    ↓
5. Entity Resolution
    ↓
Resolved Entities + Record Links + Evidence
```

### 2. Components

| Component | Responsibility |
|---|---|
| **Ingestion** | Accept records from Polars DataFrames, CSV, JSON, and other supported sources. |
| **Normalization** | Standardize values for comparison without modifying the original data. |
| **Candidate Generation** | Find plausible matching records efficiently, avoiding unnecessary pairwise comparisons. |
| **Comparison** | Compare candidate records using exact, string, token, and domain-specific comparisons. |
| **Scoring** | Combine comparison results into a match score. |
| **Resolution** | Decide whether records match, do not match, or require review. |
| **Entity Management** | Create canonical entity IDs and associate records with entities. |
| **Evidence** | Record why a match was accepted or rejected, including the comparison results. |
| **Clustering** | Group records that refer to the same entity while guarding against incorrect transitive merges. |

### 3. Similarity Algorithms

**Exact matching**
- Exact equality
- Normalized equality

**String similarity**
- Levenshtein
- Damerau–Levenshtein
- Jaro
- Jaro–Winkler
- N-gram similarity

**Token similarity**
- Jaccard
- Cosine similarity
- Token sort similarity
- Token set similarity

**Specialized matching — later**
- Phonetic matching
- Email and phone matching
- Address matching
- Date and numeric comparison
- Domain-specific comparisons

These algorithms are building blocks, not independent decisions about entity identity.

### 4. Candidate Generation

Start with multiple blocking strategies:

- Exact normalized values
- Selected field combinations
- Prefix or phonetic keys where appropriate
- Sorted-neighborhood matching later

Deduplicate candidate pairs and track which blocking rules generated them.

**Key metric:** Candidate generation must retain as many true matches as possible while substantially reducing comparisons.

### 5. Resolution Strategy

For each candidate pair:

1. Compare relevant fields.
2. Account for missing values and contradictory evidence.
3. Calculate a configurable score.
4. Apply configurable decision thresholds.
5. Accept, reject, or flag the match for review.
6. Preserve the evidence behind the decision.

A similarity score is not automatically a probability. Calibrated probabilities can be introduced later.

### 6. Entity and Record Model

Keep these concepts separate:

- **Record:** An original observation from a data source.
- **Entity:** The real-world person, company, organization, or other object.
- **Record link:** An association between a record and an entity.
- **Match evidence:** The information supporting that association.
- **Entity relationship:** A relationship between distinct entities; not itself a match.

Never overwrite the original records. Entity merges and splits should be traceable and reversible.

### 7. Python API

```python
import hermes as hr

# Resolve records
result = hr.resolve(data)

# Configure matching
result = hr.resolve(
    data,
    columns=["name", "email", "address"],
    entity_type="person",
)

# Compare individual values
score = hr.similarity("Apple Inc.", "Apple Incorporated")
```

The API should support configurable columns, entity types, normalization, comparison algorithms, and resolution thresholds without forcing users to configure every detail.

### 8. Rust Module Structure

```text
src/
├── lib.rs
├── ingestion/
│   ├── mod.rs
│   ├── record.rs
│   └── normalize.rs
├── candidates/
│   ├── mod.rs
│   ├── blocking.rs
│   └── pairs.rs
├── comparison/
│   ├── mod.rs
│   ├── exact.rs
│   ├── edit.rs
│   ├── token.rs
│   └── score.rs
├── resolution/
│   ├── mod.rs
│   ├── decision.rs
│   └── cluster.rs
├── entities/
│   ├── mod.rs
│   ├── entity.rs
│   └── record_link.rs
├── evidence/
│   ├── mod.rs
│   └── match_evidence.rs
└── python.rs
```

Start as **one Rust crate with modules**, using PyO3 for Python bindings. Use Polars for Python-side tabular operations; Hermes does not need its own DataFrame implementation.

### 9. Implementation Order

1. Record and entity data models.
2. Normalization.
3. Exact and string comparison.
4. Candidate generation.
5. Scoring and decision thresholds.
6. Entity creation and record linking.
7. Evidence and provenance.
8. Clustering and safeguards against false merges.
9. Python API and packaging.
10. Evaluation benchmarks and advanced algorithms.

**Do not start with machine learning or complex clustering.** First build a correct, measurable baseline.

Evaluate it using precision, recall, F1, candidate recall, reduction ratio, false merges, and false splits.