document.addEventListener("DOMContentLoaded", () => {
  const root = document.querySelector("[data-archive-filters]");
  const results = document.querySelector("[data-archive-results]");
  if (!root || !results) {
    return;
  }

  const searchInput = root.querySelector("[data-filter-search]");
  const yearSelect = root.querySelector("[data-filter-year]");
  const seriesSelect = root.querySelector("[data-filter-series]");
  const cards = Array.from(results.querySelectorAll("[data-post-card]"));
  const emptyState = document.querySelector("[data-archive-empty]");

  function applyFilters() {
    const searchValue = (searchInput.value || "").trim().toLowerCase();
    const yearValue = yearSelect.value;
    const seriesValue = seriesSelect.value;
    let visible = 0;

    for (const card of cards) {
      const haystack = `${card.dataset.title} ${card.dataset.tags}`.trim();
      const matchesSearch = !searchValue || haystack.includes(searchValue);
      const matchesYear = !yearValue || card.dataset.year === yearValue;
      const matchesSeries = !seriesValue || card.dataset.series === seriesValue;
      const show = matchesSearch && matchesYear && matchesSeries;
      card.hidden = !show;
      if (show) {
        visible += 1;
      }
    }

    if (emptyState) {
      emptyState.hidden = visible !== 0;
    }
  }

  searchInput.addEventListener("input", applyFilters);
  yearSelect.addEventListener("change", applyFilters);
  seriesSelect.addEventListener("change", applyFilters);
});
