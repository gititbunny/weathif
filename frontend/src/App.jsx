import {
  BrowserRouter,
  Route,
  Routes,
} from "react-router-dom";
import Home from "./pages/Home";
import Simulator from "./pages/Simulator";
import Methodology from "./pages/Methodology";
import Technology from "./pages/Technology";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={<Home />}
        />

        <Route
          path="/simulator"
          element={<Simulator />}
        />

        <Route
          path="/methodology"
          element={<Methodology />}
        />

        <Route
          path="/technology"
          element={<Technology />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;