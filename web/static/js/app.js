import { createGameState } from './state.js';
import { createAudio } from './audio.js';
import { createScene } from './render/scene.js';
import { createTileRenderer } from './render/tiles.js';
import { createBoardBuilder } from './render/board.js';
import { startRenderLoop } from './render/loop.js';
import { createGameController } from './game/controller.js';
import { createRadar } from './ui/radar.js';
import { createHud } from './ui/hud.js';
import { createCameraControls } from './ui/camera.js';
import { createStageControls } from './ui/stages.js';
import { createSolverControls } from './ui/solver.js';
import { bindControls } from './ui/controls.js';

export function createApp() {
  const state = createGameState();
  const view = createScene(window.THREE);
  const audio = createAudio();
  const radar = createRadar(state);
  const hud = createHud(state, radar);
  const game = createGameController(state, view, hud, radar, audio);
  const camera = createCameraControls(state, view);
  const tiles = createTileRenderer(state, view);
  const board = createBoardBuilder(state, view, {
    ...tiles, ...game, ...camera, ...radar,
  });
  const stages = createStageControls(state, board);
  const solvers = createSolverControls(state, game, audio);
  bindControls(state, view, game, stages, solvers, camera, audio);
  const ready = stages.fetchStagesList().then(() => {
    const initialStage = state.loadedStages.length > 0 ? state.loadedStages[0].id : 'stage_01.json';
    return stages.loadStageFile(initialStage);
  });
  startRenderLoop(state, view);
  return { state, game, stages, solvers, camera, ready };
}

// A single module instance owns the state; no application variables are added to window.
export const app = createApp();
