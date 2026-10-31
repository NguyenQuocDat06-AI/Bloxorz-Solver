import { TILE_SCALE, CAM_TOP_ZOOM_FACTOR, CAM_TOP_MIN_HEIGHT, CAM_TOP_SHIFT_X, CAM_ISO_DISTANCE_FACTOR, CAM_SIDE_DISTANCE_FACTOR } from '../config.js';

export function createCameraControls(state, view) {
  function setCamera(mode) {
    document.querySelectorAll('.cam-btn').forEach(b => b.classList.remove('active'));
    const activeBtn = document.getElementById(`btn-cam-${mode}`);
    if (activeBtn) activeBtn.classList.add('active');
    state.currentCameraMode = mode;

    const cols = state.currentGrid.length > 0 ? state.currentGrid[0].length : 10;
    const rows = state.currentGrid.length > 0 ? state.currentGrid.length : 10;
    const maxDim = Math.max(cols, rows);

    if (mode === 'iso') {
      view.camera.up.set(0, 1, 0);
      view.targetCamLook.set((cols / 2) * TILE_SCALE, 0, (rows / 2) * TILE_SCALE);
      const isoDist = Math.max(14, maxDim * CAM_ISO_DISTANCE_FACTOR);
      view.targetCamPos.set((cols / 2) * TILE_SCALE - isoDist * 0.7, isoDist * 1.1, (rows / 2) * TILE_SCALE + isoDist * 0.8);
    }
    else if (mode === 'side') {
      view.camera.up.set(0, 1, 0);
      view.targetCamLook.set((cols / 2) * TILE_SCALE, 0, (rows / 2) * TILE_SCALE);
      const sideDist = Math.max(16, maxDim * CAM_SIDE_DISTANCE_FACTOR);
      view.targetCamPos.set((cols / 2) * TILE_SCALE, 10, (rows / 2) * TILE_SCALE + sideDist);
    }
    else if (mode === 'top') {
      // Xoay 90 độ sang phải: Bàn cờ nằm ngang cực đẹp trên màn hình 16:9
      view.camera.up.set(0, 0, -1);
      view.targetCamLook.set((cols / 2) * TILE_SCALE + CAM_TOP_SHIFT_X, 0, (rows / 2) * TILE_SCALE);

      // Tự động phóng to thích ứng: Màn hẹp phóng to, màn dài tự động lùi ra
      const topHeight = Math.max(CAM_TOP_MIN_HEIGHT, maxDim * CAM_TOP_ZOOM_FACTOR);
      view.targetCamPos.set(view.targetCamLook.x + 0.01, topHeight, view.targetCamLook.z);
    }
  }
  return { setCamera };
}
