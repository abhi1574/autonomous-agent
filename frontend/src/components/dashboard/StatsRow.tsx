interface Stat {
  icon : string
  bg   : string
  color: string
  val  : string | number
  label: string
  trend: string
  trendColor: string
}

interface Props { stats: Stat[] }

export default function StatsRow({ stats }: Props) {
  return (
    <div className="grid grid-cols-4 gap-2.5">
      {stats.map((s, i) => (
        <div key={i} className="bg-white border border-gray-200 rounded-xl p-4">
          <div className="flex items-center justify-between mb-3">
            <div className={`w-8 h-8 ${s.bg} rounded-lg flex items-center justify-center`}>
              <i className={`ti ${s.icon} text-base ${s.color}`} />
            </div>
            <span className={`text-[10px] font-medium ${s.trendColor}`}>{s.trend}</span>
          </div>
          <div className="text-2xl font-medium text-gray-900">{s.val}</div>
          <div className="text-xs text-gray-500 mt-1">{s.label}</div>
        </div>
      ))}
    </div>
  )
}