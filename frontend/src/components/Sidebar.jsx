// src/components/Sidebar.jsx
// Enterprise Navigation Console — SafeLine / ShieldCore Style

import React from 'react'

export default function Sidebar({ currentTab, onSelectTab, flowCount, wsConnected, theme, toggleTheme }) {
  const navItems = [
    {
      id: 'dashboard',
      icon: (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <rect x="3" y="3" width="7" height="9" rx="1"/>
          <rect x="14" y="3" width="7" height="5" rx="1"/>
          <rect x="14" y="12" width="7" height="9" rx="1"/>
          <rect x="3" y="16" width="7" height="5" rx="1"/>
        </svg>
      ),
      title: 'Live SOC Dashboard',
      subtitle: 'Real-time Zero-Trust & ML Matrix',
      badge: `${flowCount} flows`,
      badgeType: 'info',
    },
    {
      id: 'adversarial',
      icon: (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="12" cy="12" r="10"/>
          <circle cx="12" cy="12" r="6"/>
          <circle cx="12" cy="12" r="2"/>
        </svg>
      ),
      title: 'Adversarial Tests',
      subtitle: 'Red-Team Evasion & Defense',
      badge: 'Red Team',
      badgeType: 'block',
    },
    {
      id: 'incidents',
      icon: (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <polyline points="14 2 14 8 20 8"/>
          <line x1="16" y1="13" x2="8" y2="13"/>
          <line x1="16" y1="17" x2="8" y2="17"/>
          <polyline points="10 9 9 9 8 9"/>
        </svg>
      ),
      title: 'Incident Audit Trail',
      subtitle: 'Autonomous SOC & VLAN State',
      badge: 'AI Guardrail',
      badgeType: 'accent',
    },
    {
      id: 'reports',
      icon: (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
          <polyline points="7 10 12 15 17 10"/>
          <line x1="12" y1="15" x2="12" y2="3"/>
        </svg>
      ),
      title: 'Reports & Export',
      subtitle: 'Daily & Monthly PDF Reports',
      badge: 'PDF',
      badgeType: 'allow',
    },
  ]

  return (
    <aside className="app-sidebar">
      <div className="sidebar-brand">
        <div className="sidebar-logo-emblem">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
            <path
              d="M12 2L3 7V12C3 17.52 6.84 22.74 12 24C17.16 22.74 21 17.52 21 12V7L12 2Z"
              stroke="var(--accent)"
              strokeWidth="1.6"
              strokeLinecap="round"
              strokeLinejoin="round"
              fill="var(--accent-subtle)"
            />
            <path
              d="M12 7V17M8 11L12 7L16 11"
              stroke="var(--accent)"
              strokeWidth="1.6"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </div>
        <div className="sidebar-brand-text">
          <div className="brand-main">TRUST<span className="accent-text">FLOW</span></div>
          <div className="brand-tag">NEXT-GEN AI FIREWALL</div>
        </div>
      </div>

      <div className="sidebar-nav-section">
        <div className="sidebar-section-title">NAVIGATION CONSOLE</div>
        <nav className="sidebar-nav">
          {navItems.map((item) => {
            const isActive = currentTab === item.id
            return (
              <button
                key={item.id}
                className={`sidebar-nav-item ${isActive ? 'active' : ''}`}
                onClick={() => onSelectTab(item.id)}
              >
                <div className="nav-icon">{item.icon}</div>
                <div className="nav-info">
                  <div className="nav-title">{item.title}</div>
                  <div className="nav-subtitle">{item.subtitle}</div>
                </div>
                {item.badge && (
                  <span className={`nav-badge badge-${item.badgeType}`}>
                    {item.badge}
                  </span>
                )}
                {isActive && <div className="nav-indicator" />}
              </button>
            )
          })}
        </nav>
      </div>

      <div className="sidebar-defense-status">
        <div className="sidebar-section-title">SYSTEM INTEGRITY</div>
        <div className="status-cards-col">
          <div className="status-pill">
            <span className={`status-led ${wsConnected ? 'online' : 'offline'}`} />
            <div className="status-text">
              <span className="status-label">FastAPI Engine</span>
              <span className="status-value">{wsConnected ? 'Connected (Port 8000)' : 'Offline'}</span>
            </div>
          </div>
          <div className="status-pill">
            <span className="status-led online" />
            <div className="status-text">
              <span className="status-label">Ollama SOC Agent</span>
              <span className="status-value">Llama-3.2 (Temp 0.0)</span>
            </div>
          </div>
          <div className="status-pill">
            <span className="status-led online" />
            <div className="status-text">
              <span className="status-label">Active Defense</span>
              <span className="status-value">Windows Netsh + Honeypot 2222</span>
            </div>
          </div>
        </div>
      </div>

      <div className="sidebar-footer">
        <div className="sidebar-footer-row">
          <div>
            <div className="sidebar-version">TrustFlow NGFW v2.4 Enterprise</div>
            <div className="sidebar-status-sub">Zero-Trust Active</div>
          </div>
          {toggleTheme && (
            <button
              className="theme-toggle-sidebar-btn"
              onClick={toggleTheme}
              title={`Switch to ${theme === 'light' ? 'dark' : 'light'} theme`}
              aria-label="Toggle theme"
            >
              {theme === 'light' ? (
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
                </svg>
              ) : (
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="12" cy="12" r="5"/>
                  <line x1="12" y1="1" x2="12" y2="3"/>
                  <line x1="12" y1="21" x2="12" y2="23"/>
                  <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
                  <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
                  <line x1="1" y1="12" x2="3" y2="12"/>
                  <line x1="21" y1="12" x2="23" y2="12"/>
                  <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
                  <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
                </svg>
              )}
            </button>
          )}
        </div>
      </div>
    </aside>
  )
}
