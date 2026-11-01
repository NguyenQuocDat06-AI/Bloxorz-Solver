export function startRenderLoop(state, view) {
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  function renderLoop() {
    requestAnimationFrame(renderLoop);
    if (!state.inGameActive) return;

    const nowTime = (window.__virtualTime !== undefined ? window.__virtualTime : performance.now()) * 0.001;
    view.boardGroup.children.forEach(child => {
      if (child.name === "floatingCrystal") {
        child.rotation.y += 0.03;
        child.rotation.x = Math.sin(nowTime * 2 + child.userData.phase) * 0.15;
        child.position.y = child.userData.baseY + Math.sin(nowTime * 3 + child.userData.phase) * 0.08;
      } else if (child.name === 'goalDepthLight') {
        const pulse = motion.matches ? 1 : 0.9 + Math.sin(nowTime * 1.6 + child.userData.phase) * 0.1;
        child.material.opacity = child.userData.opacity * pulse;
      }
    });

    if (view.activeMarker && view.activeMarker.visible && !state.isRolling) {
      view.activeMarker.rotation.y += 0.04;
      const curCube = state.activeCube === 1 ? view.cubeA : view.cubeB;
      view.activeMarker.position.x = curCube.position.x;
      view.activeMarker.position.z = curCube.position.z;
      view.activeMarker.position.y = curCube.position.y + 1.35 + Math.sin(nowTime * 5) * 0.12;
    }

    view.camera.position.lerp(view.targetCamPos, 0.05);
    view.camera.lookAt(view.targetCamLook);

    view.renderer.render(view.scene, view.camera);
  }
  renderLoop();
}
