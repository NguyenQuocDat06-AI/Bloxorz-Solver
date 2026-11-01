import { TILE_SCALE } from '../config.js';

export function bindKeyboard(state, view, game, stages, audio, completion) {
  const { roll, resetStage, syncBlockTransform } = game;
  const { closeStageModal } = stages;
  const { playAudio } = audio;
  window.addEventListener('keydown', (e) => {
    if (completion.handleKeydown(e)) return;
    if (document.getElementById('stage-modal').classList.contains('active')) {
      if (e.key === 'Escape') closeStageModal();
      return;
    }
    if (!state.inGameActive) return;
    if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key)) e.preventDefault();

    if (e.code === 'Space' || e.key === ' ') {
      e.preventDefault();
      if (state.gameState !== "PLAYING" || state.isRolling || state.blockOrient !== 3) return;

      if (state.blockOrient === 3) {
        state.activeCube = state.activeCube === 1 ? 2 : 1;
        playAudio('switch_cube');
        syncBlockTransform();

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
