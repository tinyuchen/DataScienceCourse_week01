async function loadPopulation() {
  const res = await fetch("data/cleaned.json", { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to load data/cleaned.json");
  const j = await res.json();

  const byYear = new Map(j.years.map(d => [d.year, d.population_billion]));
  const fmt = (b) => `${b.toFixed(1)}B`;

  document.getElementById("p2024").textContent = fmt(byYear.get(2024));
  document.getElementById("p2030").textContent = fmt(byYear.get(2030));
  document.getElementById("p2050").textContent = fmt(byYear.get(2050));
  document.getElementById("p2100").textContent = fmt(byYear.get(2100));

  document.getElementById("meanPop").textContent = `${j.summary.mean_population_billion.toFixed(3)}B`;
  document.getElementById("cagrAll").textContent = `${j.summary.cagr_2024_2100_pct.toFixed(3)}% / year`;

  document.getElementById("yearNow").textContent = new Date().getFullYear();
}

loadPopulation().catch(err => {
  console.error(err);
  alert("資料載入失敗：請確認 Actions 已產生 data/cleaned.json");
});
