const fs = require("node:fs");
const path = require("node:path");
const yaml = require("js-yaml");

const REPO_ROOT = path.resolve(__dirname, "../../..");
const METADATA_PATH = path.join(
  REPO_ROOT,
  "publication_strategy_and_archive",
  "substack_archive",
  "metadata.json",
);
const POST_MAP_PATH = path.join(
  REPO_ROOT,
  "publication_strategy_and_archive",
  "post_map.yaml",
);
const PORTFOLIO_MANIFEST_PATH = process.env.PORTFOLIO_MANIFEST_PATH
  ? path.resolve(process.env.PORTFOLIO_MANIFEST_PATH)
  : path.join(
      REPO_ROOT,
      "publication_strategy_and_archive",
      "portfolio",
      "portfolio_manifest.yaml",
    );

const PORTFOLIO_SECTIONS = Object.freeze({
  FLAGSHIP: "flagship_artifact_ids",
  SUPPORTING: "supporting_artifact_ids",
});

function normalizePathPrefix(rawPrefix = "/") {
  if (!rawPrefix || rawPrefix === "/") {
    return "/";
  }
  const trimmed = rawPrefix.replace(/^\/+|\/+$/g, "");
  return trimmed ? `/${trimmed}/` : "/";
}

function normalizeSiteUrl(rawUrl, pathPrefix) {
  const trimmed = (rawUrl || "").replace(/\/$/, "");
  if (!trimmed || pathPrefix === "/") {
    return trimmed;
  }
  const prefixWithoutTrailingSlash = pathPrefix.replace(/\/$/, "");
  if (trimmed.endsWith(prefixWithoutTrailingSlash)) {
    return trimmed.slice(0, -prefixWithoutTrailingSlash.length) || trimmed;
  }
  return trimmed;
}

function withPathPrefix(pathPrefix, routePath) {
  const normalized = routePath.startsWith("/") ? routePath : `/${routePath}`;
  if (pathPrefix === "/") {
    return normalized;
  }
  return `${pathPrefix.replace(/\/$/, "")}${normalized}`;
}

function formatDisplayDate(dateValue) {
  return new Intl.DateTimeFormat("en", {
    year: "numeric",
    month: "long",
    day: "numeric",
  }).format(new Date(dateValue));
}

function loadJson(jsonPath) {
  return JSON.parse(fs.readFileSync(jsonPath, "utf8"));
}

function loadYaml(yamlPath) {
  return yaml.load(fs.readFileSync(yamlPath, "utf8")) || {};
}

function loadPortfolioManifest() {
  if (!fs.existsSync(PORTFOLIO_MANIFEST_PATH)) {
    throw new Error(
      `Missing portfolio manifest: ${PORTFOLIO_MANIFEST_PATH}. ` +
        "Generate the reviewed portfolio decision layer before building the mirror.",
    );
  }

  const manifest = loadYaml(PORTFOLIO_MANIFEST_PATH);
  if (!Array.isArray(manifest.artifacts)) {
    throw new Error("Portfolio manifest artifacts must be a list.");
  }
  if (!manifest.homepage || typeof manifest.homepage !== "object") {
    throw new Error("Portfolio manifest homepage must be an object.");
  }
  return manifest;
}

function portfolioEvidenceUrl(artifact, post, site) {
  const configured = artifact.homepage?.evidence_url;
  if (typeof configured === "string" && configured.trim()) {
    return configured.trim();
  }

  for (const rawAnchor of artifact.evidence_anchors || []) {
    if (typeof rawAnchor !== "string" || !rawAnchor.trim()) {
      continue;
    }
    const anchor = rawAnchor.trim();
    if (/^https?:\/\//.test(anchor)) {
      return anchor;
    }
    if (/^[A-Za-z0-9_.\/-]+(?:#[A-Za-z0-9_.:-]+)?$/.test(anchor)) {
      return `${site.repoUrl}/blob/main/${anchor}`;
    }
  }

  return post.researchFolderUrl;
}

function buildPortfolioData(manifest, mirroredPosts, site) {
  const artifactsById = new Map();
  for (const artifact of manifest.artifacts) {
    if (!artifact || typeof artifact !== "object" || !artifact.artifact_id) {
      continue;
    }
    if (artifactsById.has(artifact.artifact_id)) {
      throw new Error(`Duplicate portfolio artifact_id: ${artifact.artifact_id}`);
    }
    artifactsById.set(artifact.artifact_id, artifact);
  }

  const postsBySlug = new Map(mirroredPosts.map((post) => [post.slug, post]));
  const selectSection = (section) => {
    const key = PORTFOLIO_SECTIONS[section];
    const artifactIds = manifest.homepage[key] || [];
    if (!Array.isArray(artifactIds)) {
      throw new Error(`Portfolio homepage.${key} must be a list.`);
    }
    if (artifactIds.length > 4) {
      throw new Error(`Portfolio homepage exceeds four ${section.toLowerCase()} essays.`);
    }

    return artifactIds.map((artifactId, index) => {
      const artifact = artifactsById.get(artifactId);
      if (!artifact) {
        throw new Error(`Portfolio homepage references unknown artifact: ${artifactId}`);
      }
      if (artifact.platform !== "SUBSTACK") {
        throw new Error(`Portfolio homepage artifact must be SUBSTACK: ${artifactId}`);
      }
      if (artifact.selection_tier !== section) {
        throw new Error(
          `Portfolio homepage artifact ${artifactId} must have selection_tier ${section}.`,
        );
      }

      const slug = artifact.platform_id;
      const post = postsBySlug.get(slug);
      if (!post) {
        throw new Error(
          `Portfolio homepage artifact ${artifactId} has no enabled mirror post for ${slug}.`,
        );
      }
      if (artifact.current_url !== post.url) {
        throw new Error(
          `Portfolio URL drift for ${artifactId}: manifest ${artifact.current_url}, archive ${post.url}.`,
        );
      }

      const annotation = artifact.homepage?.annotation || artifact.rationale;
      if (typeof annotation !== "string" || !annotation.trim()) {
        throw new Error(`Portfolio homepage artifact ${artifactId} is missing its annotation.`);
      }

      return {
        ...post,
        artifactId,
        portfolioSection: section,
        portfolioOrder: index + 1,
        portfolioAnnotation: annotation.trim(),
        portfolioEvidenceUrl: portfolioEvidenceUrl(artifact, post, site),
      };
    });
  };

  return {
    version: manifest.portfolio_version,
    disclosure: manifest.ai_disclosure,
    professionalProfileUrl: manifest.professional_profile_url,
    flagshipPosts: selectSection("FLAGSHIP"),
    supportingPosts: selectSection("SUPPORTING"),
  };
}

function stripArchiveHeader(markdown) {
  return markdown.replace(/^# .*?\n\nDate: .*?\nURL: .*?\n\n/s, "").trim();
}

function rewriteArchiveAssets(markdown, pathPrefix) {
  return markdown.replace(
    /\((assets\/[^)]+)\)/g,
    (_match, assetPath) => `(${withPathPrefix(pathPrefix, `/raw/substack_archive/${assetPath}`)})`,
  );
}

function buildSiteConfig() {
  const pathPrefix = normalizePathPrefix(process.env.ELEVENTY_PATH_PREFIX || "/");
  return {
    title: "Rooted Layers Mirror",
    publicationTitle: "Rooted Layers",
    tagline: "Substack essays, mirrored with their research layers and source folders.",
    description:
      "A public GitHub Pages mirror of Rooted Layers. Substack remains canonical. The mirror keeps each essay close to its research package, source archive, and provenance trail.",
    substackUrl: "https://lambpetros.substack.com",
    repoUrl: process.env.MIRROR_REPO_URL || "https://github.com/petroslamb/content",
    siteUrl: normalizeSiteUrl(
      process.env.MIRROR_SITE_URL || "https://petroslamb.github.io/content",
      pathPrefix,
    ),
    pathPrefix,
  };
}

function buildArchiveData() {
  const site = buildSiteConfig();
  const manifest = loadJson(METADATA_PATH);
  const postMap = (loadYaml(POST_MAP_PATH).posts || {});
  const portfolioManifest = loadPortfolioManifest();

  const posts = manifest
    .filter((post) => Boolean(post.md_path) && Boolean(post.html_path))
    .map((post) => {
      const mapEntry = postMap[post.slug] || {};
      const mdAbsolute = path.join(REPO_ROOT, post.md_path);
      const htmlAbsolute = path.join(REPO_ROOT, post.html_path);
      const bodyMarkdown = fs.existsSync(mdAbsolute)
        ? rewriteArchiveAssets(stripArchiveHeader(fs.readFileSync(mdAbsolute, "utf8")), site.pathPrefix)
        : "The local markdown snapshot is missing for this post.";
      const rawMarkdownPath = `/raw/substack_archive/${path.basename(post.md_path)}`;
      const rawHtmlPath = `/raw/substack_archive/${path.basename(post.html_path)}`;
      const researchFolder = mapEntry.research_folder;
      const hasResearchFolder = Boolean(researchFolder) && researchFolder !== ".";
      const researchPath = hasResearchFolder ? researchFolder : "";
      const summary =
        mapEntry.summary ||
        `Archive mirror for ${post.title}. The research package mapping has not been filled in yet.`;
      const heroImageBasename = post.hero_image ? path.basename(post.hero_image) : "";

      return {
        ...post,
        title: mapEntry.title || post.title,
        summary,
        tags: mapEntry.tags || [],
        featured: Boolean(mapEntry.featured),
        status: mapEntry.status || "published",
        researchFolder: researchFolder || null,
        researchFolderLabel: hasResearchFolder ? `${researchFolder}/` : "Repository root",
        researchFolderUrl: hasResearchFolder
          ? `${site.repoUrl}/tree/main/${researchPath}`
          : site.repoUrl,
        pendingResearchPackage: !mapEntry.research_folder,
        bodyMarkdown,
        permalink: `/posts/${post.slug}/`,
        rawMarkdownPath,
        rawHtmlPath,
        githubMarkdownUrl: `${site.repoUrl}/blob/main/${post.md_path}`,
        githubHtmlUrl: `${site.repoUrl}/blob/main/${post.html_path}`,
        githubMirrorUrl: `${site.repoUrl}/tree/main/publication_strategy_and_archive/mirror`,
        heroImagePath: heroImageBasename
          ? `/raw/substack_archive/assets/${heroImageBasename}`
          : null,
        heroImageUrl: heroImageBasename
          ? withPathPrefix(site.pathPrefix, `/raw/substack_archive/assets/${heroImageBasename}`)
          : null,
        seriesKey: mapEntry.series_key || null,
        seriesTitle: mapEntry.series_title || null,
        seriesOrder: mapEntry.series_order || null,
        formattedDate: formatDisplayDate(post.post_date),
        year: new Date(post.post_date).getUTCFullYear(),
        fetchedAtDisplay: formatDisplayDate(post.fetched_at),
        rawMarkdownExists: fs.existsSync(mdAbsolute),
        rawHtmlExists: fs.existsSync(htmlAbsolute),
      };
    })
    .sort((left, right) => new Date(right.post_date) - new Date(left.post_date));

  const mirroredPosts = posts.filter((post) => post.mirror_enabled);
  const seriesMap = new Map();
  for (const post of mirroredPosts) {
    if (!post.seriesKey) {
      continue;
    }
    if (!seriesMap.has(post.seriesKey)) {
      seriesMap.set(post.seriesKey, []);
    }
    seriesMap.get(post.seriesKey).push(post);
  }

  const series = Array.from(seriesMap.entries())
    .map(([key, seriesPosts]) => {
      const ordered = [...seriesPosts].sort((left, right) => {
        const leftOrder = left.seriesOrder ?? Number.MAX_SAFE_INTEGER;
        const rightOrder = right.seriesOrder ?? Number.MAX_SAFE_INTEGER;
        if (leftOrder !== rightOrder) {
          return leftOrder - rightOrder;
        }
        return new Date(left.post_date) - new Date(right.post_date);
      });
      ordered.forEach((post, index) => {
        post.series = {
          key,
          title: ordered[0].seriesTitle || key,
          index,
          total: ordered.length,
          previous: index > 0 ? ordered[index - 1] : null,
          next: index < ordered.length - 1 ? ordered[index + 1] : null,
        };
      });
      return {
        key,
        title: ordered[0].seriesTitle || key,
        permalink: `/series/${key}/`,
        posts: ordered,
        postCount: ordered.length,
        summary: `${ordered.length} mirrored posts in publication order.`,
      };
    })
    .sort((left, right) => right.postCount - left.postCount || left.title.localeCompare(right.title));

  const uniqueTags = [...new Set(mirroredPosts.flatMap((post) => post.tags))].sort();
  const uniqueYears = [...new Set(mirroredPosts.map((post) => String(post.year)))].sort((a, b) => b.localeCompare(a));

  return {
    generatedAt: new Date().toISOString(),
    posts: mirroredPosts,
    portfolio: buildPortfolioData(portfolioManifest, mirroredPosts, site),
    series,
    filters: {
      tags: uniqueTags,
      years: uniqueYears,
    },
    stats: {
      totalPosts: mirroredPosts.length,
      totalSeries: series.length,
      totalFolders: new Set(mirroredPosts.map((post) => post.researchFolder || ".")).size,
      lastFetchedAt: mirroredPosts[0]?.fetched_at || null,
      lastFetchedAtDisplay: mirroredPosts[0]?.fetchedAtDisplay || "",
    },
    site,
  };
}

module.exports = {
  buildArchiveData,
  buildPortfolioData,
  buildSiteConfig,
  formatDisplayDate,
  loadPortfolioManifest,
  normalizePathPrefix,
  normalizeSiteUrl,
  withPathPrefix,
};
