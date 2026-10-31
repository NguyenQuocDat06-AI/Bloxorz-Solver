import * as defaultApi from '../api.js';

export function createSolverControls(state, game, audio, api = defaultApi) {
  const { resetStage, roll, syncBlockTransform } = game;
  const { playAudio } = audio;
  function toggleDfsIds(e) {
    if (e) e.stopPropagation();
    state.currentDfsMode = (state.currentDfsMode === 'DFS') ? 'IDS' : 'DFS';
    const btn = document.getElementById('btn-dfs-main');
    const label = document.getElementById('dfs-btn-label');
    const toggle = document.getElementById('btn-dfs-toggle');
    if (state.currentDfsMode === 'DFS') {
      label.textContent = 'DFS (Chiều sâu)';
      btn.style.background = 'linear-gradient(135deg, rgba(16, 185, 129, 0.35), rgba(5, 150, 105, 0.2))';
      btn.style.borderColor = 'rgba(16, 185, 129, 0.4)';
      toggle.innerHTML = '<span>⇄ IDS</span>';
      toggle.style.background = 'rgba(6, 182, 212, 0.2)';
      toggle.style.borderColor = 'rgba(6, 182, 212, 0.4)';
      toggle.style.color = '#38bdf8';
    } else {
      label.textContent = 'IDS (Sâu dần tối ưu)';
      btn.style.background = 'linear-gradient(135deg, rgba(6, 182, 212, 0.35), rgba(14, 116, 144, 0.2))';
      btn.style.borderColor = 'rgba(6, 182, 212, 0.5)';
      toggle.innerHTML = '<span>⇄ DFS</span>';
      toggle.style.background = 'rgba(16, 185, 129, 0.2)';
      toggle.style.borderColor = 'rgba(16, 185, 129, 0.4)';
      toggle.style.color = '#34d399';
    }
  }

  function runDfsSolver() {
    callPythonSolver(state.currentDfsMode);
  }

  async function callPythonSolver(algo) {
    document.getElementById('bm-algo').textContent = algo;
    document.getElementById('bm-time').textContent = 'Calculating...';
    try {
      const data = await api.solveStage(state.currentStageFile, algo);
      if (data.status === 'NOT_IMPLEMENTED') {
        alert(`[Nhắc nhở]: Thành viên phụ trách ${algo} chưa viết code trong solvers/!`);
        document.getElementById('bm-time').textContent = 'Not implemented';
        return;
      }
      document.getElementById('bm-time').textContent = `${data.time_ms} ms`;
      document.getElementById('bm-mem').textContent = `${data.memory_kb} KB`;
      document.getElementById('bm-nodes').textContent = data.expanded_nodes;
      document.getElementById('bm-steps').textContent = data.steps;

      if (data.status === 'FOUND' && data.path.length > 0) {
        resetStage();
        function play(idx) {
          if (idx >= data.path.length) return;
          const act = data.path[idx];
          if (act === 'SWITCH' || act === 'SWITCH_CUBE') {
            if (state.blockOrient === 3) {
              state.activeCube = state.activeCube === 1 ? 2 : 1;
              playAudio('switch_cube');
              syncBlockTransform();
            }
            setTimeout(() => play(idx + 1), 220);
          } else {
            roll(act, () => setTimeout(() => play(idx + 1), 60));
          }
        }
        setTimeout(() => play(0), 300);
      }
    } catch (e) {
      console.error(e);
      document.getElementById('bm-time').textContent = 'Error';
    }
  }
  return { toggleDfsIds, runDfsSolver, callPythonSolver };
}
