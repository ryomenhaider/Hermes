"use client";

import { ArrowRight } from "lucide-react";
import { motion } from "framer-motion";
import { MapTexture } from "@/components/MapTexture";
import { PipelineStrip } from "@/components/PipelineStrip";
import { DOCS_URL, GITHUB_URL } from "@/lib/constants";

const fadeUp = {
  initial: { opacity: 0, y: 16 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true, margin: "-80px" },
  transition: { duration: 0.6, ease: "easeOut" as const },
};

export function Hero() {
  return (
    <section className="relative overflow-hidden">
      <div className="absolute inset-0" aria-hidden="true">
        <MapTexture />
        <div
          className="absolute inset-0 opacity-[0.35]"
          style={{
            backgroundImage:
              "linear-gradient(to right, rgba(47,111,104,0.06) 1px, transparent 1px), linear-gradient(to bottom, rgba(47,111,104,0.06) 1px, transparent 1px)",
            backgroundSize: "72px 72px",
          }}
        />
      </div>

      <div className="relative mx-auto flex max-w-6xl flex-col items-center px-5 pb-24 pt-24 text-center sm:px-8 sm:pt-32">
        <motion.p
          {...fadeUp}
          className="mb-6 font-mono text-xs font-medium uppercase tracking-[0.4em] text-teal"
        >
          Hermes
        </motion.p>

        <motion.h1
          {...fadeUp}
          transition={{ duration: 0.6, ease: "easeOut", delay: 0.05 }}
          className="max-w-3xl font-sans text-4xl font-bold leading-[1.05] tracking-tight text-offwhite sm:text-6xl md:text-7xl"
        >
          Reliable data.
          <br />
          Real intelligence.
        </motion.h1>

        <motion.p
          {...fadeUp}
          transition={{ duration: 0.6, ease: "easeOut", delay: 0.12 }}
          className="mt-7 max-w-xl text-base leading-relaxed text-gray-bright sm:text-lg"
        >
          Hermes is a modern data infrastructure platform for acquiring, processing
          and serving structured and unstructured data at scale.
        </motion.p>

        <motion.div
          {...fadeUp}
          transition={{ duration: 0.6, ease: "easeOut", delay: 0.18 }}
          className="mt-10 w-full"
        >
          <PipelineStrip />
        </motion.div>

        <motion.div
          {...fadeUp}
          transition={{ duration: 0.6, ease: "easeOut", delay: 0.24 }}
          className="mt-12 flex flex-col gap-3 sm:flex-row sm:gap-4"
        >
          <a
            href={DOCS_URL}
            className="inline-flex items-center justify-center gap-2 rounded-sm bg-teal px-7 py-3.5 font-sans text-sm font-semibold text-midnight transition-colors duration-150 hover:bg-[#3a8379]"
          >
            Documentation
            <ArrowRight className="h-4 w-4" aria-hidden="true" />
          </a>
          <a
            href={GITHUB_URL}
            className="inline-flex items-center justify-center gap-2 rounded-sm border border-offwhite/25 px-7 py-3.5 font-sans text-sm font-semibold text-offwhite transition-colors duration-150 hover:border-teal hover:text-teal"
          >
            View on GitHub
          </a>
        </motion.div>
      </div>
    </section>
  );
}
