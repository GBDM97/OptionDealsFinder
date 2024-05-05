import styled from "styled-components";
import tableData from "../data/lockOutput.json";
import { useFimatheContext } from "../context/useFimatheContext";
import ChannelRefComponent from "../components/ChannelRefComponent";

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
    </>
  );
};

export default OptionsPage;
