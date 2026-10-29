## 1. What Company should expose

Split it into three groups:

**Identifiers (filled at resolve time, no network call afterwards)**
- `name`, `legal_name`, `aliases`
- `country`, `jurisdiction`
- `lei`, `cik`, `permid`, `wikidata_id`, `website`/`domain`
- `listings`: a **list**, not a single symbol. Apple trades on several exchanges, each with its own ticker and exchange code.
- `securities`: ISIN, CUSIP, SEDOL, FIGI per share class
- `industry_codes`: SIC, NAICS, ISIC

**Data (lazy, fetched on first access, then cached)**
- `profile` (description, HQ, employees, sector)
- `financials` (income statement, balance sheet, cash flow)
- `filings`
- `news`
- `prices`
- `ownership` (institutions, insiders)
- `officers`
- `corporate_actions` (dividends, splits)
- `estimates`
- `events` (earnings dates etc.)
- `relations` (parent, subsidiaries, peers)

**Rule of thumb:** a `@property` can't take arguments. If you need a date range or period, make the property return an object that has methods. For example, `apple.prices` returns a `Prices` object, and then you call `apple.prices.history(start, end)`. Use `functools.cached_property` so each one hits the network only once.

## 2. Identifiers and where to get them

First, an important point: **entity, security, and listing are three different things.**
- The **entity** is the company (Apple Inc.). It has a LEI, CIK, and registration number.
- The **security** is a share class. It has an ISIN, CUSIP, and FIGI.
- The **listing** is a security on an exchange. It has a ticker and an exchange code (MIC).

Most people's code breaks because they treat "symbol" as a company identifier. It's a listing identifier.

| Identifier | Level | Source | Notes |
|---|---|---|---|
| **LEI** | Entity | GLEIF API (free, global) | Also gives legal name, jurisdiction, registration number, and parent/child ownership |
| **CIK** | Entity | SEC EDGAR (`company_tickers.json`, submissions API) | US-listed only; also gives SIC, former names, fiscal year end. Needs a User-Agent header |
| **Ticker + exchange** | Listing | Exchange listing files, SEC, OpenFIGI | Ticker alone is ambiguous across countries |
| **FIGI** | Security/listing | OpenFIGI (free, global) | Best way to map ticker/ISIN/CUSIP to each other |
| **ISIN** | Security | OpenFIGI, GLEIF's ISIN-LEI mapping file | For US securities it's computable: `US` + CUSIP + check digit |
| **CUSIP** | Security | Derived from ISIN, or SEC filings | US/Canada only, and the licensing is restrictive |
| **SEDOL** | Security | Mostly paid | UK-centric; skip at first |
| **Wikidata QID** | Entity | Wikidata API/SPARQL | Your **crosswalk hub**: one entry often links to ticker, ISIN, LEI, CIK, website, and PermID |
| **PermID** | Entity | LSEG's free API | Good extra cross-reference |
| **Registration number** | Entity | National registries (Companies House UK, SECP Pakistan, etc.), OpenCorporates | Different per country, so this is what makes "global" hard |
| **Domain/website** | Entity | Wikidata, profile data | Great tiebreaker for disambiguation |

Rate limits and key requirements for these APIs change, so check each one's current docs before you build around them.

## What actually makes `resolve_company` hard

1. **Ambiguity.** "Apple" matches Apple Inc., Apple Hospitality REIT, and others. Return a best match with a confidence score plus a list of candidates, and let the user override.
2. **The crosswalk.** Start from one anchor (usually the Wikidata QID or LEI) and expand outward to the others. Store your own internal ID and map every external ID to it.
3. **Not everything exists everywhere.** A private company has no ticker. A non-US company has no CIK. So every identifier should be `Optional`.
4. **Global means per-country sources.** US has EDGAR, UK has Companies House, and so on. Design a provider interface now (`SECProvider`, `GLEIFProvider`, ...) so adding a country later doesn't change `Company`.

A good order to build in: GLEIF + OpenFIGI + SEC first, since they're free and cover the most ground, then add Wikidata as the glue.

Want me to go deeper on the resolution/matching logic, or on the provider interface design?