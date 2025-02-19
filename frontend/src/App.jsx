import { Routes, Route } from "react-router-dom";
import Navbar from "./Navbar";
import Home from "./Home";
import PetProfile from "./PetProfile";
import Reminders from "./Reminders";

function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/pet-profile" element={<PetProfile />} />
        <Route path="/reminders" element={<Reminders />} />
      </Routes>
    </>
  );
}

export default App;
