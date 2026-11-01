
export function createBridgeController(state, view, { playAudio, drawRadar }) {
  const getNow = () => (window.__virtualTime !== undefined ? window.__virtualTime : performance.now());
  const bridgeAnimations = new Map();
  const switchAnimations = new Map();

  function beginAnimation(versions, key) {
    const runId = state.runId, stageFile = state.currentStageFile;
    const version = (versions.get(key) || 0) + 1;
    versions.set(key, version);
    return () => state.runId === runId && state.currentStageFile === stageFile
      && versions.get(key) === version;
  }

  function triggerSwitches(occupied, orient) {
    let triggeredAny = false;
    for (const [r, c] of occupied) {
      const key = `${r},${c}`;
      const sw = state.switchMap[key];
      if (!sw) continue;

      let canTrigger = false;
      if (sw.type === 'SOFT_SWITCH' || sw.type === 4) {
        canTrigger = true; // Kích hoạt ở mọi tư thế (đứng, nằm, hoặc khối đơn 1x1x1)
      } else if (sw.type === 'HEAVY_SWITCH' || sw.type === 5
        || sw.type === 'SPLIT_SWITCH' || sw.type === 6) {
        canTrigger = (orient === 0); // Công tắc nặng và tách cần khối đứng.
      }

      if (canTrigger) {
        triggeredAny = true;
        depressSwitch(key);

        if (sw.type === 'HEAVY_SWITCH' || sw.type === 5) {
          playAudio('switch_heavy');
        } else if (sw.type === 'SOFT_SWITCH' || sw.type === 4) {
          playAudio('switch_soft');
        }

        (sw.linked_bridges || []).forEach(bId => {
          if (state.bridgeStates[bId] !== undefined) {
            let newState = state.bridgeStates[bId];
            const behavior = sw.behavior || 'toggle';
            if (behavior === 'toggle') newState = !state.bridgeStates[bId];
            else if (behavior === 'perm_open' || behavior === 'permanent') newState = true;
            else if (behavior === 'perm_close') newState = false;

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
    const isCurrent = beginAnimation(switchAnimations, key);
    const grp = swObj.group;
    const targetY = swObj.pressedY;
    const startY = grp.position.y;
    const startTime = getNow();
    const dur = 120;

    function animDown(now) {
      if (!isCurrent()) return;
      const p = Math.min((getNow() - startTime) / dur, 1.0);
      grp.position.y = startY + (targetY - startY) * p;
      if (p < 1.0) {
        requestAnimationFrame(animDown);
      } else {
        setTimeout(() => {
          if (!isCurrent()) return;
          const upStart = getNow();
          function animUp(t) {
            if (!isCurrent()) return;
            const upP = Math.min((getNow() - upStart) / 100, 1.0);
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
    const isCurrent = beginAnimation(bridgeAnimations, bId);
    state.bridgeStates[bId] = open;
    playAudio('bridge');
    const groups = view.bridgeMeshGroups[bId] || [];

    groups.forEach(grp => {
      if (open) {
        grp.visible = true;
        const targetY = grp.userData.baseY || -0.13;
        const startY = grp.position.y < -5 ? -4 : grp.position.y;
        grp.position.y = startY;
        const startTime = getNow();
        const dur = 280;

        function rise(t) {
          if (!isCurrent()) return;
          const p = Math.min((getNow() - startTime) / dur, 1.0);
          const ease = 1 - Math.pow(1 - p, 3);
          grp.position.y = startY + (targetY - startY) * ease;
          if (p < 1.0) requestAnimationFrame(rise);
        }
        requestAnimationFrame(rise);
      } else {
        const startY = grp.position.y;
        const targetY = -6;
        const startTime = getNow();
        const dur = 260;

        function sink(t) {
          if (!isCurrent()) return;
          const p = Math.min((getNow() - startTime) / dur, 1.0);
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
