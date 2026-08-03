const config = window.MARKET_CONFIG;

const ticker = config.ticker;
const assetType = config.asset_type;
const previousClose = config.previous_close;

let currentPrice = config.initial_price;
let lastTimestamp = config.timestamp;

document.getElementById("ticker").innerHTML = ticker;

function updateWidget(price, timestamp = null) {
  currentPrice = price;

  if (timestamp !== null) {
    lastTimestamp = timestamp;
    updateSessionInfo();
  }

  document.getElementById("price").innerHTML = "$" + price.toFixed(2);

  if (previousClose !== null) {
    const change = price - previousClose;
    const changePct = (change / previousClose) * 100;

    const positive = change >= 0;

    const element = document.getElementById("change");

    element.innerHTML =
      `${positive ? "+" : ""}${change.toFixed(2)} ` +
      `(${positive ? "+" : ""}${changePct.toFixed(2)}%)`;

    element.className = positive ? "change positive" : "change negative";
  }
}

function setStatus(text, color) {
  const element = document.getElementById("status");

  element.innerHTML = text;
  element.style.color = color;
}

function updateMarketStatus() {
  if (assetType === "crypto") {
    setStatus("● MARKET OPEN 24/7", "#22c55e");
    return;
  }

  const now = new Date();

  const ny = new Date(
    now.toLocaleString("en-US", {
      timeZone: "America/New_York",
    }),
  );

  const day = ny.getDay();

  if (day === 0 || day === 6) {
    setStatus("● MARKET CLOSED", "#94a3b8");
    return;
  }

  const minutes = ny.getHours() * 60 + ny.getMinutes();

  if (minutes >= 570 && minutes < 960) {
    setStatus("● MARKET OPEN", "#22c55e");
  } else {
    setStatus("● MARKET CLOSED", "#94a3b8");
  }
}

function formatLastUpdate() {
  if (!lastTimestamp) {
    return "";
  }

  return new Date(lastTimestamp * 1000).toLocaleString();
}

function updateSessionInfo() {
  document.getElementById("session-info").innerHTML = lastTimestamp
    ? `Last update: ${formatLastUpdate()}`
    : "";
}

const channel = new BroadcastChannel("market_prices");

channel.onmessage = (event) => {
  const data = event.data;

  if (data.ticker !== ticker) {
    return;
  }

  updateWidget(Number(data.price), Number(data.timestamp));
};

if (currentPrice !== null) {
  updateWidget(Number(currentPrice), lastTimestamp);
}

updateMarketStatus();
updateSessionInfo();

setInterval(updateMarketStatus, 60000);
