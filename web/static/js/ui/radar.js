
export function createRadar(state) {
  function drawRadar() {
    const radarCanvas = document.getElementById('radar-canvas');
    if (!radarCanvas || !state.currentGrid || state.currentGrid.length === 0) return;
    const ctx = radarCanvas.getContext('2d');
    const rows = state.currentGrid.length;
    const cols = state.currentGrid[0].length;

    const width = radarCanvas.width;
    const height = radarCanvas.height;
    ctx.clearRect(0, 0, width, height);

    const pad = 10;
    const cellW = (width - pad * 2) / cols;
    const cellH = (height - pad * 2) / rows;
    const cellSize = Math.min(cellW, cellH, 15);
    const startX = (width - cols * cellSize) / 2;
    const startY = (height - rows * cellSize) / 2;

    const dimEl = document.getElementById('radar-dim');
    if (dimEl) dimEl.textContent = `${cols}×${rows}`;

    const tileColors = {
      0: 'transparent',
      1: '#1e293b',
      2: '#9a3412',
      3: '#0284c7',
      4: '#ca8a04',
      5: '#be123c',
      6: '#7e22ce',
      7: '#059669',
      9: '#b45309'
    };

    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const type = state.currentGrid[r][c];
        if (type === 0) continue;
        const cx = startX + c * cellSize;
        const cy = startY + r * cellSize;

        let cellFill = tileColors[type] || '#334155';
        let cellStroke = 'rgba(255, 255, 255, 0.12)';
        if (type === 3) {
          const bId = state.bridgeCellToId[`${r},${c}`];
          const isOpen = bId ? (state.bridgeStates[bId] === true) : true;
          if (isOpen) {
            cellFill = '#0284c7';
            cellStroke = '#38bdf8';
          } else {
            cellFill = '#08111d';
            cellStroke = 'rgba(56, 189, 248, 0.28)';
          }
        }

        ctx.fillStyle = cellFill;
        ctx.strokeStyle = cellStroke;
        ctx.lineWidth = 1;
        ctx.beginPath();
        if (ctx.roundRect) ctx.roundRect(cx + 1, cy + 1, cellSize - 2, cellSize - 2, 2);
        else ctx.rect(cx + 1, cy + 1, cellSize - 2, cellSize - 2);
        ctx.fill();
        ctx.stroke();

        if (type === 9) {
          ctx.fillStyle = '#fde047';
          ctx.beginPath();
          ctx.arc(cx + cellSize / 2, cy + cellSize / 2, cellSize * 0.28, 0, Math.PI * 2);
          ctx.fill();
        } else if (type === 4) {
          ctx.fillStyle = '#fef08a';
          ctx.beginPath();
          ctx.arc(cx + cellSize / 2, cy + cellSize / 2, cellSize * 0.22, 0, Math.PI * 2);
          ctx.fill();
        } else if (type === 5) {
          ctx.strokeStyle = '#fda4af';
          ctx.lineWidth = 1.5;
          ctx.beginPath();
          ctx.moveTo(cx + 3, cy + 3); ctx.lineTo(cx + cellSize - 3, cy + cellSize - 3);
          ctx.moveTo(cx + cellSize - 3, cy + 3); ctx.lineTo(cx + 3, cy + cellSize - 3);
          ctx.stroke();
        }
      }
    }

    // Vẽ vị trí khối hộp Bloxorz phát sáng trên Radar (Hỗ trợ cả chế độ phân tách SPLIT)
    if (state.currentGrid && state.gameState === "PLAYING") {
      ctx.fillStyle = '#00f2fe';
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 1.5;
      ctx.shadowColor = '#00f2fe';
      ctx.shadowBlur = 8;

      if (state.blockOrient === 0) {
        const bx = startX + state.blockC * cellSize;
        const by = startY + state.blockR * cellSize;
        ctx.fillRect(bx + 1, by + 1, cellSize - 2, cellSize - 2);
        ctx.strokeRect(bx + 1, by + 1, cellSize - 2, cellSize - 2);
      } else if (state.blockOrient === 1) {
        const bx = startX + state.blockC * cellSize;
        const by = startY + state.blockR * cellSize;
        ctx.fillRect(bx + 1, by + 1, cellSize * 2 - 2, cellSize - 2);
        ctx.strokeRect(bx + 1, by + 1, cellSize * 2 - 2, cellSize - 2);
      } else if (state.blockOrient === 2) {
        const bx = startX + state.blockC * cellSize;
        const by = startY + state.blockR * cellSize;
        ctx.fillRect(bx + 1, by + 1, cellSize - 2, cellSize * 2 - 2);
        ctx.strokeRect(bx + 1, by + 1, cellSize - 2, cellSize * 2 - 2);
      } else if (state.blockOrient === 3) {
        // Khối con 1
        const bx1 = startX + state.blockC * cellSize;
        const by1 = startY + state.blockR * cellSize;
        ctx.fillStyle = state.activeCube === 1 ? '#00f2fe' : '#0284c7';
        ctx.strokeStyle = state.activeCube === 1 ? '#ffffff' : 'rgba(255, 255, 255, 0.4)';
        ctx.lineWidth = state.activeCube === 1 ? 2 : 1;
        ctx.shadowBlur = state.activeCube === 1 ? 10 : 2;
        ctx.fillRect(bx1 + 1, by1 + 1, cellSize - 2, cellSize - 2);
        ctx.strokeRect(bx1 + 1, by1 + 1, cellSize - 2, cellSize - 2);

        // Khối con 2
        const bx2 = startX + state.blockC2 * cellSize;
        const by2 = startY + state.blockR2 * cellSize;
        ctx.fillStyle = state.activeCube === 2 ? '#00f2fe' : '#0284c7';
        ctx.strokeStyle = state.activeCube === 2 ? '#ffffff' : 'rgba(255, 255, 255, 0.4)';
        ctx.lineWidth = state.activeCube === 2 ? 2 : 1;
        ctx.shadowBlur = state.activeCube === 2 ? 10 : 2;
        ctx.fillRect(bx2 + 1, by2 + 1, cellSize - 2, cellSize - 2);
        ctx.strokeRect(bx2 + 1, by2 + 1, cellSize - 2, cellSize - 2);
      }
      ctx.shadowBlur = 0;
    }
  }
  return { drawRadar };
}
