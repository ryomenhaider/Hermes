import { Header } from "@/components/Header";
import { Hero } from "@/components/Hero";
import { HowItWorks } from "@/components/HowItWorks";
import { Features } from "@/components/Features";
import { DocsPreview } from "@/components/DocsPreview";
import { Footer } from "@/components/Footer";

export default function Home() {
  return (
    <>
      <Header />
  <main id="main-content" className="flex-1">
        <Hero />
        <HowItWorks />
        <Features />
        <DocsPreview />
      </main>
      <Footer />
    </>
  );
}
