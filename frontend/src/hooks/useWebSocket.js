// src/hooks/useWebSocket.js
// Maintains a persistent WebSocket connection to /ws.
// Returns { flows, connected } where flows is an array of received responses.

import { useState, useEffect, useRef, useCallback } from 'react'

const WS_URL = 'ws://127.0.0.1:8000/ws'
const MAX_FLOWS = 100   // keep last 100 in feed

export function useWebSocket() {
  const [flows, setFlows]         = useState([])
  const [connected, setConnected] = useState(false)
  const wsRef = useRef(null)

  const connect = useCallback(() => {
    if (wsRef.current && wsRef.current.readyState < 2) return  // already open/connecting

    const ws = new WebSocket(WS_URL)
    wsRef.current = ws

    ws.onopen  = () => setConnected(true)
    ws.onclose = () => {
      setConnected(false)
      setTimeout(connect, 3000)   // auto-reconnect after 3s
    }
    ws.onerror = () => ws.close()
    ws.onmessage = (evt) => {
      try {
        const data = JSON.parse(evt.data)
        const entry = { ...data, _ts: new Date().toLocaleTimeString() }
        setFlows(prev => [entry, ...prev].slice(0, MAX_FLOWS))
      } catch (_) { /* ignore malformed */ }
    }
  }, [])

  useEffect(() => {
    connect()
    return () => wsRef.current?.close()
  }, [connect])

  // sendFlow lets the Trust Panel re-send with different trust signals
  const sendFlow = useCallback((payload) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(payload))
    }
  }, [])

  return { flows, connected, sendFlow }
}
