"use client";

import { motion } from "framer-motion";
import {
  Database,
  Share2,
  FileText,
  Settings,
  CheckCircle,
  Zap,
  ArrowRight,
} from "lucide-react";
import { EntityGraph } from "@/components/EntityGraph";

const PIPELINE = [
  { label: "Source", icon: Database },
  { label: "Acquire", icon: Share2 },
  { label: "Parse", icon: FileText },
  { label: "Normalize", icon: Settings },
  { label: "Validate", icon: CheckCircle },
  { label: "Store", icon: Database },
  { label: "Serve", icon: Zap },
];

const DATA_ROWS = [
  ["USA", "GDP", "27438.6", "2024-01-01"],
  ["DEU", "CPI", "112.4", "2024-01-01"],
  ["JPN", "GDP", "4226.8", "2024-01-01"],
  ["GBR", "GDP", "3340.0", "2024-01-01"],
];

const sectionFade = {
  initial: { opacity: 0, y: 24 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true, margin: "-80px" },
  transition: { duration: 0.6, ease: "easeOut" as const },
};

export function HowItWorks() {
  return (
    <section className="relative border-t border-white/[0.06] bg-[#0e1114]">
      <div className="mx-auto max-w-6xl px-5 py-24 sm:px-8">
        <motion.div {...sectionFade} className="mb-14 text-center">
          <p className="mb-3 font-mono text-xs font-medium uppercase tracking-[0.3em] text-teal">
            Pipeline
          </p>
          <h2 className="font-sans text-3xl font-bold tracking-tight text-offwhite sm:text-4xl">
            How Hermes works
          </h2>
        </motion.div>

        {/* Connected icon tiles */}
        <motion.div
          {...sectionFade}
          className="flex flex-col items-center justify-center gap-3 md:flex-row md:gap-2"
        >
          {PIPELINE.map((step, i) => (
            <motion.div
              key={step.label}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-60px" }}
              transition={{ duration: 0.4, delay: i * 0.06 }}
              className="flex w-full flex-col items-center gap-3 md:w-auto md:flex-row md:gap-2"
            >
              <div className="flex flex-col items-center gap-3 rounded-md border border-white/[0.07] bg-midnight px-6 py-5 transition-colors duration-200 hover:border-teal/50">
                <step.icon className="h-6 w-6 text-teal" aria-hidden="true" />
                <span className="font-mono text-[11px] uppercase tracking-[0.2em] text-gray-bright">
                  {step.label}
                </span>
              </div>
              {i < PIPELINE.length - 1 && (
                <ArrowRight
                  className="hidden h-4 w-4 rotate-90 text-teal/60 md:block md:rotate-0"
                  aria-hidden="true"
                />
              )}
            </motion.div>
          ))}
        </motion.div>

        {/* Three supporting cards */}
        <div className="mt-16 grid grid-cols-1 gap-6 lg:grid-cols-3">
          {/* Sample data table */}
          <motion.div
            {...sectionFade}
            className="rounded-md border border-white/[0.07] bg-midnight p-5"
          >
            <p className="mb-4 font-mono text-xs uppercase tracking-[0.2em] text-gray">
              Sample data
            </p>
            <table className="w-full border-collapse font-mono text-xs">
              <thead>
                <tr className="text-left text-gray">
                  <th className="pb-2 font-normal">country_code</th>
                  <th className="pb-2 font-normal">indicator</th>
                  <th className="pb-2 text-right font-normal">value</th>
                  <th className="pb-2 text-right font-normal">date</th>
                </tr>
              </thead>
              <tbody>
                {DATA_ROWS.map((row) => (
                  <tr
                    key={row.join("-")}
                    className="border-t border-white/[0.05] text-gray-bright"
                  >
                    <td className="py-1.5 text-offwhite">{row[0]}</td>
                    <td className="py-1.5">{row[1]}</td>
                    <td className="py-1.5 text-right">{row[2]}</td>
                    <td className="py-1.5 text-right">{row[3]}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </motion.div>

          {/* Entity graph */}
          <motion.div
            {...sectionFade}
            className="rounded-md border border-white/[0.07] bg-midnight p-5"
          >
            <p className="mb-4 font-mono text-xs uppercase tracking-[0.2em] text-gray">
              Entity graph
            </p>
            <div className="h-40 sm:h-48">
              <EntityGraph />
            </div>
          </motion.div>

          {/* Code snippet */}
          <motion.div
            {...sectionFade}
            className="overflow-hidden rounded-md border border-white/[0.07] bg-midnight"
          >
            <div
              className="flex items-center gap-2 border-b border-white/[0.07] px-4 py-2.5"
              aria-hidden="true"
            >
              <span className="h-2.5 w-2.5 rounded-full bg-teal/60" />
              <span className="h-2.5 w-2.5 rounded-full bg-white/15" />
              <span className="h-2.5 w-2.5 rounded-full bg-white/15" />
            </div>
            <pre className="overflow-x-auto p-5 font-mono text-[13px] leading-relaxed text-gray-bright">
              <code>
                <span className="text-[#4aa89e]">import</span>{" "}
                <span className="text-offwhite">hermes</span>{" "}
                <span className="text-[#4aa89e]">as</span>{" "}
                <span className="text-offwhite">hr</span>
                {"\n"}
                <span className="text-[#4aa89e]">import</span>{" "}
                <span className="text-offwhite">polars</span>{" "}
                <span className="text-[#4aa89e]">as</span>{" "}
                <span className="text-offwhite">pl</span>
                {"\n\n"}
                <span className="text-offwhite">df</span>{" "}
                <span className="text-teal">=</span>{" "}
                <span className="text-offwhite">pl</span>
                <span className="text-gray">.</span>
                <span className="text-teal">read_csv</span>
                <span className="text-gray">(</span>
                <span className="text-[#b3a1e6]">&quot;gdp.csv&quot;</span>
                <span className="text-gray">)</span>
                {"\n\n"}
                <span className="text-orange">report</span>{" "}
                <span className="text-teal">=</span>{" "}
                <span className="text-offwhite">hr</span>
                <span className="text-gray">.</span>
                <span className="text-teal">profile</span>
                <span className="text-gray">(</span>
                <span className="text-offwhite">df</span>
                <span className="text-gray">)</span>
                {"\n"}
                <span className="text-offwhite">ds</span>{" "}
                <span className="text-teal">=</span>{" "}
                <span className="text-offwhite">hr</span>
                <span className="text-gray">.</span>
                <span className="text-teal">Dataset</span>
                <span className="text-gray">(</span>
                <span className="text-[#b3a1e6]">name=&quot;gdp&quot;</span>
                <span className="text-gray">,</span>{" "}
                <span className="text-[#b3a1e6]">data_ref=&quot;gdp.csv&quot;</span>
                <span className="text-gray">,</span>{" "}
                <span className="text-[#b3a1e6]">data=df</span>
                <span className="text-gray">)</span>
                {"\n"}
                <span className="text-offwhite">ds</span>
                <span className="text-gray">.</span>
                <span className="text-teal">save</span>
                <span className="text-gray">(</span>
                <span className="text-[#b3a1e6]">&quot;output&quot;</span>
                <span className="text-gray">,</span>{" "}
                <span className="text-[#b3a1e6]">format=&quot;parquet&quot;</span>
                <span className="text-gray">)</span>
              </code>
            </pre>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
