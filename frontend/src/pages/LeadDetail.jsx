import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import "./LeadDetail.css";

export default function LeadDetail() {
  const { id } = useParams();
  const [lead, setLead] = useState(null);
  const [interactions, setInteractions] = useState([]);
  const [note, setNote] = useState("");
  const [intType, setIntType] = useState("Call");
  const [aiResult, setAiResult] = useState({ type: null, content: null });

  useEffect(() => {
    fetch(`http://localhost:8000/leads/${id}`)
      .then(res => res.json())
      .then(data => setLead(data));
      
    fetch(`http://localhost:8000/interactions?lead_id=${id}`)
      .then(res => res.json())
      .then(data => setInteractions(data));
  }, [id]);

  const handleStageChange = async (newStage) => {
    const res = await fetch(`http://localhost:8000/leads/${id}/stage`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ new_stage: newStage })
    });
    if (res.ok) {
      const updated = await res.json();
      setLead(updated);
    }
  };

  const handleLogInteraction = async (e) => {
    e.preventDefault();
    const res = await fetch(`http://localhost:8000/interactions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ lead_id: id, type: intType, notes: note })
    });
    if (res.ok) {
      const data = await res.json();
      setInteractions([data, ...interactions]);
      setNote("");
    }
  };

  const triggerAI = async (endpoint) => {
    setAiResult({ type: "Loading...", content: "Loading..." });
    const res = await fetch(`http://localhost:8000/ai/${endpoint}/${id}`);
    const data = await res.json();
    const val = Object.values(data)[0];
    setAiResult({ type: endpoint, content: val });
  };

  if (!lead) return <div className="p-xl text-muted">Loading...</div>;

  return (
    <div className="lead-detail-page slide-in">
      <div className="lead-header card">
        <div className="lh-left">
          <h1 className="lead-name">{lead.name}</h1>
          <div className="lead-meta text-muted">
            {lead.email} • {lead.net_worth_tier} Tier
          </div>
          <div className="lead-interests mt-2">
            Interests: <strong>{lead.interest_areas}</strong>
          </div>
        </div>
        <div className="lh-right">
          <label>Stage Pipeline</label>
          <select 
            value={lead.stage} 
            onChange={(e) => handleStageChange(e.target.value)}
            className="stage-select"
          >
            <option>Cold</option>
            <option>Contacted</option>
            <option>Interested</option>
            <option>Committed</option>
          </select>
        </div>
      </div>

      <div className="detail-grid">
        <div className="interactions-col">
          <div className="card">
            <h3>Log Interaction</h3>
            <form onSubmit={handleLogInteraction} className="interaction-form">
              <select value={intType} onChange={e => setIntType(e.target.value)} className="int-select">
                <option>Call</option>
                <option>Email</option>
                <option>Meeting</option>
              </select>
              <textarea 
                placeholder="Notes from interaction..." 
                value={note}
                onChange={e => setNote(e.target.value)}
                required
              />
              <button className="primary-btn">Log Interaction</button>
            </form>
          </div>

          <div className="timeline mt-3">
            <h3>History</h3>
            {interactions.map(int => (
              <div key={int.id} className="timeline-item">
                <div className="tl-dot"></div>
                <div className="tl-content card">
                  <div className="tl-head text-muted">
                    <strong>{int.type}</strong> • {new Date(int.date).toLocaleDateString()}
                  </div>
                  <div className="tl-body">{int.notes}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="ai-col">
          <div className="card ai-card">
            <h3>✨ AI Assistant</h3>
            <div className="ai-actions">
              <button onClick={() => triggerAI('generate-email')} className="ghost-btn">Generate Email</button>
              <button onClick={() => triggerAI('summary')} className="ghost-btn">Summarize</button>
              <button onClick={() => triggerAI('score')} className="ghost-btn">Lead Score</button>
              <button onClick={() => triggerAI('next-action')} className="ghost-btn">Next Action</button>
            </div>
            {aiResult.content && (
              <div className="ai-result">
                <h4>{aiResult.type}</h4>
                <div className="ai-content">{aiResult.content}</div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
