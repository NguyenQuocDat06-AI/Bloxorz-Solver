export function bindViewport(state, view, camera) {
  const viewport = document.getElementById('game-viewport');

  function resize() {
    const width = viewport.clientWidth;
    const height = viewport.clientHeight;
    if (!width || !height) return;

    view.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    view.renderer.setSize(width, height, false);
    view.camera.aspect = width / height;
    view.camera.updateProjectionMatrix();
    camera.setCamera(state.currentCameraMode);
    view.camera.position.copy(view.targetCamPos);
    view.camera.lookAt(view.targetCamLook);
  }

  const observer = new ResizeObserver(resize);
  observer.observe(viewport);
  window.addEventListener('resize', resize);
}
