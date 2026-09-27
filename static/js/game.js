/* ==========================================================================
   POKÉMON CODE ADVENTURE - FRONTEND GAME ENGINE
   ========================================================================== */

// --------------------------------------------------------------------------
// 1. RETRO 8-BIT AUDIO SYNTHESIZER (WEB AUDIO API - ZERO EXTERNAL MP3s)
// --------------------------------------------------------------------------
class SoundEngine {
    constructor() {
        this.ctx = null;
        this.muted = false;
    }

    init() {
        if (!this.ctx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            this.ctx = new AudioContext();
        }
        if (this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
    }

    playTone(freq, type, duration, startDelay = 0) {
        if (this.muted) return;
        this.init();
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();

        osc.type = type;
        osc.frequency.setValueAtTime(freq, this.ctx.currentTime + startDelay);

        gain.gain.setValueAtTime(0.15, this.ctx.currentTime + startDelay);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + startDelay + duration);

        osc.connect(gain);
        gain.connect(this.ctx.destination);

        osc.start(this.ctx.currentTime + startDelay);
        osc.stop(this.ctx.currentTime + startDelay + duration);
    }

    playHit() {
        if (this.muted) return;
        this.init();
        // White noise thump
        const bufferSize = this.ctx.sampleRate * 0.12;
        const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
            data[i] = Math.random() * 2 - 1;
        }

        const noise = this.ctx.createBufferSource();
        noise.buffer = buffer;

        const gain = this.ctx.createGain();
        gain.gain.setValueAtTime(0.3, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + 0.12);

        noise.connect(gain);
        gain.connect(this.ctx.destination);
        noise.start();

        // Low pitch slide
        this.playTone(180, 'sawtooth', 0.15);
    }

    playCritical() {
        this.playHit();
        this.playTone(660, 'square', 0.1, 0.05);
        this.playTone(880, 'square', 0.15, 0.12);
    }

    playHeal() {
        this.playTone(330, 'sine', 0.1, 0.0);
        this.playTone(392, 'sine', 0.1, 0.08);
        this.playTone(523, 'sine', 0.1, 0.16);
        this.playTone(659, 'sine', 0.2, 0.24);
    }

    playFaint() {
        this.playTone(300, 'triangle', 0.15, 0.0);
        this.playTone(240, 'triangle', 0.15, 0.12);
        this.playTone(180, 'triangle', 0.25, 0.24);
        this.playTone(120, 'triangle', 0.35, 0.40);
    }

    playBallShake() {
        this.playTone(220, 'triangle', 0.08);
    }

    playCatchSuccess() {
        this.playTone(523, 'square', 0.1, 0.0);
        this.playTone(659, 'square', 0.1, 0.1);
        this.playTone(784, 'square', 0.15, 0.2);
        this.playTone(1046, 'square', 0.35, 0.32);
    }

    playLevelUp() {
        if (this.muted) return;
        this.playTone(440, 'square', 0.1, 0.0);
        this.playTone(554, 'square', 0.1, 0.08);
        this.playTone(659, 'square', 0.1, 0.16);
        this.playTone(880, 'square', 0.25, 0.24);
    }

    playEvolution() {
        if (this.muted) return;
        this.playTone(523, 'sine', 0.14, 0.0);
        this.playTone(659, 'sine', 0.14, 0.12);
        this.playTone(784, 'sine', 0.14, 0.24);
        this.playTone(1046, 'sine', 0.25, 0.36);
        this.playTone(1318, 'sine', 0.45, 0.50);
    }

    playBadgeFanfare() {
        if (this.muted) return;
        this.init();
        const notes = [523, 659, 784, 1046, 784, 1046];
        const times = [0, 0.12, 0.24, 0.36, 0.54, 0.72];
        const durs = [0.1, 0.1, 0.1, 0.16, 0.16, 0.45];
        notes.forEach((freq, idx) => {
            this.playTone(freq, 'triangle', durs[idx], times[idx]);
            this.playTone(freq * 0.5, 'sine', durs[idx], times[idx]);
        });
    }

    playClick() {
        this.playTone(400, 'sine', 0.04);
    }
}

const sound = new SoundEngine();

// --------------------------------------------------------------------------
// 2. GAME STATE & UI CONTROLLER
// --------------------------------------------------------------------------
const state = {
    player: null,
    enemy: null,
    party: [],
    active_index: 0,
    storage: [],
    potions: 3,
    pokedex: [],
    badges: [],
    is_gym_battle: false,
    busy: false
};

let movesDatabase = {};

// DOM Elements
const screenStarter = document.getElementById('screen-starter-select');
const screenBattle = document.getElementById('screen-battle');
const starterContainer = document.getElementById('starter-cards-container');

const dialogueText = document.getElementById('dialogue-text');
const mainActionsGrid = document.getElementById('main-actions-grid');
const movesGrid = document.getElementById('moves-grid');
const bagMenu = document.getElementById('bag-menu');
const catchMenu = document.getElementById('catch-menu');
const btnPokemon = document.getElementById('btn-pokemon');
const playerPartyBalls = document.getElementById('player-party-balls');

// Party Switch Modal Elements
const modalPartySwitch = document.getElementById('modal-party-switch');
const partySwitchTitle = document.getElementById('party-switch-title');
const partySwitchSubtitle = document.getElementById('party-switch-subtitle');
const partySwitchList = document.getElementById('party-switch-list');
const btnClosePartySwitch = document.getElementById('btn-close-party-switch');
const btnCancelPartySwitch = document.getElementById('btn-cancel-party-switch');

// Pokédex Team Builder Elements
const pokedexPartyGrid = document.getElementById('pokedex-party-grid');
const btnHealParty = document.getElementById('btn-heal-party');

const playerSprite = document.getElementById('player-sprite');
const playerName = document.getElementById('player-name');
const playerLevel = document.getElementById('player-level');
const playerHpFill = document.getElementById('player-hp-fill');
const playerHpCur = document.getElementById('player-hp-cur');
const playerHpMax = document.getElementById('player-hp-max');
const playerExpFill = document.getElementById('player-exp-fill');
const playerExpCur = document.getElementById('player-exp-cur');
const playerExpMax = document.getElementById('player-exp-max');
const playerDamageFloat = document.getElementById('player-damage-float');

// Top Nav Partner Badge
const navPartnerCard = document.getElementById('nav-partner-card');
const navPartnerSprite = document.getElementById('nav-partner-sprite');
const navPartnerName = document.getElementById('nav-partner-name');
const navPartnerLevel = document.getElementById('nav-partner-level');
const navPartnerExp = document.getElementById('nav-partner-exp');

const enemySprite = document.getElementById('enemy-sprite');
const enemyName = document.getElementById('enemy-name');
const enemyLevel = document.getElementById('enemy-level');
const enemyHpFill = document.getElementById('enemy-hp-fill');
const enemyHpCur = document.getElementById('enemy-hp-cur');
const enemyHpMax = document.getElementById('enemy-hp-max');
const enemyDamageFloat = document.getElementById('enemy-damage-float');

const potionCount = document.getElementById('potion-count');
const pokedexCount = document.getElementById('pokedex-count');
const badgesCount = document.getElementById('badges-count');
const btnSound = document.getElementById('btn-sound');
const btnGyms = document.getElementById('btn-gyms');
const btnToggleMode = document.getElementById('btn-toggle-mode');
const modeText = document.getElementById('mode-text');
const enemyBadgeIcon = document.getElementById('enemy-badge-icon');

// Gym Modals
const modalGym = document.getElementById('modal-gym');
const btnCloseGym = document.getElementById('btn-close-gym');
const gymsListContainer = document.getElementById('gyms-list-container');

const modalBadge = document.getElementById('modal-badge');
const badgeModalTitle = document.getElementById('badge-modal-title');
const badgeAnimIcon = document.getElementById('badge-anim-icon');
const badgeModalName = document.getElementById('badge-modal-name');
const badgeModalDialogue = document.getElementById('badge-modal-dialogue');
const badgeRewardExp = document.getElementById('badge-reward-exp');
const badgeRewardItems = document.getElementById('badge-reward-items');
const btnCloseBadge = document.getElementById('btn-close-badge');

// Modals
const modalBug = document.getElementById('modal-bug-catcher');
const errFile = document.getElementById('err-file');
const errFunction = document.getElementById('err-function');
const errMessage = document.getElementById('err-message');
const errHint = document.getElementById('err-hint');
const btnCloseBug = document.getElementById('btn-close-bug');

const modalVictory = document.getElementById('modal-victory');
const victoryTitle = document.getElementById('victory-title');
const victoryMessage = document.getElementById('victory-message');
const victoryExp = document.getElementById('victory-exp');
const victoryPlayerStatus = document.getElementById('victory-player-status');
const btnNextBattle = document.getElementById('btn-next-battle');

const modalEvolution = document.getElementById('modal-evolution');
const evolutionAnnouncement = document.getElementById('evolution-announcement');
const evoSpriteOld = document.getElementById('evo-sprite-old');
const evoSpriteNew = document.getElementById('evo-sprite-new');
const evolutionCongrats = document.getElementById('evolution-congrats');
const btnCloseEvolution = document.getElementById('btn-close-evolution');

const modalPokedex = document.getElementById('modal-pokedex');
const pokedexPartnerCard = document.getElementById('pokedex-partner-card');
const pokedexPartnerSprite = document.getElementById('pokedex-partner-sprite');
const pokedexPartnerName = document.getElementById('pokedex-partner-name');
const pokedexPartnerLevel = document.getElementById('pokedex-partner-level');
const pokedexPartnerHp = document.getElementById('pokedex-partner-hp');
const pokedexPartnerExp = document.getElementById('pokedex-partner-exp');
const pokedexPartnerToNext = document.getElementById('pokedex-partner-to-next');
const pokedexPartnerExpFill = document.getElementById('pokedex-partner-exp-fill');
const pokedexPartnerMoves = document.getElementById('pokedex-partner-moves');
const pokedexList = document.getElementById('pokedex-list');
const btnPokedex = document.getElementById('btn-pokedex');
const btnClosePokedex = document.getElementById('btn-close-pokedex');

const modalGuide = document.getElementById('modal-guide');
const btnGuide = document.getElementById('btn-guide');
const btnCloseGuide = document.getElementById('btn-close-guide');
const btnCloseGuideFooter = document.getElementById('btn-close-guide-footer');

// Animation
const pokeballAnimContainer = document.getElementById('pokeball-anim-container');
const animPokeball = document.getElementById('anim-pokeball');
const animStars = document.getElementById('anim-stars');

// --------------------------------------------------------------------------
// 3. INITIALIZATION & STARTER SELECTION
// --------------------------------------------------------------------------
window.addEventListener('DOMContentLoaded', () => {
    loadStarters();
    setupEventListeners();
});

function setupEventListeners() {
    // Sound Toggle
    btnSound.addEventListener('click', () => {
        sound.muted = !sound.muted;
        btnSound.textContent = sound.muted ? '🔇 SOUND: OFF' : '🔊 SOUND: ON';
    });

    // Mode Toggle (Teacher Feature)
    btnToggleMode.addEventListener('click', async () => {
        try {
            const res = await fetch('/api/toggle_mode', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({})
            });
            const data = await res.json();
            if (!res.ok || !data.success) {
                setDialogue(data.message || "Teacher reference solutions unavailable.");
                return;
            }
            modeText.textContent = data.use_solution ? 'TEACHER SOLUTION' : 'STUDENT CODE';
            btnToggleMode.style.background = data.use_solution ? '#27ae60' : '#9b59b6';
            setDialogue(`Switched active mode to: ${data.mode_name}`);
        } catch (err) {
            console.error(err);
        }
    });

    // Fight menu
    document.getElementById('btn-fight').addEventListener('click', () => {
        if (state.busy) return;
        sound.playClick();
        mainActionsGrid.classList.add('hidden');
        movesGrid.classList.remove('hidden');
    });

    // Bag menu
    document.getElementById('btn-bag').addEventListener('click', () => {
        if (state.busy) return;
        sound.playClick();
        mainActionsGrid.classList.add('hidden');
        bagMenu.classList.remove('hidden');
    });

    // Catch menu
    document.getElementById('btn-catch').addEventListener('click', () => {
        if (state.busy) return;
        sound.playClick();
        mainActionsGrid.classList.add('hidden');
        catchMenu.classList.remove('hidden');
    });

    // Pokemon Switch button
    if (btnPokemon) {
        btnPokemon.addEventListener('click', () => {
            if (state.busy) return;
            openPartySwitchModal(true);
        });
    }

    // Run button
    document.getElementById('btn-run').addEventListener('click', () => {
        if (state.busy) return;
        state.busy = true;
        sound.playClick();
        setDialogue("Got away safely! Finding another wild Pokémon...");
        setTimeout(() => triggerNextBattle(), 1200);
    });

    // Party Switch Modal close/cancel
    if (btnClosePartySwitch) {
        btnClosePartySwitch.addEventListener('click', () => {
            modalPartySwitch.classList.add('hidden');
        });
    }
    if (btnCancelPartySwitch) {
        btnCancelPartySwitch.addEventListener('click', () => {
            modalPartySwitch.classList.add('hidden');
        });
    }

    // Nurse Joy Heal
    if (btnHealParty) {
        btnHealParty.addEventListener('click', handleHealPartyTeam);
    }

    // Submenu Back buttons
    document.getElementById('btn-bag-back').addEventListener('click', showMainActions);
    document.getElementById('btn-catch-back').addEventListener('click', showMainActions);

    // Use Potion
    document.getElementById('btn-use-potion').addEventListener('click', handleUsePotion);

    // Ball Selector buttons
    document.querySelectorAll('.btn-ball').forEach(btn => {
        btn.addEventListener('click', () => {
            const ball = btn.dataset.ball;
            handleThrowBall(ball);
        });
    });

    // Modals
    btnCloseBug.addEventListener('click', () => {
        modalBug.classList.add('hidden');
        state.busy = false;
    });

    btnNextBattle.addEventListener('click', () => {
        modalVictory.classList.add('hidden');
        triggerNextBattle();
    });

    btnPokedex.addEventListener('click', () => {
        renderPokedex();
        modalPokedex.classList.remove('hidden');
    });

    btnClosePokedex.addEventListener('click', () => {
        modalPokedex.classList.add('hidden');
    });

    if (btnGyms) {
        btnGyms.addEventListener('click', openGymModal);
    }

    if (btnCloseGym) {
        btnCloseGym.addEventListener('click', () => {
            sound.playClick();
            modalGym.classList.add('hidden');
        });
    }

    if (btnCloseBadge) {
        btnCloseBadge.addEventListener('click', () => {
            sound.playClick();
            modalBadge.classList.add('hidden');
        });
    }

    if (btnCloseEvolution) {
        btnCloseEvolution.addEventListener('click', () => {
            sound.playClick();
            modalEvolution.classList.add('hidden');
        });
    }

    if (btnGuide) {
        btnGuide.addEventListener('click', () => {
            sound.playClick();
            modalGuide.classList.remove('hidden');
        });
    }

    if (btnCloseGuide) {
        btnCloseGuide.addEventListener('click', () => {
            modalGuide.classList.add('hidden');
        });
    }

    if (btnCloseGuideFooter) {
        btnCloseGuideFooter.addEventListener('click', () => {
            sound.playClick();
            modalGuide.classList.add('hidden');
        });
    }

    // Guide Tab Switching
    document.querySelectorAll('.guide-tabs .tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            sound.playClick();
            document.querySelectorAll('.guide-tabs .tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.guide-tab-content').forEach(c => c.classList.add('hidden'));

            btn.classList.add('active');
            const targetId = btn.dataset.tab;
            const targetContent = document.getElementById(targetId);
            if (targetContent) {
                targetContent.classList.remove('hidden');
            }
        });
    });
}

function showMainActions() {
    sound.playClick();
    movesGrid.classList.add('hidden');
    bagMenu.classList.add('hidden');
    catchMenu.classList.add('hidden');
    mainActionsGrid.classList.remove('hidden');
}

// --------------------------------------------------------------------------
// 4. STARTERS LAB
// --------------------------------------------------------------------------
async function loadStarters() {
    try {
        const res = await fetch('/api/starters');
        const data = await res.json();
        if (data.success) {
            if (data.moves_database) {
                movesDatabase = data.moves_database;
            }
            renderStarterCards(data.starters);
            if (data.has_solutions === false) {
                btnToggleMode.classList.add('hidden');
            }
        }
    } catch (e) {
        starterContainer.innerHTML = `<div class="error-msg">Failed to load starters: ${e.message}</div>`;
    }
}

function renderStarterCards(starters) {
    starterContainer.innerHTML = '';
    starters.forEach(mon => {
        const card = document.createElement('div');
        card.className = 'starter-card';
        card.innerHTML = `
            <div class="starter-sprite-wrap">
                <img class="starter-sprite" src="${mon.sprite}" alt="${mon.name}">
            </div>
            <div class="starter-name">${mon.name.toUpperCase()}</div>
            <div><span class="type-badge type-${mon.type}">${mon.type.toUpperCase()}</span></div>
            <div class="starter-stats">
                <div class="starter-level-row">⭐ <strong>Level: 5</strong> | EXP: 0 / 100</div>
                <div>HP: ${mon.hp}</div>
                <div>ATK: ${mon.attack} | DEF: ${mon.defense}</div>
                <div>Moves: ${mon.moves.slice(0, 2).join(', ')}</div>
            </div>
            <button class="btn-retro btn-choose" data-id="${mon.id}">I CHOOSE YOU!</button>
        `;
        card.querySelector('.btn-choose').addEventListener('click', () => chooseStarter(mon.id));
        starterContainer.appendChild(card);
    });
}

async function chooseStarter(choice) {
    sound.playClick();
    setDialogue("Professor Oak is registering your starter partner...");

    try {
        const res = await fetch('/api/choose_starter', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ choice: choice })
        });

        const data = await res.json();

        if (!res.ok || data.student_error) {
            showBugCatcher(data);
            return;
        }

        // Transition to Battle Arena
        state.player = data.player;
        state.enemy = data.enemy;
        state.potions = data.potions;
        if (data.party) state.party = data.party;
        if (data.active_index !== undefined) state.active_index = data.active_index;
        if (data.storage) state.storage = data.storage;
        if (data.badges) {
            state.badges = data.badges;
            if (badgesCount) badgesCount.textContent = `${state.badges.length}/5`;
        }
        if (data.pokedex) {
            state.pokedex = data.pokedex;
            pokedexCount.textContent = state.pokedex.length;
        }

        updateHpUI();
        updateBattleUI();
        updatePartyBallsUI();

        screenStarter.classList.remove('active');
        screenBattle.classList.add('active');

        // Play dialogue
        runDialogueSequence(data.dialogue);

    } catch (err) {
        showBugCatcher({
            file: "starters.py",
            function: "create_starter",
            message: err.message,
            hint: "Check starters.py and make sure create_starter() returns a Pokemon instance!"
        });
    }
}

// --------------------------------------------------------------------------
// 5. BATTLE LOGIC & API CALLS
// --------------------------------------------------------------------------
function updateBattleUI() {
    if (!state.player || !state.enemy) return;

    playerName.textContent = state.player.name.toUpperCase();
    if (playerLevel) playerLevel.textContent = `Lv. ${state.player.level || 5}`;
    playerHpMax.textContent = state.player.max_hp;
    playerSprite.src = state.player.back_sprite || state.player.front_sprite;

    enemyName.textContent = state.enemy.name.toUpperCase();
    if (enemyLevel) enemyLevel.textContent = `Lv. ${state.enemy.level || 5}`;
    enemyHpMax.textContent = state.enemy.max_hp;
    enemySprite.src = state.enemy.front_sprite;
    enemySprite.classList.remove('anim-faint');

    potionCount.textContent = state.potions;

    // Render Moves
    movesGrid.innerHTML = '';
    state.player.moves.forEach(moveName => {
        const info = (movesDatabase && movesDatabase[moveName]) || { name: moveName, type: 'Normal', power: 40 };
        const moveType = info.type || 'Normal';
        const movePower = info.power || 40;

        const btn = document.createElement('button');
        btn.className = 'btn-retro btn-move';
        btn.innerHTML = `
            <div class="move-top-row">
                <span class="move-name">${moveName.toUpperCase()}</span>
                <span class="move-type-badge type-${moveType}">${moveType.toUpperCase()}</span>
            </div>
            <div class="move-bottom-row">
                <span class="move-power">POW: ${movePower}</span>
            </div>
        `;
        btn.addEventListener('click', () => handlePlayerAttack(moveName));
        movesGrid.appendChild(btn);
    });

    const backBtn = document.createElement('button');
    backBtn.className = 'btn-retro btn-back';
    backBtn.textContent = 'BACK';
    backBtn.addEventListener('click', showMainActions);
    movesGrid.appendChild(backBtn);

    updateTopNavPartner();
}

function updateHpUI() {
    if (!state.player || !state.enemy) return;

    // Player HP
    playerHpCur.textContent = state.player.hp;
    const playerPct = Math.max(0, Math.min(100, (state.player.hp / state.player.max_hp) * 100));
    playerHpFill.style.width = `${playerPct}%`;
    setHpColor(playerHpFill, playerPct);

    // Player EXP
    const curExp = state.player.exp || 0;
    const maxExp = state.player.max_exp || 100;
    const expPct = Math.max(0, Math.min(100, (curExp / maxExp) * 100));
    if (playerExpFill) {
        playerExpFill.style.width = `${expPct}%`;
    }
    if (playerExpCur) {
        playerExpCur.textContent = curExp;
    }
    if (playerExpMax) {
        playerExpMax.textContent = maxExp;
    }

    // Enemy HP
    enemyHpCur.textContent = state.enemy.hp;
    const enemyPct = Math.max(0, Math.min(100, (state.enemy.hp / state.enemy.max_hp) * 100));
    enemyHpFill.style.width = `${enemyPct}%`;
    setHpColor(enemyHpFill, enemyPct);

    updateTopNavPartner();
}

function updateTopNavPartner() {
    if (!state.player || !navPartnerCard) return;
    navPartnerCard.classList.remove('hidden');
    if (navPartnerSprite) {
        navPartnerSprite.src = state.player.front_sprite;
    }
    if (navPartnerName) {
        navPartnerName.textContent = state.player.name.toUpperCase();
    }
    if (navPartnerLevel) {
        navPartnerLevel.textContent = `Lv. ${state.player.level || 5}`;
    }
    if (navPartnerExp) {
        navPartnerExp.textContent = `EXP: ${state.player.exp || 0}/100`;
    }
}

function setHpColor(element, percentage) {
    element.classList.remove('hp-green', 'hp-yellow', 'hp-red');
    if (percentage > 50) {
        element.classList.add('hp-green');
    } else if (percentage > 20) {
        element.classList.add('hp-yellow');
    } else {
        element.classList.add('hp-red');
    }
}

// --------------------------------------------------------------------------
// 4-POKÉMON PARTY & SWITCHING FUNCTIONS
// --------------------------------------------------------------------------
function updatePartyBallsUI() {
    if (!playerPartyBalls) return;
    playerPartyBalls.innerHTML = '';

    const maxSlots = 4;
    for (let i = 0; i < maxSlots; i++) {
        const dot = document.createElement('span');
        if (i < state.party.length) {
            const mon = state.party[i];
            const isFainted = Boolean(mon.is_fainted || mon.hp <= 0);
            const isActive = (i === state.active_index);

            if (isActive) {
                dot.className = 'party-ball-dot ball-active';
                dot.title = `Slot ${i + 1}: ${mon.name} (Active - ${mon.hp}/${mon.max_hp} HP)`;
            } else if (!isFainted) {
                dot.className = 'party-ball-dot ball-conscious';
                dot.title = `Slot ${i + 1}: ${mon.name} (Ready - ${mon.hp}/${mon.max_hp} HP)`;
            } else {
                dot.className = 'party-ball-dot ball-fainted';
                dot.title = `Slot ${i + 1}: ${mon.name} (Fainted)`;
            }
        } else {
            dot.className = 'party-ball-dot ball-empty';
            dot.title = `Slot ${i + 1}: Empty (Catch wild Pokémon to add!)`;
        }
        playerPartyBalls.appendChild(dot);
    }
}

function openPartySwitchModal(isVoluntary = true) {
    if (!state.party || state.party.length === 0) return;

    sound.playClick();
    modalPartySwitch.classList.remove('hidden');

    if (isVoluntary) {
        partySwitchTitle.textContent = "CHOOSE A POKÉMON";
        partySwitchSubtitle.textContent = "Select a conscious Pokémon from your 4-member party to switch in (this uses your turn):";
        if (btnCancelPartySwitch) btnCancelPartySwitch.style.display = 'block';
        if (btnClosePartySwitch) btnClosePartySwitch.style.display = 'block';
    } else {
        partySwitchTitle.textContent = "POKÉMON FAINTED!";
        partySwitchSubtitle.textContent = "Your Pokémon fainted and cannot fight! Choose your next teammate to send out:";
        if (btnCancelPartySwitch) btnCancelPartySwitch.style.display = 'none';
        if (btnClosePartySwitch) btnClosePartySwitch.style.display = 'none';
    }

    renderPartySwitchList(isVoluntary);
}

function renderPartySwitchList(isVoluntary) {
    if (!partySwitchList) return;
    partySwitchList.innerHTML = '';

    state.party.forEach((mon, idx) => {
        const card = document.createElement('div');
        const isActive = (idx === state.active_index);
        const isFainted = Boolean(mon.is_fainted || mon.hp <= 0);

        let cardClass = 'party-member-card';
        if (isActive) cardClass += ' is-active';
        if (isFainted) cardClass += ' is-fainted';
        card.className = cardClass;

        const hpPct = Math.max(0, Math.min(100, (mon.hp / mon.max_hp) * 100));
        let hpColor = 'hp-green';
        if (hpPct <= 20) hpColor = 'hp-red';
        else if (hpPct <= 50) hpColor = 'hp-yellow';

        let actionHtml = '';
        if (isActive && !isFainted) {
            actionHtml = `<span class="badge-status-active">IN BATTLE</span>`;
        } else if (isFainted) {
            actionHtml = `<span class="badge-status-fainted">FAINTED</span>`;
        } else {
            actionHtml = `<button class="btn-retro btn-switch-in" data-index="${idx}">GO! ➡️</button>`;
        }

        card.innerHTML = `
            <img class="party-member-sprite" src="${mon.front_sprite || '/static/images/sprites/pikachu.gif'}" alt="${mon.name}">
            <div class="party-member-info">
                <div class="party-member-header">
                    <span class="party-member-name">${mon.name.toUpperCase()}</span>
                    <span class="badge-level">Lv. ${mon.level || 5}</span>
                </div>
                <div class="party-member-hp-row">
                    <span>HP: ${mon.hp} / ${mon.max_hp}</span>
                    <span>${mon.poke_type || 'Normal'}</span>
                </div>
                <div class="hp-bar-bg" style="height: 6px;">
                    <div class="hp-bar-fill ${hpColor}" style="width: ${hpPct}%;"></div>
                </div>
            </div>
            <div class="party-member-actions">
                ${actionHtml}
            </div>
        `;

        partySwitchList.appendChild(card);
    });

    // Attach click listeners to the GO! buttons
    partySwitchList.querySelectorAll('.btn-switch-in').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const targetIdx = parseInt(e.currentTarget.getAttribute('data-index'), 10);
            executeSwitchPokemon(targetIdx, isVoluntary);
        });
    });
}

async function executeSwitchPokemon(targetIdx, isVoluntary) {
    if (state.busy) return;
    state.busy = true;
    sound.playClick();
    modalPartySwitch.classList.add('hidden');

    try {
        const res = await fetch('/api/switch_pokemon', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                target_index: targetIdx,
                is_voluntary: isVoluntary
            })
        });

        const data = await res.json();
        if (!res.ok || data.student_error) {
            showBugCatcher(data);
            state.busy = false;
            return;
        }

        // Update state
        state.player = data.player;
        if (data.party) state.party = data.party;
        if (data.active_index !== undefined) state.active_index = data.active_index;
        if (data.enemy) state.enemy = data.enemy;

        // Visual update
        playerSprite.classList.remove('anim-faint');
        playerSprite.style.opacity = '1';
        updateHpUI();
        updateBattleUI();
        updatePartyBallsUI();

        // Process combat animations/events if any
        if (data.events && data.events.length > 0) {
            await playCombatEvents(data.events, data.dialogue);
        } else if (data.dialogue && data.dialogue.length > 0) {
            await runDialogueSequence(data.dialogue);
        }

        // Check if incoming pokemon fainted from counter-attack
        if (data.switch_required) {
            sound.playFaint();
            playerSprite.classList.add('anim-faint');
            await wait(600);
            openPartySwitchModal(false);
            return;
        }

        if (data.battle_over) {
            sound.playFaint();
            setDialogue("All your Pokémon have fainted! You blacked out and rushed to Pokémon Center...");
            await wait(1800);
            triggerNextBattle();
            return;
        }

    } catch (err) {
        showBugCatcher({
            file: "team.py",
            function: "switch_pokemon",
            message: err.message,
            hint: "Check your Pokémon team switching logic!"
        });
    } finally {
        state.busy = false;
    }
}

async function handleTeamAction(action, payload) {
    sound.playClick();
    try {
        const res = await fetch('/api/team/manage', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: action, ...payload })
        });
        const data = await res.json();
        if (!res.ok || data.student_error) {
            alert(data.message || "Team action could not be completed.");
            return;
        }

        if (data.party) state.party = data.party;
        if (data.active_index !== undefined) state.active_index = data.active_index;
        if (data.storage) state.storage = data.storage;
        if (data.pokedex) {
            state.pokedex = data.pokedex;
            if (pokedexCount) pokedexCount.textContent = state.pokedex.length;
        }
        if (data.player) state.player = data.player;

        updateHpUI();
        updateBattleUI();
        updatePartyBallsUI();
        renderPokedex();

        if (data.message) {
            setDialogue(data.message);
        }
    } catch (err) {
        console.error("Team manage error:", err);
    }
}

async function handleHealPartyTeam() {
    sound.playHeal();
    await handleTeamAction('heal_all', {});
    alert("❤️ Nurse Joy: Your entire Pokémon team has been fully healed back to maximum HP!");
}

async function handlePlayerAttack(moveName) {
    if (state.busy) return;
    state.busy = true;
    showMainActions();

    try {
        const res = await fetch('/api/attack', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ move: moveName })
        });

        const data = await res.json();

        if (!res.ok || data.student_error) {
            showBugCatcher(data);
            return;
        }

        // Animate Combat Events Sequentially
        await playCombatEvents(data.events, data.dialogue);

        // Update state
        state.player = data.player;
        state.enemy = data.enemy;
        if (data.party) state.party = data.party;
        if (data.active_index !== undefined) state.active_index = data.active_index;
        if (data.badges) {
            state.badges = data.badges;
            if (badgesCount) badgesCount.textContent = `${state.badges.length}/5`;
        }
        if (data.potions !== undefined) {
            state.potions = data.potions;
            if (potionCount) potionCount.textContent = state.potions;
        }
        updateHpUI();
        updateBattleUI();
        updatePartyBallsUI();

        if (data.switch_required) {
            sound.playFaint();
            playerSprite.classList.add('anim-faint');
            await wait(600);
            openPartySwitchModal(false);
            return;
        }

        if (data.battle_over) {
            if (data.is_gym_victory) {
                sound.playBadgeFanfare();
                showBadgeModal(data);
                if (enemyBadgeIcon) enemyBadgeIcon.classList.add('hidden');
                state.is_gym_battle = false;
            } else if (data.victory) {
                sound.playCatchSuccess();
                showVictoryModal(`You defeated the wild ${data.enemy.name}!`, "VICTORY!", data.exp_gained);
            } else {
                sound.playFaint();
                setDialogue(`${state.player.name} fainted! All your Pokémon fainted! Rushing to Pokémon Center...`);
                if (enemyBadgeIcon) enemyBadgeIcon.classList.add('hidden');
                state.is_gym_battle = false;
                setTimeout(() => triggerNextBattle(), 2000);
            }
        }

    } catch (err) {
        showBugCatcher({
            file: "battle.py",
            function: "calculate_damage",
            message: err.message,
            hint: "Check calculate_damage() in battle.py!"
        });
    } finally {
        state.busy = false;
    }
}

async function handleUsePotion() {
    if (state.busy) return;
    if (state.potions <= 0) {
        setDialogue("You don't have any Potions left!");
        return;
    }

    state.busy = true;
    showMainActions();

    try {
        const res = await fetch('/api/item', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ item: 'potion' })
        });
        const data = await res.json();

        if (!res.ok || data.student_error) {
            showBugCatcher(data);
            return;
        }

        sound.playHeal();
        state.player = data.player;
        state.potions = data.potions;
        if (data.party) state.party = data.party;
        if (data.active_index !== undefined) state.active_index = data.active_index;
        potionCount.textContent = state.potions;
        updateHpUI();
        updatePartyBallsUI();

        await playCombatEvents(data.events, data.dialogue);

        if (data.switch_required) {
            sound.playFaint();
            playerSprite.classList.add('anim-faint');
            await wait(600);
            openPartySwitchModal(false);
            return;
        }

        if (data.battle_over) {
            sound.playFaint();
            setDialogue(`${state.player.name} fainted! All your Pokémon fainted! Rushing to Pokémon Center...`);
            setTimeout(() => triggerNextBattle(), 2000);
        }

    } catch (err) {
        showBugCatcher({
            file: "pokemon.py",
            function: "heal",
            message: err.message,
            hint: "Check heal() in pokemon.py!"
        });
    } finally {
        state.busy = false;
    }
}

async function handleThrowBall(ballType) {
    if (state.busy) return;
    state.busy = true;
    showMainActions();

    try {
        const res = await fetch('/api/catch', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ball_type: ballType })
        });
        const data = await res.json();

        if (!res.ok || data.student_error) {
            if (data.gym_catch_blocked) {
                setDialogue(data.message || "You can't catch a Gym Leader's Pokémon!");
                sound.playTone(200, 'sawtooth', 0.2);
                return;
            }
            showBugCatcher(data);
            return;
        }

        // Play Ball Throw Animation
        await playCatchAnimation(ballType, data.shakes, data.caught);

        if (data.caught) {
            sound.playCatchSuccess();
            state.pokedex = data.pokedex;
            pokedexCount.textContent = state.pokedex.length;
            if (data.player) {
                state.player = data.player;
            }
            if (data.party) state.party = data.party;
            if (data.active_index !== undefined) state.active_index = data.active_index;
            updateBattleUI();
            updateHpUI();
            updatePartyBallsUI();
            showVictoryModal(`Gotcha! Wild ${state.enemy.name} was caught!`, "POKÉMON CAUGHT!", data.exp_gained);
        } else {
            // Show escape text
            if (data.dialogue && data.dialogue.length > 0) {
                setDialogue(data.dialogue[0]);
                await wait(800);
            }

            // Retaliation events (if any)
            if (data.events && data.events.length > 1) {
                await playCombatEvents(data.events.slice(1), data.dialogue.slice(1));
            }

            if (data.party) state.party = data.party;
            if (data.active_index !== undefined) state.active_index = data.active_index;
            updatePartyBallsUI();

            if (data.switch_required) {
                sound.playFaint();
                playerSprite.classList.add('anim-faint');
                await wait(600);
                openPartySwitchModal(false);
                return;
            }

            if (data.battle_over) {
                sound.playFaint();
                setDialogue(`${state.player.name} fainted! All your Pokémon fainted! Rushing to Pokémon Center...`);
                setTimeout(() => triggerNextBattle(), 2000);
            }
        }

    } catch (err) {
        showBugCatcher({
            file: "catching.py",
            function: "attempt_catch",
            message: err.message,
            hint: "Check attempt_catch() in catching.py!"
        });
    } finally {
        state.busy = false;
    }
}

async function playCombatEvents(events, dialogueList) {
    for (let i = 0; i < events.length; i++) {
        const ev = events[i];
        if (dialogueList && dialogueList[i]) {
            setDialogue(dialogueList[i]);
        }

        if (ev.type === 'player_attack') {
            playerSprite.classList.add('anim-lunge-forward');
            await wait(200);
            if (ev.is_critical) sound.playCritical(); else sound.playHit();
            enemySprite.classList.add('anim-hurt');
            showDamageFloat(enemyDamageFloat, `-${ev.damage}`);
            state.enemy.hp = ev.enemy_hp;
            updateHpUI();
            await wait(450);
            playerSprite.classList.remove('anim-lunge-forward');
            enemySprite.classList.remove('anim-hurt');

        } else if (ev.type === 'enemy_attack') {
            enemySprite.classList.add('anim-lunge-enemy');
            await wait(200);
            if (ev.is_critical) sound.playCritical(); else sound.playHit();
            playerSprite.classList.add('anim-hurt');
            showDamageFloat(playerDamageFloat, `-${ev.damage}`);
            state.player.hp = ev.player_hp;
            updateHpUI();
            await wait(450);
            enemySprite.classList.remove('anim-lunge-enemy');
            playerSprite.classList.remove('anim-hurt');

        } else if (ev.type === 'enemy_faint') {
            sound.playFaint();
            enemySprite.classList.add('anim-faint');
            await wait(700);

        } else if (ev.type === 'player_faint') {
            sound.playFaint();
            playerSprite.classList.add('anim-faint');
            await wait(700);

        } else if (ev.type === 'heal') {
            sound.playHeal();
            showDamageFloat(playerDamageFloat, `+${ev.healed}`, '#2ecc71');
            await wait(500);

        } else if (ev.type === 'level_up') {
            sound.playLevelUp();
            showDamageFloat(playerDamageFloat, `LEVEL UP! Lv. ${ev.level}`, '#f1c40f');
            if (playerLevel) playerLevel.textContent = `Lv. ${ev.level}`;
            if (state.player) {
                state.player.level = ev.level;
                state.player.max_hp = ev.max_hp;
                state.player.hp = ev.max_hp;
            }
            updateHpUI();
            await wait(900);

        } else if (ev.type === 'evolution') {
            sound.playEvolution();
            await playEvolutionCutscene(ev);

        } else if (ev.type === 'gym_next_mon') {
            sound.playHit();
            state.enemy = ev.enemy;
            enemyName.textContent = ev.enemy.name.toUpperCase();
            if (enemyLevel) enemyLevel.textContent = `Lv. ${ev.enemy.level || 5}`;
            enemyHpMax.textContent = ev.enemy.max_hp;
            enemyHpCur.textContent = ev.enemy.hp;
            enemySprite.src = ev.enemy.front_sprite;
            enemySprite.classList.remove('anim-faint');
            enemySprite.style.opacity = '1';
            updateHpUI();
            await wait(800);

        } else if (ev.type === 'badge_earned') {
            sound.playBadgeFanfare();
            await wait(600);
        }
    }
}

async function playCatchAnimation(ballType, shakes, caught) {
    setDialogue(`Threw a ${ballType.replace('-', ' ').toUpperCase()}!`);
    pokeballAnimContainer.classList.remove('hidden');
    animPokeball.src = `/static/images/sprites/${ballType}.png`;
    animStars.classList.add('hidden');

    animPokeball.className = 'anim-pokeball ball-arc';
    await wait(700);

    // Enemy hides inside ball
    enemySprite.style.opacity = '0';

    // Ball shakes
    for (let s = 1; s <= shakes; s++) {
        animPokeball.className = 'anim-pokeball ball-wobble';
        sound.playBallShake();
        setDialogue(`Shake ${s}...`);
        await wait(600);
    }

    if (caught) {
        animStars.classList.remove('hidden');
        await wait(600);
    } else {
        // Break free!
        enemySprite.style.opacity = '1';
        pokeballAnimContainer.classList.add('hidden');
        await wait(300);
    }

    pokeballAnimContainer.classList.add('hidden');
    enemySprite.style.opacity = '1';
}

function showDamageFloat(elem, text, color = '#e74c3c') {
    elem.textContent = text;
    elem.style.color = color;
    elem.style.opacity = '1';
    elem.style.transform = 'translateY(-15px)';
    elem.style.transition = 'all 0.5s ease-out';
    setTimeout(() => {
        elem.style.opacity = '0';
        elem.style.transform = 'translateY(0)';
    }, 600);
}

// --------------------------------------------------------------------------
// 6. NEXT BATTLE & POKEDEX
// --------------------------------------------------------------------------
async function triggerNextBattle() {
    state.busy = true;
    try {
        const res = await fetch('/api/next_battle', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
        });
        const data = await res.json();

        if (!res.ok || data.student_error) {
            showBugCatcher(data);
            return;
        }

        if (data.success) {
            state.player = data.player;
            state.enemy = data.enemy;
            if (data.party) state.party = data.party;
            if (data.active_index !== undefined) state.active_index = data.active_index;
            state.is_gym_battle = false;
            if (enemyBadgeIcon) enemyBadgeIcon.classList.add('hidden');
            if (data.badges) {
                state.badges = data.badges;
                if (badgesCount) badgesCount.textContent = `${state.badges.length}/5`;
            }
            playerSprite.classList.remove('anim-faint');
            enemySprite.classList.remove('anim-faint');
            playerSprite.style.opacity = '1';
            enemySprite.style.opacity = '1';
            updateBattleUI();
            updateHpUI();
            updatePartyBallsUI();
            setDialogue(data.dialogue[0]);
        }
    } catch (err) {
        showBugCatcher({
            file: "battle.py",
            function: "next_battle",
            message: err.message,
            hint: "Check your battle logic!"
        });
    } finally {
        state.busy = false;
    }
}

function renderPokedex() {
    // 1. Render Active 4-Pokémon Battle Party Grid
    if (pokedexPartyGrid) {
        pokedexPartyGrid.innerHTML = '';
        const maxSlots = 4;
        for (let i = 0; i < maxSlots; i++) {
            const card = document.createElement('div');
            if (i < state.party.length) {
                const mon = state.party[i];
                const isActive = (i === state.active_index);
                const isFainted = Boolean(mon.is_fainted || mon.hp <= 0);

                let slotClass = 'pokedex-slot-card';
                if (isActive) slotClass += ' is-active';
                card.className = slotClass;

                const curExp = mon.exp || 0;
                const maxExp = mon.max_exp || 100;
                const hpPct = Math.max(0, Math.min(100, (mon.hp / mon.max_hp) * 100));

                let actionBtns = '';
                if (!isActive && !isFainted) {
                    actionBtns += `<button class="btn-slot-lead" data-idx="${i}">SET LEAD</button>`;
                }
                if (state.party.length > 1) {
                    actionBtns += `<button class="btn-slot-deposit" data-idx="${i}">DEPOSIT</button>`;
                }

                card.innerHTML = `
                    <img class="pokedex-slot-sprite" src="${mon.front_sprite || '/static/images/sprites/pikachu.gif'}" alt="${mon.name}">
                    <div class="pokedex-slot-info">
                        <div class="pokedex-slot-title">
                            <span>${mon.name.toUpperCase()}</span>
                            <span class="badge-level">Lv. ${mon.level || 5}</span>
                        </div>
                        <div class="pokedex-slot-stats">
                            HP: ${mon.hp}/${mon.max_hp} | EXP: ${curExp}/${maxExp}
                        </div>
                        <div class="hp-bar-bg" style="height: 5px; margin-top: 2px;">
                            <div class="hp-bar-fill ${isFainted ? 'hp-red' : (hpPct > 50 ? 'hp-green' : 'hp-yellow')}" style="width: ${hpPct}%;"></div>
                        </div>
                    </div>
                    <div class="pokedex-slot-actions">
                        ${isActive ? '<span class="badge-status-active">LEAD</span>' : actionBtns}
                    </div>
                `;
            } else {
                card.className = 'pokedex-slot-card empty-slot';
                card.innerHTML = `<span>⚪ Empty Slot ${i + 1}</span>`;
            }
            pokedexPartyGrid.appendChild(card);
        }

        // Attach listeners for deposit and set lead
        pokedexPartyGrid.querySelectorAll('.btn-slot-lead').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const idx = parseInt(e.currentTarget.getAttribute('data-idx'), 10);
                await handleTeamAction('swap_slots', { index1: 0, index2: idx });
            });
        });

        pokedexPartyGrid.querySelectorAll('.btn-slot-deposit').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const idx = parseInt(e.currentTarget.getAttribute('data-idx'), 10);
                await handleTeamAction('deposit', { index: idx });
            });
        });
    }

    // 2. Render Registered Pokémon in Pokédex / PC Storage
    if (!pokedexList) return;
    if (!state.pokedex || state.pokedex.length === 0) {
        pokedexList.innerHTML = `<div class="empty-pokedex">No Pokémon registered yet! Pick a starter or catch wild Pokémon during battle!</div>`;
        return;
    }

    pokedexList.innerHTML = '';
    const partyNames = state.party.map(m => m.name.toLowerCase());

    state.pokedex.forEach(name => {
        const monCard = document.createElement('div');
        monCard.className = 'pokedex-mon-card';
        const inParty = partyNames.includes(name.toLowerCase());
        const spriteUrl = `/static/images/sprites/${name.toLowerCase()}.gif`;

        let actionHtml = '';
        if (inParty) {
            actionHtml = `<span class="badge-in-party">⭐ IN PARTY</span>`;
        } else if (state.party.length < 4) {
            actionHtml = `<button class="btn-add-to-party" data-species="${name}">➕ BRING (SLOT ${state.party.length + 1})</button>`;
        } else {
            actionHtml = `<button class="btn-add-to-party" data-species="${name}" data-swap="true">🔄 SWAP INTO PARTY</button>`;
        }

        monCard.innerHTML = `
            <div class="pokedex-mon-left">
                <img class="pokedex-mon-sprite" src="${spriteUrl}" alt="${name}" onerror="this.src='/static/images/sprites/pikachu.gif'">
                <span class="pokedex-mon-name">${name.toUpperCase()}</span>
            </div>
            <div>
                ${actionHtml}
            </div>
        `;

        pokedexList.appendChild(monCard);
    });

    // Attach click listeners to BRING / SWAP buttons
    pokedexList.querySelectorAll('.btn-add-to-party').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const species = e.currentTarget.getAttribute('data-species');
            const isSwap = e.currentTarget.getAttribute('data-swap') === 'true';

            if (isSwap && state.party.length >= 4) {
                await handleTeamAction('deposit', { index: state.party.length - 1 });
            }
            await handleTeamAction('add_from_pokedex', { species: species });
        });
    });
}

function showVictoryModal(msg, title = "VICTORY!", exp = null) {
    victoryTitle.textContent = title;
    victoryMessage.textContent = msg;
    if (victoryExp) {
        if (exp) {
            victoryExp.textContent = `⭐ +${exp} EXP Gained!`;
        } else {
            victoryExp.textContent = `⭐ +60 EXP Gained!`;
        }
    }
    if (victoryPlayerStatus && state.player) {
        const curExp = state.player.exp || 0;
        const lvl = state.player.level || 5;
        const toNext = Math.max(0, 100 - curExp);
        victoryPlayerStatus.textContent = `${state.player.name.toUpperCase()}: Lv. ${lvl} (${curExp} / 100 EXP — ${toNext} to next Level)`;
    }
    modalVictory.classList.remove('hidden');
}

async function playEvolutionCutscene(ev) {
    if (!modalEvolution) return;
    evolutionAnnouncement.textContent = `What? ${ev.old_name.toUpperCase()} is evolving!`;
    evoSpriteOld.src = `/static/images/sprites/${ev.old_name.toLowerCase()}.gif`;
    evoSpriteNew.src = ev.front_sprite;
    evolutionCongrats.textContent = `Congratulations! Your ${ev.old_name.toUpperCase()} evolved into ${ev.new_name.toUpperCase()}!`;
    modalEvolution.classList.remove('hidden');

    if (state.player) {
        state.player.name = ev.new_name;
        state.player.front_sprite = ev.front_sprite;
        state.player.back_sprite = ev.back_sprite;
        playerSprite.src = ev.back_sprite || ev.front_sprite;
        playerName.textContent = ev.new_name.toUpperCase();
    }

    await new Promise(resolve => {
        let resolved = false;
        const timer = setTimeout(() => {
            if (!resolved) {
                resolved = true;
                modalEvolution.classList.add('hidden');
                resolve();
            }
        }, 4000);

        const onClick = () => {
            if (!resolved) {
                resolved = true;
                clearTimeout(timer);
                modalEvolution.classList.add('hidden');
                resolve();
            }
        };
        if (btnCloseEvolution) {
            btnCloseEvolution.onclick = onClick;
        }
    });
}

function showBugCatcher(data) {
    sound.playTone(200, 'sawtooth', 0.25);
    errFile.textContent = data.file || "Python File";
    errFunction.textContent = data.function || "Function";
    errMessage.textContent = data.message || "An unexpected error occurred.";
    errHint.textContent = data.hint || "Review your code logic and parameters!";
    modalBug.classList.remove('hidden');
}

function setDialogue(text) {
    dialogueText.textContent = text;
}

function runDialogueSequence(lines) {
    if (!lines || lines.length === 0) return;
    let idx = 0;
    setDialogue(lines[0]);
    const interval = setInterval(() => {
        idx++;
        if (idx < lines.length) {
            setDialogue(lines[idx]);
        } else {
            clearInterval(interval);
        }
    }, 2000);
}

function wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// --------------------------------------------------------------------------
// 7. GYM SYSTEM CONTROLLER
// --------------------------------------------------------------------------
async function openGymModal() {
    sound.playClick();
    try {
        const res = await fetch('/api/gyms');
        const data = await res.json();
        if (data.success) {
            state.badges = data.badges || [];
            if (badgesCount) badgesCount.textContent = `${state.badges.length}/5`;
            renderGymCards(data.gyms);
            modalGym.classList.remove('hidden');
        }
    } catch (err) {
        console.error("Failed to load Gyms:", err);
    }
}

function renderGymCards(gyms) {
    if (!gymsListContainer) return;
    gymsListContainer.innerHTML = '';

    gyms.forEach(gym => {
        const card = document.createElement('div');
        const isDefeated = gym.is_defeated;
        const isUnlocked = gym.is_unlocked;
        const statusClass = isDefeated ? 'defeated' : (isUnlocked ? 'unlocked' : 'locked');
        card.className = `gym-card ${statusClass}`;

        let statusLabel = '🔒 LOCKED';
        if (isDefeated) {
            statusLabel = '🏆 DEFEATED';
        } else if (isUnlocked) {
            statusLabel = '⚔️ UNLOCKED';
        }

        const teamNames = (gym.team_preview || []).map(m => `${m.name} (Lv.${m.level})`).join(', ');

        card.innerHTML = `
            <div class="gym-card-header">
                <div>
                    <span class="gym-badge-icon">${gym.badge_icon}</span>
                    <span class="gym-title">${gym.name.toUpperCase()}</span>
                </div>
                <span class="gym-status-banner ${statusClass}">${statusLabel}</span>
            </div>
            <div class="gym-leader-info">
                <div><strong>Leader:</strong> ${gym.leader} (${gym.title})</div>
                <div><strong>City:</strong> ${gym.city} | <strong>Type:</strong> <span class="type-badge type-${gym.type}">${gym.type.toUpperCase()}</span></div>
                <div><strong>Rec. Level:</strong> Lv. ${gym.recommended_level}</div>
                <div><strong>Team:</strong> ${teamNames}</div>
            </div>
            <div class="gym-meta-row">
                <span class="badge-tag">${gym.badge_icon} ${gym.badge_name.toUpperCase()}</span>
                <span style="font-size: 7px; color: #7f8c8d;">+${gym.reward_exp} EXP</span>
            </div>
            ${isUnlocked && state.player ? `
                <button class="btn-retro ${isDefeated ? 'btn-blue' : 'btn-yellow'} btn-small btn-challenge-gym" style="margin-top: 6px; width: 100%;">
                    ${isDefeated ? 'RE-CHALLENGE GYM ⚔️' : 'CHALLENGE GYM! ⚔️'}
                </button>
            ` : (isUnlocked && !state.player ? `
                <button class="btn-retro btn-back btn-small" style="margin-top: 6px; width: 100%;" disabled>
                    PICK STARTER FIRST
                </button>
            ` : `
                <div style="font-size: 8px; color: #7f8c8d; text-align: center; margin-top: 6px; font-weight: bold;">
                    Defeat previous Gym Leaders to unlock
                </div>
            `)}
        `;

        const btnChallenge = card.querySelector('.btn-challenge-gym');
        if (btnChallenge) {
            btnChallenge.addEventListener('click', () => startGymChallenge(gym.id));
        }

        gymsListContainer.appendChild(card);
    });
}

async function startGymChallenge(gymId) {
    if (state.busy) return;
    if (!state.player) {
        setDialogue("Choose a starter Pokémon first before challenging Gym Leaders!");
        return;
    }

    state.busy = true;
    modalGym.classList.add('hidden');
    sound.playClick();
    setDialogue("Entering the Pokémon Gym...");

    try {
        const res = await fetch('/api/gym/challenge', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ gym_id: gymId })
        });

        const data = await res.json();
        if (!res.ok || data.student_error) {
            showBugCatcher(data);
            return;
        }

        state.player = data.player;
        state.enemy = data.enemy;
        if (data.party) state.party = data.party;
        if (data.active_index !== undefined) state.active_index = data.active_index;
        state.is_gym_battle = true;

        // Show enemy badge icon in HUD
        if (enemyBadgeIcon && data.gym) {
            enemyBadgeIcon.textContent = data.gym.badge_icon;
            enemyBadgeIcon.title = `${data.gym.leader}'s ${data.gym.badge_name}`;
            enemyBadgeIcon.classList.remove('hidden');
        }

        playerSprite.classList.remove('anim-faint');
        enemySprite.classList.remove('anim-faint');
        playerSprite.style.opacity = '1';
        enemySprite.style.opacity = '1';

        updateBattleUI();
        updateHpUI();
        updatePartyBallsUI();

        screenStarter.classList.remove('active');
        screenBattle.classList.add('active');

        runDialogueSequence(data.dialogue);

    } catch (err) {
        showBugCatcher({
            file: "gym.py",
            function: "startGymChallenge",
            message: err.message,
            hint: "Check gym challenge logic!"
        });
    } finally {
        state.busy = false;
    }
}

function showBadgeModal(info) {
    if (!modalBadge) return;
    badgeModalTitle.textContent = `${(info.leader || 'GYM LEADER').toUpperCase()}'S GYM DEFEATED!`;
    badgeAnimIcon.textContent = info.badge_icon || '🏆';
    badgeModalName.textContent = `${(info.badge_earned || 'BADGE').toUpperCase()} EARNED!`;
    badgeModalDialogue.textContent = `Leader ${info.leader || 'Brock'}: "Incredible battle, Trainer! Take this official League Badge as proof of your victory!"`;
    badgeRewardExp.textContent = `⭐ +${info.exp_gained || 150} EXP Gained!`;
    badgeRewardItems.textContent = `💊 Potions: ${state.potions} in Bag`;
    modalBadge.classList.remove('hidden');
}

