function getUnixTimestamp(date) {
  return Math.floor(date.getTime() / 1000);
}

function getPeriodRange(interval) {
  const now = new Date();
  const end = getUnixTimestamp(now);
  let startDate = new Date(now);

  switch (interval) {
  case '1d':
    startDate.setMonth(now.getMonth() - 2); // 2 months lookback for daily data
    break;
  case '1wk':
    startDate.setMonth(now.getMonth() - 6); // 6 months lookback for weekly data
    break;
  case '1mo':
    startDate.setFullYear(now.getFullYear() - 1); // 1 year lookback for monthly data
    break;
  default:
    throw new Error(`Unsupported interval: ${interval}`);
}

  const start = getUnixTimestamp(startDate);
  return { start, end };
}

function stdDev(values) {
  const mean = values.reduce((a, b) => a + b, 0) / values.length;
  const variance = values.reduce((a, b) => a + (b - mean) ** 2, 0) / values.length;
  return Math.sqrt(variance);
}

async function fetchYahooFinanceChart(symbol, interval = '1d') {
  const { start: period1, end: period2 } = getPeriodRange(interval);
  const url = `https://query2.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(symbol)}?period1=${period1}&period2=${period2}&interval=${interval}&includePrePost=true&events=div%7Csplit%7Cearn&lang=en-US&region=US&source=cosaic`;

  try {
    const response = await fetch(url);
    const data = await response.json();

    if (!data.chart || !data.chart.result || data.chart.result.length === 0) {
      console.error('No data found in response');
      return;
    }

    const result = data.chart.result[0];
    const timestamps = result.timestamp;
    const indicators = result.indicators.quote[0];
    const closes = indicators.close;

    const finalData = timestamps.map((ts, i) => {
      const date = new Date(ts * 1000);
      return {
        timestamp: ts,
        day: date.toISOString().split('T')[0],
        hour: date.toISOString().split('T')[1].slice(0, 5),
        open: parseFloat(indicators.open[i]?.toFixed(2)),
        high: parseFloat(indicators.high[i]?.toFixed(2)),
        low: parseFloat(indicators.low[i]?.toFixed(2)),
        close: parseFloat(closes[i]?.toFixed(2)),
        volume: indicators.volume[i]
      };
    });

    // 1️⃣ Average high-low range
    const ranges = finalData.map(d => (d.high != null && d.low != null ? d.high - d.low : 0));
    const avgHighLowRange = parseFloat((ranges.reduce((a, b) => a + b, 0) / ranges.length).toFixed(2));

    // 2️⃣ Historical Volatility (log returns)
    const logReturns = [];
    for (let i = 1; i < closes.length; i++) {
      const prev = closes[i - 1];
      const curr = closes[i];
      if (prev > 0 && curr > 0) {
        logReturns.push(Math.log(curr / prev));
      }
    }
    const dailyHV = stdDev(logReturns);
    const hvBasedMove = parseFloat((closes[closes.length - 1] * dailyHV * Math.sqrt(closes.length)).toFixed(2));

    // 3️⃣ Standard deviation of daily close price changes
    const dailyDiffs = [];
    for (let i = 1; i < closes.length; i++) {
      const prev = closes[i - 1];
      const curr = closes[i];
      if (prev != null && curr != null) {
        dailyDiffs.push(curr - prev);
      }
    }
    const stdDevPriceChange = parseFloat(stdDev(dailyDiffs).toFixed(2));

    // 🔢 Output results
    console.log(`\n📈 Price movement analysis for ${symbol} over ${interval} period:`);
    console.log(`1. Avg High-Low Range: $${avgHighLowRange}`);
    console.log(`2. HV-Based Expected Move: $${hvBasedMove}`);
    console.log(`3. Std Dev of Daily Price Changes: $${stdDevPriceChange}`);

    return {
      data: finalData,
      metrics: {
        avgHighLowRange,
        hvBasedMove,
        stdDevPriceChange
      }
    };
  } catch (err) {
    console.error('Error fetching or processing data:', err);
  }
}

fetchYahooFinanceChart('TSLA', '1mo');
