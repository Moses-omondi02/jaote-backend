import { Link } from "react-router-dom";
import "./Navbar.css";

export default function Navbar() {
  return (
    <nav className="navbar">
      <h1>Volunteer Task Board</h1>
      <div className="nav-links">
        <Link to="/">Tasks</Link>
        <Link to="/add">Add Task</Link>
        <Link to="/signups">Signups</Link>
      </div>
    </nav>
  );
}
