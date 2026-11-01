import { TILE_SCALE } from '../config.js';

export function buildGoal(view, x, z) {
  const { THREE } = view;
  const outer = TILE_SCALE * 1.02;
  const opening = TILE_SCALE * 0.96;
  const half = opening / 2;

  const shape = new THREE.Shape();
  shape.moveTo(-outer / 2, -outer / 2);
  shape.lineTo(outer / 2, -outer / 2);
  shape.lineTo(outer / 2, outer / 2);
  shape.lineTo(-outer / 2, outer / 2);
  shape.closePath();
  const hole = new THREE.Path();
  hole.moveTo(-half, -half);
  hole.lineTo(-half, half);
  hole.lineTo(half, half);
  hole.lineTo(half, -half);
  hole.closePath();
  shape.holes.push(hole);

  const frameGeometry = new THREE.ExtrudeGeometry(shape, {
    depth: 0.24, steps: 1, bevelEnabled: true,
    bevelThickness: 0.01, bevelSize: 0.01, bevelSegments: 2, curveSegments: 1,
  });
  const frame = new THREE.Mesh(frameGeometry, [view.goalFrameMat, view.metalDarkMat]);
  frame.name = 'goalFrame';
  frame.rotation.x = -Math.PI / 2;
  frame.position.set(x, -0.24, z);
  view.boardGroup.add(frame);

  const lightBar = new THREE.BoxGeometry(TILE_SCALE * 0.72, 0.012, 0.022);
  const lightEdge = (outer + opening) / 4;
  [[0, -lightEdge, 0], [0, lightEdge, 0],
    [-lightEdge, 0, Math.PI / 2], [lightEdge, 0, Math.PI / 2]].forEach(([dx, dz, angle]) => {
    const light = new THREE.Mesh(lightBar, view.goalHaloMat);
    light.name = 'goalLight';
    light.position.set(x + dx, 0.025, z + dz);
    light.rotation.y = angle;
    view.boardGroup.add(light);
  });
  const cornerGeometry = new THREE.BoxGeometry(0.045, 0.014, 0.045);
  [-lightEdge, lightEdge].forEach(dx => [-lightEdge, lightEdge].forEach(dz => {
    const corner = new THREE.Mesh(cornerGeometry, view.goalHaloMat);
    corner.position.set(x + dx, 0.025, z + dz);
    view.boardGroup.add(corner);
  }));

  [[0.10, 0.11], [0.055, 0.22]].forEach(([width, opacity]) => {
    const geometry = new THREE.BoxGeometry(opening, 0.006, width);
    const material = new THREE.MeshBasicMaterial({
      color: 0x42e0c6, transparent: true, opacity, toneMapped: false,
      depthWrite: false, blending: THREE.AdditiveBlending,
    });
    [[0, -lightEdge, 0], [0, lightEdge, 0],
      [-lightEdge, 0, Math.PI / 2], [lightEdge, 0, Math.PI / 2]].forEach(([dx, dz, angle]) => {
      const glow = new THREE.Mesh(geometry, material);
      glow.position.set(x + dx, 0.018, z + dz);
      glow.rotation.y = angle;
      view.boardGroup.add(glow);
    });
  });

  // Mặt trong hố không che khối khi rơi.
  const depth = 6;
  const pitMaterial = new THREE.MeshBasicMaterial({ color: 0x06121c });
  const wallGeometry = new THREE.PlaneGeometry(opening, depth);
  [[-half, 0, Math.PI / 2], [half, 0, -Math.PI / 2],
    [0, -half, 0], [0, half, Math.PI]].forEach(([dx, dz, angle]) => {
    const wall = new THREE.Mesh(wallGeometry, pitMaterial);
    wall.name = 'goalPit';
    wall.position.set(x + dx, -depth / 2, z + dz);
    wall.rotation.y = angle;
    view.boardGroup.add(wall);
  });

  const bottom = new THREE.Mesh(new THREE.PlaneGeometry(opening, opening), pitMaterial);
  bottom.name = 'goalPit';
  bottom.rotation.x = -Math.PI / 2;
  bottom.position.set(x, -depth, z);
  view.boardGroup.add(bottom);

  const depthBar = new THREE.BoxGeometry(opening - 0.04, 0.018, 0.014);
  const inset = half - 0.02;
  [-0.28, -0.85, -1.7].forEach((y, index) => {
    const opacity = [0.72, 0.38, 0.18][index];
    const material = new THREE.MeshBasicMaterial({
      color: 0x53e1cf, transparent: true, opacity, toneMapped: false,
      depthWrite: false, blending: THREE.AdditiveBlending,
    });
    [[0, -inset, 0], [0, inset, 0],
      [-inset, 0, Math.PI / 2], [inset, 0, Math.PI / 2]].forEach(([dx, dz, angle]) => {
      const band = new THREE.Mesh(depthBar, material);
      band.name = 'goalDepthLight';
      band.userData = { opacity, phase: index * 0.8 };
      band.position.set(x + dx, y, z + dz);
      band.rotation.y = angle;
      view.boardGroup.add(band);
    });
  });

  const glow = new THREE.PointLight(0x63e6d2, 0.7, TILE_SCALE * 2.2, 2);
  glow.name = 'goalGlow';
  glow.position.set(x, 0.35, z);
  view.boardGroup.add(glow);
}
