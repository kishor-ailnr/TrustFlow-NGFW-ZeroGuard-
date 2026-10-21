// src/components/FederatedPanel.jsx
// Panel 5 — federated learning accuracy chart (recharts)
// Enterprise styling: flat solid line, token colors, no glow, hairline borders

import {
  ResponsiveContainer, LineChart, Line, XAxis, YAxis,
  CartesianGrid, Tooltip, ReferenceLine
} from 'recharts'

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null
  return (
    <div style={{
      background: 'var(--surface-raised)',
      border: '1px solid var(--border)',
      boxShadow: 'var(--shadow-sm)',
      borderRadius: 4, padding: '6px 10px', fontSize: 11,
      fontFamily: "var(--font-body)"
    }}>
      <div style={{ color: 'var(--text-muted)', marginBottom: 2 }}>Round {label}</div>
      <div style={{ color: 'var(--accent)', fontFamily: "var(--font-mono)", fontWeight: 700 }}>
        Accuracy: {(payload[0].value * 100).toFixed(1)}%
      </div>
    </div>
  )
}

export default function FederatedPanel({ data, error }) {
  return (
    <div className="panel panel-stage-5">
      <div className="panel-header">
        <span className="panel-title">Federated Learning</span>
        <span className="panel-badge">2 simulated nodes</span>
      </div>

      {error && (
        <div style={{ padding: 14, fontSize: 12, color: 'var(--text-muted)' }}>
          No data yet — run federated training to populate.
        </div>
      )}

      {!error && (!data || data.length === 0) && (
        <div className="empty-state" style={{ height: '100%' }}>
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
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis
                dataKey="round"
                tick={{ fill: 'var(--text-secondary)', fontSize: 10, fontFamily: 'var(--font-mono)' }}
                label={{ value: 'Round', position: 'insideBottom', offset: -2, fill: 'var(--text-muted)', fontSize: 10 }}
              />
              <YAxis
                domain={[0.5, 1.0]}
                tick={{ fill: 'var(--text-secondary)', fontSize: 10, fontFamily: 'var(--font-mono)' }}
                tickFormatter={v => `${(v * 100).toFixed(0)}%`}
              />
              <Tooltip content={<CustomTooltip />} />
              <ReferenceLine y={0.9} stroke="var(--text-muted)" strokeDasharray="3 3"
                label={{ value: '90% Target', fill: 'var(--text-muted)', fontSize: 9 }} />
              <Line
                type="monotone"
                dataKey="accuracy"
                stroke="var(--accent)"
                strokeWidth={2}
                dot={{ fill: 'var(--accent)', r: 3, strokeWidth: 1, stroke: 'var(--surface)' }}
                activeDot={{ r: 5, fill: 'var(--accent-hover)', stroke: 'var(--surface)', strokeWidth: 2 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  )
}
