import "./Layout.css";
import { Link, useLocation } from "react-router-dom";

export default function AppLayout({ children }) {
  const location = useLocation();

  const navItems = [
    { name: "Dashboard", path: "/" },
    { name: "Leads", path: "/leads" },
    { name: "Reminders", path: "/reminders" },
  ];

  return (
    <div className="app-layout">
      {/* Sidebar added back as a fixed left element */}
      <aside className="sidebar">
        <div className="sidebar-brand">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"></path><path d="M2 12h20"></path></svg>
          <span className="brand-title">Investor CRM</span>
        </div>
        
        <nav className="sidebar-nav">
          {navItems.map(item => (
            <Link 
              key={item.path} 
              to={item.path} 
              className={`nav-link ${location.pathname === item.path ? "active" : ""}`}
            >
              {item.name}
            </Link>
          ))}
        </nav>
      </aside>

      <div className="main-wrapper">
        <header className="top-navbar">
          <div className="page-header">{navItems.find(i => i.path === location.pathname)?.name || "Detail"}</div>
        </header>
        <main className="main-content">
          {children}
        </main>
      </div>
    </div>
  );
}
