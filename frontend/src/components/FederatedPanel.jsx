// src/components/FederatedPanel.jsx
// Panel 5 — federated learning accuracy chart (recharts)

import {
  ResponsiveContainer, LineChart, Line, XAxis, YAxis,
  CartesianGrid, Tooltip, ReferenceLine
} from 'recharts'

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null
  return (
    <div style={{
      background: 'rgba(20, 23, 28, 0.95)',
      backdropFilter: 'blur(12px)',
      border: '1px solid rgba(201, 162, 39, 0.35)',
      boxShadow: '0 8px 24px rgba(0,0,0,0.6)',
      borderRadius: 8, padding: '8px 12px', fontSize: 11,
      fontFamily: "var(--font-body, 'Plus Jakarta Sans', sans-serif)"
    }}>
      <div style={{ color: 'var(--text-muted, #8A8F98)', marginBottom: 4 }}>Round {label}</div>
      <div style={{ color: 'var(--gold, #C9A227)', fontFamily: "var(--font-mono, 'JetBrains Mono', monospace)", fontWeight: 700 }}>
        Accuracy: {(payload[0].value * 100).toFixed(1)}%
      </div>
    </div>
  )
}

export default function FederatedPanel({ data, error }) {
  return (
    <div className="panel panel-stage-5">
      <div className="panel-header">
        <span className="panel-title">🔗 Federated Learning</span>
        <span className="panel-badge">2 simulated nodes</span>
      </div>

      {error && (
        <div style={{ padding: 14, fontSize: 12, color: 'var(--text-muted)' }}>
          No data yet — run federated training to populate.
        </div>
      )}

      {!error && (!data || data.length === 0) && (
        <div className="empty-state" style={{ height: '100%' }}>
          <div className="empty-icon">🔗</div>
          <div>No federated rounds logged yet</div>
        </div>
      )}

      {data && data.length > 0 && (
        <div className="fed-chart-wrap">
          <div style={{ fontSize: 10, color: 'var(--text-muted)', marginBottom: 6, paddingLeft: 8, textTransform: 'uppercase', letterSpacing: '0.8px' }}>
            Model Accuracy by Round
          </div>
          <ResponsiveContainer width="100%" height="82%">
            <LineChart data={data} margin={{ top: 4, right: 16, left: -16, bottom: 4 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(85, 80, 62, 0.3)" />
              <XAxis
                dataKey="round"
                tick={{ fill: '#8A8F98', fontSize: 10, fontFamily: 'JetBrains Mono' }}
                label={{ value: 'Round', position: 'insideBottom', offset: -2, fill: '#8A8F98', fontSize: 10 }}
              />
              <YAxis
                domain={[0.5, 1.0]}
                tick={{ fill: '#8A8F98', fontSize: 10, fontFamily: 'JetBrains Mono' }}
                tickFormatter={v => `${(v * 100).toFixed(0)}%`}
              />
              <Tooltip content={<CustomTooltip />} />
              <ReferenceLine y={0.9} stroke="var(--gold, #C9A227)" strokeDasharray="3 3"
                label={{ value: '90% Target', fill: 'var(--gold, #C9A227)', fontSize: 9 }} />
              <Line
                type="monotone"
                dataKey="accuracy"
                stroke="#C9A227"
                strokeWidth={2}
                dot={{ fill: '#C9A227', r: 3.5, strokeWidth: 1, stroke: '#14171C' }}
                activeDot={{ r: 5.5, fill: '#E7E3D8', stroke: '#C9A227', strokeWidth: 2 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  )
}

