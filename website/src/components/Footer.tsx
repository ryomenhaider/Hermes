import Link from "next/link";
import { LogoMark } from "@/components/Logo";
import { SocialLinks } from "@/components/SocialLinks";
import { DOCS_URL, GITHUB_URL } from "@/lib/constants";

const FOOTER_LINKS = [
  { label: "Docs", href: DOCS_URL },
  { label: "GitHub", href: GITHUB_URL },
];

export function Footer() {
  return (
    <footer className="border-t border-white/[0.06] bg-midnight">
      <div className="mx-auto max-w-6xl px-5 py-12 sm:px-8">
        <div className="flex flex-col gap-8 sm:flex-row sm:items-start sm:justify-between">
          {/* Brand */}
          <div className="flex items-center gap-3">
            <LogoMark className="h-6 w-9 shrink-0" />
            <div>
              <p className="font-sans text-sm font-bold uppercase leading-none tracking-[0.28em] text-offwhite">
                Hermes
              </p>
              <p className="mt-1.5 font-mono text-[10px] uppercase tracking-[0.22em] text-gray">
                DATA INFRASTRUCTURE
              </p>
            </div>
          </div>

          {/* Links + Social */}
          <div className="flex flex-col gap-6 sm:items-end">
            <nav className="flex items-center gap-6" aria-label="Footer">
              {FOOTER_LINKS.map((l) => (
                <a
                  key={l.label}
                  href={l.href}
                  className="text-sm font-medium text-gray-bright transition-colors duration-150 hover:text-teal"
                >
                  {l.label}
                </a>
              ))}
            </nav>
            <SocialLinks />
          </div>
        </div>

        <div className="mt-10 border-t border-white/[0.06] pt-6 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <p className="text-xs text-gray">
            &copy; {new Date().getFullYear()} Hermes. All rights reserved.
          </p>
          <p className="text-xs text-gray">
            Built for reliable data infrastructure.
          </p>
        </div>
      </div>
    </footer>
  );
}
