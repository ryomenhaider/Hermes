"use client";

import { useEffect, useRef, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import {
  CheckCircle,
  Database,
  FileText,
  Layers,
  Settings,
  Share2,
  Zap,
  type LucideIcon,
} from "lucide-react";
import { SectionHead } from "@/components/SectionHead";
import { Code } from "@/components/Code";
import { EntityGraph } from "@/components/EntityGraph";
import { DATA_ROWS, PIPELINE } from "@/lib/constants";

gsap.registerPlugin(ScrollTrigger);

const ICONS: Record<string, LucideIcon> = {
  database: Database,
  share: Share2,
  file: FileText,
  settings: Settings,
  check: CheckCircle,
  layers: Layers,
  zap: Zap,
};

const SAMPLE = `import hermes as hr

gdp = hr.fetch("world_bank", indicator="NY.GDP.MKTP.CD")
clean = hr.normalize(gdp, report=True)`;

function StageDetail({ index }: { index: number }) {
  const stage = PIPELINE[index];
  const Icon = ICONS[stage.icon];

  return (
    <div className="panel brackets h-full p-6">
      <div className="flex items-center gap-3">
        <span className="flex h-9 w-9 items-center justify-center border border-teal/50 text-teal-bright">
          <Icon className="h-4 w-4" aria-hidden="true" />
        </span>
        <div>
          <p className="label text-teal-bright">{stage.label}</p>
          <p className="label mt-1 text-gray">{stage.code}</p>
        </div>
      </div>

      <h3 className="mt-6 font-sans text-xl font-semibold tracking-tight text-offwhite">
        {stage.headline}
      </h3>
      <p className="mt-3 text-sm leading-relaxed text-gray-bright">{stage.body}</p>

      <ul className="mt-6 space-y-2 border-t border-hairline pt-5">
        {stage.signal.map((s) => (
          <li key={s} className="label flex items-center gap-2.5 text-gray">
            <span className="h-1 w-1 rotate-45 bg-teal-bright" aria-hidden="true" />
            {s}
          </li>
        ))}
      </ul>
    </div>
  );
}

export function HowItWorks() {
  const [active, setActive] = useState(0);
  const scroller = useRef<HTMLDivElement>(null);
  const fill = useRef<HTMLSpanElement>(null);

  // Not gated on motion preference: the tall scroller would leave anyone who
  // skips the animation stuck on stage 1 with a lot of empty page below.
  useEffect(() => {
    const ctx = gsap.context(() => {
      const mm = gsap.matchMedia();

      mm.add("(min-width: 768px)", () => {
        const trigger = ScrollTrigger.create({
          trigger: scroller.current,
          start: "top top",
          end: "bottom bottom",
          onUpdate: (self) => {
            if (fill.current) gsap.set(fill.current, { scaleY: self.progress });
            const next = Math.min(
              PIPELINE.length - 1,
              Math.floor(self.progress * PIPELINE.length),
            );
            setActive((prev) => (prev === next ? prev : next));
          },
        });
        return () => trigger.kill();
      });
    }, scroller);

    return () => ctx.revert();
  }, []);

  return (
    <section id="platform" className="relative border-t border-hairline bg-panel">
      <div className="shell py-24">
        <SectionHead
          index="01"
          kicker="Platform"
          title="Seven stages. One interface."
          lede="Every dataset moves through the same pipeline, whatever it started as. Scroll or select a stage. Each one is a single module with a single job."
        />
      </div>

      {/* Desktop: the stage row sticks while the page scrolls through it */}
      <div
        ref={scroller}
        className="hidden md:block"
        style={{ height: `${PIPELINE.length * 55}vh` }}
      >
        <div className="sticky top-16 flex h-[calc(100vh-4rem)] items-center">
          <div className="shell grid w-full grid-cols-[1fr_1fr] items-center gap-14">
            <div>
              <div className="relative">
                <ol className="border-l border-hairline">
                  {PIPELINE.map((stage, i) => {
                    const Icon = ICONS[stage.icon];
                    const on = i === active;
                    return (
                      <li key={stage.id}>
                        <button
                          type="button"
                          onClick={() => setActive(i)}
                          aria-current={on ? "step" : undefined}
                          aria-label={`Stage ${i + 1}: ${stage.label}`}
                          className={`flex w-full items-center gap-4 border-l-2 py-3 pl-5 text-left transition-all duration-300 ${
                            on
                              ? "border-teal-bright bg-midnight/60"
                              : "border-transparent opacity-45 hover:opacity-80"
                          }`}
                        >
                          <Icon
                            className={`h-4 w-4 shrink-0 ${on ? "text-teal-bright" : "text-gray"}`}
                            aria-hidden="true"
                          />
                          <span className="label tabular w-6 shrink-0 text-gray">
                            {String(i + 1).padStart(2, "0")}
                          </span>
                          <span
                            className={`font-sans text-base font-medium tracking-tight ${
                              on ? "text-offwhite" : "text-gray-bright"
                            }`}
                          >
                            {stage.label}
                          </span>
                        </button>
                      </li>
                    );
                  })}
                </ol>
                <span
                  ref={fill}
                  aria-hidden="true"
                  className="absolute -left-px top-0 h-full w-px origin-top scale-y-0 bg-teal-bright"
                />
              </div>

              <div className="mt-8 h-px w-full bg-hairline">
                <span className="label mt-3 block text-gray">
                  Stage {String(active + 1).padStart(2, "0")} /{" "}
                  {String(PIPELINE.length).padStart(2, "0")}
                </span>
              </div>
            </div>

            <AnimatePresence mode="wait">
              <motion.div
                key={PIPELINE[active].id}
                initial={{ opacity: 0, y: 14 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -14 }}
                transition={{ duration: 0.28, ease: "easeOut" }}
              >
                <StageDetail index={active} />
              </motion.div>
            </AnimatePresence>
          </div>
        </div>
      </div>

      {/* Mobile: the same stages, stacked and read in order */}
      <div className="shell pb-24 md:hidden">
        <ol className="space-y-4">
          {PIPELINE.map((stage, i) => (
            <li key={stage.id}>
              <div className="flex items-baseline gap-3 pb-2">
                <span className="label tabular text-teal-bright">
                  {String(i + 1).padStart(2, "0")}
                </span>
                <span className="label text-gray">{stage.label}</span>
              </div>
              <StageDetail index={i} />
            </li>
          ))}
        </ol>
      </div>

      {/* Evidence band */}
      <div className="border-t border-hairline">
        <div className="shell grid grid-cols-1 gap-px bg-hairline lg:grid-cols-3">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.6, ease: "easeOut" }}
            className="panel brackets rounded-none border-0 bg-midnight p-6"
          >
            <p className="label text-gray">Normalized output</p>
            <table className="mt-4 w-full border-collapse font-mono text-[11px]">
              <thead>
                <tr className="text-left text-gray">
                  <th className="pb-2 font-normal">country</th>
                  <th className="pb-2 font-normal">indicator</th>
                  <th className="pb-2 text-right font-normal">value</th>
                  <th className="pb-2 text-right font-normal">date</th>
                </tr>
              </thead>
              <tbody>
                {DATA_ROWS.map((row) => (
                  <tr key={row[0]} className="border-t border-hairline text-gray-bright">
                    <td className="py-1.5 text-offwhite">{row[0]}</td>
                    <td className="py-1.5">{row[1]}</td>
                    <td className="py-1.5 text-right tabular">{row[2]}</td>
                    <td className="py-1.5 text-right tabular">{row[3]}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.6, ease: "easeOut" }}
            className="panel brackets rounded-none border-0 bg-midnight p-6"
          >
            <p className="label text-gray">Entity resolution</p>
            <div className="mt-4 h-40">
              <EntityGraph />
            </div>
            <p className="label mt-4 text-gray">Hover a node</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: 0.6, ease: "easeOut" }}
            className="panel brackets rounded-none border-0 bg-midnight p-6"
          >
            <p className="label text-gray">The whole call</p>
            <pre className="mt-4 overflow-x-auto">
              <Code>{SAMPLE}</Code>
            </pre>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
