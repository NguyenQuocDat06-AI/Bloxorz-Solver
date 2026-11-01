export function createTextures(THREE, anisotropy = 1) {
  function canvasTexture(canvas) {
    const texture = new THREE.CanvasTexture(canvas);
    texture.anisotropy = anisotropy;
    return texture;
  }

  function makeTileTexture() {
    const c = document.createElement('canvas'); c.width = 512; c.height = 512;
    const ctx = c.getContext('2d');
    const grad = ctx.createLinearGradient(0, 0, 512, 512);
    grad.addColorStop(0, '#2c3e55');
    grad.addColorStop(1, '#1a2636');
    ctx.fillStyle = grad; ctx.fillRect(0, 0, 512, 512);
    // Viền thẳng tránh quầng sáng trên mặt ô.
    ctx.strokeStyle = 'rgba(148, 191, 214, 0.15)';
    ctx.lineWidth = 2;
    ctx.strokeRect(12, 12, 488, 488);
    ctx.strokeStyle = 'rgba(56, 189, 248, 0.7)';
    ctx.lineWidth = 6;
    ctx.strokeRect(6, 6, 500, 500);
    return canvasTexture(c);
  }

  function makeFragileTexture() {
    const c = document.createElement('canvas'); c.width = 512; c.height = 512;
    const ctx = c.getContext('2d');
    const grad = ctx.createLinearGradient(0, 0, 512, 512);
    grad.addColorStop(0, '#ea580c');
    grad.addColorStop(0.4, '#f97316');
    grad.addColorStop(1, '#c2410c');
    ctx.fillStyle = grad; ctx.fillRect(0, 0, 512, 512);

    const innerFragile = ctx.createRadialGradient(256, 256, 100, 256, 256, 254);
    innerFragile.addColorStop(0, 'rgba(255, 237, 213, 0.12)');
    innerFragile.addColorStop(1, 'rgba(67, 20, 7, 0.4)');
    ctx.fillStyle = innerFragile;
    ctx.fillRect(10, 10, 492, 492);

    const cracks = [
      [[50, 40], [130, 130], [220, 170], [340, 180], [470, 170]],
      [[220, 170], [250, 270], [290, 360], [320, 470]],
      [[130, 130], [110, 250], [80, 350], [40, 450]],
      [[340, 180], [400, 270], [470, 350]],
      [[250, 270], [190, 340], [190, 460]],
      [[220, 170], [160, 210], [140, 260]]
    ];

    ctx.lineWidth = 6;
    ctx.strokeStyle = '#270800';
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    cracks.forEach(pts => {
      ctx.beginPath();
      ctx.moveTo(pts[0][0], pts[0][1]);
      for (let k = 1; k < pts.length; k++) ctx.lineTo(pts[k][0], pts[k][1]);
      ctx.stroke();
    });

    ctx.lineWidth = 2;
    ctx.strokeStyle = '#ffedd5';
    cracks.forEach(pts => {
      ctx.beginPath();
      ctx.moveTo(pts[0][0], pts[0][1]);
      for (let k = 1; k < pts.length; k++) ctx.lineTo(pts[k][0], pts[k][1]);
      ctx.stroke();
    });

    ctx.strokeStyle = 'rgba(194, 65, 12, 0.95)';
    ctx.lineWidth = 8;
    ctx.strokeRect(6, 6, 500, 500);

    return canvasTexture(c);
  }

  function makeBridgeTexture() {
    const c = document.createElement('canvas'); c.width = 512; c.height = 512;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(0, 0, 512, 512);

    for (let y = 18; y < 500; y += 34) {
      const slatGrad = ctx.createLinearGradient(0, y, 0, y + 24);
      slatGrad.addColorStop(0, '#334155');
      slatGrad.addColorStop(0.5, '#64748b');
      slatGrad.addColorStop(1, '#1e293b');
      ctx.fillStyle = slatGrad;
      ctx.fillRect(24, y, 464, 24);

      ctx.fillStyle = '#cbd5e1';
      ctx.beginPath(); ctx.arc(36, y + 12, 3.5, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.arc(476, y + 12, 3.5, 0, Math.PI * 2); ctx.fill();
    }

    ctx.fillStyle = '#00f2fe';
    ctx.fillRect(10, 10, 8, 492);
    ctx.fillRect(494, 10, 8, 492);

    ctx.strokeStyle = 'rgba(0, 242, 254, 0.7)';
    ctx.lineWidth = 6;
    ctx.strokeRect(4, 4, 504, 504);
    return canvasTexture(c);
  }

  function makeBlockTexture() {
    const c = document.createElement('canvas'); c.width = 512; c.height = 512;
    const ctx = c.getContext('2d');
    const grad = ctx.createLinearGradient(0, 0, 0, 512);
    grad.addColorStop(0, '#c25e16');
    grad.addColorStop(1, '#78350f');
    ctx.fillStyle = grad; ctx.fillRect(0, 0, 512, 512);
    for (let y = 0; y < 512; y += 3) {
      ctx.fillStyle = `rgba(255, 237, 213, ${0.06 + Math.sin(y * 0.22) * 0.05})`;
      ctx.fillRect(0, y, 512, 2);
    }
    ctx.strokeStyle = 'rgba(251, 191, 36, 0.85)';
    ctx.lineWidth = 8;
    ctx.strokeRect(6, 6, 500, 500);
    return canvasTexture(c);
  }
  return { makeTileTexture, makeFragileTexture, makeBridgeTexture, makeBlockTexture };
}
