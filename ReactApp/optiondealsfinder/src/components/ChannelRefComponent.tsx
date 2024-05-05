import { SetStateAction, useState } from "react";
import { useFimatheContext } from "../context/useFimatheContext";
import { FimatheRef, IFimatheRef } from "../context/FimatheContext";
import jsonData from "../data/initialRefs.json";

const getTickerName = (opt: string) => {
  const numberIndex = opt.match(/\d/)?.index;
  return opt.slice(0, numberIndex);
};

const updateRef = (
  inputRef: number,
  refNumber: number,
  ref: IFimatheRef | null,
  tickerName: string
) => {
  if (ref && ref[tickerName]) {
    if (refNumber === 1) {
      ref[tickerName].ref1 = inputRef;
    } else {
      ref[tickerName].ref2 = inputRef;
    }
    return ref;
  } else if (ref && !ref[tickerName]) {
    ref[tickerName] = { ref1: 0, ref2: 0 };
    return ref;
  } else {
    return jsonData;
  }
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
  opt: string;
  refNumber: number;
  ref: IFimatheRef | null;
  setRef: (p: IFimatheRef) => void;
}> = ({ opt, refNumber, ref, setRef }) => {
  const tickerName = getTickerName(opt);

  const [open, setOpen] = useState(!assetRefExists(tickerName, refNumber, ref));

  const [insertedRef, setInsertedRef] = useState(
    insertedRefInitialState(tickerName, refNumber, ref)
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
    <>
      <p>
        {ref && ref[tickerName] && refNumber === 1
          ? ref[tickerName].ref1
          : null}
        {ref && ref[tickerName] && refNumber === 2
          ? ref[tickerName].ref2
          : null}
      </p>
      <button onClick={() => setOpen(true)} type="button">
        Edit
      </button>
    </>
  );
};

export default ChannelRefComponent;
