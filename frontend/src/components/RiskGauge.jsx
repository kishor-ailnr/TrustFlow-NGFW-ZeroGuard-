// src/components/RiskGauge.jsx
// Enterprise Precision Instrument Dial for fused_risk_score.
// Flat surfaces, hairline borders, single accent color, no gradients, no glows.

import { useEffect, useRef, useState } from 'react'

const R        = 66          // ring radius
const CX       = 100         // SVG center (viewBox 200x180)
const CY       = 92
const CIRC     = 2 * Math.PI * R   // ~414.69
const STROKE_W = 8
const GAP_DEG  = 64          // open gap at the bottom
const GAP_RAD  = (GAP_DEG / 360) * CIRC   // open gap length

// Clamp score 0-100 and compute stroke-dashoffset
function computeOffset(score) {
  const usable = CIRC - GAP_RAD
  const filled = (Math.min(Math.max(score, 0), 100) / 100) * usable
  return CIRC - filled
}

// Count-up animation synchronized with the sweep
function useAnimatedScore(target, durationMs = 600) {
  const [display, setDisplay] = useState(target)
  const raf  = useRef(null)
  const prev = useRef(target)

  useEffect(() => {
    const from = prev.current
    const to   = target
    if (Math.abs(from - to) < 0.05) { setDisplay(to); return }

    const start = performance.now()
    const tick  = (now) => {
      const t = Math.min((now - start) / durationMs, 1)
      const ease = 1 - Math.pow(1 - t, 3)
      setDisplay(from + (to - from) * ease)
      if (t < 1) {
        raf.current = requestAnimationFrame(tick)
      } else {
        prev.current = to
        setDisplay(to)
      }
    }
    raf.current = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(raf.current)
  }, [target, durationMs])

  return display
}

// Generate fine chronograph ticks along the usable arc
function generateTicks() {
  const ticks = []
  const totalTicks = 40 // every 2.5%
  const startAngle = 90 + GAP_DEG / 2
  const sweepAngle = 360 - GAP_DEG

  for (let i = 0; i <= totalTicks; i++) {
    const pct = i / totalTicks
    const angleDeg = startAngle + pct * sweepAngle
    const angleRad = (angleDeg * Math.PI) / 180
    const isMajor = i % 4 === 0 // every 10%
    const isMid   = i % 4 === 2
    const innerR  = isMajor ? 52 : (isMid ? 55 : 57)
    const outerR  = 59

    const x1 = CX + innerR * Math.cos(angleRad)
    const y1 = CY + innerR * Math.sin(angleRad)
    const x2 = CX + outerR * Math.cos(angleRad)
    const y2 = CY + outerR * Math.sin(angleRad)

    let label = null
    if (i === 0) label = '0'
    else if (i === 20) label = '50'
    else if (i === 40) label = '100'

    const labelR = 45
    const lx = CX + labelR * Math.cos(angleRad)
    const ly = CY + labelR * Math.sin(angleRad) + 2.5

    ticks.push({
      key: i, x1, y1, x2, y2, isMajor, label, lx, ly, pct: pct * 100
    })
  }
  return ticks
}

const TICKS = generateTicks()

export default function RiskGauge({ score = 0, size = 150 }) {
  const animated = useAnimatedScore(score, 600)
  const offset   = computeOffset(animated)
  const rotationDeg = 90 + GAP_DEG / 2

  return (
    <div className="risk-gauge-container">
      <svg
        viewBox="0 0 200 180"
        width={size}
        height={size * 0.9}
        style={{ overflow: 'visible' }}
        aria-label={`Fused risk score: ${score.toFixed(1)}`}
      >
        {/* Outer bezel circle */}
        <circle
          cx={CX} cy={CY} r={84}
          fill="var(--surface-raised)"
          stroke="var(--border)"
          strokeWidth="1"
        />

        {/* Chronograph tick marks */}
        <g className="chronograph-ticks" opacity="0.8">
          {TICKS.map((t) => (
            <g key={t.key}>
              <line
                x1={t.x1} y1={t.y1} x2={t.x2} y2={t.y2}
                stroke={t.pct <= animated ? 'var(--accent)' : 'var(--border-strong)'}
                strokeWidth={t.isMajor ? 1.2 : 0.7}
                strokeLinecap="round"
              />
              {t.label && (
                <text
                  x={t.lx} y={t.ly}
                  textAnchor="middle"
                  fontFamily="var(--font-mono)"
                  fontSize="6.5"
                  fontWeight="600"
                  fill="var(--text-muted)"
                >
                  {t.label}
                </text>
              )}
            </g>
          ))}
        </g>

        {/* Inactive track arc */}
        <circle
          cx={CX} cy={CY} r={R}
          fill="none"
          stroke="var(--border-strong)"
          strokeWidth={STROKE_W}
          strokeDasharray={`${CIRC - GAP_RAD} ${GAP_RAD}`}
          strokeDashoffset={0}
          strokeLinecap="round"
          transform={`rotate(${rotationDeg} ${CX} ${CY})`}
        />

        {/* Active arc with accent color */}
        <circle
          cx={CX} cy={CY} r={R}
          fill="none"
          stroke="var(--accent)"
          strokeWidth={STROKE_W}
          strokeDasharray={`${CIRC - GAP_RAD} ${GAP_RAD}`}
          strokeDashoffset={offset}
          strokeLinecap="round"
          transform={`rotate(${rotationDeg} ${CX} ${CY})`}
          style={{
            transition: 'stroke-dashoffset 0.6s cubic-bezier(0.16, 1, 0.3, 1)',
          }}
        />

        {/* Center score readout */}
        <text
          x={CX}
          y={CY + 5}
          textAnchor="middle"
          fill="var(--text-primary)"
          fontFamily="var(--font-mono)"
          fontSize="24"
          fontWeight="700"
          letterSpacing="-0.5px"
        >
          {animated.toFixed(1)}
        </text>

        {/* Dial Subtitle */}
        <text
          x={CX}
          y={CY + 22}
          textAnchor="middle"
          fill="var(--text-muted)"
          fontFamily="var(--font-body)"
          fontSize="7"
          fontWeight="600"
          letterSpacing="0.8px"
        >
          FUSED RISK SCORE
        </text>
      </svg>
    </div>
  )
}
