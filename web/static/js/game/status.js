
export function createStatusController(state, view, { playAudio, triggerSwitches, triggerSplit, resetStage }) {
  function checkGameStatus(justMovedCells = null, onComplete = null) {
    const occupied = [];
    if (state.blockOrient === 0) occupied.push([state.blockR, state.blockC]);
    else if (state.blockOrient === 1) { occupied.push([state.blockR, state.blockC]); occupied.push([state.blockR, state.blockC + 1]); }
    else if (state.blockOrient === 2) { occupied.push([state.blockR, state.blockC]); occupied.push([state.blockR + 1, state.blockC]); }
    else if (state.blockOrient === 3) { occupied.push([state.blockR, state.blockC]); occupied.push([state.blockR2, state.blockC2]); }

    const rows = state.currentGrid.length, cols = state.currentGrid[0].length;
    let valid = true, isFragileFall = false, isBridgeFall = false;

    for (const [r, c] of occupied) {
      if (r < 0 || r >= rows || c < 0 || c >= cols || state.currentGrid[r][c] === 0) {
        valid = false; break;
      }
      // Kiểm tra cầu nối: nếu ô này thuộc cầu và cầu đang đóng thì rơi vực
      const bId = state.bridgeCellToId[`${r},${c}`];
      if (bId && !state.bridgeStates[bId]) {
        valid = false; isBridgeFall = true; break;
      }
      // Khối đứng 1x1x2 hoặc khối đơn 1x1x1 bước lên gạch vỡ => Sập gạch
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
      document.getElementById('ui-status').textContent = isFragileFall ? 'BROKEN TILE' : (isBridgeFall ? 'BRIDGE CLOSED' : 'FELL OFF');
      let fallY = 0;
      function drop() {
        fallY -= 0.6;
        if (state.blockOrient === 3) {
          view.cubeA.position.y -= 0.6;
          view.cubeB.position.y -= 0.6;
          view.activeMarker.position.y -= 0.6;
        } else {
          view.blockMaster.position.y = fallY;
        }
        if (fallY > -15) requestAnimationFrame(drop);
        else setTimeout(resetStage, 600);
      }
      drop();
      return false;
    }

    // Khối tiếp đất an toàn: Kích hoạt công tắc mềm (4) hoặc công tắc nặng (5)
    const cellsToCheckSwitches = (justMovedCells !== null) ? justMovedCells : occupied;
    triggerSwitches(cellsToCheckSwitches, state.blockOrient);

    // Kiểm tra lại nếu hành động kích hoạt công tắc làm sập cây cầu bên dưới chân khối
    let fellAfterSwitch = false;
    for (const [r, c] of occupied) {
      const bId = state.bridgeCellToId[`${r},${c}`];
      if (bId && !state.bridgeStates[bId]) {
        fellAfterSwitch = true; break;
      }
    }
    if (fellAfterSwitch) {
      state.gameState = "FELL";
      playAudio('fall');
      document.getElementById('ui-status').className = 'status-badge status-fell';
      document.getElementById('ui-status').textContent = 'BRIDGE COLLAPSED';
      let fallY = 0;
      function dropSwitch() {
        fallY -= 0.6;
        if (state.blockOrient === 3) {
          view.cubeA.position.y -= 0.6;
          view.cubeB.position.y -= 0.6;
          view.activeMarker.position.y -= 0.6;
        } else {
          view.blockMaster.position.y = fallY;
        }
        if (fallY > -15) requestAnimationFrame(dropSwitch);
        else setTimeout(resetStage, 600);
      }
      dropSwitch();
      return false;
    }

    // Kiểm tra ô tách khối (SPLIT SWITCH - Ô 6): Chỉ kích hoạt khi khối ĐỨNG THẲNG (1x1x2)
    if (state.blockOrient === 0) {
      const key = `${state.blockR},${state.blockC}`;
      const sw = state.switchMap[key];
      const isSplitSwitch = (sw && (sw.type === 'SPLIT_SWITCH' || sw.type === 6)) || (state.currentGrid[state.blockR][state.blockC] === 6);
      if (isSplitSwitch) {
        let targets = (sw && sw.split_targets && sw.split_targets.length === 2) ? sw.split_targets : null;
        if (!targets) {
          targets = [[state.blockR, Math.max(0, state.blockC - 1)], [state.blockR, Math.min(cols - 1, state.blockC + 1)]];
        }
        triggerSplit(targets, onComplete);
        return true;
      }
    }

    // Kiểm tra ô đích: Chỉ chiến thắng khi khối ĐỨNG THẲNG (1x1) trên ô số 9
    if (state.blockOrient === 0 && state.currentGrid[state.blockR][state.blockC] === 9) {
      state.gameState = "WON";
      playAudio('win');
      document.getElementById('ui-status').className = 'status-badge status-won';
      document.getElementById('ui-status').textContent = 'VICTORY!';
      let fallY = 0;
      function dropGoal() {
        fallY -= 0.2; view.blockMaster.position.y = fallY;
        if (fallY > -4) requestAnimationFrame(dropGoal);
      }
      dropGoal();
    }
    return false;
  }
  return { checkGameStatus };
}
