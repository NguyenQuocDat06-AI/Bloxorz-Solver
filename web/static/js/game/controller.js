import { createBlockRenderer } from '../render/block.js';
import { createBridgeController } from './bridges.js';
import { createSplitAnimations } from './split.js';
import { createMovement } from './movement.js';
import { createStatusController } from './status.js';

export function createGameController(state, view, hud, radar, audio, { onWin = () => {}, onGoal = () => {}, onReset = () => {} } = {}) {
  const { playAudio } = audio;
  const { drawRadar } = radar;
  const { syncBlockTransform } = createBlockRenderer(state, view, hud);
  const { triggerSwitches } = createBridgeController(state, view, { playAudio, drawRadar });
  // Callback tránh phụ thuộc vòng giữa các controller.
  let status;
  const checkGameStatus = (...args) => status.checkGameStatus(...args);
  const { triggerSplit, triggerMerge } = createSplitAnimations(state, view, {
    playAudio, syncBlockTransform, checkGameStatus,
  });
  const { roll } = createMovement(state, view, {
    playAudio, syncBlockTransform, triggerMerge, checkGameStatus,
  });
  status = createStatusController(state, view, {
    playAudio, triggerSwitches, triggerSplit, resetStage, onWin, onGoal,
  });

  function resetStage() {
    if (!state.currentStageData) return;
    state.runId++;
    onReset();
    state.blockR = state.currentStageData.start[0];
    state.blockC = state.currentStageData.start[1];
    state.blockR2 = state.blockR;
    state.blockC2 = state.blockC;
    state.blockOrient = 0;
    state.activeCube = 1;
    state.moves = 0;
    state.gameState = "PLAYING";
    state.isRolling = false;
    view.cubeA.rotation.set(0, 0, 0);
    view.cubeB.rotation.set(0, 0, 0);
    document.getElementById('ui-status').className = 'status-badge status-playing';
    document.getElementById('ui-status').textContent = 'Đang chơi';
    ['bm-algo', 'bm-time', 'bm-mem', 'bm-nodes', 'bm-steps'].forEach(id => {
      document.getElementById(id).textContent = '---';
    });

    if (state.currentStageData.bridges) {
      for (const [bId, bInfo] of Object.entries(state.currentStageData.bridges)) {
        const initOpen = (bInfo.initial_open === true);
        state.bridgeStates[bId] = initOpen;
        const groups = view.bridgeMeshGroups[bId] || [];
        groups.forEach(grp => {
          grp.visible = initOpen;
          grp.position.y = initOpen ? (grp.userData.baseY || -0.13) : -15;
        });
      }
    }

    Object.values(view.switchMeshes).forEach(swObj => {
      if (swObj && swObj.group) {
        swObj.group.position.y = swObj.baseY;
      }
    });

    syncBlockTransform();
  }
  return { resetStage, roll, triggerSplit, syncBlockTransform };
}
