const markdownIt = require("markdown-it");
const { buildSiteConfig } = require("./publication_strategy_and_archive/mirror/lib/archive-data");

module.exports = function (eleventyConfig) {
  const site = buildSiteConfig();
  const markdownLibrary = markdownIt({
    html: true,
    linkify: true,
    typographer: false,
  });

  eleventyConfig.setLibrary("md", markdownLibrary);

  eleventyConfig.addWatchTarget("publication_strategy_and_archive/substack_archive");
  eleventyConfig.addWatchTarget("publication_strategy_and_archive/post_map.yaml");
  eleventyConfig.addWatchTarget(
    "publication_strategy_and_archive/portfolio/portfolio_manifest.yaml",
  );

  eleventyConfig.addPassthroughCopy({
    "publication_strategy_and_archive/mirror/src/static": "assets",
  });
  eleventyConfig.addPassthroughCopy({
    "publication_strategy_and_archive/substack_archive": "raw/substack_archive",
  });

  eleventyConfig.addGlobalData("site", site);
  eleventyConfig.addGlobalData("buildTimestamp", new Date().toISOString());

  eleventyConfig.addFilter("renderPostContent", (markdown) => markdownLibrary.render(markdown || ""));
  eleventyConfig.addFilter("absoluteUrl", (routePath, siteUrl = site.siteUrl) => {
    if (!routePath) {
      return siteUrl;
    }
    const normalizedSite = (siteUrl || "").replace(/\/$/, "");
    const normalizedPath = routePath.startsWith("/") ? routePath : `/${routePath}`;
    return `${normalizedSite}${normalizedPath}`;
  });
  eleventyConfig.addFilter("json", (value) => JSON.stringify(value, null, 2));

  return {
    pathPrefix: site.pathPrefix,
    dir: {
      input: "publication_strategy_and_archive/mirror/src",
      includes: "_includes",
      data: "_data",
      output: "publication_strategy_and_archive/mirror/_site",
    },
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
    templateFormats: ["njk", "md", "html"],
  };
};
