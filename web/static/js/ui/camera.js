import { TILE_SCALE } from '../config.js';

export function createCameraControls(state, view) {
  function setCamera(mode) {
    document.querySelectorAll('.cam-btn').forEach(b => b.classList.remove('active'));
    const activeBtn = document.getElementById(`btn-cam-${mode}`);
    if (activeBtn) activeBtn.classList.add('active');
    state.currentCameraMode = mode;

    const cols = state.currentGrid.length > 0 ? state.currentGrid[0].length : 10;
    const rows = state.currentGrid.length > 0 ? state.currentGrid.length : 10;
    const { Vector3 } = view.THREE;
    const directions = {
      iso: new Vector3(-0.7, 1.1, 0.8),
      side: new Vector3(0, 0.45, 1),
      top: new Vector3(0, 1, 0.001),
    };
    const direction = (directions[mode] || directions.iso).normalize();
    view.camera.up.set(0, mode === 'top' ? 0 : 1, mode === 'top' ? -1 : 0);
    view.targetCamLook.set((cols - 1) * TILE_SCALE / 2, TILE_SCALE * 0.75, (rows - 1) * TILE_SCALE / 2);

    const right = new Vector3().crossVectors(view.camera.up, direction).normalize();
    const up = new Vector3().crossVectors(direction, right).normalize();
    const verticalTan = Math.tan(view.camera.fov * Math.PI / 360);
    const horizontalTan = verticalTan * view.camera.aspect;
    let distance = 12;

    // Chừa khung cho bàn cờ và khối đứng.
    state.currentGrid.forEach((row, r) => row.forEach((tile, c) => {
      if (tile === 0) return;
      for (const x of [(c - 0.5) * TILE_SCALE, (c + 0.5) * TILE_SCALE]) {
        for (const y of [-0.5, TILE_SCALE * 2.5]) {
          for (const z of [(r - 0.5) * TILE_SCALE, (r + 0.5) * TILE_SCALE]) {
            const offset = new Vector3(x, y, z).sub(view.targetCamLook);
            const depth = offset.dot(direction);
            distance = Math.max(distance,
              Math.abs(offset.dot(right)) / horizontalTan + depth,
              Math.abs(offset.dot(up)) / verticalTan + depth);
          }
        }
      }
    }));
    view.targetCamPos.copy(view.targetCamLook).addScaledVector(direction, distance * 1.12);
  }
  return { setCamera };
}
