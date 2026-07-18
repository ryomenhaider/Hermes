export default function FeaturesDoc() {
  return (
    <>
      <h1><code>Features</code></h1>
      <p><strong>Module:</strong> <code>hermes/features.py</code></p>

      <h2>What It Does</h2>
      <p>
        Lists all available features and their metadata. Features describe what
        economic indicators, transformations, and data products are available
        through the Hermes SDK.
      </p>

      <h2>Usage</h2>
      <pre><code>{`from hermes.features import list_available

features = list_available()

for f in features:
    print(f"{f['name']}: {f['description']}")`}</code></pre>

      <h2>Feature Schema</h2>
      <p>Each feature returned by <code>list_available()</code> is a dict with:</p>
      <ul>
        <li><strong>name</strong> — Short identifier for the feature</li>
        <li><strong>description</strong> — Human-readable explanation</li>
        <li><strong>category</strong> — Grouping (e.g. "indicator", "transform")</li>
        <li><strong>source</strong> — Origin connector (Fred, BIS, IMF, World Bank)</li>
      </ul>
    </>
  );
}
