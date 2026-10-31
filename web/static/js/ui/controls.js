import { bindKeyboard } from './keyboard.js';

export function bindControls(state, view, game, stages, solvers, camera, audio) {
  const actions = {
    start: () => stages.startGame(),
    'open-stages': () => stages.openStageModal(),
    'close-stages': () => stages.closeStageModal(),
    reset: () => game.resetStage(),
    'run-dfs': () => solvers.runDfsSolver(),
    'toggle-dfs': (event) => solvers.toggleDfsIds(event),
  };
  document.querySelectorAll('[data-action]').forEach(element => {
    element.addEventListener('click', actions[element.dataset.action]);
  });
  document.querySelectorAll('[data-algorithm]').forEach(element => {
    element.addEventListener('click', () => solvers.callPythonSolver(element.dataset.algorithm));
  });
  document.querySelectorAll('[data-camera]').forEach(element => {
    element.addEventListener('click', () => camera.setCamera(element.dataset.camera));
  });
  bindKeyboard(state, view, game, stages, audio);
}
