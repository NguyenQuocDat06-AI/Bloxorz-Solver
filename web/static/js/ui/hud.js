
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
      const c1Fill = state.activeCube === 1 ? '#00f2fe' : '#c25e16';
      const c2Fill = state.activeCube === 2 ? '#00f2fe' : '#c25e16';
      container.innerHTML = `<svg width="18" height="18" viewBox="0 0 18 18"><rect x="1" y="5" width="7" height="8" rx="1.5" fill="${c1Fill}" stroke="#fbbf24" stroke-width="1.2"/><rect x="10" y="5" width="7" height="8" rx="1.5" fill="${c2Fill}" stroke="#fbbf24" stroke-width="1.2"/></svg>`;
    }
  }

  function updateBlockHud() {
    document.getElementById('ui-moves').textContent = state.moves;

    const orientNames = [
      "Đứng (1 × 1)",
      "Nằm ngang (2 × 1)",
      "Nằm dọc (1 × 2)",
      `Khối con ${state.activeCube} (Space để đổi)`
    ];
    document.getElementById('ui-orient').textContent = orientNames[state.blockOrient];

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
        curTileEl.textContent = "Khoảng trống";
        curTileEl.style.color = '#ef4444';
      } else if (curType === 1) {
        curTileEl.textContent = "Sàn thường";
        curTileEl.style.color = '#38bdf8';
      } else if (curType === 2) {
        curTileEl.textContent = "Ô yếu";
        curTileEl.style.color = '#f87171';
      } else if (curType === 3) {
        const bId = state.bridgeCellToId[`${curR},${curC}`];
        const isOpen = bId ? (state.bridgeStates[bId] === true) : true;
        curTileEl.textContent = isOpen ? "Cầu mở" : "Cầu đóng";
        curTileEl.style.color = isOpen ? '#38bdf8' : '#f87171';
      } else if (curType === 4) {
        curTileEl.textContent = "Công tắc mềm";
        curTileEl.style.color = '#facc15';
      } else if (curType === 5) {
        curTileEl.textContent = "Công tắc nặng";
        curTileEl.style.color = '#f43f5e';
      } else if (curType === 6) {
        curTileEl.textContent = "Công tắc phân tách";
        curTileEl.style.color = '#c084fc';
      } else if (curType === 7) {
        curTileEl.textContent = "Ô dịch chuyển";
        curTileEl.style.color = '#34d399';
      } else if (curType === 9) {
        curTileEl.textContent = "Ô đích";
        curTileEl.style.color = '#86dfc6';
      } else {
        curTileEl.textContent = 'Ô chưa xác định';
        curTileEl.style.color = '#94a3b8';
      }
    }

    updateOrientIcon(state.blockOrient);
    drawRadar();
  }
  return { updateBlockHud };
}
