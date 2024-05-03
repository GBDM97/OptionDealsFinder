import React, { useState } from "react";
import "./App.css";
import styled from "styled-components";
import tableData from "./data/lockOutput.json";
import useFimatheRef, { FimatheRef } from "./hooks/useFimatheRef";
import { strict } from "assert";

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

const RefInput = styled.input`
  type: number;
`;

const MyTable: React.FC = () => {
  const { ref, setRef } = useFimatheRef();
  const updateRef = (ticker: string, inputRef: number, refNumber: number) => {
    const numberIndex = ticker.match(/\d/)?.index;
    const tickerName: string = ticker.slice(0, numberIndex);
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
        {tableData.map((row: Array<string | number>) => (
          <TableRow key={row[0]}>
            {row.map((v) => (
              <TableCell>{v}</TableCell>
            ))}
            <RefInput
              onChange={(e) =>
                updateRef(row[1].toString(), parseInt(e.target.value), 1)
              }
            />
            <RefInput
              onChange={(e) =>
                updateRef(row[1].toString(), parseInt(e.target.value), 2)
              }
            />
          </TableRow>
        ))}
      </tbody>
    </Table>
  );
};

export default MyTable;
