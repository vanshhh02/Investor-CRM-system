import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "./Leads.css";

export default function Leads() {
  const [leads, setLeads] = useState([]);
  const [showAddForm, setShowAddForm] = useState(false);
  const [formData, setFormData] = useState({ name: "", email: "", linkedin: "", net_worth_tier: "Medium", interest_areas: "" });

  useEffect(() => {
    fetch("http://localhost:8000/leads")
      .then(res => res.json())
      .then(data => setLeads(data))
      .catch(err => console.error(err));
  }, []);

  const handleAddSubmit = async (e) => {
    e.preventDefault();
    const payload = {
      ...formData,
      interest_areas: formData.interest_areas.split(',').map(s => s.trim())
    };
    
    try {
      const res = await fetch("http://localhost:8000/leads", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        const newLead = await res.json();
        setLeads([...leads, newLead]);
        setShowAddForm(false);
      }
    } catch(err) { console.error(err); }
  };

  const getStageColor = (stage) => {
    if (stage === "Cold") return "var(--color-blue)";
    if (stage === "Contacted") return "var(--color-yellow)";
    if (stage === "Interested") return "var(--color-green)";
    if (stage === "Committed") return "var(--color-purple)";
    return "var(--text-muted)";
  };

  return (
    <div className="leads-page slide-in">
      <div className="page-header-row">
        <h1 className="page-title">Investor Pipeline</h1>
        <button className="primary-btn" onClick={() => setShowAddForm(!showAddForm)}>+ Add Lead</button>
      </div>

      {showAddForm && (
        <form className="add-lead-form card slide-down" onSubmit={handleAddSubmit}>
          <h3>New Lead</h3>
          <div className="form-grid">
            <input placeholder="Name" required value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} />
            <input placeholder="Email" type="email" required value={formData.email} onChange={e => setFormData({...formData, email: e.target.value})} />
            <input placeholder="LinkedIn URL" value={formData.linkedin} onChange={e => setFormData({...formData, linkedin: e.target.value})} />
            <select value={formData.net_worth_tier} onChange={e => setFormData({...formData, net_worth_tier: e.target.value})}>
              <option value="High">High Tier</option>
              <option value="Medium">Medium Tier</option>
              <option value="Low">Low Tier</option>
            </select>
            <input placeholder="Interest Areas (comma separated)" className="full-width" value={formData.interest_areas} onChange={e => setFormData({...formData, interest_areas: e.target.value})} />
          </div>
          <div className="form-actions">
            <button type="submit" className="primary-btn">Save</button>
            <button type="button" className="ghost-btn" onClick={() => setShowAddForm(false)}>Cancel</button>
          </div>
        </form>
      )}

      <div className="leads-table-container card">
        <table className="leads-table">
          <thead>
            <tr>
              <th>Investor</th>
              <th>Stage</th>
              <th>Tier</th>
              <th>Email</th>
            </tr>
          </thead>
          <tbody>
            {leads.length === 0 ? (
              <tr><td colSpan="4" style={{textAlign:"center", padding: "2rem"}}>No leads yet</td></tr>
            ) : leads.map(l => (
              <tr key={l.id}>
                <td>
                  <Link to={`/leads/${l.id}`} className="lead-link">{l.name}</Link>
                </td>
                <td>
                  <span className="stage-badge" style={{color: getStageColor(l.stage), backgroundColor: `${getStageColor(l.stage)}22`}}>
                    {l.stage}
                  </span>
                </td>
                <td>{l.net_worth_tier}</td>
                <td className="text-muted">{l.email}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
