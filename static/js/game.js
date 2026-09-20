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
    potions: 3,
    pokedex: [],
    busy: false
};

// DOM Elements
const screenStarter = document.getElementById('screen-starter-select');
const screenBattle = document.getElementById('screen-battle');
const starterContainer = document.getElementById('starter-cards-container');

const dialogueText = document.getElementById('dialogue-text');
const mainActionsGrid = document.getElementById('main-actions-grid');
const movesGrid = document.getElementById('moves-grid');
const bagMenu = document.getElementById('bag-menu');
const catchMenu = document.getElementById('catch-menu');

const playerSprite = document.getElementById('player-sprite');
const playerName = document.getElementById('player-name');
const playerHpFill = document.getElementById('player-hp-fill');
const playerHpCur = document.getElementById('player-hp-cur');
const playerHpMax = document.getElementById('player-hp-max');
const playerDamageFloat = document.getElementById('player-damage-float');

const enemySprite = document.getElementById('enemy-sprite');
const enemyName = document.getElementById('enemy-name');
const enemyHpFill = document.getElementById('enemy-hp-fill');
const enemyHpCur = document.getElementById('enemy-hp-cur');
const enemyHpMax = document.getElementById('enemy-hp-max');
const enemyDamageFloat = document.getElementById('enemy-damage-float');

const potionCount = document.getElementById('potion-count');
const pokedexCount = document.getElementById('pokedex-count');
const btnSound = document.getElementById('btn-sound');
const btnToggleMode = document.getElementById('btn-toggle-mode');
const modeText = document.getElementById('mode-text');

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
const btnNextBattle = document.getElementById('btn-next-battle');

const modalPokedex = document.getElementById('modal-pokedex');
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

    // Run button
    document.getElementById('btn-run').addEventListener('click', () => {
        if (state.busy) return;
        sound.playClick();
        setDialogue("Got away safely! Finding another wild Pokémon...");
        setTimeout(() => triggerNextBattle(), 1200);
    });

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
        if (data.pokedex) {
            state.pokedex = data.pokedex;
            pokedexCount.textContent = state.pokedex.length;
        }

        updateHpUI();
        updateBattleUI();

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
    playerHpMax.textContent = state.player.max_hp;
    playerSprite.src = state.player.back_sprite || state.player.front_sprite;

    enemyName.textContent = state.enemy.name.toUpperCase();
    enemyHpMax.textContent = state.enemy.max_hp;
    enemySprite.src = state.enemy.front_sprite;
    enemySprite.classList.remove('anim-faint');

    potionCount.textContent = state.potions;

    // Render Moves
    movesGrid.innerHTML = '';
    state.player.moves.forEach(moveName => {
        const btn = document.createElement('button');
        btn.className = 'btn-retro btn-move';
        btn.innerHTML = `
            <span>${moveName.toUpperCase()}</span>
            <span class="move-power">POW: 40+</span>
        `;
        btn.addEventListener('click', () => handlePlayerAttack(moveName));
        movesGrid.appendChild(btn);
    });

    const backBtn = document.createElement('button');
    backBtn.className = 'btn-retro btn-back';
    backBtn.textContent = 'BACK';
    backBtn.addEventListener('click', showMainActions);
    movesGrid.appendChild(backBtn);
}

function updateHpUI() {
    if (!state.player || !state.enemy) return;

    // Player HP
    playerHpCur.textContent = state.player.hp;
    const playerPct = Math.max(0, Math.min(100, (state.player.hp / state.player.max_hp) * 100));
    playerHpFill.style.width = `${playerPct}%`;
    setHpColor(playerHpFill, playerPct);

    // Enemy HP
    enemyHpCur.textContent = state.enemy.hp;
    const enemyPct = Math.max(0, Math.min(100, (state.enemy.hp / state.enemy.max_hp) * 100));
    enemyHpFill.style.width = `${enemyPct}%`;
    setHpColor(enemyHpFill, enemyPct);
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
        updateHpUI();

        if (data.battle_over) {
            if (data.victory) {
                sound.playCatchSuccess();
                showVictoryModal(`You defeated the wild ${data.enemy.name}!`);
            } else {
                sound.playFaint();
                setDialogue(`${state.player.name} fainted! Better train more!`);
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
        potionCount.textContent = state.potions;
        updateHpUI();

        await playCombatEvents(data.events, data.dialogue);

    } catch (err) {
        console.error(err);
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
            showBugCatcher(data);
            return;
        }

        // Play Ball Throw Animation
        await playCatchAnimation(ballType, data.shakes, data.caught);

        if (data.caught) {
            sound.playCatchSuccess();
            state.pokedex = data.pokedex;
            pokedexCount.textContent = state.pokedex.length;
            showVictoryModal(`Gotcha! Wild ${state.enemy.name} was caught!`, "POKÉMON CAUGHT!");
        } else {
            // Retaliation events
            await playCombatEvents(data.events.slice(1), data.dialogue);
            if (data.battle_over) {
                sound.playFaint();
                setDialogue(`${state.player.name} fainted!`);
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

        } else if (ev.type === 'heal') {
            sound.playHeal();
            showDamageFloat(playerDamageFloat, `+${ev.healed}`, '#2ecc71');
            await wait(500);
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
        if (data.success) {
            state.player = data.player;
            state.enemy = data.enemy;
            enemySprite.style.opacity = '1';
            updateBattleUI();
            updateHpUI();
            setDialogue(data.dialogue[0]);
        }
    } catch (err) {
        console.error(err);
    } finally {
        state.busy = false;
    }
}

function renderPokedex() {
    if (!state.pokedex || state.pokedex.length === 0) {
        pokedexList.innerHTML = `<div class="empty-pokedex">No Pokémon registered yet! Pick a starter or catch wild Pokémon during battle!</div>`;
        return;
    }
    pokedexList.innerHTML = '';
    state.pokedex.forEach(name => {
        const item = document.createElement('div');
        item.className = 'pokedex-item';
        item.innerHTML = `<span>🔴 ${name}</span>`;
        pokedexList.appendChild(item);
    });
}

function showVictoryModal(msg, title = "VICTORY!") {
    victoryTitle.textContent = title;
    victoryMessage.textContent = msg;
    modalVictory.classList.remove('hidden');
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
