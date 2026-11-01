import { TILE_SCALE } from '../config.js';
import { buildGoal } from './goal.js';

export function createTileRenderer(state, view) {
  const { THREE } = view;
  function buildTiles() {
    const rows = state.currentGrid.length;
    const cols = state.currentGrid[0].length;
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const type = state.currentGrid[r][c];
        if (type === 0) continue; // Khoảng trống / Vực thẳm
        const x = c * TILE_SCALE, z = r * TILE_SCALE;

        if (type === 1) {
          // Sàn thường.
          const tMesh = new THREE.Mesh(
            new THREE.BoxGeometry(TILE_SCALE * 0.96, 0.35, TILE_SCALE * 0.96),
            [view.sideMat, view.sideMat, view.tileMat, view.sideMat, view.sideMat, view.sideMat]
          );
          tMesh.position.set(x, -0.175, z);
          tMesh.receiveShadow = true;
          view.boardGroup.add(tMesh);
        }
        else if (type === 2) {
          // Ô yếu.
          const fragMesh = new THREE.Mesh(
            new THREE.BoxGeometry(TILE_SCALE * 0.96, 0.20, TILE_SCALE * 0.96),
            [view.fragileSideMat, view.fragileSideMat, view.fragileMat, view.fragileSideMat, view.fragileSideMat, view.fragileSideMat]
          );
          fragMesh.position.set(x, -0.10, z);
          fragMesh.receiveShadow = true;
          view.boardGroup.add(fragMesh);
        }
        else if (type === 3) {
          // Cầu.
          const bId = state.bridgeCellToId[`${r},${c}`];
          const brGroup = new THREE.Group();

          const brMesh = new THREE.Mesh(
            new THREE.BoxGeometry(TILE_SCALE * 0.94, 0.26, TILE_SCALE * 0.94),
            [view.bridgeSideMat, view.bridgeSideMat, view.bridgeMat, view.bridgeSideMat, view.bridgeSideMat, view.bridgeSideMat]
          );
          brMesh.position.set(0, 0, 0);
          brMesh.receiveShadow = true;
          brGroup.add(brMesh);

          const railGeo = new THREE.BoxGeometry(0.08, 0.16, TILE_SCALE * 0.94);
          const railMat = new THREE.MeshStandardMaterial({ color: 0x00f2fe, emissive: 0x00f2fe, emissiveIntensity: 0.8 });
          const railLeft = new THREE.Mesh(railGeo, railMat);
          railLeft.position.set(-(TILE_SCALE * 0.44), 0.17, 0);
          const railRight = new THREE.Mesh(railGeo, railMat);
          railRight.position.set((TILE_SCALE * 0.44), 0.17, 0);
          brGroup.add(railLeft);
          brGroup.add(railRight);

          const isOpen = bId ? (state.bridgeStates[bId] === true) : true;
          brGroup.userData = { baseY: -0.13, r: r, c: c, bridgeId: bId };
          brGroup.position.set(x, isOpen ? -0.13 : -15, z);
          brGroup.visible = isOpen;

          view.boardGroup.add(brGroup);
          if (bId) {
            if (!view.bridgeMeshGroups[bId]) view.bridgeMeshGroups[bId] = [];
            view.bridgeMeshGroups[bId].push(brGroup);
          }
        }
        else if (type === 4) {
          // Công tắc mềm.
          const baseMesh = new THREE.Mesh(
            new THREE.BoxGeometry(TILE_SCALE * 0.96, 0.35, TILE_SCALE * 0.96),
            [view.sideMat, view.sideMat, view.tileMat, view.sideMat, view.sideMat, view.sideMat]
          );
          baseMesh.position.set(x, -0.175, z);
          baseMesh.receiveShadow = true;
          view.boardGroup.add(baseMesh);

          const ringPlate = new THREE.Mesh(new THREE.CylinderGeometry(0.54, 0.58, 0.06, 24), view.metalDarkMat);
          ringPlate.position.set(x, 0.03, z);
          view.boardGroup.add(ringPlate);

          const swBtnGroup = new THREE.Group();
          swBtnGroup.position.set(x, 0, z);

          const swBtn = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.45, 0.14, 24), view.softSwitchMat);
          swBtn.position.set(0, 0.10, 0);
          swBtn.castShadow = true;
          swBtnGroup.add(swBtn);

          const swPip = new THREE.Mesh(new THREE.SphereGeometry(0.12, 16, 12), new THREE.MeshBasicMaterial({ color: 0xfffbeb }));
          swPip.position.set(0, 0.17, 0);
          swBtnGroup.add(swPip);

          view.boardGroup.add(swBtnGroup);
          view.switchMeshes[`${r},${c}`] = {
            type: 'SOFT_SWITCH',
            group: swBtnGroup,
            baseY: 0,
            pressedY: -0.07
          };
        }
        else if (type === 5) {
          // Công tắc nặng.
          const baseMesh = new THREE.Mesh(
            new THREE.BoxGeometry(TILE_SCALE * 0.96, 0.35, TILE_SCALE * 0.96),
            [view.sideMat, view.sideMat, view.tileMat, view.sideMat, view.sideMat, view.sideMat]
          );
          baseMesh.position.set(x, -0.175, z);
          baseMesh.receiveShadow = true;
          view.boardGroup.add(baseMesh);

          const sqPlate = new THREE.Mesh(new THREE.BoxGeometry(1.25, 0.05, 1.25), view.metalDarkMat);
          sqPlate.position.set(x, 0.025, z);
          view.boardGroup.add(sqPlate);

          const boltGeo = new THREE.CylinderGeometry(0.06, 0.06, 0.06, 8);
          const corners = [[-0.5, -0.5], [0.5, -0.5], [-0.5, 0.5], [0.5, 0.5]];
          corners.forEach(([cx, cz]) => {
            const bolt = new THREE.Mesh(boltGeo, view.boltMat);
            bolt.position.set(x + cx, 0.06, z + cz);
            view.boardGroup.add(bolt);
          });

          const heavyGroup = new THREE.Group();
          heavyGroup.position.set(x, 0, z);

          const beamGeo = new THREE.BoxGeometry(0.96, 0.15, 0.26);
          const beam1 = new THREE.Mesh(beamGeo, view.heavySwitchMat);
          beam1.position.set(0, 0.11, 0);
          beam1.rotation.y = Math.PI / 4;
          beam1.castShadow = true;

          const beam2 = new THREE.Mesh(beamGeo, view.heavySwitchMat);
          beam2.position.set(0, 0.11, 0);
          beam2.rotation.y = -Math.PI / 4;
          beam2.castShadow = true;

          heavyGroup.add(beam1);
          heavyGroup.add(beam2);
          view.boardGroup.add(heavyGroup);

          view.switchMeshes[`${r},${c}`] = {
            type: 'HEAVY_SWITCH',
            group: heavyGroup,
            baseY: 0,
            pressedY: -0.06
          };
        }
        else if (type === 6) {
          // Công tắc phân tách.
          const baseMesh = new THREE.Mesh(
            new THREE.BoxGeometry(TILE_SCALE * 0.96, 0.35, TILE_SCALE * 0.96),
            [view.sideMat, view.sideMat, view.tileMat, view.sideMat, view.sideMat, view.sideMat]
          );
          baseMesh.position.set(x, -0.175, z);
          baseMesh.receiveShadow = true;
          view.boardGroup.add(baseMesh);

          const ringRune = new THREE.Mesh(
            new THREE.RingGeometry(0.36, 0.58, 32),
            new THREE.MeshBasicMaterial({ color: 0xa855f7, side: THREE.DoubleSide })
          );
          ringRune.rotation.x = -Math.PI / 2;
          ringRune.position.set(x, 0.015, z);
          view.boardGroup.add(ringRune);

          const crystal = new THREE.Mesh(new THREE.OctahedronGeometry(0.38, 0), view.splitSwitchMat);
          crystal.name = "floatingCrystal";
          crystal.userData = { baseY: 0.55, phase: (r * 7 + c * 13) % 10 };
          crystal.position.set(x, 0.55, z);
          crystal.castShadow = true;
          view.boardGroup.add(crystal);
        }
        else if (type === 7) {
          // Ô dịch chuyển.
          const baseMesh = new THREE.Mesh(
            new THREE.BoxGeometry(TILE_SCALE * 0.96, 0.35, TILE_SCALE * 0.96),
            [view.sideMat, view.sideMat, view.tileMat, view.sideMat, view.sideMat, view.sideMat]
          );
          baseMesh.position.set(x, -0.175, z);
          view.boardGroup.add(baseMesh);

          const emeraldRune = new THREE.Mesh(
            new THREE.RingGeometry(0.35, 0.56, 32),
            new THREE.MeshBasicMaterial({ color: 0x10b981, side: THREE.DoubleSide })
          );
          emeraldRune.rotation.x = -Math.PI / 2;
          emeraldRune.position.set(x, 0.015, z);
          view.boardGroup.add(emeraldRune);

          const gem = new THREE.Mesh(
            new THREE.OctahedronGeometry(0.34, 0),
            new THREE.MeshStandardMaterial({ color: 0x10b981, emissive: 0x059669, emissiveIntensity: 0.8, roughness: 0.1 })
          );
          gem.name = "floatingCrystal";
          gem.userData = { baseY: 0.52, phase: (r * 3 + c * 5) % 10 };
          gem.position.set(x, 0.52, z);
          view.boardGroup.add(gem);
        }
        else if (type === 9) {
          buildGoal(view, x, z);
        }
      }
    }

  }
  return { buildTiles };
}
