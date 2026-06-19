import { useState } from 'react'
import ReactMarkdown from 'react-markdown'

interface Props { result: string | null; status: string; taskTitle?: string }

export default function ResultBox({ result, status, taskTitle }: Props) {
  const [copied, setCopied] = useState(false)

  const copyResult = () => {
    if (result) {
      navigator.clipboard.writeText(result)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  const downloadResult = () => {
    if (!result) return
    const blob = new Blob([result], { type: 'text/plain' })
    const url  = URL.createObjectURL(blob)
    const a    = document.createElement('a')
    a.href     = url
    a.download = `${taskTitle || 'agent-result'}.txt`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
      <div className="px-4 py-3 border-b border-gray-100 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <i className="ti ti-sparkles text-brand-500 text-base" />
          <span className="text-sm font-medium text-gray-900">Result</span>
          {taskTitle && (
            <span className="text-xs text-gray-400 truncate max-w-[300px]">— {taskTitle}</span>
          )}
        </div>
        <div className="flex items-center gap-2">
          {result && (
            <>
              <button onClick={copyResult}
                className="flex items-center gap-1.5 px-2.5 py-1 text-xs text-gray-500 border border-gray-200 rounded-lg hover:bg-gray-50">
                <i className={`ti ${copied ? 'ti-check' : 'ti-copy'} text-xs`} />
                {copied ? 'Copied!' : 'Copy'}
              </button>
              <button onClick={downloadResult}
                className="flex items-center gap-1.5 px-2.5 py-1 text-xs text-gray-500 border border-gray-200 rounded-lg hover:bg-gray-50">
                <i className="ti ti-download text-xs" />
                Download
              </button>
            </>
          )}
          <span className={`text-[11px] font-medium px-2.5 py-1 rounded-full
            ${status === 'completed' ? 'bg-green-50 text-green-600' :
              status === 'running'   ? 'bg-orange-50 text-orange-500' :
              status === 'failed'    ? 'bg-red-50 text-red-500' :
                                       'text-gray-400'}`}>
            {status}
          </span>
        </div>
      </div>

      <div className="p-4">
        {!result ? (
          <div className="bg-gray-50 rounded-lg p-6 min-h-[100px] flex flex-col items-center justify-center gap-2 text-gray-400">
            <i className={`ti ${status === 'running' ? 'ti-loader animate-spin' : 'ti-inbox'} text-2xl`} />
            <span className="text-xs text-center">
              {status === 'running'
                ? 'Agents are working — result appears when all subtasks complete...'
                : 'Submit a task to see results here'}
            </span>
          </div>
        ) : (
          <div className="flex flex-col gap-3">
            {/* Metadata chips */}
            <div className="flex items-center gap-2 flex-wrap">
              <span className="flex items-center gap-1.5 text-[11px] font-medium px-2.5 py-1 rounded-full bg-green-50 text-green-700">
                <i className="ti ti-circle-check text-xs" />Completed
              </span>
              <span className="flex items-center gap-1.5 text-[11px] font-medium px-2.5 py-1 rounded-full bg-brand-50 text-brand-600">
                <i className="ti ti-robot text-xs" />Multi-agent synthesis
              </span>
              <span className="flex items-center gap-1.5 text-[11px] font-medium px-2.5 py-1 rounded-full bg-blue-50 text-blue-600">
                <i className="ti ti-file-text text-xs" />
                {result.split(' ').length} words
              </span>
            </div>

            {/* Markdown rendered result */}
            <div className="bg-gray-50 rounded-lg p-5 prose prose-sm max-w-none
              prose-headings:text-gray-900 prose-headings:font-medium
              prose-h2:text-base prose-h2:border-b prose-h2:border-gray-200 prose-h2:pb-1 prose-h2:mb-3
              prose-h3:text-sm
              prose-p:text-gray-700 prose-p:leading-relaxed prose-p:text-sm
              prose-li:text-gray-700 prose-li:text-sm
              prose-strong:text-gray-900 prose-strong:font-medium
              prose-a:text-brand-600 prose-a:no-underline hover:prose-a:underline">
              <ReactMarkdown>{result}</ReactMarkdown>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}