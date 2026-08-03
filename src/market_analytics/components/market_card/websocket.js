const config = window.MARKET_CONFIG;

const ticker = config.ticker;
const assetType = config.asset_type;
const initialPrice = config.initial_price;
const previousClose = config.previous_close;
const FINNHUB_API_KEY = config.finnhub_key;

let currentPrice = initialPrice !== null ? Number(initialPrice) : null;
let lastTimestamp = config.timestamp !== null ? Number(config.timestamp) : null;
let socketStarted = false;

document.getElementById("ticker").innerHTML = ticker;

function updateWidget(price, timestamp = null) {
  currentPrice = price;

  if (timestamp !== null) {
    lastTimestamp = Number(timestamp);
    updateSessionInfo();
  }

  document.getElementById("price").innerHTML = "$" + price.toFixed(2);

  if (previousClose !== null) {
    const change = price - previousClose;
    const changePct = (change / previousClose) * 100;

    const changeElement = document.getElementById("change");

    const positive = change >= 0;

    changeElement.innerHTML =
      `${positive ? "+" : ""}${change.toFixed(2)} ` +
      `(${positive ? "+" : ""}${changePct.toFixed(2)}%)`;

    changeElement.className = positive ? "change positive" : "change negative";
  }
}

function setStatus(text, color) {
  const element = document.getElementById("status");

  element.innerHTML = text;
  element.style.color = color;
}

function getStockMarketStatus() {
  const now = new Date();

  const ny = new Date(
    now.toLocaleString("en-US", {
      timeZone: "America/New_York",
    }),
  );

  const day = ny.getDay();

  if (day === 0 || day === 6) {
    return {
      text: "● MARKET CLOSED",
      color: "#94a3b8",
    };
  }

  const minutes = ny.getHours() * 60 + ny.getMinutes();

  if (minutes >= 570 && minutes < 960) {
    return {
      text: "● MARKET OPEN",
      color: "#22c55e",
    };
  }

  if (minutes >= 240 && minutes < 570) {
    return {
      text: "● PRE-MARKET",
      color: "#f59e0b",
    };
  }

  if (minutes >= 960 && minutes < 1200) {
    return {
      text: "● AFTER HOURS",
      color: "#f59e0b",
    };
  }

  return {
    text: "● MARKET CLOSED",
    color: "#94a3b8",
  };
}

function updateMarketStatus() {
  if (assetType === "crypto") {
    setStatus("● MARKET OPEN 24/7", "#22c55e");
    return;
  }

  const status = getStockMarketStatus();

  setStatus(status.text, status.color);

  if (status.text === "● MARKET OPEN" && !socketStarted) {
    socketStarted = true;
    connectFinnhub();
  }
}

function formatLastUpdate() {
  if (lastTimestamp === null) {
    return "";
  }

  const date = new Date(lastTimestamp * 1000);

  const parts = new Intl.DateTimeFormat("en-GB", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    timeZoneName: "short",
  }).formatToParts(date);

  const year = parts.find((part) => part.type === "year")?.value;

  const month = parts.find((part) => part.type === "month")?.value;

  const day = parts.find((part) => part.type === "day")?.value;

  const hour = parts.find((part) => part.type === "hour")?.value;

  const minute = parts.find((part) => part.type === "minute")?.value;

  const zone = parts.find((part) => part.type === "timeZoneName")?.value;

  return `${year}-${month}-${day} ${hour}:${minute} ${zone}`;
}

function updateSessionInfo() {
  const element = document.getElementById("session-info");

  if (lastTimestamp === null) {
    element.innerHTML = "";
    return;
  }

  element.innerHTML = `Last update: ${formatLastUpdate()}`;
}

function connectBinance() {
  const symbol = ticker.replace("-USD", "").toLowerCase() + "usdt";

  const socket = new WebSocket(
    `wss://stream.binance.com:9443/ws/${symbol}@trade`,
  );

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);

    updateWidget(Number(data.p), Math.floor(data.T / 1000));
  };

  socket.onclose = () => {
    console.log("Binance disconnected:", ticker);

    setTimeout(connectBinance, 5000);
  };

  socket.onerror = () => {
    console.warn("Binance websocket unavailable:", ticker);
  };
}

function connectFinnhub() {
  const socket = new WebSocket(`wss://ws.finnhub.io?token=${FINNHUB_API_KEY}`);

  socket.onopen = () => {
    console.log("Finnhub connected:", ticker);

    socket.send(
      JSON.stringify({
        type: "subscribe",
        symbol: ticker,
      }),
    );
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);

    if (data.data) {
      const trade = data.data[0];

      updateWidget(Number(trade.p), Math.floor(trade.t / 1000));
    }
  };

  socket.onerror = () => {
    console.warn("Finnhub websocket unavailable:", ticker);
  };

  socket.onclose = (event) => {
    console.log(
      "Finnhub disconnected:",
      ticker,
      "code:",
      event.code,
      "reason:",
      event.reason,
    );

    socketStarted = false;

    setTimeout(() => {
      const status = getStockMarketStatus();

      if (status.text === "● MARKET OPEN") {
        connectFinnhub();
      }
    }, 30000);
  };
}

if (currentPrice !== null) {
  updateWidget(currentPrice, lastTimestamp);
}

updateMarketStatus();
updateSessionInfo();

setInterval(updateMarketStatus, 60000);

setInterval(updateSessionInfo, 60000);

if (assetType === "crypto") {
  connectBinance();
}
