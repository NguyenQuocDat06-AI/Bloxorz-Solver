import { TILE_SCALE } from '../config.js';

export function createVictoryEffect(state, view) {
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const viewport = document.getElementById('game-viewport');
  let frame = 0;
  let group = null;
  let geometry = null;
  let originalLight = null;

  function stop() {
    cancelAnimationFrame(frame);
    frame = 0;
    viewport.classList.remove('victory-glow');
    if (originalLight) {
      view.goalHaloMat.emissiveIntensity = originalLight.halo;
      view.goalFrameMat.emissiveIntensity = originalLight.border;
      originalLight = null;
    }
    if (group) {
      view.scene.remove(group);
      group.children.forEach(ring => ring.material.dispose());
      geometry.dispose();
      group = geometry = null;
    }
  }

  function play() {
    stop();
    if (motion.matches || document.hidden || state.gameState !== 'WON') return;
    const { THREE } = view;
    const runId = state.runId, stageFile = state.currentStageFile;
    originalLight = { halo: view.goalHaloMat.emissiveIntensity, border: view.goalFrameMat.emissiveIntensity };
    group = new THREE.Group();
    group.name = 'victory-rings';
    group.position.set(state.blockC * TILE_SCALE, 0.12, state.blockR * TILE_SCALE);
    geometry = new THREE.RingGeometry(0.60, 0.67, 48);
    [0xf8d58c, 0x86dfc6, 0xffedbd].forEach(color => {
      const material = new THREE.MeshBasicMaterial({
        color, transparent: true, opacity: 0, side: THREE.DoubleSide,
        depthWrite: false, blending: THREE.AdditiveBlending,
      });
      const ring = new THREE.Mesh(geometry, material);
      ring.rotation.x = -Math.PI / 2;
      group.add(ring);
    });
    view.scene.add(group);
    viewport.classList.add('victory-glow');
    const started = performance.now();

    function animate(now) {
      const elapsed = now - started;
      if (elapsed >= 1100 || motion.matches || state.runId !== runId
        || state.currentStageFile !== stageFile || state.gameState !== 'WON') return stop();
      const fade = Math.max(0, 1 - elapsed / 1100);
      view.goalHaloMat.emissiveIntensity = originalLight.halo + 2.2 * fade * fade;
      view.goalFrameMat.emissiveIntensity = originalLight.border + 0.8 * fade;
      group.children.forEach((ring, index) => {
        const progress = (elapsed - index * 130) / 800;
        ring.visible = progress >= 0 && progress < 1;
        if (!ring.visible) return;
        const eased = 1 - (1 - progress) ** 3;
        ring.scale.setScalar(1 + eased * 3.8);
        ring.position.y = index * 0.015;
        ring.material.opacity = 0.75 * (1 - progress) ** 2;
      });
      frame = requestAnimationFrame(animate);
    }
    frame = requestAnimationFrame(animate);
  }

  motion.addEventListener('change', event => { if (event.matches) stop(); });
  document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); });
  return { play, stop };
}
