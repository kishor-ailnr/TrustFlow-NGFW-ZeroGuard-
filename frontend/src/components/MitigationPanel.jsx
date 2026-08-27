// src/components/MitigationPanel.jsx
// Panel 4 — mitigation action display with VLAN + honeypot decoy terminal + Telegram notes

import { useState, useEffect } from 'react'

function TypewriterText({ text, speed = 16 }) {
  const [displayed, setDisplayed] = useState('')

  useEffect(() => {
    setDisplayed('')
    if (!text) return
    let i = 0
    const timer = setInterval(() => {
      i++
      setDisplayed(text.slice(0, i))
      if (i >= text.length) {
        clearInterval(timer)
      }
    }, speed)
    return () => clearInterval(timer)
  }, [text, speed])

  return <span>{displayed}</span>
}

export default function MitigationPanel({ flow, vlanData }) {
  const [honeypotSession, setHoneypotSession] = useState(null)
  const [showTerminal, setShowTerminal] = useState(true)
  const [, setActiveStep] = useState(999)
  const [, setLoadingHoney] = useState(false)

  const flow_id = flow?.flow_id
  const action = flow?.action
  const reason = flow?.reason
  const source_ip = flow?.source_ip

  useEffect(() => {
    if (action === 'Quarantine' && flow_id) {
      setLoadingHoney(true)
      fetch(`http://127.0.0.1:8000/api/honeypot-session/${flow_id}`)
        .then((res) => res.json())
        .then((data) => {
          setHoneypotSession(data)
          setActiveStep(data?.commands?.length || 999)
          setLoadingHoney(false)
        })
        .catch(() => {
          setLoadingHoney(false)
        })
    } else {
      setHoneypotSession(null)
    }
  }, [flow_id, action])

  if (!flow) {
    return (
      <div className="panel panel-stage-4">
        <div className="panel-header"><span className="panel-title">⚔️ Mitigation Action</span></div>
        <div className="empty-state" style={{ height: '100%' }}>
          <div className="empty-icon">⚔️</div>
          <div>Select a flow to see action taken</div>
        </div>
      </div>
    )
  }

  const actionColors = {
    Allow:      'var(--allow)',
    'Rate-limit': 'var(--ratelimit)',
    Quarantine: 'var(--quarantine)',
    Block:      'var(--block)',
  }
  const actionIcons = {
    Allow: '✅', 'Rate-limit': '🔁', Quarantine: '🔒', Block: '🚫'
  }

  const vlanEntry = vlanData ? Object.entries(vlanData).find(([k]) => k === flow_id) : null
  const vlanInfo  = vlanEntry ? vlanEntry[1] : null

  return (
    <div className="panel panel-stage-4" style={{ overflowY: 'auto' }}>
      <div className="panel-header">
        <span className="panel-title">⚔️ Mitigation Action</span>
        <span className="panel-badge">{source_ip}</span>
      </div>
      <div className="panel-body">

        <div className="miti-action-display">
          <div className="miti-action-icon">{actionIcons[action] ?? '❓'}</div>
          <div className="miti-action-text">
            <div className="miti-action-label" style={{ color: actionColors[action] ?? 'var(--text)' }}>
              {action}
            </div>
            <div className="miti-reason">{reason}</div>
          </div>
        </div>

        <div className="miti-details">

          {action === 'Block' && (
            <div className="miti-row">
              <span className="miti-icon">🔥</span>
              <div className="miti-text">
                <strong>iptables DROP rule applied</strong> — source IP{' '}
                <code style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--text-platinum)' }}>{source_ip}</code>{' '}
                blocked at the network level via iptables. Rule persists until manually flushed.
              </div>
            </div>
          )}

          {action === 'Quarantine' && (
            <>
              <div className="miti-row">
                <span className="miti-icon">🍯</span>
                <div className="miti-text">
                  <strong>Redirected to Cowrie Honeypot</strong> — flow diverted to port 2222 SSH
                  decoy sandbox for attacker profiling and session capture.
                </div>
              </div>
              <div className="miti-row">
                <span className="miti-icon">🌐</span>
                <div className="miti-text">
                  <strong>VLAN Quarantine Status:</strong>{' '}
                  {vlanInfo ? (
                    <>
                      <span className="vlan-badge">🔒 {vlanInfo.vlan_status}</span>
                      {' '}
                      <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>
                        {vlanInfo.simulated ? '(simulated sandbox isolation)' : ''}
                        {' '}· {vlanInfo.timestamp?.slice(0, 19).replace('T', ' ')}
                      </span>
                    </>
                  ) : (
                    <span style={{ color: 'var(--text-muted)', fontSize: 12 }}>
                      🔒 QUARANTINED_VLAN_99 (Decoy Network)
                    </span>
                  )}
                </div>
              </div>

              {/* Interactive Decoy Terminal Window with scanlines and typewriter */}
              <div className="honeypot-terminal-wrapper">
                <div className="terminal-scanlines" aria-hidden="true" />
                <div className="honeypot-header">
                  <div className="honey-dots">
                    <span className="hdot hdot-red"></span>
                    <span className="hdot hdot-yellow"></span>
                    <span className="hdot hdot-green"></span>
                  </div>
                  <div className="honey-title">
                    🍯 Decoy Honeypot Shell — {honeypotSession?.session_id || 'COWRIE-SESSION'}
                  </div>
                  <button 
                    className="honey-toggle-btn"
                    onClick={() => setShowTerminal(!showTerminal)}
                  >
                    {showTerminal ? 'Hide Terminal' : 'Show Terminal'}
                  </button>
                </div>

                {showTerminal && (
                  <div className="honeypot-terminal-body">
                    <div className="honey-meta-bar">
                      <div><span className="honey-dim">Host:</span> cowrie-decoy-01:2222</div>
                      <div><span className="honey-dim">Attacker:</span> {source_ip}</div>
                      <div><span className="honey-dim">Isolation:</span> VLAN 99</div>
                      <div><span className="honey-dim">Intent:</span> <span style={{ color: '#F2994A' }}>{honeypotSession?.intent || 'Profiling'}</span></div>
                    </div>

                    <div className="honey-auth-line">
                      <span className="honey-auth-badge">AUTH TRAP</span>
                      <span>SSH login attempt: user=<code>{honeypotSession?.auth?.username || 'root'}</code> pass=<code>••••••••</code> &rarr; <strong style={{ color: '#10B981' }}>SESSION GRANTED (DECOY)</strong></span>
                    </div>

                    <div className="honey-console-stream">
                      {honeypotSession?.commands?.map((c, i) => (
                        <div key={i} className="honey-cmd-block">
                          <div className="honey-cmd-line">
                            <span className="honey-prompt">root@decoy:~#</span>
                            <span className="honey-cmd-text">
                              <TypewriterText text={c.cmd} speed={18} />
                            </span>
                          </div>
                          <div className="honey-output-text">
                            <TypewriterText text={c.output} speed={12} />
                          </div>
                        </div>
                      ))}
                      <div className="honey-cursor-line">
                        <span className="honey-prompt">root@decoy:~#</span>
                        <span className="honey-cursor">█</span>
                      </div>
                    </div>

                    <div className="honey-footer-stats">
                      <span>⌨️ <strong>{honeypotSession?.keystrokes_captured || 0}</strong> Keystrokes Logged</span>
                      <span>📦 <strong>{honeypotSession?.payloads_intercepted || 0}</strong> Malware Droppers Contained</span>
                      <span className="honey-trapping-live">
                        <span className="trapping-dot" /> Trapping Live
                      </span>
                    </div>
                  </div>
                )}
              </div>
            </>
          )}

          {(action === 'Block' || action === 'Quarantine') && (
            <div className="miti-row telegram-alert-banner">
              <span className="miti-icon telegram-plane-icon">✈️</span>
              <div className="miti-text">
                <strong>Telegram alert sent</strong> — SOC notification dispatched via Telegram bot
                (flow_id, action, risk score, trust score, reason).
              </div>
            </div>
          )}

          {(action === 'Allow' || action === 'Rate-limit') && (
            <div className="miti-row">
              <span className="miti-icon">ℹ️</span>
              <div className="miti-text" style={{ color: 'var(--text-muted)' }}>
                No blocking action taken. Flow passed the trust + risk matrix threshold.
                {action === 'Rate-limit' && ' Bandwidth throttling policy applied.'}
              </div>
            </div>
          )}

        </div>
      </div>
    </div>
  )
}

