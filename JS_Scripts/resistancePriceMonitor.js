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
      start = toDate(dates.sort()[0]) / 1000
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

  for (const [index, record] of records.entries()) {
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
      console.log(index + 1 + " of " + String(records.length - 1))
    } catch (error) {
      console.log(error)
    }
  }
  console.dir({
    AssetsAnalyzed: {
      BR: records.filter(
        (record) =>
          record.symbol.toUpperCase().endsWith(".SA") &&
          record.symbol.toUpperCase() !== "SAMPLE"
      ).length,
      US: records.filter(
        (record) =>
          !record.symbol.toUpperCase().endsWith(".SA") &&
          record.symbol.toUpperCase() !== "SAMPLE"
      ).length,
    },
  })
  console.dir({
    BR: outputList.filter((record) => record.toUpperCase().endsWith(".SA")),
    US: outputList.filter((record) => !record.toUpperCase().endsWith(".SA")),
  })
}

const resistanceRecords = [
  {
    symbol: "GLD",
    lower: {
      referenceDate1: "2025-01-02",
      referencePrice1: 247.64,
      referenceDate2: "2025-07-01",
      referencePrice2: 286.44,
    },
  },
  {
    symbol: "SLV",
    upper: {
      referencePrice1: 43,
    },
    lower: {
      referenceDate1: "2024-10-01",
      referencePrice1: 31.24,
      referenceDate2: "2025-07-01",
      referencePrice2: 34.26,
    },
  },
  {
    symbol: "SPY",
    lower: {
      referenceDate1: "2024-09-03",
      referencePrice1: 455.03,
      referenceDate2: "2025-05-01",
      referencePrice2: 490.12,
    },
  },
  {
    symbol: "IWM",
    lower: {
      referenceDate1: "2024-09-03",
      referencePrice1: 169.5,
      referenceDate2: "2025-07-01",
      referencePrice2: 177.09,
    },
  },
  {
    symbol: "EWZ",
    upper: {
      referenceDate1: "2024-09-03",
      referencePrice1: 33.2,
      referenceDate2: "2025-05-01",
      referencePrice2: 31.18,
    },
    lower: {
      referencePrice1: 20,
    },
  },
  {
    symbol: "EEM",
    upper: {
      referencePrice1: 58,
    },
    lower: {
      referenceDate1: "2024-05-01",
      referencePrice1: 34.56,
      referenceDate2: "2025-07-01",
      referencePrice2: 35.75,
    },
  },
  {
    symbol: "XLU",
    upper: {
      referenceDate1: "2024-08-01",
      referencePrice1: 85.14,
      referenceDate2: "2025-05-01",
      referencePrice2: 86.77,
    },
    lower: {
      referenceDate1: "2024-12-02",
      referencePrice1: 60.41,
      referenceDate2: "2025-08-01",
      referencePrice2: 61.92,
    },
  },
  {
    symbol: "DIA",
    lower: {
      referenceDate1: "2025-04-01",
      referencePrice1: 368.34,
      referenceDate2: "2025-07-01",
      referencePrice2: 376.34,
    },
  },
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
    symbol: "MSFT",
    lower: {
      referenceDate1: "2025-04-01",
      referencePrice1: 348.15,
      referenceDate2: "2025-08-01",
      referencePrice2: 367.51,
    },
  },
  {
    symbol: "AAPL",
    lower: {
      referenceDate1: "2024-09-03",
      referencePrice1: 172.59,
      referenceDate2: "2025-07-01",
      referencePrice2: 195.02,
    },
  },
  {
    symbol: "GOOG",
    lower: {
      referenceDate1: "2025-02-03",
      referencePrice1: 139.4,
      referenceDate2: "2025-07-01",
      referencePrice2: 150.01,
    },
  },
  {
    symbol: "META",
    lower: {
      referenceDate1: "2025-03-03",
      referencePrice1: 585.33,
      referenceDate2: "2025-08-01",
      referencePrice2: 685.26,
    },
  },
  {
    symbol: "TSLA",
    upper: {
      referencePrice1: 420,
    },
    lower: {
      referenceDate1: "2025-03-03",
      referencePrice1: 202.5,
      referenceDate2: "2025-08-01",
      referencePrice2: 221.86,
    },
  },
  {
    symbol: "BRK-B",
    lower: {
      referenceDate1: "2025-03-03",
      referencePrice1: 425.26,
      referenceDate2: "2025-08-01",
      referencePrice2: 453.42,
    },
  },
  {
    symbol: "JPM",
    lower: {
      referenceDate1: "2025-03-03",
      referencePrice1: 226.47,
      referenceDate2: "2025-08-01",
      referencePrice2: 254.59,
    },
  },
  {
    symbol: "V",
    lower: {
      referenceDate1: "2025-03-03",
      referencePrice1: 286.04,
      referenceDate2: "2025-08-01",
      referencePrice2: 310.44,
    },
  },
  {
    symbol: "MA",
    lower: {
      referenceDate1: "2025-03-03",
      referencePrice1: 497.62,
      referenceDate2: "2025-08-01",
      referencePrice2: 536.31,
    },
  },
  {
    symbol: "JNJ",
    lower: {
      referenceDate1: "2025-03-03",
      referencePrice1: 139.59,
      referenceDate2: "2025-08-01",
      referencePrice2: 142.17,
    },
  },
  {
    symbol: "HD",
    lower: {
      referenceDate1: "2025-03-03",
      referencePrice1: 322.8,
      referenceDate2: "2025-08-01",
      referencePrice2: 336.15,
    },
  },
  {
    symbol: "PLTR",
    lower: {
      referenceDate1: "2025-03-03",
      referencePrice1: 76.78,
      referenceDate2: "2025-08-01",
      referencePrice2: 127.38,
    },
  },
  {
    symbol: "ABBV",
    lower: {
      referenceDate1: "2025-03-03",
      referencePrice1: 169.64,
      referenceDate2: "2025-08-01",
      referencePrice2: 178.93,
    },
  },
  {
    symbol: "BAC",
    lower: {
      referenceDate1: "2025-03-03",
      referencePrice1: 30.48,
      referenceDate2: "2025-08-01",
      referencePrice2: 31.71,
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
      referencePrice1: 8.78,
    },
  },
  {
    symbol: "B3SA3.SA",
    upper: {
      referencePrice1: 15.1,
    },
    lower: {
      referencePrice1: 9,
    },
  },
  {
    symbol: "SUZB3.SA",
    upper: {
      referencePrice1: 65.95,
    },
    lower: {
      referenceDate1: "2023-04-03",
      referencePrice1: 37.88,
      referenceDate2: "2025-07-01",
      referencePrice2: 48.69,
    },
  },
  {
    symbol: "BRAV3.SA",
    upper: {
      referenceDate1: "2024-12-02",
      referencePrice1: 28.757,
      referenceDate2: "2025-06-02",
      referencePrice2: 23.208,
    },
    lower: {
      referencePrice1: 15.457,
    },
  },
  {
    symbol: "ELET3.SA",
    upper: {
      referencePrice1: 45,
    },
    lower: {
      referencePrice1: 33.3,
    },
  },
  {
    symbol: "SBSP3.SA",
    upper: {
      referenceDate1: "2024-08-01",
      referencePrice1: 100.78,
      referenceDate2: "2025-07-01",
      referencePrice2: 124.53,
    },
    lower: {
      referenceDate1: "2025-01-02",
      referencePrice1: 86.02,
      referenceDate2: "2025-08-01",
      referencePrice2: 101.14,
    },
  },
  {
    symbol: "BBSE3.SA",
    upper: {
      referenceDate1: "2024-11-01",
      referencePrice1: 42.5,
      referenceDate2: "2025-08-01",
      referencePrice2: 42.9,
    },
    lower: {
      referenceDate1: "2024-12-02",
      referencePrice1: 30,
      referenceDate2: "2025-07-01",
      referencePrice2: 30.4,
    },
  },
  {
    symbol: "COGN3.SA",
    upper: {
      referencePrice1: 3.36,
    },
  },
  {
    symbol: "ITSA4.SA",
    upper: {
      referencePrice1: 11.18,
    },
    lower: {
      referenceDate1: "2023-11-01",
      referencePrice1: 7.59,
      referenceDate2: "2025-08-01",
      referencePrice2: 8.39,
    },
  },
  {
    symbol: "EMBR3.SA",
    upper: {
      referenceDate1: "2025-03-05",
      referencePrice1: 73.97,
      referenceDate2: "2025-08-01",
      referencePrice2: 86.55,
    },
    lower: {
      referenceDate1: "2025-04-01",
      referencePrice1: 58.13,
      referenceDate2: "2025-09-01",
      referencePrice2: 71.17,
    },
  },
  {
    symbol: "USIM5.SA",
    upper: {
      referenceDate1: "2024-10-01",
      referencePrice1: 8.57,
      referenceDate2: "2025-05-02",
      referencePrice2: 5.93,
    },
    lower: {
      referencePrice1: 0.82,
    },
  },
  {
    symbol: "CSNA3.SA",
    upper: {
      referenceDate1: "2023-11-01",
      referencePrice1: 21.24,
      referenceDate2: "2025-06-02",
      referencePrice2: 8.89,
    },
    lower: {
      referencePrice1: 2.79,
    },
  },
  {
    symbol: "SMAL11.SA",
    upper: {
      referenceDate1: "2024-10-01",
      referencePrice1: 114.04,
      referenceDate2: "2025-06-02",
      referencePrice2: 112.73,
    },
    lower: {
      referencePrice1: 84,
    },
  },
  {
    symbol: "MRFG3.SA",
    upper: {
      referencePrice1: 28,
    },
    lower: {
      referencePrice1: 5,
    },
  },
  {
    symbol: "CMIG4.SA",
    upper: {
      referenceDate1: "2024-06-03",
      referencePrice1: 12.38,
      referenceDate2: "2025-05-02",
      referencePrice2: 13.24,
    },
    lower: {
      referenceDate1: "2024-02-01",
      referencePrice1: 8.46,
      referenceDate2: "2025-08-01",
      referencePrice2: 9.9,
    },
  },
  {
    symbol: "BRFS3.SA",
    upper: {
      referenceDate1: "2024-03-01",
      referencePrice1: 31.32,
      referenceDate2: "2024-12-02",
      referencePrice2: 29.55,
    },
    lower: {
      referencePrice1: 11.83,
    },
  },
  {
    symbol: "BRKM5.SA",
    upper: {
      referenceDate1: "2025-04-01",
      referencePrice1: 18.7,
      referenceDate2: "2025-08-01",
      referencePrice2: 15.91,
    },
    lower: {
      referenceDate1: "2025-04-01",
      referencePrice1: 8.88,
      referenceDate2: "2025-08-01",
      referencePrice2: 7.56,
    },
  },
  {
    symbol: "BPAC11.SA",
    upper: {
      referenceDate1: "2025-01-02",
      referencePrice1: 42.92,
      referenceDate2: "2025-08-01",
      referencePrice2: 45.52,
    },
    lower: {
      referenceDate1: "2025-03-05",
      referencePrice1: 27.37,
      referenceDate2: "2025-08-01",
      referencePrice2: 29.13,
    },
  },
  {
    symbol: "EGIE3.SA",
    upper: {
      referencePrice1: 48,
    },
    lower: {
      referenceDate1: "2024-07-01",
      referencePrice1: 33.95,
      referenceDate2: "2025-04-01",
      referencePrice2: 35,
    },
  },
  {
    symbol: "BRAP4.SA",
    upper: {
      referenceDate1: "2025-01-02",
      referencePrice1: 20.15,
      referenceDate2: "2025-07-01",
      referencePrice2: 16.9,
    },
    lower: {
      referencePrice1: 12.2,
    },
  },
  {
    symbol: "RDOR3.SA",
    upper: {
      referencePrice1: 39,
    },
    lower: {
      referenceDate1: "2025-01-03",
      referencePrice1: 25.215,
      referenceDate2: "2025-07-01",
      referencePrice2: 26.513,
    },
  },
  {
    symbol: "VBBR3.SA",
    upper: {
      referenceDate1: "2024-12-02",
      referencePrice1: 26.99,
      referenceDate2: "2025-06-02",
      referencePrice2: 26.53,
    },
    lower: {
      referencePrice1: 16,
    },
  },
  {
    symbol: "ENEV3.SA",
    upper: {
      referencePrice1: 16.4,
    },
    lower: {
      referencePrice1: 9.35,
    },
  },
  {
    symbol: "ALOS3.SA",
    upper: {
      referenceDate1: "2023-11-01",
      referencePrice1: 27.23,
      referenceDate2: "2025-06-02",
      referencePrice2: 25.15,
    },
    lower: {
      referenceDate1: "2023-08-01",
      referencePrice1: 15.42,
      referenceDate2: "2025-08-01",
      referencePrice2: 15.85,
    },
  },
  {
    symbol: "CPLE6.SA",
    upper: {
      referenceDate1: "2025-02-03",
      referencePrice1: 12.65,
      referenceDate2: "2025-08-01",
      referencePrice2: 13.16,
    },
    lower: {
      referenceDate1: "2024-07-01",
      referencePrice1: 8.16,
      referenceDate2: "2025-07-01",
      referencePrice2: 9.24,
    },
  },
  {
    symbol: "ASAI3.SA",
    upper: {
      referenceDate1: "2025-06-02",
      referencePrice1: 12.063,
      referenceDate2: "2025-08-01",
      referencePrice2: 11.472,
    },
    lower: {
      referenceDate1: "2025-01-02",
      referencePrice1: 4.898,
      referenceDate2: "2025-06-02",
      referencePrice2: 3.494,
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
      referenceDate2: "2025-09-01",
      referencePrice2: 58.13,
    },
  },
]

checkProximity(resistanceRecords, 2)
