import { TILE_SCALE } from '../config.js';

export function createBlockRenderer(state, view, { updateBlockHud }) {
  function syncBlockTransform() {
    const u = TILE_SCALE, half = u * 0.5;
    if (state.blockOrient === 0) {
      view.cubeA.position.set(0, half, 0); view.cubeB.position.set(0, half + u, 0);
      view.blockMaster.position.set(state.blockC * u, 0, state.blockR * u);
      view.activeMarker.visible = false;
      view.blockMatA.emissive.setHex(0x000000);
      view.blockMatB.emissive.setHex(0x000000);
    } else if (state.blockOrient === 1) {
      view.cubeA.position.set(-half, half, 0); view.cubeB.position.set(half, half, 0);
      view.blockMaster.position.set((state.blockC + 0.5) * u, 0, state.blockR * u);
      view.activeMarker.visible = false;
      view.blockMatA.emissive.setHex(0x000000);
      view.blockMatB.emissive.setHex(0x000000);
    } else if (state.blockOrient === 2) {
      view.cubeA.position.set(0, half, -half); view.cubeB.position.set(0, half, half);
      view.blockMaster.position.set(state.blockC * u, 0, (state.blockR + 0.5) * u);
      view.activeMarker.visible = false;
      view.blockMatA.emissive.setHex(0x000000);
      view.blockMatB.emissive.setHex(0x000000);
    } else if (state.blockOrient === 3) {
      view.blockMaster.position.set(0, 0, 0);
      view.cubeA.position.set(state.blockC * u, half, state.blockR * u);
      view.cubeB.position.set(state.blockC2 * u, half, state.blockR2 * u);
      view.activeMarker.visible = true;
      const targetPos = (state.activeCube === 1 ? view.cubeA.position : view.cubeB.position);
      view.activeMarker.position.set(targetPos.x, half + 1.35, targetPos.z);
      view.blockMatA.emissive.setHex(state.activeCube === 1 ? 0x00f2fe : 0x000000);
      view.blockMatA.emissiveIntensity = state.activeCube === 1 ? 0.45 : 0;
      view.blockMatB.emissive.setHex(state.activeCube === 2 ? 0x00f2fe : 0x000000);
      view.blockMatB.emissiveIntensity = state.activeCube === 2 ? 0.45 : 0;
    }
    view.blockMaster.rotation.set(0, 0, 0);
    updateBlockHud();
  }
  return { syncBlockTransform };
}
