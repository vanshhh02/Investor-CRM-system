import { useState, useEffect } from "react";
import "./Dashboard.css";

export default function Dashboard() {
  const [leads, setLeads] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/leads")
      .then(res => res.json())
      .then(data => setLeads(data));
  }, []);

  const total = leads.length;
  const interested = leads.filter(l => l.stage === "Interested").length;
  const committed = leads.filter(l => l.stage === "Committed").length;

  const getStagePercent = (stageName) => {
    if (total === 0) return 0;
    const count = leads.filter(l => l.stage === stageName).length;
    return (count / total) * 100;
  };

  const getTierData = (tierName) => {
    if (total === 0) return { count: 0, percent: "0%" };
    const count = leads.filter(l => l.net_worth_tier === tierName).length;
    return { count, percent: Math.round((count / total) * 100) + "%" };
  };

  const highTier = getTierData("High");
  const mediumTier = getTierData("Medium");
  const lowTier = getTierData("Low");

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1 className="dashboard-title">Dashboard</h1>
        <p className="dashboard-subtitle">Overview of your investor pipeline</p>
      </div>

      <div className="summary-cards">
        <div className="card summary-card">
          <div className="card-top">
            <span className="card-label">TOTAL LEADS</span>
            <div className="card-icon text-gray">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
            </div>
          </div>
          <div className="card-value">{total}</div>
        </div>

        <div className="card summary-card">
          <div className="card-top">
            <span className="card-label">INTERESTED</span>
            <div className="card-icon text-green">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>
            </div>
          </div>
          <div className="card-value text-green">{interested}</div>
        </div>

        <div className="card summary-card">
          <div className="card-top">
            <span className="card-label">COMMITTED</span>
            <div className="card-icon text-purple">
               <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
            </div>
          </div>
          <div className="card-value text-purple">{committed}</div>
        </div>
      </div>

      <div className="card p-stage-card">
        <h3 className="card-title">Pipeline Stages</h3>
        
        <div className="pipeline-list">
          <div className="pipeline-item">
            <span className="dot dot-blue"></span>
            <span className="p-label">Cold</span>
            <div className="p-bar-container">
              <div className="p-bar bg-blue" style={{ width: `${getStagePercent('Cold')}%` }}></div>
            </div>
            <span className="p-count">{leads.filter(l => l.stage === 'Cold').length}</span>
          </div>
          
          <div className="pipeline-item">
            <span className="dot dot-yellow"></span>
            <span className="p-label">Contacted</span>
            <div className="p-bar-container">
              <div className="p-bar bg-yellow" style={{ width: `${getStagePercent('Contacted')}%` }}></div>
            </div>
            <span className="p-count">{leads.filter(l => l.stage === 'Contacted').length}</span>
          </div>

          <div className="pipeline-item">
            <span className="dot dot-green"></span>
            <span className="p-label">Interested</span>
            <div className="p-bar-container">
              <div className="p-bar bg-green" style={{ width: `${getStagePercent('Interested')}%` }}></div>
            </div>
            <span className="p-count">{interested}</span>
          </div>

          <div className="pipeline-item">
            <span className="dot dot-purple"></span>
            <span className="p-label">Committed</span>
            <div className="p-bar-container">
              <div className="p-bar bg-purple" style={{ width: `${getStagePercent('Committed')}%` }}></div>
            </div>
            <span className="p-count">{committed}</span>
          </div>
        </div>
      </div>

      <div className="card tier-card">
        <h3 className="card-title">Tier Breakdown</h3>
        
        <div className="tier-list">
          <div className="tier-item">
            <div className="tier-left">
              <span className="dot dot-yellow"></span>
              <span className="t-label">High Tier</span>
            </div>
            <div className="tier-right">
              <span className="t-count">{highTier.count}</span>
              <span className="t-perc">{highTier.percent}</span>
            </div>
          </div>
          
          <div className="tier-item">
             <div className="tier-left">
              <span className="dot dot-blue"></span>
              <span className="t-label">Medium Tier</span>
            </div>
            <div className="tier-right">
              <span className="t-count">{mediumTier.count}</span>
              <span className="t-perc">{mediumTier.percent}</span>
            </div>
          </div>

          <div className="tier-item">
            <div className="tier-left">
              <span className="dot dot-gray"></span>
              <span className="t-label">Low Tier</span>
            </div>
             <div className="tier-right">
              <span className="t-count">{lowTier.count}</span>
              <span className="t-perc">{lowTier.percent}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
