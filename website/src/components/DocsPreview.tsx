"use client";

import { motion } from "framer-motion";
import { ArrowRight, Database, FileStack, Network, ServerCog } from "lucide-react";
import { DOCS_URL, GITHUB_URL } from "@/lib/constants";

const DOCS_NAV = [
  { label: "Introduction" },
  { label: "Quickstart" },
  { label: "Installation" },
  { header: "CORE" },
  { label: "Acquisition" },
  { label: "Parsing" },
  { label: "Normalization" },
  { label: "Validation" },
  { label: "Metadata" },
  { label: "Entities" },
  { header: "DATA" },
  { label: "Datasets" },
  { label: "Schemas" },
  { label: "Storage" },
  { label: "Querying" },
  { label: "Export" },
  { header: "REFERENCE" },
  { label: "Python API" },
  { label: "CLI" },
  { label: "Configuration" },
];

const FEATURE_BADGES = [
  { icon: Database, label: "Multi-source acquisition" },
  { icon: FileStack, label: "Schema normalization" },
  { icon: Network, label: "Entity resolution" },
  { icon: ServerCog, label: "Scalable storage" },
];

const sectionFade = {
  initial: { opacity: 0, y: 24 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true, margin: "-80px" },
  transition: { duration: 0.6, ease: "easeOut" as const },
};

export function DocsPreview() {
  return (
    <section className="relative border-t border-white/[0.06] bg-[#0e1114]">
      <div className="mx-auto max-w-6xl px-5 py-24 sm:px-8">
        {/* Mockup */}
        <motion.div {...sectionFade} className="overflow-hidden rounded-lg border border-white/[0.08] bg-midnight shadow-2xl shadow-black/50">
          <div className="flex">
            {/* Sidebar mockup */}
            <aside className="hidden w-64 shrink-0 border-r border-white/[0.07] p-5 sm:block" aria-hidden="true">
              <nav className="space-y-1 font-sans">
                {DOCS_NAV.map((item, i) =>
                  item.header ? (
                    <p
                      key={`${item.header}-${i}`}
                      className="px-2 pb-1 pt-4 font-mono text-[10px] font-semibold uppercase tracking-[0.25em] text-teal"
                    >
                      {item.header}
                    </p>
                  ) : (
                   <p
  key={item.label}
  className={`cursor-default rounded-sm px-2 py-1 text-sm ${
    item.label === "Introduction"
      ? "bg-teal/10 font-medium text-teal"
      : "text-gray-bright"
  }`}
>
  {item.label}
</p>
                  )
                )}
              </nav>
            </aside>

            {/* Main content mockup */}
            <div className="min-w-0 flex-1 p-6 sm:p-8">
              <p className="font-mono text-xs uppercase tracking-[0.25em] text-teal" aria-hidden="true">
                Introduction
              </p>
              <h3 className="mt-3 font-sans text-2xl font-bold tracking-tight text-offwhite">
                Introduction
              </h3>
              <p className="mt-3 max-w-lg text-sm leading-relaxed text-gray-bright">
                Hermes provides a unified interface for acquiring, processing and
                serving data — from financial feeds to geopolitical sources — with
                built-in validation, normalization and provenance tracking.
              </p>

              {/* Install command */}
              <div className="mt-6 flex items-center gap-3 overflow-x-auto rounded-md border border-white/[0.07] bg-[#0e1114] px-4 py-3 font-mono text-sm">
                <span className="text-teal" aria-hidden="true">
                  $
                </span>
                <code className="whitespace-nowrap text-gray-bright">
                  pip install hermes-plt
                </code>
                <span className="ml-auto h-2 w-2 shrink-0 rounded-full border border-teal" aria-hidden="true" />
              </div>

              {/* Feature badges */}
              <div className="mt-6 flex flex-wrap gap-2">
                {FEATURE_BADGES.map((b) => (
                  <span
                    key={b.label}
                    className="inline-flex items-center gap-1.5 rounded-sm border border-teal/30 px-2.5 py-1 text-xs text-gray-bright"
                  >
                    <b.icon className="h-3.5 w-3.5 text-teal" aria-hidden="true" />
                    {b.label}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </motion.div>

        {/* CTA */}
        <motion.div
          {...sectionFade}
          className="mx-auto mt-20 max-w-2xl text-center"
        >
          <h2 className="font-sans text-3xl font-bold tracking-tight text-offwhite sm:text-4xl">
            Data infrastructure for the modern world.
          </h2>
          <p className="mt-4 text-base leading-relaxed text-gray-bright">
            Hermes provides a unified interface for acquiring, processing and
            serving data from multiple sources. Built for scale, designed for
            reliability.
          </p>
          <div className="mt-8 flex flex-col justify-center gap-4 sm:flex-row">
            <a
              href={DOCS_URL}
              className="inline-flex items-center justify-center gap-2 rounded-sm bg-teal px-7 py-3.5 font-sans text-sm font-semibold text-midnight transition-colors duration-150 hover:bg-[#3a8379]"
            >
              Get Started
              <ArrowRight className="h-4 w-4" aria-hidden="true" />
            </a>
            <a
              href={GITHUB_URL}
              className="inline-flex items-center justify-center gap-2 rounded-sm border border-offwhite/30 px-7 py-3.5 font-sans text-sm font-semibold text-offwhite transition-colors duration-150 hover:border-offwhite/60"
            >
              View on GitHub
            </a>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
