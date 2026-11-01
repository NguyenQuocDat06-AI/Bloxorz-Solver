
import { DIFFICULTY_LABELS, TILE_SCALE } from '../config.js';
import { clearBoard } from './dispose.js';

export function createBoardBuilder(state, view, { buildTiles, resetStage, setCamera, drawRadar }) {
  function buildBoard(data) {
    state.currentStageData = data;
    state.currentGrid = data.grid;

    // Căn vùng đổ bóng theo kích thước bàn cờ.
    const rows = data.grid.length, cols = data.grid[0].length;
    const centerX = (cols - 1) * TILE_SCALE / 2, centerZ = (rows - 1) * TILE_SCALE / 2;
    const light = view.keyLight;
    light.position.set(centerX - 22, 45, centerZ + 18);
    light.target.position.set(centerX, 0, centerZ);
    const extent = Math.hypot(cols, rows) * TILE_SCALE / 2 + 4;
    Object.assign(light.shadow.camera, { left: -extent, right: extent, top: extent, bottom: -extent, near: 0.5, far: 100 });
    light.shadow.camera.updateProjectionMatrix();

    clearBoard(view);

    state.stageBridges = data.bridges || {};
    state.bridgeStates = {};
    state.bridgeCellToId = {};
    view.bridgeMeshGroups = {};
    state.switchMap = {};
    view.switchMeshes = {};

    if (data.bridges) {
      for (const [bId, bInfo] of Object.entries(data.bridges)) {
        state.bridgeStates[bId] = (bInfo.initial_open === true);
        view.bridgeMeshGroups[bId] = [];
        if (Array.isArray(bInfo.cells)) {
          bInfo.cells.forEach(([br, bc]) => {
            state.bridgeCellToId[`${br},${bc}`] = bId;
          });
        }
      }
    }

    if (Array.isArray(data.switches)) {
      data.switches.forEach(sw => {
        if (sw.pos && sw.pos.length === 2) {
          const key = `${sw.pos[0]},${sw.pos[1]}`;
          state.switchMap[key] = {
            type: typeof sw.type === 'string' ? sw.type.toUpperCase() : sw.type,
            behavior: (sw.behavior || 'toggle').toLowerCase(),
            linked_bridges: sw.linked_bridges || [],
            split_targets: sw.split_targets || null
          };
        }
      });
    }

    buildTiles();

    const stageName = data.name || (state.loadedStages.find(s => s.id === state.currentStageFile)?.name) || state.currentStageFile;
    const stageDiff = String(data.difficulty || (state.loadedStages.find(s => s.id === state.currentStageFile)?.diff) || "medium").toLowerCase();
    document.getElementById('hud-stage-name').textContent = stageName;
    const diffEl = document.getElementById('hud-stage-diff');
    diffEl.textContent = DIFFICULTY_LABELS[stageDiff] || stageDiff;
    diffEl.className = `diff-badge diff-${stageDiff}`;

    resetStage();

    setCamera(state.currentCameraMode);
    drawRadar();
  }
  return { buildBoard };
}
