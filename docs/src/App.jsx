import { BrowserRouter, Routes, Route } from 'react-router-dom';
import DocLayout from './layout/DocLayout';
import Home from './pages/Home';
import GettingStarted from './pages/docs/GettingStarted';
import HermesDoc from './pages/docs/Hermes';
import FredDoc from './pages/docs/Fred';
import BISDoc from './pages/docs/BIS';
import IMFDoc from './pages/docs/IMF';
import WorldBankDoc from './pages/docs/WorldBank';
import SchemasDoc from './pages/docs/Schemas';
import FeaturesDoc from './pages/docs/Filters';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/docs" element={<DocLayout />}>
          <Route index element={<GettingStarted />} />
          <Route path="getting-started" element={<GettingStarted />} />
          <Route path="hermes" element={<HermesDoc />} />
          <Route path="fred" element={<FredDoc />} />
          <Route path="bis" element={<BISDoc />} />
          <Route path="imf" element={<IMFDoc />} />
          <Route path="world-bank" element={<WorldBankDoc />} />
          <Route path="schemas" element={<SchemasDoc />} />
          <Route path="features" element={<FeaturesDoc />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
