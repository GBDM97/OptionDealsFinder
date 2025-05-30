const toFloat = (val, decimals = 2) => {
  if((typeof val) !== 'string' && (typeof val) !== 'number' || val === '-' || !val ) return NaN;
  return parseFloat(parseFloat(val.toString().replace(',', '.')).toFixed(decimals));
}

const extractOptions = () => {
  const rows = Array.from(document.querySelectorAll('tbody'))[1].querySelectorAll("tr");
  const options = [];
  rows.forEach(row => {
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

const generateVerticalSpreads = (options, useMid, listType, price) => {
    const results = [];

    for (let i = 0; i < options.length; i++) {
        for (let j = 0; j < options.length; j++) {
          const o1 = options[i];
          const o2 = options[j];

          if (i === j) continue;
          if(o1.strike > o2.strike) continue;
          let long;
          let short;

          if(listType === 'OTMCalls'|| listType === 'ITMPuts'){
            short = o1
            long = o2
          }

          if(listType === 'ITMCalls'|| listType === 'OTMPuts'){
            short = o2
            long = o1
          }

          const longPrice = useMid ? long.mid : long.ask;
          const shortPrice = useMid ? short.mid : short.bid;

          const spreadWidth = Math.abs(short.strike - long.strike);
          const cost = longPrice - shortPrice;
          const isDebit = cost > 0;

          const maxProfit = isDebit ? spreadWidth - cost : cost *-1;
          const maxLoss = isDebit ? cost : (spreadWidth + cost);
          const gainPercentage = (maxProfit / maxLoss)*100;
          const distance = Math.abs(price - short.strike);

          if(listType === 'OTMCalls' && isDebit) continue;
          if(listType === 'OTMPuts' && isDebit) continue;
          if(maxProfit <= 0) continue;
          
          results.push({
              type: isDebit ? 'DebitSpread' : 'CreditSpread',
              gainPercentage: +(gainPercentage).toFixed(2),
              optionType: long.type + (listType === "OTMCalls" || listType === 'OTMPuts' ? " - OTM" : " - ITM"),
              shortStrike: short.strike,
              cost: +cost.toFixed(2),
              maxProfit: +maxProfit.toFixed(2),
              maxLoss: +maxLoss.toFixed(2),
              index: gainPercentage * distance,
              additionalInformation :{
                maxProfit: +maxProfit.toFixed(2),
                maxLoss: +maxLoss.toFixed(2),
                spreadWidth,
                distance,
                longStrike: long.strike,
                long,
                short
              }
          });
          }
    }
    return results.sort((a, b) => b.gainPercentage - a.gainPercentage);
};

const generateStructures = (spreads) => {
  ironCondors = [];
  hybrids = [];
  for (let i = 0; i < spreads.length; i++) {
    for (let j = 0; j < spreads.length; j++) {
      const s1 = spreads[i];
      const s2 = spreads[j];
      let hybrid = false;
      if (i === j) continue;
      if (s1.optionType === s2.optionType) continue;
      if (s1.shortStrike === s2.shortStrike) continue;

      if((s1.optionType === 'CALL - OTM' && s2.optionType === 'PUT - ITM')||
         (s1.optionType === 'CALL - ITM' && s2.optionType === 'PUT - OTM')||
         (s2.optionType === 'CALL - OTM' && s1.optionType === 'PUT - ITM')||
         (s2.optionType === 'CALL - ITM' && s1.optionType === 'PUT - OTM')){
            hybrid = true;
         }
      const s1p = s1.additionalInformation.maxProfit;
      const s2p = s2.additionalInformation.maxProfit;
      const s1l = s1.additionalInformation.maxLoss;
      const s2l = s2.additionalInformation.maxLoss;
      const structureMaxProfit = s1p + s2p;
      const structureMaxLoss = hybrid ? s1l + s2l : Math.min(s1p - s2l, s2p - s1l) *-1;
      const structureGainPercentage = (structureMaxProfit / structureMaxLoss) *100;
      const distance = Math.min(s1.additionalInformation.distance, s2.additionalInformation.distance);
      const index = (distance*25) + structureGainPercentage;

      if(structureGainPercentage < 20) continue;
      
      if(hybrid) {
        hybrids.push({
          gainPercentage: structureGainPercentage,
          structureMaxProfit,
          structureMaxLoss,
          index,
          s1,
          s2
        })
      } else {
        ironCondors.push({
          gainPercentage: structureGainPercentage,
          structureMaxProfit,
          structureMaxLoss,
          index,
          s1,
          s2
        })
      }
      
    }
  }
  hybrids.sort((a, b) => b.gainPercentage - a.gainPercentage);
  ironCondors.sort((a, b) => b.index - a.index);
  return {ironCondors,hybrids};
}

const find = (useMid = false, lowerResistance, upperResistance) => {
    let options = temp1;
    const price = Array.from(document.querySelector('tbody')
                                     .querySelector('tr')
                                     .querySelectorAll('td'))[2]
                                     .querySelector("td soma-caption").textContent.trim();
    const lowerLimit = toFloat(lowerResistance || price);
    const upperLimit = toFloat(upperResistance || price);
    const calls = options.filter(v => v.type === 'CALL');
    const OTMCalls = calls.filter(o => o.strike >= upperLimit);
    const ITMCalls = calls.filter(o => o.strike <= lowerLimit);
    const puts = options.filter(v => v.type === 'PUT');
    const ITMPuts = puts.filter(o => o.strike >= upperLimit);
    const OTMPuts = puts.filter(o => o.strike <= lowerLimit);

    const OTMCallsSpreads = generateVerticalSpreads(OTMCalls, useMid, 'OTMCalls', upperLimit);
    const ITMCallsSpreads = generateVerticalSpreads(ITMCalls, useMid, 'ITMCalls', lowerLimit);
    const ITMPutsSpreads = generateVerticalSpreads(ITMPuts, useMid, 'ITMPuts', upperLimit);
    const OTMPutsSpreads = generateVerticalSpreads(OTMPuts, useMid, 'OTMPuts', lowerLimit);
    const spreads = [...OTMCallsSpreads, ...ITMCallsSpreads, ...ITMPutsSpreads, ...OTMPutsSpreads];
    const structures = generateStructures(spreads);
    const all = [...structures.ironCondors, ...spreads].sort((a, b) => b.index - a.index);

    console.dir({all, ironCondors: structures.ironCondors, hybrids: structures.hybrids, spreads});
};

find();

//iterar por faixas de porcentagem de 1% pegando a melhor operação por distância
  //ordenar por porcentagem e iterar a lista, salva a primeira distancia, se encontrar uma distância maior sobreescreve, terminou a faixa, registra e vai pra próxima
//teste uma situação onde se encontraria travas de credito itm, pois são oportunidades de arbitragem
//pense em alguma verificação de distância da trava
//teste se os preços não estão sendo modificados pela ineficiência do js em calculos