import { Link } from 'react-router-dom';
import '../App.css';

export default function Home() {
  return (
    <div className="landing-hero">
      <div className="mb-8">
        <span className="text-7xl font-black tracking-tighter block">HERMES</span>
        <span className="text-lg tracking-[0.3em] uppercase text-gray-500">Data Intelligence Platform</span>
      </div>
      <p className="subtitle">
        Foundational intelligence data platform for acquiring, validating, normalizing,
        storing, and serving intelligence datasets.
      </p>
      <p className="text-sm text-gray-500 max-w-xl">
        Hermes is a Python SDK that connects to 30+ free global data sources (FRED, BIS, IMF,
        World Bank, GDELT, UN Comtrade, and more), normalizes everything to canonical schemas,
        engineers intelligence features, and provides a storage layer for caching, metadata
        tracking, and data lineage.
      </p>
      <div className="flex gap-4 mt-8">
        <Link
          to="/docs/getting-started"
          className="px-6 py-3 bg-black text-white font-medium text-sm border-2 border-black hover:bg-white hover:text-black transition-colors"
        >
          GET STARTED
        </Link>
        <a
          href="https://github.com/ryomenhaider/Hermes"
          target="_blank"
          className="px-6 py-3 bg-white text-black font-medium text-sm border-2 border-black hover:bg-black hover:text-white transition-colors"
        >
          GITHUB
        </a>
      </div>
    </div>
  );
}
