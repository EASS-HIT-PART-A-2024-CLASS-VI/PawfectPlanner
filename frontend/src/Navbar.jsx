import { Link } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  return (
    <nav className="navbar">
      <Link to="/">Home</Link>
      <Link to="/profile">Pet Profile</Link>
      <Link to="/reminders">Reminders</Link>
      <Link to="/treatments">Treatments</Link>
      <Link to="/vet-locator">Find a Vet</Link>
    </nav>
  );
}

export default Navbar;
