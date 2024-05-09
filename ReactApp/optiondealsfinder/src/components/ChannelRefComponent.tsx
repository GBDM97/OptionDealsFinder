import { useEffect, useState } from "react";
import { useFimatheContext } from "../context/useFimatheContext";
import { IFimatheRef } from "../context/FimatheContext";
import jsonData from "../data/initialRefs.json";

const updateRef = (
  inputRef: number,
  refNumber: number,
  ref: IFimatheRef | null,
  tickerName: string
) => {
  ref = { ...ref };
  if (!(ref && ref[tickerName])) {
    ref = jsonData;
    ref[tickerName] = { ref1: 0, ref2: 0 };
  }
  if (refNumber === 1) {
    ref[tickerName].ref1 = inputRef;
  } else {
    ref[tickerName].ref2 = inputRef;
  }
  return ref;
};

const assetRefExists = (
  ticker: string,
  refNumber: number,
  ref: IFimatheRef | null
) => {
  return (
    ref &&
    ticker in ref &&
    ((refNumber === 1 && !!ref[ticker].ref1) ||
      (refNumber === 2 && !!ref[ticker].ref2))
  );
};

const insertedRefInitialState = (
  tickerName: string,
  refNumber: number,
  ref: IFimatheRef | null
) => {
  if (ref && refNumber === 1) {
    return ref[tickerName]?.ref1.toString();
  } else if (ref && refNumber === 2) {
    return ref[tickerName]?.ref2.toString();
  } else {
    return "";
  }
};

const ChannelRefComponent: React.FC<{
  tickerName: string;
  refNumber: number;
}> = ({ tickerName, refNumber }) => {
  const { ref, setRef } = useFimatheContext();

  const [open, setOpen] = useState(!assetRefExists(tickerName, refNumber, ref));

  const [insertedRef, setInsertedRef] = useState(
    insertedRefInitialState(tickerName, refNumber, ref)
  );

  useEffect(() => {
    setInsertedRef(insertedRefInitialState(tickerName, refNumber, ref));
    setOpen(!assetRefExists(tickerName, refNumber, ref));
  }, [ref, tickerName]);

  return open ? (
    <>
      <input
        onChange={(e) => setInsertedRef(e.target.value)}
        type="text"
        value={insertedRef !== "0" ? insertedRef : ""}
      />
      <button
        onClick={() => {
          setOpen(false);
          setRef(
            updateRef(
              parseFloat(insertedRef) ? parseFloat(insertedRef) : 0,
              refNumber,
              ref,
              tickerName
            )
          );
        }}
        type="button"
      >
        Save
      </button>
    </>
  ) : (
    <div style={{ display: "block" }}>
      <p style={{ display: "inline" }}>
        {refNumber === 1 && ref && ref[tickerName].ref1}
        {refNumber === 2 && ref && ref[tickerName].ref2}
      </p>
      &nbsp;
      <button onClick={() => setOpen(true)} type="button">
        Edit
      </button>
    </div>
  );
};

export default ChannelRefComponent;
