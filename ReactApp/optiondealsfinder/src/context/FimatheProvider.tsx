import { useState } from "react";
import { FimatheContext, IFimatheRef } from "./FimatheContext";
import jsonData from "../data/initialRefs.json";

export const FimatheProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [ref, setRef] = useState<IFimatheRef | null>(jsonData);
  return (
    <FimatheContext.Provider value={{ ref, setRef }}>
      {children}
    </FimatheContext.Provider>
  );
};
