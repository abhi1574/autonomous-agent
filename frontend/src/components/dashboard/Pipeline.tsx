interface Step {
  title : string
  agent : string
  status: 'done' | 'running' | 'waiting' | 'idle'
}

interface Props {
  steps   : Step[]
  progress: number
}

const agentIcons: Record<string, string> = {
  research: 'ti-world-search',
  rag     : 'ti-database-search',
  critic  : 'ti-message-star',
  coding  : 'ti-code',
  browser : 'ti-browser',
}

const agentBg: Record<string, string> = {
  research: 'bg-blue-50',
  rag     : 'bg-green-50',
  critic  : 'bg-brand-50',
  coding  : 'bg-orange-50',
  browser : 'bg-red-50',
}

export default function Pipeline({ steps, progress }: Props) {
  if (!steps.length) {
    return (
      <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
        <div className="px-4 py-3 border-b border-gray-100 flex items-center gap-2">
          <i className="ti ti-git-branch text-brand-500 text-base" />
          <span className="text-sm font-medium text-gray-900">Task pipeline</span>
        </div>
        <div className="flex items-center justify-center gap-2 py-8 text-gray-400 text-sm">
          <i className="ti ti-arrow-right text-base" />
          Submit a task to see the pipeline
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
      <div className="px-4 py-3 border-b border-gray-100 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <i className="ti ti-git-branch text-brand-500 text-base" />
          <span className="text-sm font-medium text-gray-900">Task pipeline</span>
        </div>
        <span className={`text-[11px] font-medium px-2.5 py-1 rounded-full
          ${progress === 100 ? 'bg-green-50 text-green-700' : 'bg-orange-50 text-orange-700'}`}>
          {steps.filter(s => s.status === 'done').length}/{steps.length}
        </span>
      </div>
      <div className="p-4">
        <div className="flex rounded-lg overflow-hidden border border-gray-200 mb-3">
          {steps.map((s, i) => (
            <div key={i} className={`flex-1 py-2.5 px-1 text-center border-r border-gray-200 last:border-r-0
              ${s.status === 'done'    ? 'bg-green-50' :
                s.status === 'running' ? 'bg-orange-50' : 'bg-gray-50 opacity-60'}`}>
              <div className={`w-6 h-6 rounded-full mx-auto mb-1.5 flex items-center justify-center ${agentBg[s.agent] || 'bg-gray-100'}`}>
                <i className={`ti ${agentIcons[s.agent] || 'ti-robot'} text-xs
                  ${s.status === 'done' ? 'text-green-600' : s.status === 'running' ? 'text-orange-600' : 'text-gray-400'}`} />
              </div>
              <div className="text-[10px] font-medium text-gray-700 truncate px-0.5">{s.title}</div>
              <div className="text-[10px] text-gray-400">{s.agent}</div>
            </div>
          ))}
        </div>
        <div className="flex justify-between text-[11px] text-gray-400 mb-1.5">
          <span>{steps.filter(s => s.status === 'done').length} / {steps.length} subtasks</span>
          <span className="text-brand-600 font-medium">{progress}%</span>
        </div>
        <div className="h-1 bg-gray-100 rounded-full overflow-hidden">
          <div className="h-full bg-brand-500 rounded-full transition-all duration-500"
            style={{ width: `${progress}%` }} />
        </div>
      </div>
    </div>
  )
}