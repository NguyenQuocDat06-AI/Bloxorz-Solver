
export function createBoardBuilder(state, view, { buildTiles, resetStage, setCamera, drawRadar }) {
  function buildBoard(data) {
    state.currentStageData = data;
    state.currentGrid = data.grid;

    // Xóa các mesh ô sàn cũ
    while (view.boardGroup.children.length > 0) {
      view.boardGroup.remove(view.boardGroup.children[0]);
    }

    // Khởi tạo và thiết lập lại bản đồ cầu nối và công tắc
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
            type: sw.type,
            behavior: sw.behavior || 'toggle',
            linked_bridges: sw.linked_bridges || [],
            split_targets: sw.split_targets || null
          };
        }
      });
    }

    buildTiles();

    // Cập nhật thông tin HUD động từ file stage JSON hoặc từ danh sách đã nạp
    const stageName = data.name || (state.loadedStages.find(s => s.id === state.currentStageFile)?.name) || state.currentStageFile;
    const stageDiff = String(data.difficulty || (state.loadedStages.find(s => s.id === state.currentStageFile)?.diff) || "medium").toLowerCase();
    document.getElementById('hud-stage-name').textContent = stageName;
    const diffEl = document.getElementById('hud-stage-diff');
    diffEl.textContent = stageDiff.toUpperCase();
    diffEl.className = `diff-badge diff-${stageDiff}`;

    // Đặt vị trí khối hộp ban đầu
    resetStage();

    // Tự động căn chỉnh camera và độ phóng to thích ứng theo kích thước stage mới
    setCamera(state.currentCameraMode);
    drawRadar();
  }
  return { buildBoard };
}
