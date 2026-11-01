
export function createStatusController(state, view, { playAudio, triggerSwitches, triggerSplit, resetStage, onWin = () => {}, onGoal = () => {} }) {
  function checkGameStatus(justMovedCells = null, onComplete = null) {
    if (state.gameState !== 'PLAYING') return false;
    const runId = state.runId, stageFile = state.currentStageFile;
    const isCurrentRun = () => state.runId === runId && state.currentStageFile === stageFile;
    const occupied = [];
    if (state.blockOrient === 0) occupied.push([state.blockR, state.blockC]);
    else if (state.blockOrient === 1) { occupied.push([state.blockR, state.blockC]); occupied.push([state.blockR, state.blockC + 1]); }
    else if (state.blockOrient === 2) { occupied.push([state.blockR, state.blockC]); occupied.push([state.blockR + 1, state.blockC]); }
    else if (state.blockOrient === 3) { occupied.push([state.blockR, state.blockC]); occupied.push([state.blockR2, state.blockC2]); }

    // Thứ tự: công tắc, tách khối, kiểm tra ô đỡ.
    triggerSwitches(justMovedCells !== null ? justMovedCells : occupied, state.blockOrient);
    if (state.blockOrient === 0) {
      const sw = state.switchMap[`${state.blockR},${state.blockC}`];
      if (sw && (sw.type === 'SPLIT_SWITCH' || sw.type === 6)
        && sw.split_targets && sw.split_targets.length === 2) {
        triggerSplit(sw.split_targets, onComplete);
        return true;
      }
    }

    const rows = state.currentGrid.length, cols = state.currentGrid[0].length;
    let valid = !(state.blockOrient === 3
      && state.blockR === state.blockR2 && state.blockC === state.blockC2);
    let isFragileFall = false, isBridgeFall = false;

    for (const [r, c] of occupied) {
      if (r < 0 || r >= rows || c < 0 || c >= cols || state.currentGrid[r][c] === 0) {
        valid = false; break;
      }
      const bId = state.bridgeCellToId[`${r},${c}`];
      if (bId && !state.bridgeStates[bId]) {
        valid = false; isBridgeFall = true; break;
      }
      // Ô yếu chỉ đỡ khối nằm.
      if (state.blockOrient === 0 && state.currentGrid[r][c] === 2) {
        valid = false; isFragileFall = true; break;
      }
      if (state.blockOrient === 3 && state.currentGrid[r][c] === 2) {
        valid = false; isFragileFall = true; break;
      }
    }

    if (!valid) {
      state.gameState = "FELL";
      playAudio('fall');
      document.getElementById('ui-status').className = 'status-badge status-fell';
      document.getElementById('ui-status').textContent = isFragileFall ? 'Ô yếu bị vỡ' : (isBridgeFall ? 'Cầu đã đóng' : 'Rơi khỏi bàn');
      let fallY = 0;
      function drop() {
        if (!isCurrentRun()) return;
        fallY -= 0.6;
        if (state.blockOrient === 3) {
          view.cubeA.position.y -= 0.6;
          view.cubeB.position.y -= 0.6;
          view.activeMarker.position.y -= 0.6;
        } else {
          view.blockMaster.position.y = fallY;
        }
        if (fallY > -15) requestAnimationFrame(drop);
        else setTimeout(() => { if (isCurrentRun()) resetStage(); }, 600);
      }
      drop();
      return false;
    }

    if (state.blockOrient === 0 && state.currentGrid[state.blockR][state.blockC] === 9) {
      state.gameState = "WON";
      onGoal();
      playAudio('win');
      document.getElementById('ui-status').className = 'status-badge status-won';
      document.getElementById('ui-status').textContent = 'Hoàn thành';
      let fallY = 0;
      function dropGoal() {
        if (!isCurrentRun() || state.gameState !== 'WON') return;
        fallY -= 0.2; view.blockMaster.position.y = fallY;
        if (fallY > -4) requestAnimationFrame(dropGoal);
        else onWin();
      }
      dropGoal();
    }
    return false;
  }
  return { checkGameStatus };
}
