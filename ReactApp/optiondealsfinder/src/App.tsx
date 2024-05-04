import React, { useEffect, useMemo, useRef, useState } from "react";
import "./App.css";
import styled from "styled-components";
import tableData from "./data/lockOutput.json";
import useFimatheRef, { FimatheRef } from "./hooks/useFimatheRef";

const Table = styled.table`
  width: 100%;
  border-collapse: collapse;
  background-color: black;
`;

const TableHead = styled.thead`
  background-color: black;
  color: white;
  border-bottom: 1px solid white;
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
  border-bottom: 1px solid #ddd;
`;

const getTickerName = (opt: string) => {
  const numberIndex = opt.match(/\d/)?.index;
  return opt.slice(0, numberIndex);
};

const App: React.FC = () => {
  const { ref, setRef } = useFimatheRef();

  const assetRefExists = (ticker: string, refNumber: number) => {
    return (
      ticker in ref &&
      ((refNumber === 1 && !!ref[ticker].ref1) ||
        (refNumber === 2 && !!ref[ticker].ref2))
    );
  };

  const insertedRefInitialState = (tickerName: string, refNumber: number) => {
    if (refNumber === 1) {
      return ref[tickerName]?.ref1.toString();
    } else if (refNumber === 2) {
      return ref[tickerName]?.ref2.toString();
    } else {
      return "";
    }
  };

  const ChannelRefComponent: React.FC<{ opt: string; refNumber: number }> = ({
    opt,
    refNumber,
  }) => {
    const tickerName = getTickerName(opt);
    const [open, setOpen] = useState(!assetRefExists(tickerName, refNumber));
    const [insertedRef, setInsertedRef] = useState(
      insertedRefInitialState(tickerName, refNumber)
    );

    return open ? (
      <>
        <input
          onChange={(e) => setInsertedRef(e.target.value)}
          type="text"
          value={insertedRef}
        />
        <button
          onClick={() => {
            setOpen(false);
            updateRef(
              tickerName,
              parseFloat(insertedRef) ? parseFloat(insertedRef) : 0,
              refNumber
            );
          }}
          type="button"
        >
          Save
        </button>
      </>
    ) : (
      <>
        <p>{refNumber === 1 ? ref[tickerName]?.ref1 : ref[tickerName]?.ref2}</p>
        <button onClick={() => setOpen(true)} type="button">
          Edit
        </button>
      </>
    );
  };

  const updateRef = (
    tickerName: string,
    inputRef: number,
    refNumber: number
  ) => {
    const newState: FimatheRef = { ...ref }[tickerName]
      ? { ...ref }
      : { [tickerName]: { ref1: 0, ref2: 0 } };
    if (refNumber === 1) {
      newState[tickerName].ref1 = inputRef;
    } else {
      newState[tickerName].ref2 = inputRef;
    }
    setRef(newState);
  };
  useEffect(() => {
    scrollTo(0, 0);
  }, []);
  return (
    <Table>
      <TableHead
        style={{
          position: "sticky",
          top: 0,
        }}
      >
        <TableRow>
          <TableHeaderCell>something to test</TableHeaderCell>
          <TableHeaderCell>{JSON.stringify(ref)}</TableHeaderCell>
          <TableHeaderCell>3</TableHeaderCell>
          <TableHeaderCell>4</TableHeaderCell>
          <TableHeaderCell>4</TableHeaderCell>
          <TableHeaderCell>4</TableHeaderCell>
          <TableHeaderCell>4</TableHeaderCell>
          <TableHeaderCell></TableHeaderCell>
          <TableHeaderCell></TableHeaderCell>
          <TableHeaderCell></TableHeaderCell>
        </TableRow>
      </TableHead>
      <tbody>
        {tableData.map((row: Array<string | number>, tableIndex) => (
          <TableRow key={tableIndex}>
            {row.map((v, valueIndex) => (
              <TableCell key={valueIndex}>{v}</TableCell>
            ))}
            <TableCell>
              <ChannelRefComponent opt={row[1].toString()} refNumber={1} />
              <ChannelRefComponent opt={row[1].toString()} refNumber={2} />
            </TableCell>
          </TableRow>
        ))}
      </tbody>
    </Table>
  );
};

export default App;
