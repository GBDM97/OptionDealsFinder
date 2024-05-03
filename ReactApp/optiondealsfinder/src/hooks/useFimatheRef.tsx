import React, { useState } from "react";
import jsonData from "../data/initialRefs.json";

export type FimatheRef = { [key: string]: { ref1: number; ref2: number } };

const initialRefs: FimatheRef = jsonData;

const useFimatheRef = () => {
  const [ref, setRef] = useState(initialRefs);
  return { ref, setRef };
};

export default useFimatheRef;
