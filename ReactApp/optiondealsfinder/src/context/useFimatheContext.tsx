import { useContext } from "react";
import { FimatheContext, FimatheRef } from "./FimatheContext";

export const useFimatheContext = () => {
  const fimatheContext = useContext(FimatheContext);
  if (fimatheContext === undefined) {
    throw new Error("useFimatheContext must be inside a FimatheProvider");
  }
  return fimatheContext;
};
