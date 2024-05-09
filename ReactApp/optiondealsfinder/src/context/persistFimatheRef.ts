import { IFimatheRef } from "./FimatheContext";

const persistFimatheRef = async (ref: IFimatheRef | null) => {
  if (ref) {
    await navigator.clipboard.writeText(JSON.stringify(ref));
    alert("Ref copied to clipboard.");
  }
};

export default persistFimatheRef;
