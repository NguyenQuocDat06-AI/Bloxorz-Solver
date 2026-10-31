
export function createHud(state, { drawRadar }) {
  function updateOrientIcon(orient) {
    const container = document.getElementById('orient-icon');
    if (!container) return;
    if (orient === 0) {
      container.innerHTML = `<svg width="18" height="18" viewBox="0 0 18 18"><rect x="4" y="2" width="10" height="14" rx="2" fill="#c25e16" stroke="#fbbf24" stroke-width="1.2"/></svg>`;
    } else if (orient === 1) {
      container.innerHTML = `<svg width="18" height="18" viewBox="0 0 18 18"><rect x="1" y="5" width="16" height="8" rx="2" fill="#c25e16" stroke="#fbbf24" stroke-width="1.2"/><line x1="9" y1="5" x2="9" y2="13" stroke="#fbbf24" stroke-width="1"/></svg>`;
    } else if (orient === 2) {
      container.innerHTML = `<svg width="18" height="18" viewBox="0 0 18 18"><rect x="5" y="1" width="8" height="16" rx="2" fill="#c25e16" stroke="#fbbf24" stroke-width="1.2"/><line x1="5" y1="9" x2="13" y2="9" stroke="#fbbf24" stroke-width="1"/></svg>`;
    } else if (orient === 3) {
      // Tách khối (Split): 2 ô vuông con riêng rẽ, khối active có màu cyan
      const c1Fill = state.activeCube === 1 ? '#00f2fe' : '#c25e16';
      const c2Fill = state.activeCube === 2 ? '#00f2fe' : '#c25e16';
      container.innerHTML = `<svg width="18" height="18" viewBox="0 0 18 18"><rect x="1" y="5" width="7" height="8" rx="1.5" fill="${c1Fill}" stroke="#fbbf24" stroke-width="1.2"/><rect x="10" y="5" width="7" height="8" rx="1.5" fill="${c2Fill}" stroke="#fbbf24" stroke-width="1.2"/></svg>`;
    }
  }

  function updateBlockHud() {
    document.getElementById('ui-moves').textContent = state.moves;

    const orientNames = [
      "Standing (1 × 1)",
      "Lying Horizontal (2 × 1)",
      "Lying Vertical (1 × 2)",
      `Split Cubes (Đang chọn Khối ${state.activeCube} • Nhấn Space đổi)`
    ];
    document.getElementById('ui-orient').textContent = orientNames[state.blockOrient];

    // Cập nhật ô đang đứng với trạng thái chi tiết của công tắc và cầu
    let curR = state.blockR, curC = state.blockC;
    if (state.blockOrient === 3 && state.activeCube === 2) {
      curR = state.blockR2; curC = state.blockC2;
    }
    let curType = 1;
    if (state.currentGrid && state.currentGrid[curR] && state.currentGrid[curR][curC] !== undefined) {
      curType = state.currentGrid[curR][curC];
    }
    const curTileEl = document.getElementById('ui-current-tile');
    if (curTileEl) {
      if (curType === 0) {
        curTileEl.textContent = "Khoảng Trống [0] ⚠️";
        curTileEl.style.color = '#ef4444';
      } else if (curType === 1) {
        curTileEl.textContent = "Sàn Chuẩn [1]";
        curTileEl.style.color = '#38bdf8';
      } else if (curType === 2) {
        curTileEl.textContent = "Gạch Vỡ (Nguy Hiểm) [2] ⚠️";
        curTileEl.style.color = '#f87171';
      } else if (curType === 3) {
        const bId = state.bridgeCellToId[`${curR},${curC}`];
        const isOpen = bId ? (state.bridgeStates[bId] === true) : true;
        curTileEl.textContent = isOpen ? "Cầu Nối Nan Thép [3] (Đang Mở)" : "Cầu Đang Đóng [3] ⚠️";
        curTileEl.style.color = isOpen ? '#38bdf8' : '#f87171';
      } else if (curType === 4) {
        curTileEl.textContent = "Công Tắc Mềm [4] (Mọi tư thế)";
        curTileEl.style.color = '#facc15';
      } else if (curType === 5) {
        curTileEl.textContent = "Công Tắc Nặng [5] (Chỉ kích hoạt khi ĐỨNG 1×1)";
        curTileEl.style.color = '#f43f5e';
      } else if (curType === 6) {
        curTileEl.textContent = "Công Tắc Tách Khối [6] 🔮";
        curTileEl.style.color = '#c084fc';
      } else if (curType === 7) {
        curTileEl.textContent = "Ô Dịch Chuyển [7]";
        curTileEl.style.color = '#34d399';
      } else if (curType === 9) {
        curTileEl.textContent = "Ô Đích [9] 🎯";
        curTileEl.style.color = '#fbbf24';
      } else {
        curTileEl.textContent = `Ô [${curType}]`;
        curTileEl.style.color = '#94a3b8';
      }
    }

    updateOrientIcon(state.blockOrient);
    drawRadar();
  }
  return { updateBlockHud };
}
