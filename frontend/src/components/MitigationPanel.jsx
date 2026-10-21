// src/components/MitigationPanel.jsx
// Panel 4 — iptables enforcement, Cowrie honeypot & Telegram alert status
// Flat enterprise styling, status text colors, no emojis, no glassmorphism

import { useState, useEffect } from 'react'

function TypewriterText({ text, speed = 25 }) {
  const [displayed, setDisplayed] = useState('')

  useEffect(() => {
    let i = 0
    setDisplayed('')
    const timer = setInterval(() => {
      if (i < text.length) {
        setDisplayed(text.slice(0, i + 1))
        i++
      } else {
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

  const { flow_id, source_ip, action, reason } = flow || {}

  useEffect(() => {
    if (flow_id && action === 'Quarantine') {
      fetch(`http://127.0.0.1:8000/api/honeypot-session/${flow_id}`)
        .then(r => r.json())
        .then(d => {
          if (d && d.session_id) setHoneypotSession(d)
        })
        .catch(() => {})
    } else {
      setHoneypotSession(null)
    }
  }, [flow_id, action])

  const actionColors = {
    Allow: 'var(--allow-text)',
    'Rate-limit': 'var(--ratelimit-text)',
    Quarantine: 'var(--quarantine-text)',
    Block: 'var(--block-text)',
  }

  const actionIcons = {
    Allow: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="20 6 9 17 4 12" />
      </svg>
    ),
    'Rate-limit': (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="23 4 23 10 17 10" />
        <polyline points="1 20 1 14 7 14" />
        <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15" />
      </svg>
    ),
    Quarantine: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
        <path d="M7 11V7a5 5 0 0 1 10 0v4" />
      </svg>
    ),
    Block: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="12" cy="12" r="10" />
        <line x1="4.93" y1="4.93" x2="19.07" y2="19.07" />
      </svg>
    ),
  }

  if (!flow) {
    return (
      <div className="panel panel-stage-4">
        <div className="panel-header"><span className="panel-title">Mitigation Action</span></div>
        <div className="empty-state" style={{ height: '100%' }}>
          <div>Select a flow to see action taken</div>
        </div>
      </div>
    )
  }

  const vlanEntry = vlanData ? Object.entries(vlanData).find(([k]) => k === flow_id) : null
  const vlanInfo  = vlanEntry ? vlanEntry[1] : null

  return (
    <div className="panel panel-stage-4" style={{ overflowY: 'auto' }}>
      <div className="panel-header">
        <span className="panel-title" style={{ color: actionColors[action] ?? 'var(--text-primary)' }}>
          Mitigation Action
        </span>
        <span className="panel-badge">{source_ip}</span>
      </div>
      <div className="panel-body">

        <div className="miti-action-display">
          <div className="miti-action-icon" style={{ color: actionColors[action] ?? 'var(--text-primary)' }}>
            {actionIcons[action] ?? null}
          </div>
          <div className="miti-action-text">
            <div className="miti-action-label" style={{ color: actionColors[action] ?? 'var(--text-primary)' }}>
              {action}
            </div>
            <div className="miti-reason">{reason}</div>
          </div>
        </div>

        <div className="miti-details">

          {action === 'Block' && (
            <div className="miti-row">
              <span className="miti-tag-badge block">FW-DROP</span>
              <div className="miti-text">
                <strong>Windows Firewall Netsh / iptables DROP rule applied</strong> — source IP{' '}
                <code style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--text-primary)' }}>{source_ip}</code>{' '}
                blocked at the kernel level. Rule persists until manually flushed.
              </div>
            </div>
          )}

          {action === 'Quarantine' && (
            <>
              <div className="miti-row">
                <span className="miti-tag-badge quarantine">HONEYPOT</span>
                <div className="miti-text">
                  <strong>Redirected to Cowrie Honeypot</strong> — flow diverted to port 2222 SSH
                  decoy sandbox for attacker profiling and session capture.
                </div>
              </div>
              <div className="miti-row">
                <span className="miti-tag-badge info">VLAN-99</span>
                <div className="miti-text">
                  <strong>VLAN Quarantine Status:</strong>{' '}
                  {vlanInfo ? (
                    <>
                      <span className="vlan-badge">{vlanInfo.vlan_status}</span>
                      {' '}
                      <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>
                        {vlanInfo.simulated ? '(simulated sandbox isolation)' : ''}
                        {' '}· {vlanInfo.timestamp?.slice(0, 19).replace('T', ' ')}
                      </span>
                    </>
                  ) : (
                    <span style={{ color: 'var(--text-muted)', fontSize: 12 }}>
                      QUARANTINED_VLAN_99 (Decoy Network)
                    </span>
                  )}
                </div>
              </div>

              {/* Decoy Terminal Window */}
              <div className="honeypot-terminal-wrapper">
                <div className="honeypot-header">
                  <div className="honey-dots">
                    <span className="hdot hdot-red"></span>
                    <span className="hdot hdot-yellow"></span>
                    <span className="hdot hdot-green"></span>
                  </div>
                  <div className="honey-title">
                    Decoy Honeypot Shell — {honeypotSession?.session_id || 'COWRIE-SESSION'}
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
                      <div><span className="honey-dim">Intent:</span> <span style={{ color: 'var(--quarantine-text)' }}>{honeypotSession?.intent || 'Profiling'}</span></div>
                    </div>

                    <div className="honey-auth-line">
                      <span className="honey-auth-badge">AUTH TRAP</span>
                      <span>SSH login attempt: user=<code>{honeypotSession?.auth?.username || 'root'}</code> pass=<code>••••••••</code> &rarr; <strong style={{ color: 'var(--allow-text)' }}>SESSION GRANTED (DECOY)</strong></span>
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
                      <span><strong>{honeypotSession?.keystrokes_captured || 0}</strong> Keystrokes Logged</span>
                      <span><strong>{honeypotSession?.payloads_intercepted || 0}</strong> Malware Droppers Contained</span>
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
              <span className="miti-tag-badge block">ALERT</span>
              <div className="miti-text">
                <strong>Telegram alert sent</strong> — SOC notification dispatched via Telegram bot
                (flow_id, action, risk score, trust score, reason).
              </div>
            </div>
          )}

          {(action === 'Allow' || action === 'Rate-limit') && (
            <div className="miti-row">
              <span className="miti-tag-badge allow">PASS</span>
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
