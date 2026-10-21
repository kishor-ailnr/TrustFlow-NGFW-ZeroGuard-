// src/components/FlowFeed.jsx
// Panel 1 — scrolling live flow list

import { useEffect, useState } from 'react'
import { riskClass } from '../utils'

function FlowScore({ score }) {
  const [val, setVal] = useState(0)
  const target = score ?? 0

  useEffect(() => {
    let start = null
    const duration = 400
    let raf = null
    const step = (ts) => {
      if (!start) start = ts
      const progress = Math.min((ts - start) / duration, 1)
      const ease = 1 - Math.pow(1 - progress, 3)
      setVal(target * ease)
      if (progress < 1) {
        raf = requestAnimationFrame(step)
      } else {
        setVal(target)
      }
    }
    raf = requestAnimationFrame(step)
    return () => cancelAnimationFrame(raf)
  }, [target])

  return <span>{val.toFixed(1)}</span>
}

export default function FlowFeed({ flows, selectedFlowId, onSelect, onOpenDetail }) {
  return (
    <div className="panel span-row panel-stage-1">
      <div className="panel-header">
        <span className="panel-title">Live Flow Feed</span>
        <span className="panel-badge">{flows.length} flows</span>
      </div>
      <div className="panel-body">
        {flows.length === 0 ? (
          <div className="empty-state">
            <div>Waiting for flows on WebSocket…</div>
            <div style={{ fontSize: 11, opacity: 0.6 }}>Send a payload to ws://127.0.0.1:8000/ws</div>
          </div>
        ) : (
          <div className="flow-feed-list">
            {flows.map((f, i) => {
              const isSelected = selectedFlowId === f.flow_id
              return (
                <div
                  key={f.flow_id ? `${f.flow_id}-${i}` : i}
                  className={`flow-item${isSelected ? ' selected' : ''}`}
                  onClick={() => onSelect(f)}
                >
                  <div className="flow-main">
                    <div className="flow-id-row">
                      <span className="flow-id" title={f.flow_id}>{f.flow_id}</span>
                      {onOpenDetail && (
                        <button
                          className="flow-inspect-pill"
                          onClick={(e) => {
                            e.stopPropagation()
                            onOpenDetail(f)
                          }}
                          title="Open detailed flow inspection page"
                        >
                          Inspect ↗
                        </button>
                      )}
                    </div>
                    <div className="flow-meta">
                      <span className="flow-ip">{f.source_ip}</span> &nbsp;·&nbsp; <span className="flow-trust">trust {f.trust_score?.toFixed(0)}</span> ({f.trust_band})
                      &nbsp;·&nbsp; <span className="flow-time">{f._ts}</span>
                    </div>
                  </div>
                  <div className="flow-right">
                    <div className={`flow-risk ${riskClass(f.fused_risk_score)}`}>
                      <FlowScore score={f.fused_risk_score} />
                    </div>
                    <div className={`action-pill ${f.action}`}>{f.action}</div>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}

