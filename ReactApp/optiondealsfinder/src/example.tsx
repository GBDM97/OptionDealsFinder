import { IFimatheRef } from "./context/FimatheContext";
import jsonData from "./data/initialRefs.json";
import { useFimatheContext } from "./context/useFimatheContext";
import { FimatheProvider } from "./context/FimatheProvider";
import { useState } from "react";

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

const App = () => {
  const [render, setrender] = useState(false);
  return (
    <>
      <FimatheProvider>
        {render}
        <button onClick={() => setrender((p) => !p)}>render</button>
        <TestChild1 />
        <TestChild2 />
      </FimatheProvider>
    </>
  );
};

const ChildsChild: React.FC<{
  reff: IFimatheRef | null;
  setRef: (p: IFimatheRef) => void;
}> = ({ reff, setRef }) => {
  return (
    <>
      <p>{JSON.stringify(reff)}</p>
      {"hwllo"}
      <input
        onChange={(e) =>
          setRef(updateRef(parseFloat(e.target.value), 1, reff, "gggg"))
        }
      ></input>
    </>
  );
};

const TestChild1 = () => {
  const { ref, setRef } = useFimatheContext();
  const setReff = (p: IFimatheRef) => {
    setRef(p);
  };
  return (
    <>
      <p>{JSON.stringify(ref)}</p>
      <input
        onChange={(e) =>
          setRef(updateRef(parseFloat(e.target.value), 1, ref, "gggg"))
        }
      ></input>
      {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((n) => (
        <ChildsChild key={n} reff={ref} setRef={setReff} />
      ))}
    </>
  );
};

const TestChild2 = () => {
  const { ref, setRef } = useFimatheContext();

  return (
    <>
      <p>{JSON.stringify(ref)}</p>
      <input
        onChange={(e) =>
          setRef(updateRef(parseFloat(e.target.value), 2, ref, "gggg"))
        }
      ></input>
    </>
  );
};

export default App;
