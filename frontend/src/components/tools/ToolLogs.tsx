import type { ToolLog } from '../../hooks/useTasks'

interface Props { logs: ToolLog[] }

const toolIcons: Record<string, { icon: string; bg: string; color: string }> = {
  web_search   : { icon: 'ti-world-search',    bg: 'bg-blue-50',   color: 'text-blue-600'   },
  llm          : { icon: 'ti-message',         bg: 'bg-brand-50',  color: 'text-brand-600'  },
  vector_search: { icon: 'ti-database-search', bg: 'bg-green-50',  color: 'text-green-600'  },
  code_executor: { icon: 'ti-code',            bg: 'bg-orange-50', color: 'text-orange-600' },
  browser      : { icon: 'ti-browser',         bg: 'bg-red-50',    color: 'text-red-600'    },
  embeddings   : { icon: 'ti-atom',            bg: 'bg-gray-100',  color: 'text-gray-600'   },
}

export default function ToolLogs({ logs }: Props) {
  if (!logs.length) {
    return (
      <div className="flex flex-col items-center justify-center py-16 gap-3 text-gray-400">
        <i className="ti ti-tools text-3xl" />
        <p className="text-sm">No tool calls yet</p>
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-2">
      {logs.map(l => {
        const t = toolIcons[l.tool_name] || { icon: 'ti-tool', bg: 'bg-gray-100', color: 'text-gray-600' }
        return (
          <div key={l.id} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
            <div className={`w-7 h-7 ${t.bg} rounded-lg flex items-center justify-center flex-shrink-0`}>
              <i className={`ti ${t.icon} text-sm ${t.color}`} />
            </div>
            <div className="flex-1">
              <div className="text-xs font-medium text-gray-900">{l.tool_name}</div>
              <div className="text-[10px] text-gray-400">{l.agent_name}</div>
            </div>
            <div className="text-right">
              <div className="text-xs font-medium text-gray-700">{l.duration_ms ?? '—'}ms</div>
              <div className={`text-[10px] font-medium ${l.status === 'success' ? 'text-green-600' : 'text-red-500'}`}>
                {l.status}
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}