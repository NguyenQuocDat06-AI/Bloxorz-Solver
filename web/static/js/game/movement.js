import { TILE_SCALE, ROLL_DURATION } from '../config.js';
import { tryMergeCubes } from './geometry.js';

export function createMovement(state, view, { playAudio, syncBlockTransform, triggerMerge, checkGameStatus }) {
  const { THREE } = view;
  function roll(dir, onComplete = null) {
    if (state.isRolling || state.gameState !== "PLAYING") return;
    const runId = state.runId, stageFile = state.currentStageFile;
    const isCurrentRun = () => state.runId === runId && state.currentStageFile === stageFile;
    state.isRolling = true; playAudio('roll');

    const u = TILE_SCALE, half = u * 0.5;

    if (state.blockOrient === 3) {
      let dr = 0, dc = 0;
      if (dir === 'UP') dr = -1;
      else if (dir === 'DOWN') dr = 1;
      else if (dir === 'LEFT') dc = -1;
      else if (dir === 'RIGHT') dc = 1;

      const curTargetCube = state.activeCube === 1 ? view.cubeA : view.cubeB;
      const curR = state.activeCube === 1 ? state.blockR : state.blockR2;
      const curC = state.activeCube === 1 ? state.blockC : state.blockC2;
      const newR = curR + dr;
      const newC = curC + dc;

      const curX = curTargetCube.position.x, curZ = curTargetCube.position.z;
      let pivot = new THREE.Vector3(), rotAxis = new THREE.Vector3();
      if (dir === 'UP') { rotAxis.set(-1, 0, 0); pivot.set(curX, 0, curZ - half); }
      else if (dir === 'DOWN') { rotAxis.set(1, 0, 0); pivot.set(curX, 0, curZ + half); }
      else if (dir === 'LEFT') { rotAxis.set(0, 0, 1); pivot.set(curX - half, 0, curZ); }
      else if (dir === 'RIGHT') { rotAxis.set(0, 0, -1); pivot.set(curX + half, 0, curZ); }

      const startPos = curTargetCube.position.clone();
      const relPos = new THREE.Vector3().subVectors(startPos, pivot);
      const getTime = () => (window.__virtualTime !== undefined ? window.__virtualTime : performance.now());
      const startTime = getTime();

      function animateSingle(t) {
        if (!isCurrentRun()) return;
        const curT = window.__virtualTime !== undefined ? window.__virtualTime : (t || performance.now());
        const progress = Math.min((curT - startTime) / ROLL_DURATION, 1.0);
        const ease = 0.5 - Math.cos(progress * Math.PI) * 0.5;
        const angle = ease * (Math.PI / 2);

        const q = new THREE.Quaternion().setFromAxisAngle(rotAxis, angle);
        curTargetCube.position.copy(relPos.clone().applyQuaternion(q).add(pivot));
        curTargetCube.quaternion.copy(q);

        if (view.activeMarker.visible) {
          view.activeMarker.position.x = curTargetCube.position.x;
          view.activeMarker.position.z = curTargetCube.position.z;
          view.activeMarker.position.y = curTargetCube.position.y + 1.35;
        }

        if (progress < 1.0) {
          requestAnimationFrame(animateSingle);
        } else {
          curTargetCube.quaternion.identity();
          curTargetCube.position.set(newC * u, half, newR * u);

          if (state.activeCube === 1) {
            state.blockR = newR; state.blockC = newC;
          } else {
            state.blockR2 = newR; state.blockC2 = newC;
          }
          state.moves++;

          const merged = tryMergeCubes(state.blockR, state.blockC, state.blockR2, state.blockC2);
          if (merged) {
            triggerMerge(merged, onComplete);
          } else {
            syncBlockTransform();
            state.isRolling = false;
            checkGameStatus([[newR, newC]]);
            if (onComplete) onComplete();
          }
        }
      }
      requestAnimationFrame(animateSingle);
      return;
    }

    const oldR = state.blockR, oldC = state.blockC, oldO = state.blockOrient;
    let newR = oldR, newC = oldC, newO = oldO;
    if (oldO === 0) {
      if (dir === 'UP') { newR = oldR - 2; newO = 2; }
      else if (dir === 'DOWN') { newR = oldR + 1; newO = 2; }
      else if (dir === 'LEFT') { newC = oldC - 2; newO = 1; }
      else if (dir === 'RIGHT') { newC = oldC + 1; newO = 1; }
    } else if (oldO === 1) {
      if (dir === 'UP') { newR = oldR - 1; newO = 1; }
      else if (dir === 'DOWN') { newR = oldR + 1; newO = 1; }
      else if (dir === 'LEFT') { newC = oldC - 1; newO = 0; }
      else if (dir === 'RIGHT') { newC = oldC + 2; newO = 0; }
    } else if (oldO === 2) {
      if (dir === 'UP') { newR = oldR - 1; newO = 0; }
      else if (dir === 'DOWN') { newR = oldR + 2; newO = 0; }
      else if (dir === 'LEFT') { newC = oldC - 1; newO = 2; }
      else if (dir === 'RIGHT') { newC = oldC + 1; newO = 2; }
    }

    const curX = view.blockMaster.position.x, curZ = view.blockMaster.position.z;
    let pivot = new THREE.Vector3(), rotAxis = new THREE.Vector3();
    if (dir === 'UP') { rotAxis.set(-1, 0, 0); pivot.set(curX, 0, (oldO === 2) ? curZ - u : curZ - half); }
    else if (dir === 'DOWN') { rotAxis.set(1, 0, 0); pivot.set(curX, 0, (oldO === 2) ? curZ + u : curZ + half); }
    else if (dir === 'LEFT') { rotAxis.set(0, 0, 1); pivot.set((oldO === 1) ? curX - u : curX - half, 0, curZ); }
    else if (dir === 'RIGHT') { rotAxis.set(0, 0, -1); pivot.set((oldO === 1) ? curX + u : curX + half, 0, curZ); }

    const startPos = view.blockMaster.position.clone();
    const relPos = new THREE.Vector3().subVectors(startPos, pivot);
    const getTime = () => (window.__virtualTime !== undefined ? window.__virtualTime : performance.now());
    const startTime = getTime();

    function animateRoll(t) {
      if (!isCurrentRun()) return;
      const curT = window.__virtualTime !== undefined ? window.__virtualTime : (t || performance.now());
      const progress = Math.min((curT - startTime) / ROLL_DURATION, 1.0);
      const ease = 0.5 - Math.cos(progress * Math.PI) * 0.5;
      const angle = ease * (Math.PI / 2);

      const q = new THREE.Quaternion().setFromAxisAngle(rotAxis, angle);
      view.blockMaster.position.copy(relPos.clone().applyQuaternion(q).add(pivot));
      view.blockMaster.quaternion.copy(q);

      if (progress < 1.0) {
        requestAnimationFrame(animateRoll);
      } else {
        state.blockR = newR; state.blockC = newC; state.blockOrient = newO; state.moves++;
        view.blockMaster.quaternion.identity();
        syncBlockTransform();
        state.isRolling = false;
        const wasSplit = checkGameStatus(null, onComplete);
        if (!wasSplit && onComplete) onComplete();
      }
    }
    requestAnimationFrame(animateRoll);
  }
  return { roll };
}
