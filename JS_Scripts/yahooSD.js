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

async function fecthAndComputeSTD(symbol, interval, maxAndMinMovement) {
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
      };
    }).filter(v=>v.open).filter(v=>v.high).filter(v=>v.low).filter(v=>v.close);

    let movementData;
    if (maxAndMinMovement){
      movementData = finalData.map((v, i) => [v.day ,Math.abs(v.high - v.low)]);
    } else {
      movementData = finalData.map((v, i) => i >= 1 ? [v.day ,Math.abs(v.close - finalData[i - 1].close)] : 0).slice(1);
    }
    const mean = movementData.reduce((sum, c) => sum + c[1], 0) / movementData.length;
    const variance = movementData.reduce((acc, c) => acc + ((c[1] - mean) ** 2), 0) / (movementData.length - 1);
    const stdDev = Math.sqrt(variance);
    const movementsPerSTDDev = movementData.map(v => [v[0],(v[1] / stdDev).toFixed(2)]);
    console.dir({
      symbol,
      interval,
      stdDev: stdDev.toFixed(2),
      movementsPerSTDDev,
    });
  } catch (err) {
    console.error('Error fetching or processing data:', err);
  }
}

const run = (ticker,maxAndMinMovement) => {
  fecthAndComputeSTD(ticker, '1d', maxAndMinMovement);
  fecthAndComputeSTD(ticker, '1wk', maxAndMinMovement);
  fecthAndComputeSTD(ticker, '1mo', maxAndMinMovement);
}

run('RUN', true)