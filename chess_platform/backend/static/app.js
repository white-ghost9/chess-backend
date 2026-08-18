const boardEl = document.getElementById('board');
const statusText = document.getElementById('status-text');
const connectBtn = document.getElementById('connectBtn');
let socket;
let selectedSquare = null;
let legalMoves = [];
let currentFen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';
let lastMove = null;

const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
const ranks = [8, 7, 6, 5, 4, 3, 2, 1];

const pieceSvg = {
  wP: `<svg viewBox="0 0 45 45" width="32" height="32"><path d="M22.5 6c-2.9 0-5.2 2.3-5.2 5.2 0 1.4.5 2.7 1.3 3.7-4.9 1.3-8.6 5.2-8.6 10.1v2.9h25.1v-2.9c0-4.9-3.7-8.8-8.6-10.1.8-1 .1-2.3 1.3-3.7 0-2.9-2.3-5.2-5.2-5.2zm-8.6 18.8v2.4h28.2v-2.4H13.9zm3.7 7.6v1.7h20.8v-1.7H17.6zm5.9 5.4v2.5h8.9v-2.5h-8.9z" fill="#fff" stroke="#000" stroke-width="1.3" stroke-linejoin="round"/></svg>`,
  wR: `<svg viewBox="0 0 45 45" width="32" height="32"><path d="M9 35h27v3H9zm3-3h21v3H12zm2-4h17v3H14zm3-5h11v3H17zm-1-8.5h3v5h11v-5h3v5h3.5v3H12.5v-3H16zm3.5-6.5h9l1.5-4h-12l1.5 4z" fill="#fff" stroke="#000" stroke-width="1.3" stroke-linejoin="round"/></svg>`,
  wN: `<svg viewBox="0 0 45 45" width="32" height="32"><path d="M19.5 8.4c-3.9 0-7 3.1-7 7 0 2.1.9 4 2.3 5.3L14 28l6.2-2.4 2.1 9.9h6.2l-1.8-9.4 5-3.5c1.7-1.3 2.7-3.3 2.7-5.5 0-3.9-3.1-7-7-7-.9 0-1.7.2-2.5.5-1.8-3.3-5.1-5.5-8.9-5.5zm-8.8 16.1v2.2h25v-2.2h-25zm5 7.3v2.2h15v-2.2h-15z" fill="#fff" stroke="#000" stroke-width="1.3" stroke-linejoin="round"/></svg>`,
  wB: `<svg viewBox="0 0 45 45" width="32" height="32"><path d="M23 8c-2.6 0-4.7 2.1-4.7 4.7 0 1.2.4 2.3 1.1 3.2l-.6 2.5c-1.7.8-3.1 2.8-3.1 5.3v1.4h14.6v-1.4c0-2.5-1.4-4.5-3.1-5.3l-.6-2.5c.7-.9 1.1-2 1.1-3.2C27.7 10.1 25.6 8 23 8zm-9.8 16.1v2.6h28.6v-2.6H13.2zm4.3 7.6v2.4h20v-2.4h-20zm3.5 5.8v2.8h13v-2.8h-13z" fill="#fff" stroke="#000" stroke-width="1.3" stroke-linejoin="round"/></svg>`,
  wQ: `<svg viewBox="0 0 45 45" width="32" height="32"><path d="M13 34h19v3H13zm-2-6h23v3H11zm7-14.5h9l1.8-4h-12.6l1.8 4zm-1.9 8.5h13.8v3H16.1zm4.4-11.5h5.1v4.5h-5.1zm-4.9-6h14l3.7-4.5h-21.4zm15.3 27.5h5.9v2.8h-5.9zm-11.7 0h5.9v2.8H23.1z" fill="#fff" stroke="#000" stroke-width="1.3" stroke-linejoin="round"/></svg>`,
  wK: `<svg viewBox="0 0 45 45" width="32" height="32"><path d="M12 35h21v3H12zm3-4h15v3H15zm2-6h11v3H17zm-1-5.5h13v3H16zm2.5-6.5h8l1.2-4.5h-10.4zm-3.8-9.5h16l1.8 4.3h-19.6zm4.3 18.5h8.5v4.5h-8.5z" fill="#fff" stroke="#000" stroke-width="1.3" stroke-linejoin="round"/></svg>`,
  bP: `<svg viewBox="0 0 45 45" width="32" height="32"><path d="M22.5 6.5c-2.9 0-5.2 2.3-5.2 5.2 0 1.4.5 2.7 1.3 3.7-4.9 1.3-8.6 5.2-8.6 10.1v2.9h25.1v-2.9c0-4.9-3.7-8.8-8.6-10.1.8-1 .1-2.3 1.3-3.7 0-2.9-2.3-5.2-5.2-5.2zm-8.6 18.8v2.4h28.2v-2.4H13.9zm3.7 7.6v1.7h20.8v-1.7H17.6zm5.9 5.4v2.5h8.9v-2.5h-8.9z" fill="#000" stroke="#fff" stroke-width="1.1" stroke-linejoin="round"/></svg>`,
  bR: `<svg viewBox="0 0 45 45" width="32" height="32"><path d="M9 35h27v3H9zm3-3h21v3H12zm2-4h17v3H14zm3-5h11v3H17zm-1-8.5h3v5h11v-5h3v5h3.5v3H12.5v-3H16zm3.5-6.5h9l1.5-4h-12l1.5 4z" fill="#000" stroke="#fff" stroke-width="1.1" stroke-linejoin="round"/></svg>`,
  bN: `<svg viewBox="0 0 45 45" width="32" height="32"><path d="M19.5 8.4c-3.9 0-7 3.1-7 7 0 2.1.9 4 2.3 5.3L14 28l6.2-2.4 2.1 9.9h6.2l-1.8-9.4 5-3.5c1.7-1.3 2.7-3.3 2.7-5.5 0-3.9-3.1-7-7-7-.9 0-1.7.2-2.5.5-1.8-3.3-5.1-5.5-8.9-5.5zm-8.8 16.1v2.2h25v-2.2h-25zm5 7.3v2.2h15v-2.2h-15z" fill="#000" stroke="#fff" stroke-width="1.1" stroke-linejoin="round"/></svg>`,
  bB: `<svg viewBox="0 0 45 45" width="32" height="32"><path d="M23 8c-2.6 0-4.7 2.1-4.7 4.7 0 1.2.4 2.3 1.1 3.2l-.6 2.5c-1.7.8-3.1 2.8-3.1 5.3v1.4h14.6v-1.4c0-2.5-1.4-4.5-3.1-5.3l-.6-2.5c.7-.9 1.1-2 1.1-3.2C27.7 10.1 25.6 8 23 8zm-9.8 16.1v2.6h28.6v-2.6H13.2zm4.3 7.6v2.4h20v-2.4h-20zm3.5 5.8v2.8h13v-2.8h-13z" fill="#000" stroke="#fff" stroke-width="1.1" stroke-linejoin="round"/></svg>`,
  bQ: `<svg viewBox="0 0 45 45" width="32" height="32"><path d="M13 34h19v3H13zm-2-6h23v3H11zm7-14.5h9l1.8-4h-12.6l1.8 4zm-1.9 8.5h13.8v3H16.1zm4.4-11.5h5.1v4.5h-5.1zm-4.9-6h14l3.7-4.5h-21.4zm15.3 27.5h5.9v2.8h-5.9zm-11.7 0h5.9v2.8H23.1z" fill="#000" stroke="#fff" stroke-width="1.1" stroke-linejoin="round"/></svg>`,
  bK: `<svg viewBox="0 0 45 45" width="32" height="32"><path d="M12 35h21v3H12zm3-4h15v3H15zm2-6h11v3H17zm-1-5.5h13v3H16zm2.5-6.5h8l1.2-4.5h-10.4zm-3.8-9.5h16l1.8 4.3h-19.6zm4.3 18.5h8.5v4.5h-8.5z" fill="#000" stroke="#fff" stroke-width="1.1" stroke-linejoin="round"/></svg>`
};

function getPieceMarkup(piece) {
  if (!piece) return '';
  const key = `${piece.color === 'w' ? 'w' : 'b'}${piece.type.toUpperCase()}`;
  return pieceSvg[key] || '';
}

function createBoard() {
  if (!boardEl) return;
  boardEl.innerHTML = '';
  for (let rank = 0; rank < 8; rank++) {
    for (let file = 0; file < 8; file++) {
      const square = document.createElement('div');
      square.className = 'square ' + (((rank + file) % 2) ? 'dark' : 'light');
      square.dataset.square = `${files[file]}${ranks[rank]}`;
      square.addEventListener('click', onSquareClick);
      boardEl.appendChild(square);
    }
  }
  renderBoard(currentFen);
}

function parseFen(fen) {
  const board = {};
  const [positions] = fen.split(' ');
  const ranksArray = positions.split('/');
  ranksArray.forEach((rankRow, rankIndex) => {
    let fileIndex = 0;
    for (const char of rankRow) {
      if (Number.isInteger(Number(char))) {
        fileIndex += Number(char);
        continue;
      }
      const square = `${files[fileIndex]}${8 - rankIndex}`;
      const upperChar = char.toUpperCase();
      // Uppercase characters in FEN indicate White ('w'), lowercase indicate Black ('b')
      board[square] = { type: upperChar, color: char === upperChar ? 'w' : 'b' };
      fileIndex += 1;
    }
  });
  return board;
}

function renderBoard(fen) {
  currentFen = fen;
  const pieceMap = parseFen(fen);
  document.querySelectorAll('.square').forEach((square) => {
    const coordinate = square.dataset.square;
    square.innerHTML = '';
    const piece = pieceMap[coordinate];
    if (piece) {
      square.innerHTML = getPieceMarkup(piece);
    }
    square.classList.remove('selected', 'last-move', 'legal');

    if (lastMove && (coordinate === lastMove.from || coordinate === lastMove.to)) {
      square.classList.add('last-move');
    }

    if (selectedSquare && coordinate === selectedSquare) {
      square.classList.add('selected');
    }

    if (legalMoves.includes(coordinate)) {
      square.classList.add('legal');
    }
  });
}

function getLegalMovesFor(squareName) {
  const ChessCtor = window.Chess || (window.Chess && window.Chess.Chess);
  if (typeof ChessCtor !== 'function') return [];
  try {
    const game = new ChessCtor(currentFen);
    const moves = game.moves({ square: squareName, verbose: true });
    return moves.map((move) => move.to);
  } catch (err) {
    return [];
  }
}

function onSquareClick(event) {
  const square = event.currentTarget.dataset.square;
  if (!selectedSquare) {
    const ChessCtor = window.Chess || (window.Chess && window.Chess.Chess);
    if (typeof ChessCtor !== 'function') return;
    const game = new ChessCtor(currentFen);
    const piece = game.get(square);
    if (!piece) return;
    selectedSquare = square;
    legalMoves = getLegalMovesFor(square);
    renderBoard(currentFen);
    return;
  }

  if (selectedSquare === square) {
    selectedSquare = null;
    legalMoves = [];
    renderBoard(currentFen);
    return;
  }

  if (legalMoves.includes(square)) {
    sendMove(selectedSquare, square);
  }

  selectedSquare = null;
  legalMoves = [];
  renderBoard(currentFen);
}

function updateStatus(text) {
  if (statusText) statusText.textContent = text;
}

function connectSocket() {
  if (socket && socket.readyState === WebSocket.OPEN) {
    return;
  }

  const url = 'ws://127.0.0.1:8000/ws/game/default/';
  socket = new WebSocket(url);

  socket.addEventListener('open', () => {
    updateStatus('Connected to match...');
    socket.send(JSON.stringify({ type: 'join.match', room_name: 'default' }));
  });

  socket.addEventListener('message', (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'match.joined' || data.type === 'match.state') {
      currentFen = data.fen || currentFen;
      renderBoard(currentFen);
      updateStatus(`Match ready. Turn: ${data.turn}`);
      return;
    }
    if (data.type === 'move.made') {
      currentFen = data.fen || currentFen;
      lastMove = { from: data.uci.slice(0, 2), to: data.uci.slice(2, 4) };
      renderBoard(currentFen);
      updateStatus(`Move made: ${data.san}. Turn: ${data.turn}`);
      return;
    }
    if (data.type === 'move.invalid') {
      updateStatus(`Invalid move: ${data.reason}`);
      return;
    }
    if (data.type === 'error') {
      updateStatus(`Error: ${data.message}`);
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
    room_name: 'default',
    move: { uci: `${from}${to}` },
    fen: currentFen,
  }));
}

if (connectBtn) {
  connectBtn.addEventListener('click', connectSocket);
}
createBoard();