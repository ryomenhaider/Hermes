module.exports = [
"[externals]/next/dist/shared/lib/no-fallback-error.external.js [external] (next/dist/shared/lib/no-fallback-error.external.js, cjs)", ((__turbopack_context__, module, exports) => {

var mod = __turbopack_context__.x("next/dist/shared/lib/no-fallback-error.external.js", () => require("next/dist/shared/lib/no-fallback-error.external.js"));

module.exports = mod;
}),
"[project]/src/app/docs/connectors/page.tsx [app-rsc] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>ConnectorsPage,
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
    title: "Connectors",
    description: "Every Hermes connector: class, fetch() signature, source, endpoints and cache TTL. World Bank, IMF, FRED, Binance, Finnhub, yfinance, SEC, OpenSanctions, GDELT, public datasets."
};
function ConnectorsPage() {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("article", {
        className: "relative",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["DocTitle"], {
                kicker: "Core Concepts",
                children: "Connectors"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 23,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Lead"], {
                children: [
                    "Ten source connectors ship with Hermes, each exposing an async ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "fetch()"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 25,
                        columnNumber: 72
                    }, this),
                    " that returns canonical records and sits behind the shared ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "RawCache"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 26,
                        columnNumber: 62
                    }, this),
                    "."
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 24,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["H2"], {
                id: "at-a-glance",
                children: "All connectors at a glance"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 29,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Table"], {
                head: [
                    "Source",
                    "Class",
                    "Cache TTL",
                    "Status"
                ],
                rows: [
                    [
                        "World Bank",
                        "hermes.connectors.World_bank",
                        "7 days",
                        "Working"
                    ],
                    [
                        "IMF (SDMX)",
                        "hermes.connectors.IMF",
                        "7 days",
                        "Working"
                    ],
                    [
                        "FRED",
                        "hermes.connectors.FRED",
                        "30 days",
                        "Working"
                    ],
                    [
                        "Binance",
                        "hermes.connectors.Binance",
                        "1 day",
                        "Working"
                    ],
                    [
                        "Finnhub",
                        "hermes.connectors.FINNHUB",
                        "7 days",
                        "Working"
                    ],
                    [
                        "Yfinance",
                        "hermes.connectors.Yfinance",
                        "1 day",
                        "Working"
                    ],
                    [
                        "SEC EDGAR",
                        "hermes.connectors.SECEDGAR",
                        "7 days",
                        "Working"
                    ],
                    [
                        "OpenSanctions",
                        "hermes.connectors.OpenSanction",
                        "30 days",
                        "Working"
                    ],
                    [
                        "Bundled datasets",
                        "hermes.connectors.PUBLIC_DATASET",
                        "—",
                        "Working"
                    ],
                    [
                        "GDELT",
                        "hermes.connectors.GDELT",
                        "—",
                        "Stub"
                    ]
                ]
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 30,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["P"], {
                children: "Source coverage spans global macro, financial markets, corporate filings, sanctions and governance intelligence. TTLs are deliberately conservative for stable public sources and tighter for fast-moving market data."
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 45,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["H2"], {
                id: "contract",
                children: "The connector contract"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 51,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["P"], {
                children: [
                    "A connector answers one question: ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("em", {
                        children: "how do I get this source's data?"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 53,
                        columnNumber: 43
                    }, this),
                    " In Hermes, each connector package pairs its ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "fetch()"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 54,
                        columnNumber: 50
                    }, this),
                    " with a parser, a normalizer and field mappings. Connectors can provide authentication, requests, pagination, rate limiting, retries and source-specific parsing — but generic retry, caching and validation belong to Hermes infrastructure, not to the connector."
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 52,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["P"], {
                children: [
                    "Connectors use ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "aiohttp"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 60,
                        columnNumber: 24
                    }, this),
                    " with exponential-backoff retries (sleeps",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "2**attempt"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 61,
                        columnNumber: 9
                    }, this),
                    " seconds) and resolve keys through ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "RawCache.get_or_fetch"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 61,
                        columnNumber: 67
                    }, this),
                    "."
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 59,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["H2"], {
                id: "world-bank",
                children: "World Bank"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 64,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Table"], {
                head: [
                    "Item",
                    "Detail"
                ],
                rows: [
                    [
                        "Class",
                        "hermes.connectors.World_bank"
                    ],
                    [
                        "Base URL",
                        "https://api.worldbank.org/v2"
                    ],
                    [
                        "Cache source",
                        "world_bank · TTL 7 days"
                    ],
                    [
                        "fetch()",
                        "fetch(country_code, indicator_code, frequency=None, most_recent=None, per_page=1000, page=1, force=False)"
                    ],
                    [
                        "Return",
                        "DataFrame with date, indicator_id, indicator_name, country, value, source"
                    ]
                ]
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 65,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$CodeBlock$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["CodeBlock"], {
                title: "python",
                code: `from hermes import Hermes
hermes = Hermes(opensanction_api="x", new_data_api="x",
                sec_username="x", sec_email="x")

df = hermes.world_bank.fetch(
    country_code="BR",
    indicator_code="SP.POP.TOTL",   # total population
    frequency="Y",
)`
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 78,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["H2"], {
                id: "imf",
                children: "IMF (SDMX)"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 91,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Table"], {
                head: [
                    "Item",
                    "Detail"
                ],
                rows: [
                    [
                        "Class",
                        "hermes.connectors.IMF"
                    ],
                    [
                        "Base URL",
                        "https://api.imf.org/external/sdmx/3.0/data/dataflow/"
                    ],
                    [
                        "Cache source",
                        "imf · TTL 7 days"
                    ],
                    [
                        "fetch()",
                        "fetch(country, agency, dataflow_id, key, version='~', force=False)"
                    ],
                    [
                        "Return",
                        "Normalized SDMX DataFrame; empty DataFrame on 404"
                    ]
                ]
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 92,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$CodeBlock$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["CodeBlock"], {
                title: "python",
                code: `# IMF WEO government debt (% of GDP)
df = hermes.imf.fetch(
    country="US",
    agency="IMF.RES",
    dataflow_id="WEO",
    key="GGXWDG_NGDP",
)`
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 105,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["H2"], {
                id: "fred",
                children: "FRED"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 116,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Table"], {
                head: [
                    "Item",
                    "Detail"
                ],
                rows: [
                    [
                        "Class",
                        "hermes.connectors.FRED"
                    ],
                    [
                        "Base URL",
                        "https://api.stlouisfed.org/fred/series/observations"
                    ],
                    [
                        "Cache source",
                        "fred · TTL 30 days"
                    ],
                    [
                        "fetch()",
                        "fetch(series_id, timeout=30.0, retries=3, force=False)"
                    ]
                ]
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 117,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["P"], {
                children: [
                    "23 curated macro series are defined in ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "fred/mappings.py"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 127,
                        columnNumber: 48
                    }, this),
                    ", including",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "GDPC1"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 128,
                        columnNumber: 9
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "A191RL1Q225SBEA"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 128,
                        columnNumber: 29
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "INDPRO"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 128,
                        columnNumber: 59
                    }, this),
                    ",",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "CPIAUCSL"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 129,
                        columnNumber: 9
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "CPILFESL"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 129,
                        columnNumber: 32
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "PCEPI"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 129,
                        columnNumber: 55
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "UNRATE"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 129,
                        columnNumber: 75
                    }, this),
                    ",",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "PAYEMS"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 130,
                        columnNumber: 9
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "CIVPART"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 130,
                        columnNumber: 30
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "FEDFUNDS"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 130,
                        columnNumber: 52
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "DGS10"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 130,
                        columnNumber: 75
                    }, this),
                    ",",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "DGS2"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 131,
                        columnNumber: 9
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "DGS3MO"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 131,
                        columnNumber: 28
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "T10Y2Y"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 131,
                        columnNumber: 49
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "T10Y3M"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 131,
                        columnNumber: 70
                    }, this),
                    ",",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "M2SL"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 132,
                        columnNumber: 9
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "TOTBKCR"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 132,
                        columnNumber: 28
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "HOUST"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 132,
                        columnNumber: 50
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "EXHOSLUSM495S"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 132,
                        columnNumber: 70
                    }, this),
                    ",",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "SP500"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 133,
                        columnNumber: 9
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "VIXCLS"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 133,
                        columnNumber: 29
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "DTWEXBGS"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 133,
                        columnNumber: 50
                    }, this),
                    "."
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 126,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$CodeBlock$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["CodeBlock"], {
                title: "python",
                code: `fd = hermes.fred.fetch(series_id="CPIAUCSL")  # CPI`
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 135,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["H2"], {
                id: "binance",
                children: "Binance"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 140,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Table"], {
                head: [
                    "Item",
                    "Detail"
                ],
                rows: [
                    [
                        "Class",
                        "hermes.connectors.Binance"
                    ],
                    [
                        "Base URL",
                        "api.binance.com (spot) / fapi.binance.com (future)"
                    ],
                    [
                        "Cache source",
                        "binance · TTL 1 day"
                    ],
                    [
                        "fetch()",
                        "fetch(mode, endpoint, symbol, interval=None, limit=None, period=None, retries=3, timeout=30.0, force=False)"
                    ],
                    [
                        "fetch_history()",
                        "fetch_history(symbol, interval='1d', market='future', years=2, max_concurrent=10)"
                    ]
                ]
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 141,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["P"], {
                children: [
                    "Endpoints (per ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "binance/mappings.py"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 158,
                        columnNumber: 24
                    }, this),
                    "): ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "ohlcv"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 158,
                        columnNumber: 59
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "trades"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 158,
                        columnNumber: 79
                    }, this),
                    ",",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "aggregated_trades"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 159,
                        columnNumber: 9
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "order_book"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 159,
                        columnNumber: 41
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "best_bid_ask"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 159,
                        columnNumber: 66
                    }, this),
                    ",",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "24hr"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 160,
                        columnNumber: 9
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "exchangeInfo"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 160,
                        columnNumber: 28
                    }, this),
                    "; plus future-only ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "fundingRate"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 160,
                        columnNumber: 72
                    }, this),
                    ",",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "openInterest"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 161,
                        columnNumber: 9
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "premiumIndex"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 161,
                        columnNumber: 36
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "openInterestHist"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 161,
                        columnNumber: 63
                    }, this),
                    ",",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "longShortRatio"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 162,
                        columnNumber: 9
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "topLongShortAccountRatio"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 162,
                        columnNumber: 38
                    }, this),
                    ",",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "topLongShortPositionRatio"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 163,
                        columnNumber: 9
                    }, this),
                    ". ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "fetch_history"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 163,
                        columnNumber: 49
                    }, this),
                    " splits the range into 1000-bar windows fetched concurrently (semaphore = 10)."
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 157,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$CodeBlock$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["CodeBlock"], {
                title: "python",
                code: `# 2 years of daily BTCUSDT futures candles
df = hermes.binance.fetch_history(
    symbol="BTCUSDT", interval="1d",
    market="future", years=2,
)`
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 166,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["H2"], {
                id: "finnhub",
                children: "Finnhub"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 175,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Table"], {
                head: [
                    "Item",
                    "Detail"
                ],
                rows: [
                    [
                        "Class",
                        "hermes.connectors.FINNHUB"
                    ],
                    [
                        "Base URL",
                        "https://finnhub.io/api/v1"
                    ],
                    [
                        "Cache source",
                        "finnhub · TTL 7 days"
                    ],
                    [
                        "fetch()",
                        "fetch(endpoint, symbol, resolution=None, _from=None, _to=None, force=False)"
                    ],
                    [
                        "fetch_candles_history()",
                        "fetch_candles_history(symbol, resolution='D', years=2)"
                    ]
                ]
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 176,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["P"], {
                children: [
                    "Endpoints: ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "candles"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 193,
                        columnNumber: 20
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "quote"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 193,
                        columnNumber: 42
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "profile"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 193,
                        columnNumber: 62
                    }, this),
                    ",",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "metric"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 194,
                        columnNumber: 9
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "peers"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 194,
                        columnNumber: 30
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "earnings"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 194,
                        columnNumber: 50
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "insider"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 194,
                        columnNumber: 73
                    }, this),
                    ",",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "eps"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 195,
                        columnNumber: 9
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "ebitda"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 195,
                        columnNumber: 27
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "revenue"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 195,
                        columnNumber: 48
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "news"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 195,
                        columnNumber: 70
                    }, this),
                    ",",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "symbol"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 196,
                        columnNumber: 9
                    }, this),
                    ". Lookback is capped by ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "FINNHUB_MAX_DAYS"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 196,
                        columnNumber: 52
                    }, this),
                    " per resolution (e.g. 1m/5m → 7d, 15m–1h → 30d, D/W/M → 365d)."
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 192,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["H2"], {
                id: "yfinance",
                children: "Yfinance"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 200,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Table"], {
                head: [
                    "Item",
                    "Detail"
                ],
                rows: [
                    [
                        "Class",
                        "hermes.connectors.Yfinance"
                    ],
                    [
                        "Cache source",
                        "yfinance · TTL 1 day"
                    ],
                    [
                        "fetch()",
                        "fetch(endpoint, symbol, force=False) — endpoints: quote, eps_estimate, revenue_estimate, earnings_history"
                    ],
                    [
                        "fetch_history()",
                        "fetch_history(symbol, interval='1d', years=2)"
                    ]
                ]
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 201,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["P"], {
                children: [
                    "Raised restricted intervals (raises ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "ValueError"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 217,
                        columnNumber: 45
                    }, this),
                    " for unsupported ones). The interval map: ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "1m/5m/15m/30m/1h/1d"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 218,
                        columnNumber: 23
                    }, this),
                    " map to themselves, ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "1w → 1wk"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 218,
                        columnNumber: 75
                    }, this),
                    ",",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "1M → 1mo"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 219,
                        columnNumber: 9
                    }, this),
                    "."
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 216,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["H2"], {
                id: "sec",
                children: "SEC EDGAR"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 222,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Table"], {
                head: [
                    "Item",
                    "Detail"
                ],
                rows: [
                    [
                        "Class",
                        "hermes.connectors.SECEDGAR"
                    ],
                    [
                        "Base URL",
                        "https://data.sec.gov/api/xbrl/companyfacts"
                    ],
                    [
                        "Cache source",
                        "sec_edgar · TTL 7 days"
                    ],
                    [
                        "fetch()",
                        "fetch(symbol, timeout=30.0, retries=3, force=False)"
                    ]
                ]
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 223,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["P"], {
                children: [
                    "Resolves a ticker to its CIK via ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "sec-cik-mapper"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 233,
                        columnNumber: 42
                    }, this),
                    " and requests",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "<user-agent> <email>"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 234,
                        columnNumber: 9
                    }, this),
                    " as required by the SEC. The",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "SEC_TAG_MAP"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 235,
                        columnNumber: 9
                    }, this),
                    " (",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "sec/tags.py"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 235,
                        columnNumber: 35
                    }, this),
                    ") maps canonical fields to XBRL GAAP tags — e.g. ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "revenue"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 236,
                        columnNumber: 16
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "net_income"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 236,
                        columnNumber: 38
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "operating_cash_flow"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 236,
                        columnNumber: 63
                    }, this),
                    ",",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "long_term_debt"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 237,
                        columnNumber: 9
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "shares_outstanding"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 237,
                        columnNumber: 38
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "dividends"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 237,
                        columnNumber: 71
                    }, this),
                    ",",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "buybacks"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 238,
                        columnNumber: 9
                    }, this),
                    ", etc."
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 232,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["H2"], {
                id: "opensanctions",
                children: "OpenSanctions"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 241,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Table"], {
                head: [
                    "Item",
                    "Detail"
                ],
                rows: [
                    [
                        "Class",
                        "hermes.connectors.OpenSanction"
                    ],
                    [
                        "Base URL",
                        "https://api.opensanctions.org"
                    ],
                    [
                        "Auth",
                        "Authorization: ApiKey &lt;key&gt;"
                    ],
                    [
                        "Cache source",
                        "OpenSanction · TTL 30 days"
                    ],
                    [
                        "fetch()",
                        "fetch(country, dataset, limit=50, changed_since=None, topic=None, facets=None, force=False)"
                    ]
                ]
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 242,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["P"], {
                children: [
                    "Supports datasets such as ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "us_ofac_sdn"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 256,
                        columnNumber: 35
                    }, this),
                    ", ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "eu_fsf"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 256,
                        columnNumber: 61
                    }, this),
                    ",",
                    " ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "uk_fcdos"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 257,
                        columnNumber: 9
                    }, this),
                    " and ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "un_sc"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 257,
                        columnNumber: 35
                    }, this),
                    ". Country ISO3 is converted to ISO2 internally before filtering."
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 255,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["H2"], {
                id: "gdelt",
                children: "GDELT"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 261,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Table"], {
                head: [
                    "Item",
                    "Detail"
                ],
                rows: [
                    [
                        "Class",
                        "hermes.connectors.GDELT"
                    ],
                    [
                        "Status",
                        "Stub (empty class)"
                    ]
                ]
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 262,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["P"], {
                children: "The GDELT connector is scaffolded but not yet implemented — global news/event data powers the geopolitical features, which are similarly stubbed."
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 269,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["H2"], {
                id: "public",
                children: "Bundled public datasets"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 274,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Table"], {
                head: [
                    "Item",
                    "Detail"
                ],
                rows: [
                    [
                        "Class",
                        "hermes.connectors.PUBLIC_DATASET"
                    ],
                    [
                        "Location",
                        "hermes/connectors/lib/datasets/"
                    ]
                ]
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 275,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["P"], {
                children: [
                    "Reads bundled local CSVs, country-filtered with years converted to ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "datetime"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 282,
                        columnNumber: 77
                    }, this),
                    ":"
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 282,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(ListRows, {}, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 283,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["H2"], {
                id: "retries",
                children: "Retries & timeouts"
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 285,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Callout"], {
                title: "Every connector",
                tone: "cedar",
                children: [
                    "All HTTP connectors default to ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "retries=3"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 287,
                        columnNumber: 40
                    }, this),
                    " and ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "timeout=30.0"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 287,
                        columnNumber: 67
                    }, this),
                    ", retrying with exponential backoff. Pass ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "force=True"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 288,
                        columnNumber: 49
                    }, this),
                    " to bypass the cache."
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 286,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["P"], {
                children: [
                    "Backoff sleeps ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        children: "2**attempt"
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 291,
                        columnNumber: 24
                    }, this),
                    " seconds so transient failures settle quickly without hammering the source. Because retry, caching and validation are handled by Hermes infrastructure rather than each connector, adding a new source never means re-implementing that plumbing."
                ]
            }, void 0, true, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 290,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doodle$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["Sparkle"], {
                className: "mt-8 h-10 w-10 opacity-50",
                color: "#ff4328",
                strokeWidth: 4
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 296,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$components$2f$Doc$2e$tsx__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["PrevNext"], {
                prev: {
                    title: "Quickstart",
                    href: "/docs/quickstart"
                },
                next: {
                    title: "Features",
                    href: "/docs/features"
                }
            }, void 0, false, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 298,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/src/app/docs/connectors/page.tsx",
        lineNumber: 22,
        columnNumber: 5
    }, this);
}
function ListRows() {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "my-4 grid gap-2 sm:grid-cols-2",
        children: [
            [
                "fetch_hrs(country)",
                "human_right_score"
            ],
            [
                "fetch_hdi(country)",
                "human development index (iso3, year, score)"
            ],
            [
                "fetch_cpi(country)",
                "global CPI"
            ],
            [
                "fetch_fsi(country)",
                "fragile states index (Total 0–120)"
            ],
            [
                "fetch_nato(country)",
                "NATO membership"
            ],
            [
                "fetch_crs(country)",
                "climate readiness score"
            ],
            [
                "fetch_cvs(country)",
                "climate vulnerability score"
            ],
            [
                "fetch_sipri(country)",
                "SIPRI military expenditure"
            ]
        ].map(([fn, desc])=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "rounded-xl border border-line bg-white px-3 py-2",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("code", {
                        className: "font-mono text-[12.5px] font-semibold text-ink",
                        children: fn
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 320,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$rsc$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$rsc$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "mt-0.5 font-body text-[13px] text-ink",
                        children: desc
                    }, void 0, false, {
                        fileName: "[project]/src/app/docs/connectors/page.tsx",
                        lineNumber: 321,
                        columnNumber: 11
                    }, this)
                ]
            }, fn, true, {
                fileName: "[project]/src/app/docs/connectors/page.tsx",
                lineNumber: 319,
                columnNumber: 9
            }, this))
    }, void 0, false, {
        fileName: "[project]/src/app/docs/connectors/page.tsx",
        lineNumber: 308,
        columnNumber: 5
    }, this);
}
}),
"[project]/src/app/docs/connectors/page.tsx [app-rsc] (ecmascript, Next.js Server Component)", (function(__turbopack_context__){

__turbopack_context__.n(__turbopack_context__.i("[project]/src/app/docs/connectors/page.tsx [app-rsc] (ecmascript)"));
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

//# sourceMappingURL=%5Broot-of-the-server%5D__13-eeqo._.js.map