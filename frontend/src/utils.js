// src/utils.js

export function riskClass(score) {
  if (score >= 90) return 'crit'
  if (score >= 70) return 'high'
  if (score >= 30) return 'med'
  return 'low'
}

export function trustColor(band) {
  if (band === 'High')   return 'var(--gold)'
  if (band === 'Medium') return 'var(--amber)'
  return 'var(--block)'
}

export function pct(val) {
  return `${Math.round((val ?? 0) * 100)}%`
}
