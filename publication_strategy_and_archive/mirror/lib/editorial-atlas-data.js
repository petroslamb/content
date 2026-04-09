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
  const essays = [...(atlas.essays || [])];
  const topAnchors = essays
    .slice()
    .sort((left, right) => {
      if (right.publication_power !== left.publication_power) {
        return right.publication_power - left.publication_power;
      }
      return right.traction - left.traction;
    })
    .slice(0, 6);

  return {
    ...atlas,
    essays,
    topAnchors,
    routes: {
      page: "/editorial-atlas/",
    },
    stats: {
      totalEssays: essays.length,
      topPower: Math.max(...essays.map((essay) => essay.publication_power || 0)),
      topTraction: Math.max(...essays.map((essay) => essay.traction || 0)),
      topCraft: Math.max(...essays.map((essay) => essay.craft || 0)),
    },
  };
}

module.exports = {
  buildEditorialAtlasData,
};
