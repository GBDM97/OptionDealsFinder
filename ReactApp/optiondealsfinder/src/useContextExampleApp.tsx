import { IFimatheRef } from "./context/FimatheContext";
import jsonData from "./data/initialRefs.json";
import { useFimatheContext } from "./context/useFimatheContext";
import { FimatheProvider } from "./context/FimatheProvider";

const updateRef = (
  inputRef: number,
  refNumber: number,
  ref: IFimatheRef | null,
  tickerName: string
) => {
  if (ref) {
    if (refNumber === 1) {
      ref[tickerName].ref1 = inputRef;
    } else {
      ref[tickerName].ref2 = inputRef;
    }
    return ref;
  } else {
    return jsonData;
  }
};

const App = () => {
  return (
    <>
      <FimatheProvider>
        <TestChild1 />
        <TestChild2 />
      </FimatheProvider>
    </>
  );
};

const ChildsChild = () => {
  const { ref, setRef } = useFimatheContext();
  return (
    <>
      <p>{JSON.stringify(ref)}</p>
      {"hwllo"}
      <input
        onChange={(e) =>
          setRef(updateRef(parseFloat(e.target.value), 1, ref, "gggg"))
        }
      ></input>
    </>
  );
};

const TestChild1 = () => {
  const { ref, setRef } = useFimatheContext();

  return (
    <>
      <p>{JSON.stringify(ref)}</p>
      <input
        onChange={(e) =>
          setRef(updateRef(parseFloat(e.target.value), 1, ref, "gggg"))
        }
      ></input>
      <ChildsChild />
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
