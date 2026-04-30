const socket = io();

const GameSocket = {
    join: (nome, mode) => socket.emit('join_' + mode, {username: nome}),
    sendAnswer: (roomId, code) => socket.emit('send_ans', {room_id: roomId, ans: code}),
    sendReady: (roomId) => socket.emit('ready', {room_id: roomId}),

    setupListeners: (handlers) => {
        socket.on('waiting_players', handlers.onWaiting);
        socket.on('new_round', handlers.onNewRound);
        socket.on('interval', handlers.onInterval);
        socket.on('update_round', handlers.onUpdateRound)
    },

    getSocketId: () => socket.id
};
