import { TILE_SCALE, CAM_FOV } from '../config.js';
import { createTextures } from './textures.js';

export function createScene(THREE) {
  const { makeTileTexture, makeFragileTexture, makeBridgeTexture, makeBlockTexture } = createTextures(THREE);
  const canvas = document.getElementById('webgl-canvas');
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  // ACES Filmic Tone Mapping: Giữ màu tươi sáng, không cháy lóa specular
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.0;

  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x060913, 0.012);

  const camera = new THREE.PerspectiveCamera(CAM_FOV, window.innerWidth / window.innerHeight, 0.1, 1000);
  let targetCamPos = new THREE.Vector3(-9, 19, 17);
  let targetCamLook = new THREE.Vector3(7.5, 0, 4.5);
  camera.position.copy(targetCamPos);
  camera.lookAt(targetCamLook);

  // Ánh sáng tươi sáng, rõ ràng nhưng không tạo vệt lóa chói mắt
  scene.add(new THREE.AmbientLight(0xffffff, 0.62));
  const dirLight = new THREE.DirectionalLight(0xffeedd, 0.85);
  dirLight.position.set(-22, 45, 18);
  dirLight.castShadow = true;
  dirLight.shadow.mapSize.width = 2048;
  dirLight.shadow.mapSize.height = 2048;
  dirLight.shadow.bias = -0.0005;
  scene.add(dirLight);
  scene.add(new THREE.DirectionalLight(0x38bdf8, 0.35));

  // Bụi sao và sàn lưới không gian
  const galaxyGeo = new THREE.BufferGeometry();
  const pos = new Float32Array(1200 * 3);
  for (let i = 0; i < 1200 * 3; i++) pos[i] = (Math.random() - 0.5) * 160;
  galaxyGeo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  scene.add(new THREE.Points(galaxyGeo, new THREE.PointsMaterial({ size: 0.45, color: 0x38bdf8 })));

  const gridHelper = new THREE.GridHelper(80, 40, 0x0284c7, 0x1e293b);
  gridHelper.position.y = -8; scene.add(gridHelper);

  // Vật liệu: Màu tươi sáng, độ nhám (roughness) cao phân tán ánh sáng đều, KHÔNG chói specular
  const tileMat = new THREE.MeshStandardMaterial({ map: makeTileTexture(), roughness: 0.65, metalness: 0.1 });
  const fragileMat = new THREE.MeshStandardMaterial({ map: makeFragileTexture(), roughness: 0.70, metalness: 0.05, emissive: 0xc2410c, emissiveIntensity: 0.12 });
  const bridgeMat = new THREE.MeshStandardMaterial({ map: makeBridgeTexture(), roughness: 0.50, metalness: 0.5, emissive: 0x0284c7, emissiveIntensity: 0.15 });
  const sideMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.8 });
  const fragileSideMat = new THREE.MeshStandardMaterial({ color: 0x431407, roughness: 0.8 });
  const bridgeSideMat = new THREE.MeshStandardMaterial({ color: 0x080e1a, roughness: 0.7 });

  // Vật liệu công tắc & chi tiết cơ khí: Màu sắc tươi sáng, tương phản cao
  const metalDarkMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.4, metalness: 0.7 });
  const boltMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.25, metalness: 0.85 });
  const softSwitchMat = new THREE.MeshStandardMaterial({ color: 0xfacc15, emissive: 0xca8a04, emissiveIntensity: 0.45, roughness: 0.4, metalness: 0.3 });
  const heavySwitchMat = new THREE.MeshStandardMaterial({ color: 0xf43f5e, emissive: 0xbe123c, emissiveIntensity: 0.5, roughness: 0.4, metalness: 0.3 });
  const splitSwitchMat = new THREE.MeshStandardMaterial({ color: 0xc084fc, emissive: 0x7e22ce, emissiveIntensity: 0.6, roughness: 0.3, metalness: 0.5 });
  const goalFrameMat = new THREE.MeshStandardMaterial({ color: 0xd97706, emissive: 0xb45309, emissiveIntensity: 0.5, roughness: 0.35, metalness: 0.7 });
  const goalHaloMat = new THREE.MeshStandardMaterial({ color: 0xfbbf24, emissive: 0xf59e0b, emissiveIntensity: 1.1, roughness: 0.3 });

  const boardGroup = new THREE.Group();
  scene.add(boardGroup);

  // Khối hộp Bloxorz (1x1x2): Cam sáng ấm, viền vàng (2 vật liệu độc lập để làm hiệu ứng phát sáng cho khối đang chọn khi tách)
  const blockMatA = new THREE.MeshStandardMaterial({ map: makeBlockTexture(), roughness: 0.45, metalness: 0.2 });
  const blockMatB = new THREE.MeshStandardMaterial({ map: makeBlockTexture(), roughness: 0.45, metalness: 0.2 });
  const cubeGeo = new THREE.BoxGeometry(TILE_SCALE * 0.92, TILE_SCALE * 0.92, TILE_SCALE * 0.92);
  const blockMaster = new THREE.Group();
  const cubeA = new THREE.Mesh(cubeGeo, blockMatA); cubeA.castShadow = true;
  const cubeB = new THREE.Mesh(cubeGeo, blockMatB); cubeB.castShadow = true;
  blockMaster.add(cubeA); blockMaster.add(cubeB); scene.add(blockMaster);

  // Cụm vòng hào quang & con trỏ chỉ báo khối đang chọn điều khiển khi ở trạng thái phân tách (SPLIT)
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
    sideMat, softSwitchMat, splitSwitchMat, targetCamLook,
    targetCamPos, tileMat, bridgeMeshGroups: {}, switchMeshes: {},
  };
}
