import { IFimatheRef } from "./FimatheContext";

const persistFimatheRef = (ref: IFimatheRef | null) => {
  ref ? alert(JSON.stringify(ref)) : null;
};

export default persistFimatheRef;
