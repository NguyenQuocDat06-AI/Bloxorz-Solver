
export function createBridgeController(state, view, { playAudio, drawRadar }) {
  function triggerSwitches(occupied, orient) {
    let triggeredAny = false;
    for (const [r, c] of occupied) {
      const key = `${r},${c}`;
      const sw = state.switchMap[key];
      if (!sw) continue;

      let canTrigger = false;
      if (sw.type === 'SOFT_SWITCH' || sw.type === 4) {
        canTrigger = true; // Kích hoạt ở mọi tư thế (đứng, nằm, hoặc khối đơn 1x1x1)
      } else if (sw.type === 'HEAVY_SWITCH' || sw.type === 5) {
        canTrigger = (orient === 0); // Chỉ kích hoạt khi khối ĐỨNG thẳng (1x1)
      }

      if (canTrigger) {
        triggeredAny = true;
        depressSwitch(key);

        if (sw.type === 'HEAVY_SWITCH' || sw.type === 5) {
          playAudio('switch_heavy');
        } else {
          playAudio('switch_soft');
        }

        (sw.linked_bridges || []).forEach(bId => {
          if (state.bridgeStates[bId] !== undefined) {
            let newState = state.bridgeStates[bId];
            if (sw.behavior === 'toggle') newState = !state.bridgeStates[bId];
            else if (sw.behavior === 'perm_open') newState = true;
            else if (sw.behavior === 'perm_close') newState = false;

            if (newState !== state.bridgeStates[bId]) {
              setBridgeState(bId, newState);
            }
          }
        });
      }
    }
    if (triggeredAny) {
      drawRadar();
    }
  }

  function depressSwitch(key) {
    const swObj = view.switchMeshes[key];
    if (!swObj || !swObj.group) return;
    const grp = swObj.group;
    const targetY = swObj.pressedY;
    const startY = grp.position.y;
    const startTime = performance.now();
    const dur = 120;

    function animDown(now) {
      const p = Math.min((now - startTime) / dur, 1.0);
      grp.position.y = startY + (targetY - startY) * p;
      if (p < 1.0) {
        requestAnimationFrame(animDown);
      } else {
        setTimeout(() => {
          const upStart = performance.now();
          function animUp(t) {
            const upP = Math.min((t - upStart) / 100, 1.0);
            grp.position.y = targetY + (swObj.baseY - targetY) * upP;
            if (upP < 1.0) requestAnimationFrame(animUp);
          }
          requestAnimationFrame(animUp);
        }, 60);
      }
    }
    requestAnimationFrame(animDown);
  }

  function setBridgeState(bId, open) {
    state.bridgeStates[bId] = open;
    playAudio('bridge');
    const groups = view.bridgeMeshGroups[bId] || [];

    groups.forEach(grp => {
      if (open) {
        grp.visible = true;
        const targetY = grp.userData.baseY || -0.13;
        const startY = grp.position.y < -5 ? -4 : grp.position.y;
        grp.position.y = startY;
        const startTime = performance.now();
        const dur = 280;

        function rise(t) {
          const p = Math.min((t - startTime) / dur, 1.0);
          const ease = 1 - Math.pow(1 - p, 3);
          grp.position.y = startY + (targetY - startY) * ease;
          if (p < 1.0) requestAnimationFrame(rise);
        }
        requestAnimationFrame(rise);
      } else {
        const startY = grp.position.y;
        const targetY = -6;
        const startTime = performance.now();
        const dur = 260;

        function sink(t) {
          const p = Math.min((t - startTime) / dur, 1.0);
          grp.position.y = startY + (targetY - startY) * p;
          if (p < 1.0) {
            requestAnimationFrame(sink);
          } else {
            grp.visible = false;
          }
        }
        requestAnimationFrame(sink);
      }
    });
  }
  return { triggerSwitches };
}
