const UI = {
    elements: {},

    init() {
        this.elements = {
            lobby: document.getElementById('lobby'),
            jogo: document.getElementById('jogo'),
            opcoes: document.getElementById('opcoes'),
            placar: document.getElementById('placar'),
            bandeira: document.getElementById('bandeira'),
            ans: document.getElementById('ans'),
            btnPronto: document.getElementById('btnpronto'),
            roundCount: document.getElementById('round_count'),
            username: document.getElementById('username'),
            msg: document.getElementById('msg')
        };
    },

    showGame(show) {
        this.elements.lobby.style.display = show ? 'none' : 'block';
        this.elements.jogo.style.display = show ? 'block' : 'none';
    },

    updateMsg(text) {
        if (this.elements.msg) this.elements.msg.innerText = text;
    },

    drawPlacar(placar) {
        this.elements.placar.innerHTML = '';
        Object.values(placar).forEach(player => {
            const div = document.createElement("div");
            div.className = "player-card";
            let icon = player.status === "correct" ? " ✅" : (player.status === "incorrect" ? " ❌" : "");
            div.innerText = `${player.name}: ${player.score}${icon}`;
            this.elements.placar.appendChild(div);
        });
    },

    drawRound(roomData, onOptionClick) {
        this.elements.ans.innerText = "";
        this.elements.bandeira.src = `https://flagcdn.com/w320/${roomData.flag}.png`;
        this.elements.opcoes.innerHTML = '';
        this.elements.roundCount.innerText = `${roomData.round_c}/213`;
        roomData.options.forEach(option => {
            const code = option[0]; // 'sg'
            const name = option[1]; // 'Singapura'

            let btn = document.createElement('button');
            btn.innerText = name;
            btn.id = "opt-" + code;
            btn.onclick = () => onOptionClick(code);
            this.elements.opcoes.appendChild(btn);
        });
    },

    colorButton(code, status) {
        const btn = document.getElementById("opt-" + code);
        if (!btn) return;
        btn.classList.remove('btn-fade');
        btn.classList.add(status === "correct" ? 'btn-correct' : 'btn-incorrect');
    },

    fadeButtons() {
        const btns = this.elements.opcoes.querySelectorAll('button');
        btns.forEach(b => b.classList.add('btn-fade'));
    },

    setReadyState(waiting) {
        this.elements.btnPronto.innerText = waiting ? "Aguardando..." : "Pronto";
        if (waiting) this.elements.btnPronto.classList.add('btn-ready-active', 'btn-fade');
        else this.elements.btnPronto.classList.remove('btn-ready-active', 'btn-fade');
    }
};
