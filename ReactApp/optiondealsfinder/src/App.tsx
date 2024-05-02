import React from "react";
import "./App.css";
import styled from "styled-components";
import tableData from "./data/lockOutput.json";

// Styled components for table and its child elements
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

const MyTable: React.FC = () => {
  return (
    <div style={{ height: "100vh", backgroundColor: "black" }}>
      <Table>
        <TableHead>
          <TableRow>
            <TableHeaderCell>something to test</TableHeaderCell>
            <TableHeaderCell>2</TableHeaderCell>
            <TableHeaderCell>3</TableHeaderCell>
            <TableHeaderCell>4</TableHeaderCell>
          </TableRow>
        </TableHead>
        <tbody>
          {tableData.map((row: Array<string | number>) => (
            <TableRow key={row[0]}>
              {row.map((v) => (
                <TableCell>{v}</TableCell>
              ))}
              <input />
              <input />
            </TableRow>
          ))}
        </tbody>
      </Table>
      <div
        style={{
          display: "grid",
          backgroundColor: "purple",
          height: "400%",
          gridTemplateRows: "100px auto 100px",
        }}
      >
        <div
          style={{
            gridRow: "1",
            backgroundColor: "orange",
            position: "sticky",
            top: 0,
          }}
        ></div>
      </div>
    </div>
  );
};

export default MyTable;
