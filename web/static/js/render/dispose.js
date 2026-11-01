export function clearBoard(view) {
  const sharedMaterials = new Set(Object.values(view).filter(value => value?.isMaterial));
  const geometries = new Set();
  const materials = new Set();

  view.boardGroup.traverse(object => {
    if (object.geometry) geometries.add(object.geometry);
    const ownMaterials = Array.isArray(object.material) ? object.material : [object.material];
    ownMaterials.forEach(material => {
      if (material && !sharedMaterials.has(material)) materials.add(material);
    });
  });

  while (view.boardGroup.children.length) view.boardGroup.remove(view.boardGroup.children[0]);
  geometries.forEach(geometry => geometry.dispose());
  materials.forEach(material => material.dispose());
}
