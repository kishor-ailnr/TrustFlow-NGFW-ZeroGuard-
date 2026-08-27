// src/App.jsx
// Root component — wires all six panels together & supports full-screen flow detail pages

import { useState, useEffect, useRef } from 'react'
import { useWebSocket } from './hooks/useWebSocket'
import { usePolling }   from './hooks/usePolling'

import CircuitBackground from './components/CircuitBackground'
import FlowFeed          from './components/FlowFeed'
import EnsemblePanel     from './components/EnsemblePanel'
import TrustPanel        from './components/TrustPanel'
import MitigationPanel    from './components/MitigationPanel'
import FederatedPanel    from './components/FederatedPanel'
import RedTeamPanel      from './components/RedTeamPanel'
import FlowDetailPage    from './components/FlowDetailPage'

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
  const [selectedFlow, setSelectedFlow] = useState(null)
  const [viewingDetailFlow, setViewingDetailFlow] = useState(null)

  const { data: vlanData }     = usePolling(`${API}/api/vlan-status`,    4000)
  const { data: fedData,  error: fedErr  } = usePolling(`${API}/api/federated-status`, 5000)
  const { data: rtData,   error: rtErr   } = usePolling(`${API}/api/redteam-status`,   5000)

  // Initialize selection once when first flow arrives, but do not overwrite when subsequent flows stream in
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
    {/* Ambient vault control room depth */}
    <div className="bg-blobs" aria-hidden="true">
      <div className="blob blob-1" />
      <div className="blob blob-2" />
      <div className="blob blob-3" />
      <div className="blob blob-4" />
      <div className="vault-mesh" />
    </div>

    {/* Continuous Animated Circuit-Line Background (Illuminated PCB traces & Traveling Pulses) */}
    <CircuitBackground />

    {viewingDetailFlow ? (
      <FlowDetailPage
        flow={viewingDetailFlow}
        vlanData={vlanData}
        redTeamData={rtData}
        onBack={() => setViewingDetailFlow(null)}
      />
    ) : (
      <div className="dashboard">

        {/* ── Top bar ─────────────────────────────────────── */}
        <header className="topbar">
          <div className="topbar-logo">
            <div className="topbar-emblem" aria-hidden="true">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L3 7V12C3 17.52 6.84 22.74 12 24C17.16 22.74 21 17.52 21 12V7L12 2Z" stroke="#C9A227" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" fill="rgba(201, 162, 39, 0.12)"/>
                <path d="M12 7V17M8 11L12 7L16 11" stroke="#E7E3D8" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
            <div className="topbar-brand">
              <span className="brand-title">TRUST<span className="gold">FLOW</span> <span className="sub-badge">NGFW</span></span>
              <span className="sub">SOC LIVE INSTRUMENT PANEL</span>
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
              <span className="counter-label">flows received</span>
            </div>
          </div>
        </header>

        {/* ── Main grid ───────────────────────────────────── */}
        <div className="main-grid">

          {/* Left column — Live Feed (spans both rows) */}
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

            {/* Row 2 */}
            <MitigationPanel
              flow={selectedFlow}
              vlanData={vlanData}
            />

            {/* Bottom-right: fed + redteam share a vertical split */}
            <div className="split-col">
              <FederatedPanel data={fedData} error={fedErr} />
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
    </>
  )
}
