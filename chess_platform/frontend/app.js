const boardEl = document.getElementById('board');
const statusText = document.getElementById('status-text');
const connectBtn = document.getElementById('connectBtn');
let socket;
let selectedSquare = null;
let currentFen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';
let lastMove = null;

const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
const ranks = [8, 7, 6, 5, 4, 3, 2, 1];
const pieceSymbols = {
  p: '♟', r: '♜', n: '♞', b: '♝', q: '♛', k: '♚',
  P: '♙', R: '♖', N: '♘', B: '♗', Q: '♕', K: '♔'
};

function getRoomName() {
  const match = window.location.pathname.match(/\/room\/([^/]+)/);
  return match ? match[1] : 'default';
}

function makeRoomName() {
  return Math.random().toString(36).slice(2, 10);
}

function createRoom() {
  const roomName = makeRoomName();
  window.location.href = '/room/' + roomName;
}

function createBoard() {
  if (!boardEl) return;
  boardEl.innerHTML = '';

  for (let rank = 0; rank < 8; rank++) {
    for (let file = 0; file < 8; file++) {
      const square = document.createElement('div');
      const squareName = files[file] + ranks[rank];

      square.className = 'square ' + (((rank + file) % 2) ? 'dark' : 'light');
      square.dataset.square = squareName;
      square.addEventListener('click', onSquareClick);
      boardEl.appendChild(square);
    }
  }

  renderBoard(currentFen);
}

function parseFen(fen) {
  const board = {};
  if (!fen) return board;

  const [positions] = fen.split(' ');
  const ranksArray = positions.split('/');

  ranksArray.forEach((rankRow, rankIndex) => {
    let fileIndex = 0;
    for (const char of rankRow) {
      if (!isNaN(parseInt(char, 10))) {
        fileIndex += parseInt(char, 10);
        continue;
      }
      if (fileIndex < 8) {
        const square = files[fileIndex] + (8 - rankIndex);
        board[square] = pieceSymbols[char] || '';
        fileIndex += 1;
      }
    }
  });

  return board;
}

function renderBoard(fen) {
  currentFen = fen;
  const pieceMap = parseFen(fen);
  document.querySelectorAll('.square').forEach((square) => {
    const coordinate = square.dataset.square;
    square.textContent = pieceMap[coordinate] || '';
    square.classList.remove('selected', 'last-move');

    if (lastMove && (coordinate === lastMove.from || coordinate === lastMove.to)) {
      square.classList.add('last-move');
    }

    if (selectedSquare === coordinate) {
      square.classList.add('selected');
    }
  });
}

function onSquareClick(event) {
  const square = event.currentTarget.dataset.square;

  if (!selectedSquare) {
    selectedSquare = square;
    event.currentTarget.classList.add('selected');
    return;
  }

  if (selectedSquare === square) {
    clearSelection();
    return;
  }

  sendMove(selectedSquare, square);
  clearSelection();
}

function clearSelection() {
  selectedSquare = null;
  document.querySelectorAll('.square').forEach((sq) => sq.classList.remove('selected'));
}

function updateStatus(text) {
  if (statusText) {
    statusText.textContent = text;
  }
}

function connectSocket() {
  if (socket && socket.readyState === WebSocket.OPEN) {
    return;
  }

  const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
  const roomName = getRoomName();
  const url = protocol + '://' + window.location.host + '/ws/game/' + roomName + '/';
  socket = new WebSocket(url);

  socket.addEventListener('open', () => {
    updateStatus('Connected to room: ' + roomName);
    socket.send(JSON.stringify({ type: 'join.match', room_name: roomName }));
  });

  socket.addEventListener('message', (event) => {
    const data = JSON.parse(event.data);

    if (data.type === 'match.joined') {
      renderBoard(data.fen);
      updateStatus('Room: ' + data.room_name + '. Turn: ' + data.turn);
      return;
    }

    if (data.type === 'match.state') {
      renderBoard(data.fen);
      updateStatus('Room synced. Turn: ' + data.turn);
      return;
    }

    if (data.type === 'move.made') {
      lastMove = { from: data.uci.slice(0, 2), to: data.uci.slice(2, 4) };
      renderBoard(data.fen);
      updateStatus('Move made: ' + data.san + '. Turn: ' + data.turn);
      return;
    }

    if (data.type === 'move.invalid') {
      updateStatus('Invalid move: ' + data.reason);
      return;
    }

    if (data.type === 'error') {
      updateStatus('Error: ' + data.message);
    }
  });

  socket.addEventListener('close', () => {
    updateStatus('Disconnected');
  });
}

function sendMove(from, to) {
  if (!socket || socket.readyState !== WebSocket.OPEN) {
    updateStatus('Socket not connected');
    return;
  }

  socket.send(JSON.stringify({
    type: 'move.make',
    room_name: getRoomName(),
    move: { uci: from + to },
    fen: currentFen,
  }));
}

if (connectBtn) {
  connectBtn.addEventListener('click', () => {
    if (window.location.pathname.startsWith('/room/')) {
      connectSocket();
      return;
    }
    createRoom();
  });
}

createBoard();
if (window.location.pathname.startsWith('/room/')) {
  connectSocket();
}