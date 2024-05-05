import { useState } from "react";
import { FimatheContext, IFimatheRef } from "./FimatheContext";

export const FimatheProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [ref, setRef] = useState<IFimatheRef | null>(null);
  return (
    <FimatheContext.Provider value={{ ref, setRef }}>
      {children}
    </FimatheContext.Provider>
  );
};
