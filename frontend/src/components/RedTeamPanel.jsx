// src/components/RedTeamPanel.jsx
// Panel 6 — adversarial / red-team test results

import { useEffect, useState } from 'react'

function StatCount({ value, duration = 600 }) {
  const [val, setVal] = useState(0)
  const target = Number(value) || 0

  useEffect(() => {
    let start = null
    let raf = null
    const step = (ts) => {
      if (!start) start = ts
      const progress = Math.min((ts - start) / duration, 1)
      const ease = 1 - Math.pow(1 - progress, 3)
      setVal(Math.round(target * ease))
      if (progress < 1) {
        raf = requestAnimationFrame(step)
      } else {
        setVal(target)
      }
    }
    raf = requestAnimationFrame(step)
    return () => cancelAnimationFrame(raf)
  }, [target, duration])

  return <span>{val}</span>
}

function DetectedBadge() {
  return (
    <span className="detected-badge-wrap">
      <svg className="check-svg" width="12" height="12" viewBox="0 0 24 24" fill="none">
        <path
          d="M4 12.5L9.5 18L20 6"
          stroke="var(--gold, #C9A227)"
          strokeWidth="3"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="check-path"
        />
      </svg>
      <span>Detected</span>
    </span>
  )
}

export default function RedTeamPanel({ data, error, onOpenDetail }) {
  if (error || !data || Object.keys(data).length === 0) {
    return (
      <div className="panel panel-stage-6">
        <div className="panel-header">
          <span className="panel-title">🎯 Adversarial Tests</span>
        </div>
        <div className="empty-state" style={{ height: '100%' }}>
          <div className="empty-icon">🎯</div>
          <div>No red-team results yet</div>
          <div style={{ fontSize: 11, opacity: 0.6 }}>Run backend/redteam/ scripts to populate</div>
        </div>
      </div>
    )
  }

  const { summary, total_tested, still_detected, evaded, per_flow } = data

  return (
    <div className="panel panel-stage-6">
      <div className="panel-header">
        <span className="panel-title">🎯 Adversarial Tests</span>
        <span className="panel-badge">{total_tested} flows tested</span>
      </div>
      <div className="panel-body">

        <div className="redteam-summary">{summary ?? `${still_detected}/${total_tested} attacks still detected after perturbation`}</div>

        <div className="redteam-stats-grid">
          {[
            { label: 'Total tested', val: total_tested, color: 'var(--text-platinum)' },
            { label: 'Still detected', val: still_detected, color: 'var(--gold)' },
            { label: 'Evaded',         val: evaded,         color: 'var(--block)' },
          ].map(({ label, val, color }) => (
            <div key={label} className="redteam-stat-card">
              <div className="redteam-stat-num" style={{ color }}>
                {val !== undefined ? <StatCount value={val} /> : '—'}
              </div>
              <div className="redteam-stat-label">{label}</div>
            </div>
          ))}
        </div>

        {per_flow && per_flow.length > 0 && (
          <div className="redteam-table-wrap">
            <table className="redteam-table">
              <thead>
                <tr>
                  <th>Flow ID</th>
                  <th>Baseline</th>
                  <th>Perturbed</th>
                  <th>Result</th>
                </tr>
              </thead>
              <tbody>
                {per_flow.map((row, i) => {
                  const evadedRow = row.perturbed_action !== row.baseline_action
                  return (
                    <tr
                      key={i}
                      className="redteam-row-anim clickable-row"
                      style={{ animationDelay: `${i * 40}ms` }}
                      onClick={() => onOpenDetail && onOpenDetail(row)}
                      title={onOpenDetail ? `Inspect flow ${row.flow_id}` : undefined}
                    >
                      <td className="cell-flow-id">
                        {row.flow_id ?? `flow-${i}`}
                      </td>
                      <td>{row.baseline_action ?? '—'}</td>
                      <td>{row.perturbed_action ?? '—'}</td>
                      <td className={evadedRow ? 'evaded' : 'detected'}>
                        {evadedRow ? '⚠ Evaded' : <DetectedBadge />}
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}

