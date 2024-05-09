const parseIsoDate = (d: string) => {
  return new Date(d).toLocaleString("es-ES").replace(",", "");
};

export default parseIsoDate;
