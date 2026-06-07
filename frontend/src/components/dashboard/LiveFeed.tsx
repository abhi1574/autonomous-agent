interface Message { agent: string; text: string; time: string; color: string }
interface Props   { messages: Message[]; connected: boolean }

export default function LiveFeed({ messages, connected }: Props) {
  return (
    <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
      <div className="px-4 py-3 border-b border-gray-100 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <i className="ti ti-activity text-brand-500 text-base" />
          <span className="text-sm font-medium text-gray-900">Live feed</span>
        </div>
        <div className="flex items-center gap-1.5 text-[11px] text-gray-400">
          <div className={`w-1.5 h-1.5 rounded-full ${connected ? 'bg-green-500' : 'bg-gray-300'}`} />
          {connected ? 'live' : 'offline'}
        </div>
      </div>
      <div className="divide-y divide-gray-50 max-h-[200px] overflow-y-auto">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-8 gap-2 text-gray-400">
            <i className="ti ti-wifi text-xl" />
            <span className="text-xs">Waiting for agent activity...</span>
          </div>
        ) : messages.map((m, i) => (
          <div key={i} className="flex gap-2.5 px-4 py-2.5">
            <div className="w-1.5 h-1.5 rounded-full mt-1.5 flex-shrink-0" style={{ background: m.color }} />
            <div>
              <div className="text-xs text-gray-800 leading-relaxed">
                <span className="font-medium">{m.agent}</span> — {m.text}
              </div>
              <div className="text-[10px] text-gray-400 mt-0.5">{m.time}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}