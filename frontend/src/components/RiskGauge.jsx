// src/components/RiskGauge.jsx
// Signature jeweled chronograph instrument dial for fused_risk_score.
// Luxury timepiece aesthetic: fine bezel tick marks, metallic rings, glowing arc sweep, and Fraunces display serif.

import { useEffect, useRef, useState } from 'react'

const R        = 66          // ring radius
const CX       = 100         // SVG center (viewBox 200x180)
const CY       = 92
const CIRC     = 2 * Math.PI * R   // ~414.69
const STROKE_W = 8.5
const GAP_DEG  = 64          // open gap at the bottom
const GAP_RAD  = (GAP_DEG / 360) * CIRC   // open gap length

// Clamp score 0-100 and compute stroke-dashoffset
function computeOffset(score) {
  const usable = CIRC - GAP_RAD                       // fillable arc length
  const filled = (Math.min(Math.max(score, 0), 100) / 100) * usable
  return CIRC - filled                                // dashoffset
}

// Dynamic color interpolation matching Vault Instrument palette
function getGaugeColor(s) {
  const stops = [
    { t: 0,   r: 163, g: 190, b: 140 },  // sage / muted trust
    { t: 30,  r: 201, g: 162, b: 39  },  // #C9A227 warm gold
    { t: 65,  r: 242, g: 153, b: 74  },  // #F2994A amber
    { t: 100, r: 226, g: 73,  b: 95  },  // #E2495F ember red
  ]
  const pct = Math.min(Math.max(s, 0), 100)
  let lo = stops[0], hi = stops[stops.length - 1]
  for (let i = 0; i < stops.length - 1; i++) {
    if (pct >= stops[i].t && pct <= stops[i + 1].t) {
      lo = stops[i]; hi = stops[i + 1]; break
    }
  }
  const span = hi.t - lo.t || 1
  const f    = (pct - lo.t) / span
  const lerp = (a, b) => Math.round(a + (b - a) * f)
  return `rgb(${lerp(lo.r, hi.r)},${lerp(lo.g, hi.g)},${lerp(lo.b, hi.b)})`
}

// Count-up animation synchronized with the 800ms sweep
function useAnimatedScore(target, durationMs = 800) {
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
      const ease = 1 - Math.pow(1 - t, 3)  // cubic ease-out ~800ms
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

    // Optional tiny labels for 0, 50, 100
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
  const animated = useAnimatedScore(score, 800)
  const color    = getGaugeColor(animated)
  const offset   = computeOffset(animated)
  const isHigh   = animated >= 70

  // Rotation so the bottom gap is centered
  const rotationDeg = 90 + GAP_DEG / 2

  // Ambient glow intensity tied to risk level
  const glowOpacity = Math.min(0.2 + (animated / 100) * 0.5, 0.75)

  return (
    <div className="gauge-instrument-container" style={{ position: 'relative', width: size, height: size * 0.9 }}>

      <svg
        viewBox="0 0 200 180"
        width={size}
        height={size * 0.9}
        style={{ overflow: 'visible' }}
        aria-label={`Fused risk score: ${score.toFixed(1)}`}
      >
        <defs>
          {/* Subtle metallic bezel rim gradient */}
          <linearGradient id="bezelTrim" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#55503E" />
            <stop offset="30%" stopColor="#8A856F" />
            <stop offset="50%" stopColor="#3A3428" />
            <stop offset="70%" stopColor="#C9A227" stopOpacity="0.4" />
            <stop offset="100%" stopColor="#1E2229" />
          </linearGradient>

          {/* Inner dial face radial gradient */}
          <radialGradient id="dialFace" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#181C22" />
            <stop offset="70%" stopColor="#111419" />
            <stop offset="100%" stopColor="#0B0D10" />
          </radialGradient>

          {/* Ambient breathing glow for active arc */}
          <filter id="dial-glow" x="-30%" y="-30%" width="160%" height="160%">
            <feGaussianBlur stdDeviation="4" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>

          {/* Soft outer aura */}
          <filter id="aura-glow" x="-40%" y="-40%" width="180%" height="180%">
            <feGaussianBlur stdDeviation="8" result="aura" />
            <feMerge>
              <feMergeNode in="aura" />
            </feMerge>
          </filter>
        </defs>

        {/* Outer watch bezel ring */}
        <circle
          cx={CX} cy={CY} r={84}
          fill="url(#dialFace)"
          stroke="url(#bezelTrim)"
          strokeWidth="1.2"
          className="dial-bezel-ring"
        />

        {/* Subtle inner milled concentric track */}
        <circle
          cx={CX} cy={CY} r={78}
          fill="none"
          stroke="rgba(201, 162, 39, 0.1)"
          strokeWidth="0.8"
          strokeDasharray="2 3"
        />

        {/* Chronograph tick marks */}
        <g className="chronograph-ticks" opacity="0.65">
          {TICKS.map((t) => (
            <g key={t.key}>
              <line
                x1={t.x1} y1={t.y1} x2={t.x2} y2={t.y2}
                stroke={t.pct <= animated ? color : (t.isMajor ? '#8A8F98' : '#3A3F4A')}
                strokeWidth={t.isMajor ? 1.2 : 0.7}
                strokeLinecap="round"
                style={{ transition: 'stroke 0.4s ease' }}
              />
              {t.label && (
                <text
                  x={t.lx} y={t.ly}
                  textAnchor="middle"
                  fontFamily="'JetBrains Mono', monospace"
                  fontSize="6.5"
                  fontWeight="600"
                  fill="#8A8F98"
                >
                  {t.label}
                </text>
              )}
            </g>
          ))}
        </g>

        {/* Recessed track arc */}
        <circle
          cx={CX} cy={CY} r={R}
          fill="none"
          stroke="rgba(35, 41, 50, 0.7)"
          strokeWidth={STROKE_W}
          strokeDasharray={`${CIRC - GAP_RAD} ${GAP_RAD}`}
          strokeDashoffset={0}
          strokeLinecap="round"
          transform={`rotate(${rotationDeg} ${CX} ${CY})`}
        />

        {/* Ambient breathing glow behind arc */}
        <circle
          cx={CX} cy={CY} r={R}
          fill="none"
          stroke={color}
          strokeWidth={STROKE_W + 4}
          strokeDasharray={`${CIRC - GAP_RAD} ${GAP_RAD}`}
          strokeDashoffset={offset}
          strokeLinecap="round"
          opacity={glowOpacity}
          filter="url(#aura-glow)"
          transform={`rotate(${rotationDeg} ${CX} ${CY})`}
          className="dial-aura-pulse"
          style={{
            transition: 'stroke-dashoffset 0.8s cubic-bezier(0.16, 1, 0.3, 1), stroke 0.6s ease',
          }}
        />

        {/* Active glowing arc with 800ms sweep */}
        <circle
          cx={CX} cy={CY} r={R}
          fill="none"
          stroke={color}
          strokeWidth={STROKE_W}
          strokeDasharray={`${CIRC - GAP_RAD} ${GAP_RAD}`}
          strokeDashoffset={offset}
          strokeLinecap="round"
          filter="url(#dial-glow)"
          transform={`rotate(${rotationDeg} ${CX} ${CY})`}
          className={isHigh ? 'dial-arc-live-breathing' : 'dial-arc-normal'}
          style={{
            transition: 'stroke-dashoffset 0.8s cubic-bezier(0.16, 1, 0.3, 1), stroke 0.6s ease',
          }}
        />

        {/* Center luxury display serif hero number */}
        <text
          x={CX} y={CY - 3}
          textAnchor="middle"
          dominantBaseline="middle"
          fontFamily="var(--font-display-serif, 'Fraunces', serif)"
          fontSize="30"
          fontWeight="700"
          fontStyle="normal"
          fill={color}
          className="dial-score-num"
          style={{ transition: 'fill 0.6s ease' }}
        >
          {animated.toFixed(1)}
        </text>

        {/* Subtitle luxury label */}
        <text
          x={CX} y={CY + 20}
          textAnchor="middle"
          fontFamily="var(--font-body, 'Plus Jakarta Sans', sans-serif)"
          fontSize="7.5"
          fontWeight="700"
          letterSpacing="1.4"
          fill="#8A8F98"
          className="dial-sub-label"
        >
          FUSED RISK INDEX
        </text>

        {/* Bottom jewel indicator */}
        <circle
          cx={CX} cy={CY + 68} r={2}
          fill={color}
          opacity="0.8"
          style={{ transition: 'fill 0.6s ease' }}
        />
      </svg>
    </div>
  )
}

