const config = window.MARKET_CONFIG;

const channel = new BroadcastChannel("market_prices");

// ----------------------
// Finnhub stocks
// ----------------------

const finnhub = new WebSocket(
  `wss://ws.finnhub.io?token=${config.finnhub_key}`,
);

finnhub.onopen = () => {
  console.log("Finnhub connected");

  config.stock_tickers.forEach((symbol) => {
    finnhub.send(
      JSON.stringify({
        type: "subscribe",
        symbol,
      }),
    );

    console.log("Finnhub subscribed:", symbol);
  });
};

finnhub.onmessage = (event) => {
  const data = JSON.parse(event.data);

  if (data.type !== "trade") {
    return;
  }

  data.data.forEach((trade) => {
    channel.postMessage({
      ticker: trade.s,

      price: trade.p,

      volume: trade.v,

      timestamp: Math.floor(trade.t / 1000),
    });
  });
};

// ----------------------
// Binance crypto
// ----------------------

config.crypto_tickers.forEach((ticker) => {
  const symbol = ticker.replace("-USD", "").toLowerCase() + "usdt";

  const binance = new WebSocket(
    `wss://stream.binance.com:9443/ws/${symbol}@trade`,
  );

  binance.onopen = () => {
    console.log("Binance connected:", ticker);
  };

  binance.onmessage = (event) => {
    const data = JSON.parse(event.data);

    channel.postMessage({
      ticker,

      price: Number(data.p),

      volume: Number(data.q),

      timestamp: Math.floor(data.T / 1000),
    });
  };

  binance.onerror = (error) => {
    console.warn("Binance error:", ticker, error);
  };

  binance.onclose = () => {
    console.warn("Binance disconnected:", ticker);
  };
});
