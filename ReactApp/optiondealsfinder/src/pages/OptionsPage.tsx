import styled from "styled-components";
import tableData from "../data/lockOutput.json";
import { useFimatheContext } from "../context/useFimatheContext";
import ChannelRefComponent from "../components/ChannelRefComponent";
import parseIsoDate from "../utils/parseIsoDate";
import { IFimatheRef } from "../context/FimatheContext";

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

const showFDI = (ref: IFimatheRef | null) => {
  if (ref) {
    const keys = Object.keys(ref);
    for (let index = 0; index < keys.length; index++) {
      if (ref[keys[index]].ref1 !== 0 && ref[keys[index]].ref2) {
        return false;
      }
    }
  }
  return true;
};

const OptionsPage = () => {
  const { ref } = useFimatheContext();
  return (
    <>
      <Table>
        <TableHead
          style={{
            position: "sticky",
            top: 0,
          }}
        >
          <TableRow>
            <TableHeaderCell>Date and Time</TableHeaderCell>
            <TableHeaderCell>Profit Level</TableHeaderCell>
            <TableHeaderCell>Buy</TableHeaderCell>
            <TableHeaderCell>Buy Price</TableHeaderCell>
            <TableHeaderCell>Sell</TableHeaderCell>
            <TableHeaderCell>Sell Price</TableHeaderCell>
            <TableHeaderCell>Multiplication</TableHeaderCell>
            <TableHeaderCell>Percentage To Max. Profit</TableHeaderCell>
            <TableHeaderCell hidden={showFDI(ref)}>
              Fimathe Distance Index
            </TableHeaderCell>
          </TableRow>
        </TableHead>
        <tbody>
          {tableData.map((row: Array<string | number>, tableIndex: number) => (
            <TableRow key={tableIndex}>
              {row.map((v, valueIndex) => (
                <TableCell key={valueIndex}>
                  {valueIndex === 0 ? parseIsoDate(v.toString()) : v}
                </TableCell>
              ))}
              <TableCell hidden={showFDI(ref)}>0</TableCell>
              <TableCell>
                <ChannelRefComponent opt={row[2].toString()} refNumber={1} />
                <ChannelRefComponent opt={row[2].toString()} refNumber={2} />
              </TableCell>
            </TableRow>
          ))}
        </tbody>
      </Table>
    </>
  );
};

export default OptionsPage;
