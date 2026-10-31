import * as defaultApi from '../api.js';

export function createStageControls(state, { buildBoard }, api = defaultApi) {
  async function fetchStagesList() {
    try {
      const data = await api.listStages();
      if (data && Array.isArray(data.stages) && data.stages.length > 0) {
        state.loadedStages = data.stages;
      }
    } catch (e) {
      console.warn("Không thể tải /api/stages từ server:", e);
    }
    populateStageGrid();
  }

  function populateStageGrid() {
    const grid = document.getElementById('stage-grid-container');
    if (!grid) return;
    grid.innerHTML = '';
    state.loadedStages.forEach((s, idx) => {
      const card = document.createElement('div');
      card.className = `stage-card ${s.id === state.currentStageFile ? 'active-stage' : ''}`;
      card.addEventListener('click', () => selectStage(s.id));
      const diffText = String(s.diff || 'medium').toLowerCase();
      card.innerHTML = `
        <div class="stage-card-top">
          <span class="stage-num">#${(idx + 1).toString().padStart(2, '0')}</span>
          <span class="diff-badge diff-${diffText}">${diffText}</span>
        </div>
        <div class="stage-name">${s.name || s.id}</div>
        <div class="stage-mech">⚙️ ${s.mech || 'Cơ bản'}</div>
      `;
      grid.appendChild(card);
    });
  }

  async function loadStageFile(stageFilename) {
    state.currentStageFile = stageFilename;
    try {
      const data = await api.loadStage(stageFilename);
      buildBoard(data);
    } catch (e) {
      console.error("Không thể tải file màn chơi:", e);
    }
  }

  function startGame(stageFilename) {
    document.getElementById('start-screen').classList.add('hidden');
    state.inGameActive = true;
    loadStageFile(stageFilename || state.currentStageFile || "stage_01.json");
  }

  function openStageModal() {
    populateStageGrid();
    document.getElementById('stage-modal').classList.add('active');
  }

  function closeStageModal() {
    document.getElementById('stage-modal').classList.remove('active');
  }

  function selectStage(stageFilename) {
    closeStageModal();
    document.getElementById('start-screen').classList.add('hidden');
    state.inGameActive = true;
    loadStageFile(stageFilename);
  }
  return { fetchStagesList, loadStageFile, startGame, openStageModal, closeStageModal };
}
