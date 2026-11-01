async function getJson(url) {
  const response = await fetch(url);
  return response.json();
}

export function listStages() {
  return getJson('/api/stages');
}

export function loadStage(filename) {
  return getJson(`/stages/${encodeURIComponent(filename)}`);
}

export function solveStage(filename, algorithm) {
  const params = new URLSearchParams({ stage: filename, algo: algorithm });
  return getJson(`/api/solve?${params}`);
}
