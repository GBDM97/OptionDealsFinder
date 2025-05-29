const extractOptions = () => {
  const rows = document.evaluate("/html/body/div[1]/soma-context/div/div[3]/div/div[3]/arsenal-loader/div/div[5]/table/tbody",
                                  document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.rows;
  const options = [];
  const toFloat = (val, decimals = 2) => {
    if((typeof val) !== 'string' && (typeof val) !== 'number' || val === '-' || !val ) return NaN;
    return parseFloat(parseFloat(val.toString().replace(',', '.')).toFixed(decimals));
  }
  Array.from(rows).forEach(row => {
    const cells = Array.from(row.querySelectorAll("td")).map(v=>v.querySelector("td soma-caption").textContent.trim());
    const strike = toFloat(cells[5]);
    const callBid = toFloat(cells[3]);
    const callAsk = toFloat(cells[4]);
    const callMid = toFloat(((callBid + callAsk) / 2));
    const putBid = toFloat(cells[6]);
    const putAsk = toFloat(cells[7]);
    const putMid = toFloat(((putBid + putAsk) / 2));
    if(!isNaN(strike) && !isNaN(callBid) && !isNaN(callAsk) && !isNaN(callMid)){
        options.push({type: 'CALL', strike, bid: callBid, ask: callAsk, mid: callMid})
    }
    if(!isNaN(strike) && !isNaN(putBid) && !isNaN(putAsk) && !isNaN(putMid)){
        options.push({type: 'PUT', strike, bid: putBid, ask: putAsk, mid: putMid})
    }
  });
  return options.sort((a, b) => a.strike - b.strike);
};

const generateVerticalSpreads = (options, useMid) => {
    const results = [];

    for (let i = 0; i < options.length; i++) {
        for (let j = 0; j < options.length; j++) {
        if (i === j) continue;
        const o1 = options[i];
        const o2 = options[j];
        
        let long;
        let short;

        // if(o1.type === 'CALL'){
        //     long = 
        //     short = 
        // }

        // const longPrice = useMid ? long.mid : long.ask;
        // const shortPrice = useMid ? short.mid : short.bid;

        // const spreadWidth = Math.abs(short.strike - long.strike);
        // const cost = longPrice - shortPrice;
        // const isDebit = cost > 0;

        // const maxProfit = isDebit ? spreadWidth - cost : cost;
        // const maxLoss = isDebit ? cost : spreadWidth - cost;

        // if (maxLoss <= 0) continue;

        // results.push({
        //     type: isDebit ? 'DebitSpread' : 'CreditSpread',
        //     optionType: long.type,
        //     longStrike: long.strike,
        //     shortStrike: short.strike,
        //     cost: +cost.toFixed(2),
        //     maxProfit: +maxProfit.toFixed(2),
        //     maxLoss: +maxLoss.toFixed(2),
        //     gainPercentage: +(maxProfit / maxLoss).toFixed(2),
        // });
        }
    }

    return results;
};

const find = (lowerResistance, upperResistance, useMid = true) => {
    let options = extractOptions();
    const lowerLimit = parseFloat(lowerResistance);
    const upperLimit = parseFloat(upperResistance);
    const calls = options.filter(v => v.type === 'CALL');
    const upperCalls = calls.filter(o => o.strike >= upperLimit);
    const lowerCalls = calls.filter(o => o.strike <= lowerLimit);
    const puts = options.filter(v => v.type === 'PUT');
    const upperPuts = puts.filter(o => o.strike >= upperLimit);
    const lowerPuts = puts.filter(o => o.strike <= lowerLimit);

    const spreads = generateVerticalSpreads(upperCalls, useMid);
    // const condors = generateIronCondors(options, useMid);
    // const all = [...spreads, ...condors].sort((a, b) => b.gainPercentage - a.gainPercentage);

    console.log("Top 10 Combinations:");
    // console.log(JSON.stringify(all.slice(0, 10), null, 2));
};

find(130, 138, false);

