const State = {
    room_id: "",
    chosen: false,
    ultima_escolha: ""
};

const actions = {
    handleJoin: (mode) => {
        const nome = UI.elements.username.value;
        if (!nome) return alert("Digite um nome!");
        GameSocket.join(nome, mode);
    },

    chooseOption: (code) => {
        if (State.chosen) return;
        State.chosen = true;
        State.ultima_escolha = code;
        UI.fadeButtons();
        GameSocket.sendAnswer(State.room_id, code);
    },

    pronto: () => {
        UI.setReadyState(true);
        GameSocket.sendReady(State.room_id);
    }
};

function pintarBotao(players) {
  if (State.ultima_escolha) {
    const meuStatus = players.find(p => p.sid === GameSocket.getSocketId())?.status;
    UI.colorButton(State.ultima_escolha, meuStatus);
  }
}

function init() {
    UI.init();

    GameSocket.setupListeners({
        onWaiting: (data) => UI.updateMsg(data.message),

        onUpdateRound: (data) => {
          UI.drawPlacar(data.players);
          pintarBotao(data.players);
        },

        onNewRound: (room) => {
            State.room_id = room.id || State.room_id; 
            State.chosen = false;
            State.ultima_escolha = "";
            UI.showGame(true);
            UI.drawPlacar(room.players);
            UI.drawRound(room, actions.chooseOption);
            UI.elements.btnPronto.style.display = 'none';
            UI.setReadyState(false);
        },

        onInterval: (data) => {
            UI.drawPlacar(data.players);
            UI.elements.btnPronto.style.display = 'block';
            pintarBotao(data.players);
        }
    });

    document.getElementById('btn-1v1').onclick = () => actions.handleJoin('1v1');
    document.getElementById('btn-solo').onclick = () => actions.handleJoin('solo');
    UI.elements.btnPronto.onclick = actions.pronto;
}

// Roda o init quando o HTML terminar de carregar
window.onload = init;
