import * as defaultApi from '../api.js';
import { DIFFICULTY_LABELS } from '../config.js';
import { createStagePreviews } from './stage-preview.js';

function normalizeSearch(value) {
  return value.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/đ/g, 'd').trim();
}

function textElement(className, text) {
  const element = document.createElement('span');
  element.className = className;
  element.textContent = text;
  return element;
}

export function createStageControls(state, { buildBoard }, api = defaultApi) {
  let previousFocus = null;
  const search = document.getElementById('stage-search');
  const preview = createStagePreviews(api);
  let stageCards = [];
  search.addEventListener('input', filterStages);
  async function fetchStagesList() {
    try {
      const data = await api.listStages();
      if (data && Array.isArray(data.stages) && data.stages.length > 0) {
        state.loadedStages = data.stages;
      }
    } catch (e) {
      console.warn("Không tải được danh sách màn:", e);
    }
    populateStageGrid();
  }

  function populateStageGrid() {
    const grid = document.getElementById('stage-grid-container');
    if (!grid) return;
    grid.replaceChildren();
    stageCards = [];
    state.loadedStages.forEach((s, idx) => {
      const card = document.createElement('button');
      card.type = 'button';
      const selected = s.id === state.currentStageFile;
      card.className = `stage-card ${selected ? 'active-stage' : ''}`;
      card.setAttribute('aria-current', selected ? 'true' : 'false');
      card.addEventListener('click', () => selectStage(s.id));
      const diffText = String(s.diff || 'medium').toLowerCase();
      const number = (idx + 1).toString().padStart(2, '0');
      const name = (s.name || s.id).replace(/^stage\s*\d+\s*[-–:]\s*/i, '');
      const heading = textElement('stage-card-top', '');
      heading.append(textElement('stage-num', `MÀN ${number}`));
      if (selected) heading.append(textElement('stage-current', 'Đang chọn'));
      const thumbnail = textElement('stage-preview', 'Đang tải bản đồ');
      thumbnail.setAttribute('aria-hidden', 'true');
      const body = textElement('stage-card-body', '');
      const mechanisms = textElement('stage-mech', '');
      (s.mech || 'Cơ bản').split(' + ').forEach(mechanism => {
        mechanisms.append(textElement('stage-mech-tag', mechanism === 'Gạch vỡ' ? 'Ô yếu' : mechanism));
      });
      const bottom = textElement('stage-card-bottom', '');
      const difficulty = textElement('diff-badge', DIFFICULTY_LABELS[diffText] || diffText);
      if (/^[a-z-]+$/.test(diffText)) difficulty.classList.add(`diff-${diffText}`);
      bottom.append(difficulty, textElement('stage-play-label', 'Chơi màn'));
      body.append(textElement('stage-name', name), mechanisms, bottom);
      card.append(heading, thumbnail, body);
      card.setAttribute('aria-label', `Màn ${number}: ${name}. ${difficulty.textContent}${selected ? '. Đang chọn' : ''}`);
      card.dataset.search = normalizeSearch(`${number} ${idx + 1} ${s.name} màn ${number} ${mechanisms.textContent} ${difficulty.textContent}`);
      stageCards.push(card);
      grid.appendChild(card);
    });
    filterStages();
  }

  function filterStages() {
    const query = normalizeSearch(search.value).split(/\s+/).filter(Boolean);
    let visible = 0;
    stageCards.forEach(card => {
      card.hidden = !query.every(word => card.dataset.search.includes(word));
      if (!card.hidden) visible++;
    });
    document.getElementById('stage-result-count').textContent = query.length
      ? `${visible} / ${stageCards.length} màn` : `${stageCards.length} màn chơi`;
    document.getElementById('stage-empty').hidden = visible > 0;
    document.getElementById('stage-grid-container').hidden = visible === 0;
    document.getElementById('stage-grid-container').scrollTop = 0;
  }

  function loadPreviews() {
    stageCards.forEach((card, idx) => preview(card.querySelector('.stage-preview'), state.loadedStages[idx].id));
  }

  async function loadStageFile(stageFilename) {
    state.currentStageFile = stageFilename;
    try {
      const data = await api.loadStage(stageFilename);
      buildBoard(data);
    } catch (e) {
      console.error("Không tải được màn chơi:", e);
    }
  }

  function startGame(stageFilename) {
    document.getElementById('start-screen').classList.add('hidden');
    document.getElementById('game-screen').hidden = false;
    state.inGameActive = true;
    loadStageFile(stageFilename || state.currentStageFile || "stage_01.json");
    document.getElementById('webgl-canvas').focus({ preventScroll: true });
  }

  function openStageModal() {
    previousFocus = document.activeElement;
    search.value = '';
    populateStageGrid();
    document.getElementById('stage-modal').classList.add('active');
    document.getElementById('start-screen').inert = true;
    document.getElementById('game-screen').inert = true;
    search.focus({ preventScroll: true });
    document.querySelector('.active-stage')?.scrollIntoView({ block: 'nearest' });
    loadPreviews();
  }

  function closeStageModal() {
    document.getElementById('stage-modal').classList.remove('active');
    document.getElementById('start-screen').inert = false;
    document.getElementById('game-screen').inert = false;
    previousFocus?.focus({ preventScroll: true });
  }

  function selectStage(stageFilename) {
    closeStageModal();
    startGame(stageFilename);
  }
  return { fetchStagesList, loadStageFile, startGame, openStageModal, closeStageModal };
}
