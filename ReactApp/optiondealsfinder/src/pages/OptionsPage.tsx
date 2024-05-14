import styled from "styled-components";
import tableData from "../data/lockOutput.json";
import { useFimatheContext } from "../context/useFimatheContext";
import ChannelRefComponent from "../components/ChannelRefComponent";
import parseIsoDate from "../utils/parseIsoDate";
import { IFimatheRef } from "../context/FimatheContext";
import { useEffect, useState } from "react";
import persistFimatheRef from "../context/persistFimatheRef";

const Table = styled.table`
  width: 100%;
  border-collapse: collapse;
  background-color: black;
`;

const TableHead = styled.thead`
  background-color: black;
  color: white;
  position: sticky;
  top: 0;
`;

const TableRow = styled.tr`
  color: white;
  &:nth-child(even) {
    background-color: #232323;
  }
`;

const TableHeaderCell = styled.th`
  padding: 12px;
  text-align: left;
  font-weight: 400;
`;

const TableCell = styled.td`
  padding: 12px;
`;

const getTickerName = (opt: string) => {
  const numberIndex = opt.match(/\d/)?.index || 2;
  return numberIndex === 1
    ? opt.slice(0, numberIndex)
    : opt.slice(0, numberIndex - 1);
};

const calculateFDI = (row: Array<string | number>, ref: IFimatheRef | null) => {
  const tickerName = getTickerName(row[2].toString());
  if (
    ref &&
    ref[tickerName] &&
    !!ref[tickerName].ref1 &&
    !!ref[tickerName].ref2
  ) {
    return (
      (parseFloat(String(row[row.length - 1])) *
        parseFloat(String(row[row.length - 2]))) /
      100 /
      Math.abs(ref[tickerName].ref1 - ref[tickerName].ref2)
    );
  }
  return 0;
};

const updateFDI = (
  list: Array<Array<string | number>>,
  ref: IFimatheRef | null
) => {
  return list.map((row: Array<string | number>) => {
    row.length > 9 ? row.pop() : null;
    row.push(calculateFDI(row, ref));
    return row;
  });
};

const OptionsPage = () => {
  const { ref } = useFimatheContext();
  const [list, setList] = useState(tableData);
  const [orderDirection, setOrderDirection] = useState([
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
  ]);

  const order = (col: number) => {
    const compareStringOrNumber = (
      p1: string | number,
      p2: string | number
    ) => {
      return typeof p1 === "string" && typeof p2 === "string"
        ? String(p1).localeCompare(String(p2))
        : parseFloat(String(p1)) - parseFloat(String(p2));
    };

    if (orderDirection[col] === "a") {
      setOrderDirection((p) => {
        p = ["", "", "", "", "", "", "", "", "", ""];
        p[col] = "d";
        return p;
      });
      setList(
        list.sort((a, b) => compareStringOrNumber(a[col], b[col])).reverse()
      );
    } else if (orderDirection[col] === "") {
      setOrderDirection((p) => {
        p = ["", "", "", "", "", "", "", "", "", ""];
        p[col] = "a";
        return p;
      });
      setList(list.sort((a, b) => compareStringOrNumber(a[col], b[col])));
    } else {
      setOrderDirection((p) => {
        p = ["", "", "", "", "", "", "", "", "", ""];
        p[col] = "";
        return p;
      });
      setList(list.sort((a, b) => compareStringOrNumber(a[2], b[2])));
    }
  };

  useEffect(() => {
    setList(updateFDI(list, ref));
  }, [ref]);

  return (
    <>
      <Table>
        <TableHead>
          <TableRow>
            <TableHeaderCell onClick={() => order(0)}>
              Date and Time
            </TableHeaderCell>
            <TableHeaderCell onClick={() => order(1)}>
              Profit Level
            </TableHeaderCell>
            <TableHeaderCell onClick={() => order(2)}>Buy</TableHeaderCell>
            <TableHeaderCell onClick={() => order(3)}>
              Buy Price
            </TableHeaderCell>
            <TableHeaderCell onClick={() => order(4)}>Sell</TableHeaderCell>
            <TableHeaderCell onClick={() => order(5)}>
              Sell Price
            </TableHeaderCell>
            <TableHeaderCell onClick={() => order(6)}>
              Multiplication
            </TableHeaderCell>
            <TableHeaderCell onClick={() => order(7)}>
              Percentage To Max. Profit
            </TableHeaderCell>
            <TableHeaderCell onClick={() => order(9)}>
              Fimathe Distance Index
            </TableHeaderCell>
            <TableHeaderCell
              onClick={() => persistFimatheRef(ref)}
              style={{ cursor: ref ? "pointer" : "default" }}
            >
              Click to copy 📃
            </TableHeaderCell>
          </TableRow>
          <TableRow
            style={{
              width: "100vw",
              backgroundColor: "gray",
              height: "1px",
              position: "fixed",
            }}
          ></TableRow>
        </TableHead>

        <tbody>
          {list.map((row: Array<string | number>, tableIndex: number) => (
            <TableRow key={tableIndex}>
              {row.map((v, valueIndex) => (
                <TableCell
                  key={valueIndex}
                  hidden={valueIndex === 8}
                  style={{
                    color:
                      valueIndex === 9 && parseFloat(String(v)) <= 1
                        ? "limeGreen"
                        : "white",
                  }}
                >
                  {valueIndex === 0 ? parseIsoDate(v.toString()) : null}
                  {valueIndex === 6 ? parseFloat(String(v)).toFixed(4) : null}
                  {valueIndex !== 0 && valueIndex !== 6 ? v : null}
                </TableCell>
              ))}
              <TableCell>
                <ChannelRefComponent
                  tickerName={getTickerName(row[2].toString())}
                  refNumber={1}
                />
                <ChannelRefComponent
                  tickerName={getTickerName(row[2].toString())}
                  refNumber={2}
                />
              </TableCell>
            </TableRow>
          ))}
        </tbody>
      </Table>
    </>
  );
};

export default OptionsPage;
