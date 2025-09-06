async function checkProximity(records, proximityThreshold) {
  let outputList = []

  function toDate(input) {
    if (typeof input === "string") {
      const [year, month] = input.split("-").map(Number)
      return new Date(year, month - 1, 1).setHours(0, 0, 0, 0)
    } else if (typeof input === "number") {
      const date = new Date(input * 1000)
      return new Date(date.getUTCFullYear(), date.getUTCMonth(), 1).setHours(
        0,
        0,
        0,
        0
      )
    } else {
      throw new Error(
        "Invalid input type. Must be a date string or timestamp (seconds)."
      )
    }
  }

  const fetchAssetData = async (record) => {
    const now = Math.floor(Date.now() / 1000)
    let start = null
    const dates = [
      record.upper?.referenceDate1,
      record.lower?.referenceDate1,
    ].filter(Boolean)
    if (dates.length) {
      start = Math.floor(new Date(dates.sort()[0]).getTime() / 1000)
    }
    const url = start
      ? `https://query2.finance.yahoo.com/v8/finance/chart/${record.symbol}?period1=${start}&period2=${now}&interval=1mo`
      : `https://query2.finance.yahoo.com/v8/finance/chart/${record.symbol}`
    const response = await fetch(url)
    const data = await response.json()
    if (!data.chart?.result?.length)
      throw new Error(`No chart data for ${record.symbol}`)
    return data.chart.result[0]
  }

  const getCurrentResistancePrice = (line, data) => {
    if (!line.referenceDate2) return line.referencePrice1
    const getRefIndex = (ref) =>
      data.timestamp.findIndex((ts) => toDate(ts) === toDate(ref))

    const referenceIndex1 = getRefIndex(line.referenceDate1)
    const referenceIndex2 = getRefIndex(line.referenceDate2)

    if (referenceIndex1 == -1)
      throw new Error(
        `No chart data for ${data.meta.symbol} ` + line.referenceDate1
      )
    if (referenceIndex2 == -1)
      throw new Error(
        `No chart data for ${data.meta.symbol} ` + line.referenceDate2
      )
    const daysDistanceToCurrentDay = data.timestamp.length - 2 - referenceIndex2
    const distanceBetweenRefs = referenceIndex2 - referenceIndex1
    const slope =
      (line.referencePrice2 - line.referencePrice1) / distanceBetweenRefs
    return line.referencePrice2 + slope * daysDistanceToCurrentDay
  }

  const isPriceNearResistance = (price, resPrice, type) => {
    const upperLimit = (1 + proximityThreshold / 100) * resPrice
    const lowerLimit = (1 - proximityThreshold / 100) * resPrice
    if (type === "upper") return price >= lowerLimit
    if (type === "lower") return price <= upperLimit
  }

  for (const record of records) {
    try {
      let { symbol, upper, lower } = record
      if (symbol === "SAMPLE") continue
      let proximity = false
      let currentResistancePrice
      const assetData = await fetchAssetData(record)
      const currentPrice = assetData.meta.regularMarketPrice

      if (upper) {
        currentResistancePrice = getCurrentResistancePrice(
          upper,
          assetData,
          symbol
        )
        proximity = isPriceNearResistance(
          currentPrice,
          currentResistancePrice,
          "upper"
        )
      }
      if (lower && !proximity) {
        currentResistancePrice = getCurrentResistancePrice(
          lower,
          assetData,
          symbol
        )
        proximity =
          proximity ||
          isPriceNearResistance(currentPrice, currentResistancePrice, "lower")
      }
      if (proximity) outputList.push(symbol)
    } catch (error) {
      console.log(error)
    }
  }
  return outputList
}

const resistanceRecords = [
  {
    symbol: "NVDA",
    upper: {
      referenceDate1: "2024-11-01",
      referencePrice1: 153.46,
      referenceDate2: "2025-07-01",
      referencePrice2: 184.59,
    },
    lower: {
      referenceDate1: "2023-11-01",
      referencePrice1: 37.81,
      referenceDate2: "2025-06-02",
      referencePrice2: 114.22,
    },
  },
  {
    symbol: "VALE3.SA",
    upper: {
      referenceDate1: "2024-12-02",
      referencePrice1: 66.63,
      referenceDate2: "2025-05-02",
      referencePrice2: 60.11,
    },
    lower: {
      referencePrice1: 48.92,
    },
  },
  {
    symbol: "BOVA11.SA",
    upper: {
      referenceDate1: "2024-02-01",
      referencePrice1: 134.4,
      referenceDate2: "2025-04-01",
      referencePrice2: 140.08,
    },
    lower: {
      referenceDate1: "2023-05-02",
      referencePrice1: 95.71,
      referenceDate2: "2025-06-02",
      referencePrice2: 121.25,
    },
  },
  {
    symbol: "PETR4.SA",
    upper: {
      referencePrice1: 42.47,
    },
    lower: {
      referenceDate1: "2023-05-02",
      referencePrice1: 23.11,
      referenceDate2: "2025-06-02",
      referencePrice2: 28.72,
    },
  },
  {
    symbol: "ITUB4.SA",
    upper: {
      referenceDate1: "2024-05-02",
      referencePrice1: 44.98,
      referenceDate2: "2025-06-02",
      referencePrice2: 48.09,
    },
    lower: {
      referenceDate1: "2023-09-01",
      referencePrice1: 23.36,
      referenceDate2: "2025-01-02",
      referencePrice2: 27.29,
    },
  },

  {
    symbol: "CSAN3.SA",
    upper: {
      referenceDate1: "2025-08-15",
      referencePrice1: 169.8,
      referenceDate2: "2025-08-19",
      referencePrice2: 169.8,
    },
    lower: {
      referenceDate1: "2025-08-15",
      referencePrice1: 169.8,
    },
  },
  {
    symbol: "B3SA3.SA",
    upper: {
      referenceDate1: "2025-08-15",
      referencePrice1: 169.8,
      referenceDate2: "2025-08-19",
      referencePrice2: 169.8,
    },
    lower: {
      referenceDate1: "2025-08-15",
      referencePrice1: 169.8,
    },
  },
  {
    symbol: "SUZB3.SA",
    upper: {
      referenceDate1: "2025-08-15",
      referencePrice1: 169.8,
      referenceDate2: "2025-08-19",
      referencePrice2: 169.8,
    },
    lower: {
      referenceDate1: "2025-08-15",
      referencePrice1: 169.8,
    },
  },
  {
    symbol: "BRAV3.SA",
    upper: {
      referenceDate1: "2025-08-15",
      referencePrice1: 169.8,
      referenceDate2: "2025-08-19",
      referencePrice2: 169.8,
    },
    lower: {
      referenceDate1: "2025-08-15",
      referencePrice1: 169.8,
    },
  },
  {
    symbol: "ELET3.SA",
    upper: {
      referenceDate1: "2025-08-15",
      referencePrice1: 169.8,
      referenceDate2: "2025-08-19",
      referencePrice2: 169.8,
    },
    lower: {
      referenceDate1: "2025-08-15",
      referencePrice1: 169.8,
    },
  },
  {
    symbol: "SBSP3.SA",
    upper: {
      referenceDate1: "2025-08-15",
      referencePrice1: 169.8,
      referenceDate2: "2025-08-19",
      referencePrice2: 169.8,
    },
    lower: {
      referenceDate1: "2025-08-15",
      referencePrice1: 169.8,
    },
  },
  {
    symbol: "SAMPLE",
    upper: {
      referenceDate1: "2025-08-15",
      referencePrice1: 169.8,
      referenceDate2: "2025-08-19",
      referencePrice2: 169.8,
    },
    lower: {
      referenceDate1: "2025-08-15",
      referencePrice1: 169.8,
    },
  },
]

checkProximity(resistanceRecords, 2).then(console.dir)
