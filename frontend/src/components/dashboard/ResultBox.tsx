interface Props { result: string | null; status: string }

export default function ResultBox({ result, status }: Props) {
  return (
    <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
      <div className="px-4 py-3 border-b border-gray-100 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <i className="ti ti-sparkles text-brand-500 text-base" />
          <span className="text-sm font-medium text-gray-900">Result</span>
        </div>
        <span className={`text-[11px] font-medium
          ${status === 'completed' ? 'text-green-600' :
            status === 'running'   ? 'text-orange-500' :
            status === 'failed'    ? 'text-red-500' : 'text-gray-400'}`}>
          {status}
        </span>
      </div>
      <div className="p-4">
        <div className="bg-gray-50 rounded-lg p-4 min-h-[90px]">
          {!result ? (
            <div className="flex flex-col items-center justify-center h-[70px] gap-2 text-gray-400">
              <i className={`ti ${status === 'running' ? 'ti-loader' : 'ti-inbox'} text-2xl`} />
              <span className="text-xs">
                {status === 'running' ? 'Agents working...' : 'Results appear here once task completes'}
              </span>
            </div>
          ) : (
            <div className="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">{result}</div>
          )}
        </div>
      </div>
    </div>
  )
}