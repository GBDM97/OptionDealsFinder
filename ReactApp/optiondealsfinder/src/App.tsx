import "./App.css";
import { FimatheProvider } from "./context/FimatheProvider";
import OptionsPage from "./pages/OptionsPage";

const App = () => {
  return (
    <FimatheProvider>
      <OptionsPage />
    </FimatheProvider>
  );
};

export default App;
