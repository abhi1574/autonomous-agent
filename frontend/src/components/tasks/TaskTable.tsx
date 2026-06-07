import type { Task } from '../../hooks/useTasks'

interface Props { tasks: Task[] }

const statusStyles: Record<string, string> = {
  pending  : 'bg-gray-100 text-gray-600',
  running  : 'bg-orange-50 text-orange-700',
  completed: 'bg-green-50 text-green-700',
  failed   : 'bg-red-50 text-red-700',
}

export default function TaskTable({ tasks }: Props) {
  if (!tasks.length) {
    return (
      <div className="flex flex-col items-center justify-center py-16 gap-3 text-gray-400">
        <i className="ti ti-list text-3xl" />
        <p className="text-sm">No tasks yet — submit one from the dashboard</p>
      </div>
    )
  }

  return (
    <table className="w-full border-collapse">
      <thead>
        <tr>
          {['Task', 'Status', 'Created'].map(h => (
            <th key={h} className="text-left text-[11px] font-medium text-gray-400 uppercase tracking-wide pb-3 border-b border-gray-100">{h}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {tasks.map(t => (
          <tr key={t.id} className="border-b border-gray-50 hover:bg-gray-50 transition-colors">
            <td className="py-3 pr-4">
              <div className="text-sm font-medium text-gray-900">{t.title}</div>
              {t.description && <div className="text-xs text-gray-400 mt-0.5 truncate max-w-[400px]">{t.description}</div>}
            </td>
            <td className="py-3 pr-4">
              <span className={`text-[11px] font-medium px-2.5 py-1 rounded-full ${statusStyles[t.status]}`}>
                {t.status}
              </span>
            </td>
            <td className="py-3 text-xs text-gray-400">
              {new Date(t.created_at).toLocaleString()}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}