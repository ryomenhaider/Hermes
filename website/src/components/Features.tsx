"use client";

import { motion } from "framer-motion";
import { Database, FileStack, Network, ServerCog } from "lucide-react";

const FEATURES = [
  {
    icon: Database,
    title: "Multi-source acquisition",
    description:
      "Fetch from 10 built-in connectors — financial APIs, government portals and files — sharing one caching and retry layer.",
  },
  {
    icon: FileStack,
    title: "Schema normalization",
    description:
      "Inconsistent source formats are normalized to versioned canonical schemas so every dataset speaks the same language.",
  },
  {
    icon: Network,
    title: "Entity resolution",
    description:
      "Resolve companies, countries and assets across identifiers — from tickers and CIKs to ISO codes and names.",
  },
  {
    icon: ServerCog,
    title: "Scalable storage",
    description:
      "Parquet-backed caching, Dataset save/export, and clean Polars, Arrow and Pandas interchange.",
  },
];

const sectionFade = {
  initial: { opacity: 0, y: 24 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true, margin: "-80px" },
  transition: { duration: 0.6, ease: "easeOut" as const },
};

export function Features() {
  return (
    <section className="border-t border-white/[0.06] bg-midnight">
      <div className="mx-auto max-w-6xl px-5 py-24 sm:px-8">
        <motion.div {...sectionFade} className="mb-14 text-center">
          <p className="mb-3 font-mono text-xs font-medium uppercase tracking-[0.3em] text-teal">
            Capabilities
          </p>
          <h2 className="font-sans text-3xl font-bold tracking-tight text-offwhite sm:text-4xl">
            Built for scale. Designed for reliability.
          </h2>
        </motion.div>

        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
          {FEATURES.map((f, i) => (
            <motion.div
              key={f.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-60px" }}
              transition={{ duration: 0.45, delay: i * 0.08 }}
              className="group rounded-md border border-white/[0.07] bg-[#0e1114] p-6 transition-all duration-200 hover:border-teal/45 hover:bg-[#101518]"
            >
              <f.icon
                className="mb-4 h-6 w-6 text-teal transition-transform duration-200 group-hover:scale-110"
                aria-hidden="true"
              />
              <h3 className="mb-2 font-sans text-lg font-semibold text-offwhite transition-colors duration-200 group-hover:text-teal">
                {f.title}
              </h3>
              <p className="text-sm leading-relaxed text-gray-bright">
                {f.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
