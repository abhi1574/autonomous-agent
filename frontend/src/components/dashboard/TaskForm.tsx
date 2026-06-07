import { useState } from 'react'

interface Props {
  onSubmit: (title: string, desc: string) => void
  loading : boolean
}

const hints = [
  { label: 'Research',  title: 'Research latest AI agent frameworks', desc: 'Find top AI frameworks in 2025, summarise key features and critique them' },
  { label: 'Write code', title: 'Write a binary search algorithm',   desc: 'Write clean Python binary search with type hints and example usage' },
  { label: 'Browse URL', title: 'Extract content from a URL',        desc: 'Navigate to https://docs.anthropic.com and summarise the main sections' },
]

export default function TaskForm({ onSubmit, loading }: Props) {
  const [title, setTitle] = useState('')
  const [desc,  setDesc ] = useState('')

  const handleSubmit = () => {
    if (!title.trim()) return
    onSubmit(title, desc)
    setTitle('')
    setDesc('')
  }

  return (
    <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
      <div className="px-4 py-3 border-b border-gray-100 flex items-center gap-2">
        <i className="ti ti-plus text-brand-500 text-base" />
        <span className="text-sm font-medium text-gray-900">New task</span>
      </div>
      <div className="p-4">
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-3">
          <input
            value={title}
            onChange={e => setTitle(e.target.value)}
            placeholder="Task title..."
            className="w-full h-9 px-3 text-sm border border-gray-200 rounded-lg bg-white focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-50 mb-2"
          />
          <textarea
            value={desc}
            onChange={e => setDesc(e.target.value)}
            placeholder="Describe what needs to be done in detail..."
            rows={3}
            className="w-full px-3 py-2 text-sm border border-gray-200 rounded-lg bg-white focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-50 resize-none mb-2"
          />
          <div className="flex items-center justify-between">
            <div className="flex gap-1.5 flex-wrap">
              {hints.map(h => (
                <button key={h.label}
                  onClick={() => { setTitle(h.title); setDesc(h.desc) }}
                  className="px-2.5 py-1 rounded-full border border-gray-200 bg-white text-[11px] text-gray-500 hover:bg-brand-50 hover:border-brand-300 hover:text-brand-600 transition-colors">
                  {h.label}
                </button>
              ))}
            </div>
            <button onClick={handleSubmit} disabled={loading || !title.trim()}
              className="flex items-center gap-1.5 px-4 py-1.5 bg-brand-500 hover:bg-brand-600 text-white text-xs font-medium rounded-lg disabled:opacity-50 transition-colors">
              <i className="ti ti-player-play text-xs" />
              {loading ? 'Running...' : 'Run'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}