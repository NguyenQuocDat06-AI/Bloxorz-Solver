export function tryMergeCubes(r1, c1, r2, c2) {
  if (r1 === r2) {
    if (c1 + 1 === c2) return { r: r1, c: c1, orient: 1 };
    if (c2 + 1 === c1) return { r: r2, c: c2, orient: 1 };
  } else if (c1 === c2) {
    if (r1 + 1 === r2) return { r: r1, c: c1, orient: 2 };
    if (r2 + 1 === r1) return { r: r2, c: c2, orient: 2 };
  }
  return null;
}
