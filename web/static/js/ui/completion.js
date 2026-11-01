import { createConfetti } from './confetti.js';

function stageTitle(name) {
  return String(name || '').replace(/^stage\s*\d+\s*[-–:]\s*/i, '');
}

export function createCompletionControls(state, game, stages, { onHide = () => {} } = {}) {
  const modal = document.getElementById('completion-modal');
  const confetti = createConfetti(modal);
  const nextButton = document.getElementById('completion-next');
  const chooseButton = document.getElementById('completion-choose');

  function nextStage() {
    const index = state.loadedStages.findIndex(stage => stage.id === state.currentStageFile);
    return index >= 0 ? state.loadedStages[index + 1] : null;
  }

  function show() {
    if (state.gameState !== 'WON' || !state.inGameActive || !modal.hidden) return;
    if (document.getElementById('stage-modal').classList.contains('active')) stages.closeStageModal();
    const index = state.loadedStages.findIndex(stage => stage.id === state.currentStageFile);
    const number = index >= 0 ? String(index + 1).padStart(2, '0') : '';
    const next = nextStage();
    document.getElementById('completion-stage-label').textContent = `HOÀN THÀNH MÀN ${number}`.trim();
    document.getElementById('completion-stage-name').textContent = stageTitle(state.currentStageData?.name) || state.currentStageFile;
    document.getElementById('completion-moves').textContent = state.moves;
    const isLast = index >= 0 && index === state.loadedStages.length - 1;
    document.getElementById('completion-description').textContent = isLast
      ? 'Bạn đã hoàn thành màn cuối cùng.' : 'Bạn đã đưa khối hộp về đích.';
    nextButton.hidden = !next;
    document.getElementById('completion-next-name').textContent = next
      ? `Màn ${String(index + 2).padStart(2, '0')} · ${stageTitle(next.name)}` : '';
    chooseButton.classList.toggle('completion-primary', !next);
    modal.hidden = false;
    document.getElementById('game-screen').inert = true;
    (next ? nextButton : chooseButton).focus({ preventScroll: true });
    confetti.play();
  }

  function hide() {
    confetti.stop();
    if (modal.hidden) return;
    onHide();
    modal.hidden = true;
    const pickerOpen = document.getElementById('stage-modal').classList.contains('active');
    document.getElementById('game-screen').inert = pickerOpen;
    if (!pickerOpen) document.getElementById('webgl-canvas').focus({ preventScroll: true });
  }

  function replay() {
    hide();
    game.resetStage();
  }

  function chooseStage() {
    hide();
    stages.openStageModal();
  }

  function next() {
    const stage = nextStage();
    if (!stage) return chooseStage();
    hide();
    stages.startGame(stage.id);
  }

  function handleKeydown(event) {
    if (modal.hidden) return false;
    if (event.key === 'Escape') {
      event.preventDefault();
      hide();
    } else if (event.key.toLowerCase() === 'r') {
      event.preventDefault();
      replay();
    } else if (event.key === 'Tab') {
      const buttons = [...modal.querySelectorAll('button')].filter(button => !button.hidden && !button.disabled);
      const first = buttons[0], last = buttons[buttons.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault(); last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault(); first.focus();
      }
    }
    return true;
  }

  return { show, hide, replay, next, chooseStage, handleKeydown };
}
