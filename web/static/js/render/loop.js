export function startRenderLoop(state, view) {
  let orbitAngle = 0;
  function renderLoop() {
    requestAnimationFrame(renderLoop);

    // Hoạt ảnh xoay & bay bổng cho tinh thể pha lê, vòng hào quang ô đích và vòng beacon chỉ báo khối active
    const nowTime = performance.now() * 0.001;
    view.boardGroup.children.forEach(child => {
      if (child.name === "floatingCrystal") {
        child.rotation.y += 0.03;
        child.rotation.x = Math.sin(nowTime * 2 + child.userData.phase) * 0.15;
        child.position.y = child.userData.baseY + Math.sin(nowTime * 3 + child.userData.phase) * 0.08;
      } else if (child.name === "goalHalo") {
        child.rotation.z += 0.02;
      }
    });

    // Vòng tròn hào quang torus activeMarker tự động xoay và nhấp nhô trên đầu khối con đang active
    if (view.activeMarker && view.activeMarker.visible && !state.isRolling) {
      view.activeMarker.rotation.z += 0.04;
      const curCube = state.activeCube === 1 ? view.cubeA : view.cubeB;
      view.activeMarker.position.x = curCube.position.x;
      view.activeMarker.position.z = curCube.position.z;
      view.activeMarker.position.y = curCube.position.y + 1.35 + Math.sin(nowTime * 5) * 0.12;
    }

    if (!state.inGameActive) {
      // Camera xoay nhẹ cinematic khi ở màn hình bắt đầu
      orbitAngle += 0.002;
      view.camera.position.x = 10 + Math.sin(orbitAngle) * 22;
      view.camera.position.z = 10 + Math.cos(orbitAngle) * 22;
      view.camera.position.y = 16;
      view.camera.lookAt(8, 0, 5);
    } else {
      view.camera.position.lerp(view.targetCamPos, 0.05);
      view.camera.lookAt(view.targetCamLook);
    }

    view.renderer.render(view.scene, view.camera);
  }
  renderLoop();
}
