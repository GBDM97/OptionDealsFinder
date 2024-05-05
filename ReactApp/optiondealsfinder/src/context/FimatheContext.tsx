import { createContext } from "react";

export interface IFimatheRef {
  [key: string]: { ref1: number; ref2: number };
}
export type FimatheRef = {
  ref: IFimatheRef | null;
  setRef: (p: IFimatheRef) => void;
};

export const FimatheContext = createContext<FimatheRef>({
  ref: {},
  setRef: () => {},
});
