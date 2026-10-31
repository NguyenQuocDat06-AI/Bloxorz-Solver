import { TILE_SCALE } from '../config.js';

export function bindKeyboard(state, view, game, stages, audio) {
  const { roll, resetStage, triggerSplit, syncBlockTransform } = game;
  const { closeStageModal } = stages;
  const { playAudio } = audio;
  window.addEventListener('keydown', (e) => {
    if (document.getElementById('stage-modal').classList.contains('active')) {
      if (e.key === 'Escape') closeStageModal();
      return;
    }
    if (!state.inGameActive) return;

    // Phím Space: Hỗ trợ cả kích hoạt Tách Khối (khi đang dẫm ô 6) và Chuyển đổi khối con (khi đã tách)
    if (e.code === 'Space' || e.key === ' ') {
      e.preventDefault();
      if (state.gameState !== "PLAYING" || state.isRolling) return;

      // Trường hợp 1: Đang ở trên ô tách khối (6) mà chưa tách -> Nhấn Space để tách ngay!
      if (state.blockOrient !== 3) {
        const occupied = [];
        if (state.blockOrient === 0) occupied.push([state.blockR, state.blockC]);
        else if (state.blockOrient === 1) { occupied.push([state.blockR, state.blockC]); occupied.push([state.blockR, state.blockC + 1]); }
        else if (state.blockOrient === 2) { occupied.push([state.blockR, state.blockC]); occupied.push([state.blockR + 1, state.blockC]); }

        let splitSwitchPos = null;
        for (const [r, c] of occupied) {
          const sw = state.switchMap[`${r},${c}`];
          if ((sw && (sw.type === 'SPLIT_SWITCH' || sw.type === 6)) || (state.currentGrid[r] && state.currentGrid[r][c] === 6)) {
            splitSwitchPos = [r, c];
            break;
          }
        }

        if (splitSwitchPos) {
          const [sr, sc] = splitSwitchPos;
          const sw = state.switchMap[`${sr},${sc}`];
          let targets = (sw && sw.split_targets && sw.split_targets.length === 2) ? sw.split_targets : null;
          if (!targets) {
            const rows = state.currentGrid.length, cols = state.currentGrid[0].length;
            targets = [[sr, Math.max(0, sc - 1)], [sr, Math.min(cols - 1, sc + 1)]];
          }
          triggerSplit(targets);
          return;
        }
      }

      // Trường hợp 2: Đang ở trạng thái phân tách (SPLIT) -> Nhấn Space chuyển đổi khối điều khiển
      if (state.blockOrient === 3) {
        state.activeCube = state.activeCube === 1 ? 2 : 1;
        playAudio('switch_cube');
        syncBlockTransform();

        // Hiệu ứng nảy nhẹ của khối vừa được kích hoạt
        const selCube = state.activeCube === 1 ? view.cubeA : view.cubeB;
        const u = TILE_SCALE, half = u * 0.5;
        const bounceStart = performance.now();
        function bounce(now) {
          const bp = Math.min((now - bounceStart) / 140, 1.0);
          selCube.position.y = half + Math.sin(bp * Math.PI) * 0.35;
          if (view.activeMarker.visible) {
            view.activeMarker.position.y = selCube.position.y + 1.35;
          }
          if (bp < 1.0) requestAnimationFrame(bounce);
          else {
            selCube.position.y = half;
            if (view.activeMarker.visible) view.activeMarker.position.y = half + 1.35;
          }
        }
        requestAnimationFrame(bounce);
      }
      return;
    }

    if (e.key === 'ArrowUp' || e.key === 'w' || e.key === 'W') roll('UP');
    else if (e.key === 'ArrowDown' || e.key === 's' || e.key === 'S') roll('DOWN');
    else if (e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') roll('LEFT');
    else if (e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') roll('RIGHT');
    else if (e.key === 'r' || e.key === 'R') resetStage();
  });
}
