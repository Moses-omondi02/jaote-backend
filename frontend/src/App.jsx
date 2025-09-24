import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import TasksPage from "./pages/Taskpage"; // 👈 make sure spelling matches filename
import AddTaskPage from "./pages/AddTaskpage";
import SignupsPage from "./pages/SignupsPage";
import "./App.css";

function App() {
  return (
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
  );
}

export default App;
