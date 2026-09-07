module.exports = [
"[externals]/next/dist/shared/lib/no-fallback-error.external.js [external] (next/dist/shared/lib/no-fallback-error.external.js, cjs)", ((__turbopack_context__, module, exports) => {

var mod = __turbopack_context__.x("next/dist/shared/lib/no-fallback-error.external.js", () => require("next/dist/shared/lib/no-fallback-error.external.js"));

module.exports = mod;
}),
"[project]/src/app/docs/api-reference/page.tsx [app-rsc] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>ApiReferencePage,
    "metadata",
    ()=>metadata
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/rsc/react-jsx-dev-runtime.js [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/components/Doc.tsx [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$CodeBlock$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/components/CodeBlock.tsx [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doodle$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/components/Doodle.tsx [app-rsc] (ecmascript)");
;
;
;
;
const metadata = {
    title: "API Reference",
    description: "Reference for the Hermes facade, RawCache, scheduler, feature registry, entities and constants."
};
function ApiReferencePage() {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("article", {
        className: "relative",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "pointer-events-none absolute -left-6 top-40 hidden opacity-40 sm:block",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doodle$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["WobbleCircle"], {
                    className: "h-20 w-20",
                    color: "#ff4328"
                }, void 0, false, {
                    fileName: "[project]/src/app/docs/api-reference/page.tsx",
                    lineNumber: 24,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 23,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["DocTitle"], {
                kicker: "Reference",
                children: "API Reference"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 26,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Lead"], {
                children: [
                    "The public surface of Hermes, centered on the ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "Hermes"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/api-reference/page.tsx",
                        lineNumber: 28,
                        columnNumber: 55
                    }, this),
                    " facade, the",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "RawCache"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/api-reference/page.tsx",
                        lineNumber: 29,
                        columnNumber: 9
                    }, this),
                    ", the scheduler, entities and constants."
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 27,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["H2"], {
                id: "index",
                children: "Reference index"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 32,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Table"], {
                head: [
                    "Section",
                    "What you'll find"
                ],
                rows: [
                    [
                        "Hermes facade",
                        "constructor, attributes, clear_cache, cache_stats"
                    ],
                    [
                        "RawCache",
                        "get / put / get_or_fetch / clear / stats"
                    ],
                    [
                        "Scheduler",
                        "schedule, start, stop, run_now, list_jobs & cron spec"
                    ],
                    [
                        "Entities",
                        "countries, iso3_to_iso2, check_iso3, get_cik"
                    ],
                    [
                        "Constants",
                        "SYMBOLS, TICKERS, CANONICAL_FREQS & more"
                    ],
                    [
                        "Dataset",
                        "the pydantic BaseModel and its fields"
                    ],
                    [
                        "Feature registry",
                        "LineageGraph and TieredPlan"
                    ]
                ]
            }, void 0, false, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 33,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["H2"], {
                id: "facade",
                children: "Hermes facade"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 46,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$CodeBlock$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["CodeBlock"], {
                title: "constructor",
                code: `Hermes(
    opensanction_api: str,
    new_data_api: str,
    fred_api: str,
    sec_username: str,
    sec_email: str,
    finnhub_api: str,
    cache_dir: str | None = None,
    use_cache: bool = True,
) -> Hermes`
            }, void 0, false, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 47,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["P"], {
                children: [
                    "Raises ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "KeyError"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/api-reference/page.tsx",
                        lineNumber: 61,
                        columnNumber: 16
                    }, this),
                    " if both ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "opensanction_api"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/api-reference/page.tsx",
                        lineNumber: 61,
                        columnNumber: 46
                    }, this),
                    " and",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "new_data_api"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/api-reference/page.tsx",
                        lineNumber: 62,
                        columnNumber: 9
                    }, this),
                    " are empty. Creates a shared ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "RawCache(cache_dir)"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/api-reference/page.tsx",
                        lineNumber: 62,
                        columnNumber: 63
                    }, this),
                    " ",
                    "unless ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "use_cache=False"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/api-reference/page.tsx",
                        lineNumber: 63,
                        columnNumber: 16
                    }, this),
                    "."
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 60,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Table"], {
                head: [
                    "Attribute",
                    "Type",
                    "Notes"
                ],
                rows: [
                    [
                        "list_countries",
                        "list[str]",
                        "249 ISO-3 codes"
                    ],
                    [
                        "lf",
                        "features",
                        "feature registry facade"
                    ],
                    [
                        "list_features",
                        "list[Callable]",
                        "= lf.list_features() (~57 features)"
                    ],
                    [
                        "country_features",
                        "pipeline",
                        "country-risk pipeline"
                    ],
                    [
                        "ta_feature",
                        "TAfeatures",
                        "technical analysis"
                    ],
                    [
                        "fa_features",
                        "FAfeatures",
                        "fundamental analysis"
                    ],
                    [
                        "crypto_history",
                        "CryptoHistory",
                        "crypto history"
                    ],
                    [
                        "filling_history",
                        "CompanyFiling",
                        "company filing history"
                    ],
                    [
                        "world_bank, imf, fred",
                        "connector",
                        "global macro"
                    ],
                    [
                        "gdelt",
                        "GDELT",
                        "stub"
                    ],
                    [
                        "opensanction",
                        "OpenSanction",
                        "sanctions"
                    ],
                    [
                        "binance, finnhub, yfin",
                        "connector",
                        "markets"
                    ],
                    [
                        "sec_edger",
                        "SECEDGAR",
                        "SEC filings (sic)"
                    ],
                    [
                        "datasets",
                        "PUBLIC_DATASET",
                        "bundled CSVs"
                    ]
                ]
            }, void 0, false, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 65,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$CodeBlock$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["CodeBlock"], {
                title: "methods",
                code: `def clear_cache(self, older_than: str | None = None) -> None
    # older_than: e.g. "7d", "24h", "2w" — parsed into timedelta

def cache_stats(self) -> dict
    # -> {"total_files", "by_source", "hits", "misses", "hit_rate"}`
            }, void 0, false, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 84,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["H2"], {
                id: "cache",
                children: "RawCache"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 93,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["P"], {
                children: [
                    "In ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "hermes/acquisition/cache.py"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/api-reference/page.tsx",
                        lineNumber: 95,
                        columnNumber: 12
                    }, this),
                    ". Default dir",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "~/.hermes_cache/raw"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/api-reference/page.tsx",
                        lineNumber: 96,
                        columnNumber: 9
                    }, this),
                    ", default TTL 24h. Cache keys are",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "sha256(source + json_params)[:16]"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/api-reference/page.tsx",
                        lineNumber: 97,
                        columnNumber: 9
                    }, this),
                    ", stored as",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "<dir>/<source>/<hash>.parquet"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/api-reference/page.tsx",
                        lineNumber: 98,
                        columnNumber: 9
                    }, this),
                    "."
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 94,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$CodeBlock$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["CodeBlock"], {
                title: "python",
                code: `RawCache(cache_dir: str | Path | None = None)

get(source, params, ttl=None)                    # raises CacheMiss on miss/expiry/corruption
put(source, params, df)                          # writes parquet + .meta.json
get_or_fetch(source, params, fetch_fn,           # cache unless force, else await & cache
             force=False, ttl=None)
clear(older_than: timedelta | None = None)       # delete .parquet (+ meta)
stats() -> {"total_files", "by_source",
            "hits", "misses", "hit_rate"}`
            }, void 0, false, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 100,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["H2"], {
                id: "scheduler",
                children: "Scheduler"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 113,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["P"], {
                children: [
                    "A full asyncio scheduler in ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "hermes/core/scheduler.py"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/api-reference/page.tsx",
                        lineNumber: 115,
                        columnNumber: 37
                    }, this),
                    " supporting interval and cron specs."
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 114,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$CodeBlock$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["CodeBlock"], {
                title: "python",
                code: `from hermes.core.scheduler import schedule, start, stop, run_now, list_jobs

@schedule(time="daily", name="nightly_refresh", timeout=600.0, retries=3)
async def refresh(dataset):
    ...

start()                     # runs loop until KeyboardInterrupt
stop()
run_now("nightly_refresh")  # async: run_now_async; sync wrapper via asyncio.run
list_jobs()                 # name, schedule, next_run, last_run, last_status, runs, failures`
            }, void 0, false, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 118,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Table"], {
                head: [
                    "Spec",
                    "Meaning"
                ],
                rows: [
                    [
                        '"hourly" / "daily" / "weekly"',
                        "1h / 1d / 1w aliases"
                    ],
                    [
                        '"30m" / "2d" / "3w"',
                        "Numeric interval suffixes (m, h, d, w)"
                    ],
                    [
                        '"0 3 * * *"',
                        "5-field cron: min hour day month weekday (Sun=0)"
                    ]
                ]
            }, void 0, false, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 131,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["P"], {
                children: [
                    "Cron supports ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "*"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/api-reference/page.tsx",
                        lineNumber: 140,
                        columnNumber: 23
                    }, this),
                    ", ranges ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "a-b"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/api-reference/page.tsx",
                        lineNumber: 140,
                        columnNumber: 46
                    }, this),
                    ", steps ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "*/n"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/api-reference/page.tsx",
                        lineNumber: 140,
                        columnNumber: 70
                    }, this),
                    " and",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "a-b/n"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/api-reference/page.tsx",
                        lineNumber: 141,
                        columnNumber: 9
                    }, this),
                    ", and comma lists. Retries use exponential backoff capped at 60s."
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 139,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["H2"], {
                id: "entities",
                children: "Entities"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 144,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$CodeBlock$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["CodeBlock"], {
                title: "python",
                code: `from hermes.entities.countries import countries, iso3_to_iso2, check_iso3
from hermes.entities.companies import get_cik

countries          # list[str] of 249 ISO-3 codes
iso3_to_iso2("USA")   # -> "US"
check_iso3("USA")     # -> None; raises RuntimeError if not ISO3
get_cik("AAPL")       # -> "CIK0320193" or "Not Found"`
            }, void 0, false, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 145,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["H2"], {
                id: "constants",
                children: "Constants"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 156,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Table"], {
                head: [
                    "Constant",
                    "Content"
                ],
                rows: [
                    [
                        "SYMBOLS",
                        "20 crypto symbols: BTCUSDT, ETHUSDT, BNBUSDT, XRPUSDT, SOLUSDT, DOGEUSDT, TRXUSDT, ADAUSDT, LINKUSDT, AVAXUSDT, SUIUSDT, LTCUSDT, BCHUSDT, HBARUSDT, NEARUSDT, UNIUSDT, DOTUSDT, APTUSDT, ARBUSDT, OPUSDT"
                    ],
                    [
                        "TICKERS",
                        "18 US equities: NVDA, AAPL, GOOGL, MSFT, AMZN, AVGO, META, TSLA, LLY, WMT, AMD, V, XOM, JNJ, ORCL, COST, NFLX, CRM"
                    ],
                    [
                        "CANONICAL_FREQS",
                        "15 intervals: 1s, 1m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M"
                    ],
                    [
                        "SUPPORTED_STOCK_FREQS",
                        "1m, 5m, 15m, 30m, 1h, 1d, 1w, 1M"
                    ],
                    [
                        "BINANCE_INTERVAL_* / FINNHUB_* / YFINANCE_*",
                        "Canonical ↔ provider interval maps and max lookbacks"
                    ]
                ]
            }, void 0, false, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 157,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["H2"], {
                id: "dataset",
                children: "Dataset"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 168,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["P"], {
                children: [
                    "A pydantic ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "BaseModel"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/api-reference/page.tsx",
                        lineNumber: 170,
                        columnNumber: 20
                    }, this),
                    " in ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "hermes/core/dataset.py"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/api-reference/page.tsx",
                        lineNumber: 170,
                        columnNumber: 46
                    }, this),
                    ":"
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 169,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$CodeBlock$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["CodeBlock"], {
                title: "python",
                code: `class Dataset(BaseModel):
    id: uuid.UUID          # default_factory=uuid4
    name: str
    version: str
    schema_ref: ...
    metadata: MetaData
    provenance: Provenance
    lineage: Lineage`
            }, void 0, false, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 172,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["P"], {
                children: [
                    "The composable parse/normalize/validate/query methods and the",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "Lineage"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/api-reference/page.tsx",
                        lineNumber: 185,
                        columnNumber: 9
                    }, this),
                    "/",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "Provenance"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/api-reference/page.tsx",
                        lineNumber: 185,
                        columnNumber: 30
                    }, this),
                    "/",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "MetaData"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/api-reference/page.tsx",
                        lineNumber: 185,
                        columnNumber: 54
                    }, this),
                    "/",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "DataVersion"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/api-reference/page.tsx",
                        lineNumber: 185,
                        columnNumber: 76
                    }, this),
                    "/",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "Result"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/api-reference/page.tsx",
                        lineNumber: 186,
                        columnNumber: 9
                    }, this),
                    " model classes are the target architecture and are being built out."
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 183,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["H2"], {
                id: "feature-registry",
                children: "Feature registry (reference)"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 189,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$CodeBlock$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["CodeBlock"], {
                title: "python",
                code: `@feature(name, group, deps, compute)
def fn(...): ...

class LineageGraph:
    register_feature(name, group, deps, compute, fn)
    get_feature(name) -> dict | None
    get_group_features(group) -> list[str]
    resolve_group(group) -> TieredPlan
    save(path) / load(path)

class TieredPlan:
    tiers: list[list[str]]
    all_features: list[str]`
            }, void 0, false, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 190,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Callout"], {
                title: "Alpha status",
                tone: "gold",
                children: [
                    "Hermes is at ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("strong", {
                        children: "v0.2.14"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/api-reference/page.tsx",
                        lineNumber: 208,
                        columnNumber: 22
                    }, this),
                    ". Connectors and features are actively tested (pytest with asyncio auto-mode; ruff + mypy in CI). Several core lifecycle modules remain placeholders while the platform matures."
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 207,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doodle$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Sparkle"], {
                className: "mt-8 h-10 w-10 opacity-50",
                color: "#ff4328",
                strokeWidth: 4
            }, void 0, false, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 212,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["PrevNext"], {
                prev: {
                    title: "Features",
                    href: "/docs/features"
                },
                next: {
                    title: "Roadmap",
                    href: "/docs/roadmap"
                }
            }, void 0, false, {
                fileName: "[project]/src/app/docs/api-reference/page.tsx",
                lineNumber: 214,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/src/app/docs/api-reference/page.tsx",
        lineNumber: 22,
        columnNumber: 5
    }, this);
}
}),
"[project]/src/app/docs/api-reference/page.tsx [app-rsc] (ecmascript, Next.js Server Component)", (function(__turbopack_context__){

__turbopack_context__.n(__turbopack_context__.i("[project]/src/app/docs/api-reference/page.tsx [app-rsc] (ecmascript)"));
}),
"[project]/src/app/favicon.ico (static in ecmascript, tag client)", ((__turbopack_context__) => {

__turbopack_context__.v("/_next/static/media/favicon.2vob68tjqpejf.ico" + (globalThis["NEXT_CLIENT_ASSET_SUFFIX"] || ''));}),
"[project]/src/app/favicon.ico.mjs { IMAGE => \"[project]/src/app/favicon.ico (static in ecmascript, tag client)\" } [app-rsc] (structured image object, ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>__TURBOPACK__default__export__
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$app$2f$favicon$2e$ico__$28$static__in__ecmascript$2c$__tag__client$29$__ = __turbopack_context__.i("[project]/src/app/favicon.ico (static in ecmascript, tag client)");
;
const __TURBOPACK__default__export__ = {
    src: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$app$2f$favicon$2e$ico__$28$static__in__ecmascript$2c$__tag__client$29$__["default"],
    width: 256,
    height: 256
};
}),
"[project]/src/components/CodeBlock.tsx [app-rsc] (client reference proxy)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "CodeBlock",
    ()=>CodeBlock
]);
// This file is generated by next-core EcmascriptClientReferenceModule.
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$server$2d$dom$2d$turbopack$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/rsc/react-server-dom-turbopack-server.js [app-rsc] (ecmascript)");
;
const CodeBlock = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$server$2d$dom$2d$turbopack$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["registerClientReference"])(function() {
    throw new Error("Attempted to call CodeBlock() from the server but CodeBlock is on the client. It's not possible to invoke a client function from the server, it can only be rendered as a Component or passed to props of a Client Component.");
}, "[project]/src/components/CodeBlock.tsx", "CodeBlock");
}),
"[project]/src/components/CodeBlock.tsx [app-rsc] (client reference proxy) <module evaluation>", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "CodeBlock",
    ()=>CodeBlock
]);
// This file is generated by next-core EcmascriptClientReferenceModule.
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$server$2d$dom$2d$turbopack$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/rsc/react-server-dom-turbopack-server.js [app-rsc] (ecmascript)");
;
const CodeBlock = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$server$2d$dom$2d$turbopack$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["registerClientReference"])(function() {
    throw new Error("Attempted to call CodeBlock() from the server but CodeBlock is on the client. It's not possible to invoke a client function from the server, it can only be rendered as a Component or passed to props of a Client Component.");
}, "[project]/src/components/CodeBlock.tsx <module evaluation>", "CodeBlock");
}),
"[project]/src/components/CodeBlock.tsx [app-rsc] (ecmascript)", ((__turbopack_context__) => {
"use strict";

var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$CodeBlock$2e$tsx__$5b$app$2d$rsc$5d$__$28$client__reference__proxy$29$__$3c$module__evaluation$3e$__ = __turbopack_context__.i("[project]/src/components/CodeBlock.tsx [app-rsc] (client reference proxy) <module evaluation>");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$CodeBlock$2e$tsx__$5b$app$2d$rsc$5d$__$28$client__reference__proxy$29$__ = __turbopack_context__.i("[project]/src/components/CodeBlock.tsx [app-rsc] (client reference proxy)");
;
__turbopack_context__.n(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$CodeBlock$2e$tsx__$5b$app$2d$rsc$5d$__$28$client__reference__proxy$29$__);
}),
"[project]/src/components/Doc.tsx [app-rsc] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "Callout",
    ()=>Callout,
    "DocLink",
    ()=>DocLink,
    "DocTitle",
    ()=>DocTitle,
    "H2",
    ()=>H2,
    "Lead",
    ()=>Lead,
    "List",
    ()=>List,
    "P",
    ()=>P,
    "PrevNext",
    ()=>PrevNext,
    "Table",
    ()=>Table
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/rsc/react-jsx-dev-runtime.js [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$react$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/client/app-dir/link.react-server.js [app-rsc] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doodle$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/components/Doodle.tsx [app-rsc] (ecmascript)");
;
;
;
function DocTitle({ children, kicker }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "relative mb-8 rounded-3xl border border-line bg-white p-5 shadow-card sm:mb-10 sm:p-6 md:p-8",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doodle$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["WobbleCircle"], {
                className: "pointer-events-none absolute -right-3 -top-4 h-12 w-12 opacity-40 sm:h-16 sm:w-16",
                color: "#ff4328"
            }, void 0, false, {
                fileName: "[project]/src/components/Doc.tsx",
                lineNumber: 7,
                columnNumber: 7
            }, this),
            kicker && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mb-3 inline-flex items-center gap-2 rounded-full border border-line bg-cream-soft/60 px-3 py-1 font-body text-xs font-bold uppercase tracking-wider text-accent",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doodle$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Sparkle"], {
                        className: "h-3.5 w-3.5",
                        color: "#ff4328",
                        strokeWidth: 4
                    }, void 0, false, {
                        fileName: "[project]/src/components/Doc.tsx",
                        lineNumber: 10,
                        columnNumber: 11
                    }, this),
                    kicker
                ]
            }, void 0, true, {
                fileName: "[project]/src/components/Doc.tsx",
                lineNumber: 9,
                columnNumber: 9
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("h1", {
                className: "font-heading text-3xl font-extrabold tracking-tight text-black sm:text-4xl md:text-5xl",
                children: children
            }, void 0, false, {
                fileName: "[project]/src/components/Doc.tsx",
                lineNumber: 14,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doodle$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Squiggle"], {
                className: "pointer-events-none absolute -bottom-2 left-8 w-20 opacity-70 sm:w-24",
                color: "#ff4328",
                strokeWidth: 4
            }, void 0, false, {
                fileName: "[project]/src/components/Doc.tsx",
                lineNumber: 17,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/src/components/Doc.tsx",
        lineNumber: 6,
        columnNumber: 5
    }, this);
}
function H2({ children, id }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "mt-10 mb-4 flex items-center gap-2 sm:mt-14",
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
            id: id,
            className: "flex items-center gap-2 font-heading text-xl font-extrabold tracking-tight text-black sm:gap-3 sm:text-2xl",
            children: [
                children,
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doodle$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Sparkle"], {
                    className: "hidden h-5 w-5 opacity-70 sm:inline",
                    color: "#ff4328",
                    strokeWidth: 4
                }, void 0, false, {
                    fileName: "[project]/src/components/Doc.tsx",
                    lineNumber: 30,
                    columnNumber: 9
                }, this)
            ]
        }, void 0, true, {
            fileName: "[project]/src/components/Doc.tsx",
            lineNumber: 25,
            columnNumber: 7
        }, this)
    }, void 0, false, {
        fileName: "[project]/src/components/Doc.tsx",
        lineNumber: 24,
        columnNumber: 5
    }, this);
}
function P({ children }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
        className: "my-4 font-body text-[16.5px] leading-relaxed text-black",
        children: children
    }, void 0, false, {
        fileName: "[project]/src/components/Doc.tsx",
        lineNumber: 37,
        columnNumber: 10
    }, this);
}
function Lead({ children }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
        className: "mb-6 text-base font-body leading-relaxed text-black sm:text-lg",
        children: children
    }, void 0, false, {
        fileName: "[project]/src/components/Doc.tsx",
        lineNumber: 42,
        columnNumber: 5
    }, this);
}
function List({ items }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("ul", {
        className: "dot-bullet my-4 space-y-2.5",
        children: items.map((item)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("li", {
                className: "font-body text-[16.5px] text-black",
                children: item
            }, item, false, {
                fileName: "[project]/src/components/Doc.tsx",
                lineNumber: 50,
                columnNumber: 9
            }, this))
    }, void 0, false, {
        fileName: "[project]/src/components/Doc.tsx",
        lineNumber: 48,
        columnNumber: 5
    }, this);
}
function Callout({ title, children, tone = "accent" }) {
    const map = {
        accent: {
            bg: "#ff4328",
            label: "Note"
        },
        cedar: {
            bg: "#1f5f4b",
            label: "Tip"
        },
        gold: {
            bg: "#b88a1f",
            label: "Warning"
        }
    };
    const t = map[tone];
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "my-6 overflow-hidden rounded-2xl border border-line bg-white shadow-card sm:my-7",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex items-center gap-2 px-3 py-2.5 sm:px-4",
                style: {
                    backgroundColor: `${t.bg}`
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doodle$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Sparkle"], {
                        className: "h-4 w-4 text-white",
                        color: "#fff",
                        strokeWidth: 4
                    }, void 0, false, {
                        fileName: "[project]/src/components/Doc.tsx",
                        lineNumber: 76,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: "font-heading text-sm font-bold text-white",
                        children: title
                    }, void 0, false, {
                        fileName: "[project]/src/components/Doc.tsx",
                        lineNumber: 77,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/src/components/Doc.tsx",
                lineNumber: 75,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "px-4 py-3 font-body text-[15px] leading-relaxed text-black sm:px-5 sm:py-4",
                children: children
            }, void 0, false, {
                fileName: "[project]/src/components/Doc.tsx",
                lineNumber: 79,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/src/components/Doc.tsx",
        lineNumber: 74,
        columnNumber: 5
    }, this);
}
function DocLink({ href, children, external }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$react$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["default"], {
        href: href,
        target: external ? "_blank" : undefined,
        rel: external ? "noopener noreferrer" : undefined,
        className: "font-medium text-accent underline decoration-accent/40 underline-offset-4 transition-colors hover:text-accent-dark hover:decoration-accent",
        children: children
    }, void 0, false, {
        fileName: "[project]/src/components/Doc.tsx",
        lineNumber: 86,
        columnNumber: 5
    }, this);
}
function PrevNext({ prev, next }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "mt-10 grid gap-3 border-t border-line/70 pt-6 sm:mt-14 sm:grid-cols-2 sm:gap-4 sm:pt-8",
        children: [
            prev ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$react$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["default"], {
                href: prev.href,
                className: "group relative rounded-2xl border border-line bg-white p-4 transition-all hover:-translate-y-0.5 hover:shadow-card sm:p-5",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "font-body text-xs uppercase tracking-wider text-black/50",
                        children: "← Previous"
                    }, void 0, false, {
                        fileName: "[project]/src/components/Doc.tsx",
                        lineNumber: 105,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "mt-1 font-heading font-bold text-black group-hover:text-accent",
                        children: prev.title
                    }, void 0, false, {
                        fileName: "[project]/src/components/Doc.tsx",
                        lineNumber: 106,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doodle$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Arrow"], {
                        className: "pointer-events-none absolute -right-2 -bottom-2 h-8 w-12 opacity-0 transition-opacity group-hover:opacity-60",
                        color: "#ff4328",
                        strokeWidth: 3
                    }, void 0, false, {
                        fileName: "[project]/src/components/Doc.tsx",
                        lineNumber: 107,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/src/components/Doc.tsx",
                lineNumber: 101,
                columnNumber: 9
            }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {}, void 0, false, {
                fileName: "[project]/src/components/Doc.tsx",
                lineNumber: 110,
                columnNumber: 9
            }, this),
            next ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$react$2d$server$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["default"], {
                href: next.href,
                className: "group relative rounded-2xl border border-line bg-white p-4 text-right transition-all hover:-translate-y-0.5 hover:shadow-card sm:p-5",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "font-body text-xs uppercase tracking-wider text-black/50",
                        children: "Next →"
                    }, void 0, false, {
                        fileName: "[project]/src/components/Doc.tsx",
                        lineNumber: 117,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "mt-1 font-heading font-bold text-black group-hover:text-accent",
                        children: next.title
                    }, void 0, false, {
                        fileName: "[project]/src/components/Doc.tsx",
                        lineNumber: 118,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doodle$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Arrow"], {
                        className: "pointer-events-none absolute -left-2 -bottom-2 h-8 w-12 rotate-180 opacity-0 transition-opacity group-hover:opacity-60",
                        color: "#ff4328",
                        strokeWidth: 3
                    }, void 0, false, {
                        fileName: "[project]/src/components/Doc.tsx",
                        lineNumber: 119,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/src/components/Doc.tsx",
                lineNumber: 113,
                columnNumber: 9
            }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {}, void 0, false, {
                fileName: "[project]/src/components/Doc.tsx",
                lineNumber: 122,
                columnNumber: 9
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/src/components/Doc.tsx",
        lineNumber: 99,
        columnNumber: 5
    }, this);
}
function Table({ head, rows }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "my-5 overflow-x-auto rounded-2xl border border-line bg-white shadow-card sm:my-6",
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("table", {
            className: "w-full min-w-[400px] text-left font-body text-[13.5px] sm:text-[15px]",
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("thead", {
                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("tr", {
                        className: "border-b border-line bg-cream-soft/70",
                        children: head.map((h)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("th", {
                                className: "px-3 py-2.5 font-heading text-xs font-bold text-black sm:px-4 sm:py-3 sm:text-sm",
                                children: h
                            }, h, false, {
                                fileName: "[project]/src/components/Doc.tsx",
                                lineNumber: 135,
                                columnNumber: 15
                            }, this))
                    }, void 0, false, {
                        fileName: "[project]/src/components/Doc.tsx",
                        lineNumber: 133,
                        columnNumber: 11
                    }, this)
                }, void 0, false, {
                    fileName: "[project]/src/components/Doc.tsx",
                    lineNumber: 132,
                    columnNumber: 9
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("tbody", {
                    children: rows.map((row, i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("tr", {
                            className: "border-b border-line/50 last:border-0",
                            children: row.map((cell, j)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("td", {
                                    className: "px-3 py-2.5 align-top text-black sm:px-4 sm:py-3",
                                    children: cell
                                }, j, false, {
                                    fileName: "[project]/src/components/Doc.tsx",
                                    lineNumber: 145,
                                    columnNumber: 17
                                }, this))
                        }, i, false, {
                            fileName: "[project]/src/components/Doc.tsx",
                            lineNumber: 143,
                            columnNumber: 13
                        }, this))
                }, void 0, false, {
                    fileName: "[project]/src/components/Doc.tsx",
                    lineNumber: 141,
                    columnNumber: 9
                }, this)
            ]
        }, void 0, true, {
            fileName: "[project]/src/components/Doc.tsx",
            lineNumber: 131,
            columnNumber: 7
        }, this)
    }, void 0, false, {
        fileName: "[project]/src/components/Doc.tsx",
        lineNumber: 130,
        columnNumber: 5
    }, this);
}
}),
];

//# sourceMappingURL=%5Broot-of-the-server%5D__00y8224._.js.map