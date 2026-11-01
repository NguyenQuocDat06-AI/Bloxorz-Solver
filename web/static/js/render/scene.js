import { TILE_SCALE, CAM_FOV } from '../config.js';
import { createTextures } from './textures.js';

export function createScene(THREE) {
  const canvas = document.getElementById('webgl-canvas');
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
  renderer.setSize(1, 1, false);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  const anisotropy = Math.min(8, renderer.capabilities.getMaxAnisotropy());
  const { makeTileTexture, makeFragileTexture, makeBridgeTexture, makeBlockTexture } = createTextures(THREE, anisotropy);

  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.0;

  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x060913, 0.012);

  const camera = new THREE.PerspectiveCamera(CAM_FOV, 1, 0.1, 1000);
  let targetCamPos = new THREE.Vector3(-9, 19, 17);
  let targetCamLook = new THREE.Vector3(7.5, 0, 4.5);
  camera.position.copy(targetCamPos);
  camera.lookAt(targetCamLook);

  scene.add(new THREE.AmbientLight(0xffffff, 0.62));
  const dirLight = new THREE.DirectionalLight(0xffeedd, 0.85);
  dirLight.position.set(-22, 45, 18);
  dirLight.castShadow = true;
  dirLight.shadow.mapSize.width = 2048;
  dirLight.shadow.mapSize.height = 2048;
  dirLight.shadow.bias = -0.0005;
  dirLight.shadow.normalBias = 0.02;
  scene.add(dirLight);
  scene.add(dirLight.target);
  scene.add(new THREE.DirectionalLight(0x38bdf8, 0.35));


  const gridHelper = new THREE.GridHelper(80, 40, 0x0284c7, 0x1e293b);
  gridHelper.position.y = -8; scene.add(gridHelper);

  const tileMat = new THREE.MeshStandardMaterial({ map: makeTileTexture(), roughness: 0.65, metalness: 0.1 });
  const fragileMat = new THREE.MeshStandardMaterial({ map: makeFragileTexture(), roughness: 0.70, metalness: 0.05, emissive: 0xc2410c, emissiveIntensity: 0.12 });
  const bridgeMat = new THREE.MeshStandardMaterial({ map: makeBridgeTexture(), roughness: 0.50, metalness: 0.5, emissive: 0x0284c7, emissiveIntensity: 0.15 });
  const sideMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.8 });
  const fragileSideMat = new THREE.MeshStandardMaterial({ color: 0x431407, roughness: 0.8 });
  const bridgeSideMat = new THREE.MeshStandardMaterial({ color: 0x080e1a, roughness: 0.7 });

  const metalDarkMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.4, metalness: 0.7 });
  const boltMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.25, metalness: 0.85 });
  const softSwitchMat = new THREE.MeshStandardMaterial({ color: 0xfacc15, emissive: 0xca8a04, emissiveIntensity: 0.45, roughness: 0.4, metalness: 0.3 });
  const heavySwitchMat = new THREE.MeshStandardMaterial({ color: 0xf43f5e, emissive: 0xbe123c, emissiveIntensity: 0.5, roughness: 0.4, metalness: 0.3 });
  const splitSwitchMat = new THREE.MeshStandardMaterial({ color: 0xc084fc, emissive: 0x7e22ce, emissiveIntensity: 0.6, roughness: 0.3, metalness: 0.5 });
  const goalFrameMat = new THREE.MeshStandardMaterial({ color: 0x607d8a, emissive: 0x102e34, emissiveIntensity: 0.18, roughness: 0.36, metalness: 0.7 });
  const goalHaloMat = new THREE.MeshStandardMaterial({ color: 0x103533, emissive: 0x21c7ab, emissiveIntensity: 1.35, roughness: 0.35, metalness: 0.05 });

  const boardGroup = new THREE.Group();
  scene.add(boardGroup);

  // Vật liệu riêng để phân biệt khối đang chọn.
  const blockMatA = new THREE.MeshStandardMaterial({ map: makeBlockTexture(), roughness: 0.45, metalness: 0.2 });
  const blockMatB = new THREE.MeshStandardMaterial({ map: makeBlockTexture(), roughness: 0.45, metalness: 0.2 });
  const cubeGeo = new THREE.BoxGeometry(TILE_SCALE * 0.92, TILE_SCALE * 0.92, TILE_SCALE * 0.92);
  const blockMaster = new THREE.Group();
  const cubeA = new THREE.Mesh(cubeGeo, blockMatA); cubeA.castShadow = true;
  const cubeB = new THREE.Mesh(cubeGeo, blockMatB); cubeB.castShadow = true;
  blockMaster.add(cubeA); blockMaster.add(cubeB); scene.add(blockMaster);

  const activeMarker = new THREE.Group();
  activeMarker.visible = false;
  scene.add(activeMarker);

  const activeTorus = new THREE.Mesh(
    new THREE.TorusGeometry(0.72, 0.08, 16, 32),
    new THREE.MeshStandardMaterial({ color: 0x00f2fe, emissive: 0x00f2fe, emissiveIntensity: 2.2, roughness: 0.1 })
  );
  activeTorus.rotation.x = Math.PI / 2;
  activeMarker.add(activeTorus);

  const activePointer = new THREE.Mesh(
    new THREE.ConeGeometry(0.22, 0.42, 16),
    new THREE.MeshBasicMaterial({ color: 0x38bdf8 })
  );
  activePointer.rotation.x = Math.PI; // Mũi nhọn chúc thẳng vào khối
  activePointer.position.y = -0.32;
  activeMarker.add(activePointer);
  return {
    THREE, activeMarker, blockMaster, blockMatA,
    blockMatB, boardGroup, boltMat, bridgeMat,
    bridgeSideMat, camera, cubeA, cubeB,
    fragileMat, fragileSideMat, goalFrameMat, goalHaloMat,
    heavySwitchMat, metalDarkMat, renderer, scene,
    sideMat, softSwitchMat, splitSwitchMat, targetCamLook, keyLight: dirLight,
    targetCamPos, tileMat, bridgeMeshGroups: {}, switchMeshes: {},
  };
}
