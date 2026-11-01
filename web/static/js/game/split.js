import { TILE_SCALE } from '../config.js';

export function createSplitAnimations(state, view, { playAudio, syncBlockTransform, checkGameStatus }) {
  const { THREE } = view;
  const getNow = () => (window.__virtualTime !== undefined ? window.__virtualTime : performance.now());
  function triggerSplit(targets, onComplete = null) {
    if (state.gameState !== "PLAYING" || state.isRolling || state.blockOrient !== 0) return;
    const runId = state.runId, stageFile = state.currentStageFile;
    const isCurrentRun = () => state.runId === runId && state.currentStageFile === stageFile;
    state.isRolling = true;
    state.gameState = "SPLITTING";
    playAudio('split');

    const u = TILE_SCALE, half = u * 0.5;
    const startPosA = new THREE.Vector3();
    const startPosB = new THREE.Vector3();
    view.cubeA.getWorldPosition(startPosA);
    view.cubeB.getWorldPosition(startPosB);

    const targetPosA = new THREE.Vector3(targets[0][1] * u, half, targets[0][0] * u);
    const targetPosB = new THREE.Vector3(targets[1][1] * u, half, targets[1][0] * u);

    view.blockMaster.position.set(0, 0, 0);
    view.blockMaster.rotation.set(0, 0, 0);
    view.cubeA.position.copy(startPosA);
    view.cubeB.position.copy(startPosB);

    const startTime = getNow();
    const dur = 480;

    function animSplit(now) {
      if (!isCurrentRun()) return;
      const p = Math.min((getNow() - startTime) / dur, 1.0);
      const ease = p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2;
      const arcY = Math.sin(p * Math.PI) * 3.2;

      view.cubeA.position.x = startPosA.x + (targetPosA.x - startPosA.x) * ease;
      view.cubeA.position.z = startPosA.z + (targetPosA.z - startPosA.z) * ease;
      view.cubeA.position.y = half + arcY;
      view.cubeA.rotation.y = ease * Math.PI * 2;

      view.cubeB.position.x = startPosB.x + (targetPosB.x - startPosB.x) * ease;
      view.cubeB.position.z = startPosB.z + (targetPosB.z - startPosB.z) * ease;
      view.cubeB.position.y = half + arcY;
      view.cubeB.rotation.y = -ease * Math.PI * 2;

      if (p < 1.0) {
        requestAnimationFrame(animSplit);
      } else {
        view.cubeA.position.copy(targetPosA);
        view.cubeB.position.copy(targetPosB);
        view.cubeA.rotation.set(0, 0, 0);
        view.cubeB.rotation.set(0, 0, 0);

        state.blockOrient = 3;
        state.blockR = targets[0][0]; state.blockC = targets[0][1];
        state.blockR2 = targets[1][0]; state.blockC2 = targets[1][1];
        state.activeCube = 1;
        state.gameState = "PLAYING";
        state.isRolling = false;

        syncBlockTransform();
        // Dịch chuyển không kích hoạt công tắc ở ô đến.
        checkGameStatus([]);
        if (onComplete) {
          setTimeout(() => { if (isCurrentRun()) onComplete(); }, 120);
        }
      }
    }
    requestAnimationFrame(animSplit);
  }

  function triggerMerge(merged, onComplete = null) {
    const runId = state.runId, stageFile = state.currentStageFile;
    const isCurrentRun = () => state.runId === runId && state.currentStageFile === stageFile;
    state.isRolling = true;
    state.gameState = "MERGING";
    playAudio('merge');
    view.activeMarker.visible = false;

    const u = TILE_SCALE, half = u * 0.5;
    const startPosA = view.cubeA.position.clone();
    const startPosB = view.cubeB.position.clone();

    const destWorldA = new THREE.Vector3();
    const destWorldB = new THREE.Vector3();

    if (merged.orient === 1) { // HORIZONTAL (2x1)
      destWorldA.set(merged.c * u, half, merged.r * u);
      destWorldB.set((merged.c + 1) * u, half, merged.r * u);
    } else { // VERTICAL (1x2)
      destWorldA.set(merged.c * u, half, merged.r * u);
      destWorldB.set(merged.c * u, half, (merged.r + 1) * u);
    }

    const startTime = getNow();
    const dur = 220;

    function animMerge(now) {
      if (!isCurrentRun()) return;
      const p = Math.min((getNow() - startTime) / dur, 1.0);
      const ease = Math.pow(p, 2.5);
      const jumpY = Math.sin(p * Math.PI) * 0.45;

      view.cubeA.position.lerpVectors(startPosA, destWorldA, ease);
      view.cubeB.position.lerpVectors(startPosB, destWorldB, ease);
      view.cubeA.position.y = half + jumpY;
      view.cubeB.position.y = half + jumpY;

      if (p < 1.0) {
        requestAnimationFrame(animMerge);
      } else {
        view.cubeA.position.copy(destWorldA);
        view.cubeB.position.copy(destWorldB);
        view.cubeA.position.y = half;
        view.cubeB.position.y = half;

        state.blockOrient = merged.orient;
        state.blockR = merged.r;
        state.blockC = merged.c;
        state.blockR2 = state.blockR;
        state.blockC2 = state.blockC;
        state.activeCube = 1;

        syncBlockTransform();
        state.gameState = "PLAYING";
        state.isRolling = false;
        // Sau khi ghép, xét công tắc trên toàn dấu chân.
        checkGameStatus();
        if (onComplete) onComplete();
      }
    }
    requestAnimationFrame(animMerge);
  }
  return { triggerSplit, triggerMerge };
}
