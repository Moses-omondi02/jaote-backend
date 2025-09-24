import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import TasksPage from "./pages/Taskpage"; // 👈 make sure spelling matches filename
import AddTaskPage from "./pages/AddTaskpage";
import SignupsPage from "./pages/SignupsPage";
import "./App.css";

function App() {
  return (
    <div className="app-container">
      <Router>
        <Navbar />
        <div className="container">
          <Routes>
            <Route path="/" element={<TasksPage />} />
            <Route path="/tasks" element={<TasksPage />} />
            <Route path="/add-task" element={<AddTaskPage />} />
            <Route path="/signups" element={<SignupsPage />} />
          </Routes>
        </div>
      </Router>

      <nav className="navbar">
        <h2>JAOTE</h2>
        <ul>
          <li>Home</li>
          <li>Tasks</li>
          <li>About</li>
        </ul>
      </nav>

      <header className="hero">
        <h1>Volunteer Task Board</h1>
        <p>Manage tasks, assign roles, and track progress easily.</p>
        <button>Get Started</button>
      </header>

      <main>
        <section className="cards">
          <div className="card">
            <h3>Task Management</h3>
            <p>Create, update, and track all volunteer tasks.</p>
          </div>
          <div className="card">
            <h3>Team Collaboration</h3>
            <p>Assign tasks and monitor team progress in real time.</p>
          </div>
          <div className="card">
            <h3>Reports</h3>
            <p>View insights and summaries of completed work.</p>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
