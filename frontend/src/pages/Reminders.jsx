import { useState, useEffect } from "react";
import "./Reminders.css";

export default function Reminders() {
  const [reminders, setReminders] = useState([]);

  const fetchReminders = () => {
    fetch("http://localhost:8000/reminders")
      .then(res => res.json())
      .then(data => setReminders(data));
  };

  useEffect(() => {
    fetchReminders();
  }, []);

  const handleGenerate = async () => {
    await fetch("http://localhost:8000/reminders/generate", { method: "POST" });
    fetchReminders();
  };

  const markComplete = async (id) => {
    await fetch(`http://localhost:8000/reminders/${id}/complete`, { method: "PUT" });
    fetchReminders();
  };

  const getPriorityColor = (priority) => {
    if (priority === "High") return "var(--color-purple)";
    if (priority === "Medium") return "var(--color-yellow)";
    return "var(--color-blue)";
  };

  return (
    <div className="reminders-page slide-in">
      <div className="page-header-row">
        <h1 className="page-title">Reminders</h1>
        <button className="primary-btn" onClick={handleGenerate}>✨ AI Smart Generate</button>
      </div>

      <div className="reminders-list mt-3">
        {reminders.length === 0 ? (
          <div className="text-muted p-xl text-center">No active reminders. Click Smart Generate.</div>
        ) : reminders.map(r => (
          <div key={r.id} className={`card reminder-card ${r.is_completed === "True" ? "completed" : ""}`}>
            <div className="rem-indicator" style={{backgroundColor: getPriorityColor(r.priority)}}></div>
            <div className="rem-content">
              <div className="rem-text">{r.message}</div>
              <div className="rem-meta text-muted mt-2">
                {r.priority} Priority • Due: {new Date(r.due_date).toLocaleDateString()}
              </div>
            </div>
            {r.is_completed === "False" && (
              <button className="ghost-btn" onClick={() => markComplete(r.id)}>
                Done
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
