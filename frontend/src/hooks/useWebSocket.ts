import { useEffect, useRef, useState } from 'react'

interface FeedMessage {
  event: string
  data : any
}

export function useWebSocket(clientId: string) {
  const [messages,   setMessages  ] = useState<FeedMessage[]>([])
  const [connected,  setConnected ] = useState(false)
  const wsRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/api/ws/${clientId}`)
    wsRef.current = ws

    ws.onopen = () => {
      setConnected(true)
      console.log('WebSocket connected')
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        setMessages(prev => [data, ...prev].slice(0, 50))
      } catch {}
    }

    ws.onclose = () => setConnected(false)
    ws.onerror = () => setConnected(false)

    return () => ws.close()
  }, [clientId])

  const send = (data: object) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(data))
    }
  }

  return { messages, connected, send }
}