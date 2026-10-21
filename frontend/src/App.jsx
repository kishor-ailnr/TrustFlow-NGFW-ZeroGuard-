// src/App.jsx
// Root component — wires Sidebar, Live SOC Matrix, Adversarial Arena, Incident Logs & PDF Report Generator
// Enterprise reskin: light/dark theme state, flat surface architecture

import { useState, useEffect, useRef } from 'react'
import { useWebSocket } from './hooks/useWebSocket'
import { usePolling }   from './hooks/usePolling'

import CircuitBackground from './components/CircuitBackground'
import Sidebar           from './components/Sidebar'
import FlowFeed          from './components/FlowFeed'
import EnsemblePanel     from './components/EnsemblePanel'
import TrustPanel        from './components/TrustPanel'
import MitigationPanel    from './components/MitigationPanel'
import RedTeamPanel      from './components/RedTeamPanel'
import FlowDetailPage    from './components/FlowDetailPage'

import ReportsPage       from './pages/ReportsPage'
import AdversarialPage   from './pages/AdversarialPage'
import IncidentsPage     from './pages/IncidentsPage'

const API = 'http://127.0.0.1:8000'

function AnimatedCounter({ value }) {
  const [display, setDisplay] = useState(value)
  const prevRef = useRef(value)

  useEffect(() => {
    const from = prevRef.current
    const to = value
    if (from === to) return
    let start = null
    const duration = 450
    let raf = null
    const step = (ts) => {
      if (!start) start = ts
      const progress = Math.min((ts - start) / duration, 1)
      const ease = 1 - Math.pow(1 - progress, 3)
      setDisplay(Math.round(from + (to - from) * ease))
      if (progress < 1) {
        raf = requestAnimationFrame(step)
      } else {
        prevRef.current = to
        setDisplay(to)
      }
    }
    raf = requestAnimationFrame(step)
    return () => cancelAnimationFrame(raf)
  }, [value])

  return <span className="odometer-number">{display}</span>
}

export default function App() {
  const { flows, connected, sendFlow } = useWebSocket()
  const [currentTab, setCurrentTab] = useState('dashboard') // 'dashboard' | 'adversarial' | 'incidents' | 'reports'
  const [selectedFlow, setSelectedFlow] = useState(null)
  const [viewingDetailFlow, setViewingDetailFlow] = useState(null)

  // Enterprise Theme State (Default: light, persisted in localStorage)
  const [theme, setTheme] = useState(() => {
    try {
      return localStorage.getItem('trustflow-theme') || 'light'
    } catch {
      return 'light'
    }
  })

  useEffect(() => {
    try {
      document.documentElement.setAttribute('data-theme', theme)
      localStorage.setItem('trustflow-theme', theme)
    } catch {
      document.documentElement.setAttribute('data-theme', theme)
    }
  }, [theme])

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light')
  }

  const { data: vlanData }         = usePolling(`${API}/api/vlan-status`,    4000)
  const { data: rtData,   error: rtErr   } = usePolling(`${API}/api/redteam-status`,   5000)
  const { data: incidentLogs }     = usePolling(`${API}/api/incident-logs`,  4000)

  // Initialize selection once when first flow arrives
  useEffect(() => {
    if (!selectedFlow && flows.length > 0) {
      setSelectedFlow(flows[0])
    }
  }, [flows, selectedFlow])

  // Helper to open detail page for any flow or flow_id
  const handleOpenDetail = (flowOrId) => {
    if (typeof flowOrId === 'object' && flowOrId !== null) {
      setViewingDetailFlow(flowOrId)
    } else {
      const match = flows.find(f => f.flow_id === flowOrId)
      if (match) {
        setViewingDetailFlow(match)
      } else if (selectedFlow) {
        setViewingDetailFlow({ ...selectedFlow, flow_id: flowOrId })
      }
    }
  }

  return (
    <>
      {/* Background layer */}
      <CircuitBackground />

      <div className="app-shell-layout">
        {/* Navigation Sidebar */}
        <Sidebar
          currentTab={currentTab}
          onSelectTab={(tab) => {
            setViewingDetailFlow(null)
            setCurrentTab(tab)
          }}
          flowCount={flows.length}
          wsConnected={connected}
          theme={theme}
          toggleTheme={toggleTheme}
        />

        {/* Main Content Area */}
        <div className="app-main-viewport">
          {viewingDetailFlow ? (
            <FlowDetailPage
              flow={viewingDetailFlow}
              vlanData={vlanData}
              redTeamData={rtData}
              onBack={() => setViewingDetailFlow(null)}
            />
          ) : currentTab === 'reports' ? (
            <ReportsPage
              flows={flows}
              incidentLogs={incidentLogs || []}
              vlanData={vlanData || {}}
              redTeamData={rtData || {}}
            />
          ) : currentTab === 'adversarial' ? (
            <AdversarialPage
              redTeamData={rtData}
              error={rtErr}
              onOpenDetail={handleOpenDetail}
            />
          ) : currentTab === 'incidents' ? (
            <IncidentsPage
              incidentLogs={incidentLogs || []}
              vlanData={vlanData || {}}
              onOpenDetail={handleOpenDetail}
            />
          ) : (
            <div className="dashboard">
              {/* ── Top bar ─────────────────────────────────────── */}
              <header className="topbar">
                <div className="topbar-logo">
                  <div className="topbar-emblem" aria-hidden="true">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                      <path
                        d="M12 2L3 7V12C3 17.52 6.84 22.74 12 24C17.16 22.74 21 17.52 21 12V7L12 2Z"
                        stroke="var(--accent)"
                        strokeWidth="1.5"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        fill="var(--accent-subtle)"
                      />
                      <path
                        d="M12 7V17M8 11L12 7L16 11"
                        stroke="var(--accent)"
                        strokeWidth="1.5"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                    </svg>
                  </div>
                  <div className="topbar-brand">
                    <span className="brand-title">TRUST<span className="accent-text">FLOW</span> <span className="sub-badge">NGFW</span></span>
                    <span className="sub">SOC LIVE OPERATIONS &amp; ZERO-TRUST CONTROL MATRIX</span>
                  </div>
                </div>
                <div className="topbar-meta">
                  <span className="meta-item date-tag">{new Date().toLocaleDateString('en-GB', { weekday: 'short', day: '2-digit', month: 'short', year: 'numeric' })}</span>
                  <div className="ws-status meta-item">
                    <div className={`ws-dot${connected ? ' connected' : ''}`} />
                    <span className="ws-label">{connected ? 'WS Connected' : 'WS Disconnected'}</span>
                  </div>
                  <div className="meta-item flow-counter-wrap">
                    <AnimatedCounter value={flows.length} />
                    <span className="counter-label">flows inspected</span>
                  </div>
                  <button
                    className="meta-item theme-toggle-pill"
                    onClick={toggleTheme}
                    title={`Switch to ${theme === 'light' ? 'dark' : 'light'} theme`}
                    aria-label="Toggle theme"
                  >
                    {theme === 'light' ? (
                      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
                      </svg>
                    ) : (
                      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
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
                    <span>{theme === 'light' ? 'Dark' : 'Light'}</span>
                  </button>
                </div>
              </header>

              {/* ── Main Operations Grid ────────────────────────── */}
              <div className="main-grid">
                {/* Left column — Live Feed (spans full height) */}
                <FlowFeed
                  flows={flows}
                  selectedFlowId={selectedFlow?.flow_id}
                  onSelect={setSelectedFlow}
                  onOpenDetail={handleOpenDetail}
                />

                {/* Right side 2×2 subgrid */}
                <div className="right-grid">
                  {/* Row 1 */}
                  <EnsemblePanel
                    flow={selectedFlow}
                    onOpenDetail={handleOpenDetail}
                  />
                  <TrustPanel
                    flow={selectedFlow}
                    sendFlow={sendFlow}
                  />

                  {/* Row 2: Mitigations + Full Extended Adversarial Tests Panel */}
                  <MitigationPanel
                    flow={selectedFlow}
                    vlanData={vlanData}
                  />

                  {/* Extended Adversarial Panel taking full bottom space without Federated */}
                  <div className="extended-adversarial-col">
                    <RedTeamPanel
                      data={rtData}
                      error={rtErr}
                      onOpenDetail={handleOpenDetail}
                    />
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  )
}
