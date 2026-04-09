const fs = require("node:fs");
const path = require("node:path");

const REPO_ROOT = path.resolve(__dirname, "../../..");
const ATLAS_PATH = path.join(
  REPO_ROOT,
  "publication_strategy_and_archive",
  "editorial_atlas",
  "atlas_data.json",
);

function loadAtlasJson() {
  return JSON.parse(fs.readFileSync(ATLAS_PATH, "utf8"));
}

function buildEditorialAtlasData() {
  const atlas = loadAtlasJson();
  const models = atlas.models || {};
  const defaultModelId = atlas.defaultModel || Object.keys(models)[0];
  
  // Transform all models to include their derived stats/anchors if not already present
  const enrichedModels = {};
  for (const [id, data] of Object.entries(models)) {
    const essays = [...(data.essays || [])];
    enrichedModels[id] = {
      ...data,
      essays,
      // The Python script now pre-calculates these, but we keep the fallback logic for robustness
      topAnchors: data.top_anchors || essays
        .slice()
        .sort((left, right) => {
          if (right.publication_power !== left.publication_power) {
            return right.publication_power - left.publication_power;
          }
          return right.traction - left.traction;
        })
        .slice(0, 6),
      stats: data.stats || {
        totalEssays: essays.length,
        topPower: Math.max(...essays.map((essay) => essay.publication_power || 0), 0),
        topTraction: Math.max(...essays.map((essay) => essay.traction || 0), 0),
        topCraft: Math.max(...essays.map((essay) => essay.craft || 0), 0),
      }
    };
  }

  const defaultModel = enrichedModels[defaultModelId] || { essays: [], stats: {}, topAnchors: [] };

  return {
    ...atlas,
    models: enrichedModels,
    defaultModel: defaultModelId,
    // Provide top-level keys for the initial SSR render (Gemini usually)
    ...defaultModel,
    routes: {
      page: "/editorial-atlas/",
    },
  };
}

module.exports = {
  buildEditorialAtlasData,
};
