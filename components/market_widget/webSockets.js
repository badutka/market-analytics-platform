const config = window.MARKET_CONFIG;

const ticker = config.ticker;
const assetType = config.asset_type;
const initialPrice = config.initial_price;
const previousClose = config.previous_close;
const FINNHUB_API_KEY = config.finnhub_key;

let currentPrice = initialPrice !== null ? Number(initialPrice) : null;

document.getElementById("ticker").innerHTML = ticker;

function updateWidget(price) {
  currentPrice = price;

  document.getElementById("price").innerHTML = "$" + price.toFixed(2);

  if (previousClose !== null) {
    const change = ((price - previousClose) / previousClose) * 100;

    const changeElement = document.getElementById("change");

    changeElement.innerHTML =
      (change >= 0 ? "▲ +" : "▼ ") + change.toFixed(2) + "%";

    changeElement.style.color = change >= 0 ? "#22c55e" : "#ef4444";
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
      color: "#9ca3af",
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
    color: "#9ca3af",
  };
}

function updateMarketStatus() {
  if (assetType === "crypto") {
    setStatus("● MARKET OPEN (24/7)", "#22c55e");
    return;
  }

  const status = getStockMarketStatus();

  setStatus(status.text, status.color);
}

function connectBinance() {
  const symbol = ticker.replace("-USD", "").toLowerCase() + "usdt";

  const socket = new WebSocket(
    `wss://stream.binance.com:9443/ws/${symbol}@trade`,
  );

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);

    updateWidget(Number(data.p));
  };

  socket.onclose = () => {
    setTimeout(connectBinance, 5000);
  };

  socket.onerror = () => {
    socket.close();
  };
}

function connectFinnhub() {
  const socket = new WebSocket(`wss://ws.finnhub.io?token=${FINNHUB_API_KEY}`);

  socket.onopen = () => {
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
      updateWidget(Number(data.data[0].p));
    }
  };

  socket.onclose = () => {
    setTimeout(connectFinnhub, 5000);
  };

  socket.onerror = () => {
    socket.close();
  };
}

// Populate immediately from REST snapshot
if (currentPrice !== null) {
  updateWidget(currentPrice);
}

updateMarketStatus();

setInterval(updateMarketStatus, 60000);

if (assetType === "crypto") {
  connectBinance();
} else {
  connectFinnhub();
}
