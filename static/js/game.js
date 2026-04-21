const socket = io();
let minha_room = "";
let meu_nome = "";
let ultima_escolha = ""; 
let chosen = false;
let ans = document.getElementById("ans");
let btnpronto = document.getElementById("btnpronto");
let round_c = document.getElementById("round_count")

function entrar() {
    meu_nome = document.getElementById('username').value;
    if (!meu_nome) return alert("Digite um nome!");
    socket.emit('join_game', {username: meu_nome});
}

socket.on('waiting', (data) => {
    document.getElementById('msg').innerText = data.msg;
});

socket.on('game_start', (room) => {
    minha_room = room.id;
    document.getElementById('lobby').style.display = 'none';
    document.getElementById('jogo').style.display = 'block';
    desenhar_round(room.round);
    desenhar_placar(room.players);
    ans.innerText = "";
    round_c.innerText = room.round_c + "/213"
});

socket.on('update_round', (placar) => {
    desenhar_placar(placar);
    colorir_meu_botao(placar);
});

socket.on('interval', (data) => {
    desenhar_placar(data.placar);
    ans.innerText = 'R: ' + data.answer;
    btnpronto.style.display = 'block';
    
    colorir_meu_botao(data.placar);
});

socket.on('new_round', (room) => {
    chosen = false;
    ultima_escolha = "";
    desenhar_placar(room.players);
    desenhar_round(room.round);
    btnpronto.style.display = 'none';
    btnpronto.classList.remove('btn-ready-active', 'btn-fade');
    btnpronto.innerText = "Pronto";
    ans.innerText = "";
    round_c.innerText = room.round_c + "/213"
});

function pronto() {
    socket.emit('ready', {room_id: minha_room});
    btnpronto.classList.add('btn-ready-active', 'btn-fade');
    btnpronto.innerText = "Aguardando...";
}

function colorir_meu_botao(placar) {
    const meu_status = placar[socket.id].status;
    if (meu_status !== "waiting" && ultima_escolha) {
        const meu_btn = document.getElementById("opt-" + ultima_escolha);
        if (meu_btn) {
            meu_btn.classList.remove('btn-fade');
            if (meu_status === "correct") {
                meu_btn.classList.add('btn-correct');
            } else if (meu_status === "incorrect") {
                meu_btn.classList.add('btn-incorrect');
            }
        }
    }
}

function desenhar_placar(placar) {
    const pldiv = document.getElementById("placar");
    pldiv.innerHTML = ''; 
    Object.values(placar).forEach(player => {
        const playerElement = document.createElement("div");
        playerElement.className = "player-card";
        let statusIcon = "";
        if (player.status === "correct") statusIcon = " ✅";
        else if (player.status === "incorrect") statusIcon = " ❌";
        playerElement.innerText = `${player.username}: ${player.score}${statusIcon}`;
        pldiv.appendChild(playerElement);
    });
}      

function desenhar_round(round) {
    document.getElementById('bandeira').src = `https://flagcdn.com/w320/${round.flag}.png`;
    const div = document.getElementById('opcoes');
    div.style.display = 'block';
    div.innerHTML = '';
    
    for (const [code, name] of Object.entries(round.options)) {
        let btn = document.createElement('button');
        btn.innerText = name;
        btn.id = "opt-" + code;
        btn.onclick = () => {
            if (chosen) return;
            ultima_escolha = code;
            socket.emit('send_ans', {room_id: minha_room, answer: code});
            chosen = true;

            const allBtns = div.querySelectorAll('button');
            allBtns.forEach(b => b.classList.add('btn-fade'));
        };
        div.appendChild(btn);
    }
}
