// src/hooks/usePolling.js
// Generic polling hook for REST endpoints.

import { useState, useEffect, useCallback } from 'react'

export function usePolling(url, intervalMs = 4000) {
  const [data, setData]   = useState(null)
  const [error, setError] = useState(null)

  const fetch_ = useCallback(() => {
    fetch(url)
      .then(r => r.json())
      .then(d => { setData(d); setError(null) })
      .catch(e => setError(e.message))
  }, [url])

  useEffect(() => {
    fetch_()
    const id = setInterval(fetch_, intervalMs)
    return () => clearInterval(id)
  }, [fetch_, intervalMs])

  return { data, error }
}
