const agents = [
  { id: 'research', label: 'research', icon: 'ti-world-search',    bg: 'bg-blue-50',   color: 'text-blue-600'   },
  { id: 'rag',      label: 'rag',      icon: 'ti-database-search', bg: 'bg-green-50',  color: 'text-green-600'  },
  { id: 'critic',   label: 'critic',   icon: 'ti-message-star',    bg: 'bg-brand-50',  color: 'text-brand-600'  },
  { id: 'coding',   label: 'coding',   icon: 'ti-code',            bg: 'bg-orange-50', color: 'text-orange-600' },
  { id: 'browser',  label: 'browser',  icon: 'ti-browser',         bg: 'bg-red-50',    color: 'text-red-600'    },
]

interface Props { busyAgents?: string[] }

export default function AgentGrid({ busyAgents = [] }: Props) {
  return (
    <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
      <div className="px-4 py-3 border-b border-gray-100 flex items-center gap-2">
        <i className="ti ti-robot text-brand-500 text-base" />
        <span className="text-sm font-medium text-gray-900">Agents</span>
      </div>
      <div className="p-4">
        <div className="grid grid-cols-5 gap-2">
          {agents.map(a => {
            const isBusy = busyAgents.includes(a.id)
            return (
              <div key={a.id} className="border border-gray-200 rounded-lg p-2.5 text-center bg-gray-50">
                <div className={`w-8 h-8 ${a.bg} rounded-full mx-auto mb-1.5 flex items-center justify-center`}>
                  <i className={`ti ${a.icon} text-base ${a.color}`} />
                </div>
                <div className="text-[11px] font-medium text-gray-700">{a.label}</div>
                <div className={`text-[10px] mt-1 font-medium ${isBusy ? 'text-orange-500' : 'text-green-500'}`}>
                  {isBusy ? 'busy' : 'idle'}
                </div>
              </div>
            )
          })}
        </div>
        <div className="flex items-center gap-3 mt-3 pt-3 border-t border-gray-100">
          <div className="flex items-center gap-1.5 text-[11px] text-gray-500"><div className="w-1.5 h-1.5 rounded-full bg-green-500" />idle</div>
          <div className="flex items-center gap-1.5 text-[11px] text-gray-500"><div className="w-1.5 h-1.5 rounded-full bg-orange-400" />busy</div>
          <div className="flex items-center gap-1.5 text-[11px] text-gray-500"><div className="w-1.5 h-1.5 rounded-full bg-gray-300" />waiting</div>
        </div>
      </div>
    </div>
  )
}