const SVG_NS = 'http://www.w3.org/2000/svg';
const TILE_COLORS = {
  1: '#344c59', 2: '#b7784b', 3: '#37869b',
  4: '#c4a552', 5: '#bd647b', 6: '#9475be', 7: '#5a9c8f',
};

function shape(tag, attributes) {
  const element = document.createElementNS(SVG_NS, tag);
  Object.entries(attributes).forEach(([key, value]) => element.setAttribute(key, value));
  return element;
}

function drawPreview(data) {
  if (!Array.isArray(data.grid) || !data.grid.length) throw new Error('Missing stage grid');
  const svg = shape('svg', { 'aria-hidden': 'true', focusable: 'false' });
  const tiles = shape('g', { 'stroke-linejoin': 'round' });
  const bounds = { left: Infinity, right: -Infinity, top: Infinity, bottom: -Infinity };
  const start = data.start || [];

  data.grid.forEach((row, r) => row.forEach((tile, c) => {
    if (!tile) return;
    const x = (c - r) * 12;
    const y = (r + c) * 6;
    const points = `${x},${y - 5.5} ${x + 11},${y} ${x},${y + 5.5} ${x - 11},${y}`;
    tiles.append(shape('path', {
      d: `M${x - 11} ${y}l11 5.5 11-5.5v3l-11 5.5-11-5.5Z`, fill: '#182a35',
    }));
    tiles.append(shape('polygon', {
      points, fill: tile === 9 ? '#0a2128' : (TILE_COLORS[tile] || TILE_COLORS[1]),
      stroke: tile === 9 ? '#81e3d0' : '#637c88', 'stroke-width': tile === 9 ? 1.2 : 0.45,
    }));
    bounds.left = Math.min(bounds.left, x - 12);
    bounds.right = Math.max(bounds.right, x + 12);
    bounds.top = Math.min(bounds.top, y - 6);
    bounds.bottom = Math.max(bounds.bottom, y + 9);
  }));

  if (!Number.isFinite(bounds.left)) throw new Error('Empty stage grid');
  const [r, c] = start;
  if (Number.isInteger(r) && Number.isInteger(c)) {
    const x = (c - r) * 12;
    const y = (r + c) * 6;
    tiles.append(shape('path', { d: `M${x - 7} ${y - 18}l7 3.5v20l-7-3.5Z`, fill: '#bd8150' }));
    tiles.append(shape('path', { d: `M${x} ${y - 14.5}l7-3.5v20l-7 3.5Z`, fill: '#e4af74' }));
    tiles.append(shape('path', { d: `M${x} ${y - 21.5}l7 3.5-7 3.5-7-3.5Z`, fill: '#f8d59a' }));
    bounds.top = Math.min(bounds.top, y - 23);
  }
  const width = bounds.right - bounds.left + 24;
  const height = bounds.bottom - bounds.top + 12;
  svg.setAttribute('viewBox', `${bounds.left - 12} ${bounds.top - 6} ${width} ${height}`);
  svg.append(tiles);
  return svg;
}

export function createStagePreviews(api) {
  const cache = new Map();
  const lanes = Array.from({ length: 3 }, () => Promise.resolve());
  let nextLane = 0;

  function load(filename) {
    if (!cache.has(filename)) {
      const lane = nextLane++ % lanes.length;
      const request = lanes[lane].then(() => api.loadStage(filename));
      lanes[lane] = request.catch(() => {});
      cache.set(filename, request);
      request.catch(() => cache.delete(filename));
    }
    return cache.get(filename);
  }

  return async function renderPreview(container, filename) {
    try {
      const data = await load(filename);
      if (container.isConnected) container.replaceChildren(drawPreview(data));
    } catch {
      if (container.isConnected) container.textContent = 'Chưa có bản xem trước';
    }
  };
}
