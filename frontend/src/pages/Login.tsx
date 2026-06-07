import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'

export default function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [showPass, setShowPass] = useState(false)
  const { login, loading, error } = useAuth()

  const handleSubmit = (e: React.FormEvent) => {
    console.log('📝 Form submitted with:', { username, password })  // A
    e.preventDefault()
    login(username, password)
  }

  const fillDemo = () => {
    setUsername('admin')
    setPassword('admin123')
  }

  return (
    <div className="min-h-screen grid grid-cols-2">

      {/* Left Panel */}
      <div className="bg-brand-600 p-12 flex flex-col justify-between">
        <div>
          <div className="flex items-center gap-3 mb-12">
            <div className="w-9 h-9 bg-white/20 rounded-xl flex items-center justify-center">
              <i className="ti ti-brain text-white text-xl" />
            </div>
            <span className="text-white font-medium text-lg">Autonomous Agent</span>
          </div>
          <h1 className="text-3xl font-medium text-white leading-snug mb-4">
            Multi-agent AI orchestration for complex tasks
          </h1>
          <p className="text-white/70 text-sm leading-relaxed">
            Submit a task — specialized agents collaborate in real-time to deliver synthesised results.
          </p>
          <div className="mt-10 flex flex-col gap-5">
            {[
              { icon: 'ti-git-branch', title: 'Dynamic task planning', sub: 'Groq LLM breaks tasks into ordered subtasks' },
              { icon: 'ti-robot',      title: '5 specialist agents',   sub: 'Research, RAG, Critic, Coding, Browser' },
              { icon: 'ti-database-search', title: 'Vector memory',   sub: 'Qdrant stores results for semantic retrieval' },
              { icon: 'ti-activity',   title: 'Real-time WebSocket',   sub: 'Watch every agent action live' },
            ].map(f => (
              <div key={f.icon} className="flex items-start gap-3">
                <div className="w-8 h-8 bg-white/10 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5">
                  <i className={`ti ${f.icon} text-white/90 text-base`} />
                </div>
                <div>
                  <div className="text-white text-sm font-medium">{f.title}</div>
                  <div className="text-white/60 text-xs mt-0.5">{f.sub}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
        <div className="text-white/40 text-xs">
          FastAPI · React · PostgreSQL · Redis · Qdrant
        </div>
      </div>

      {/* Right Panel */}
      <div className="bg-white flex items-center justify-center p-12">
        <div className="w-full max-w-sm">
          <h2 className="text-2xl font-medium text-gray-900 mb-1">Welcome back</h2>
          <p className="text-sm text-gray-500 mb-8">Sign in to your agent dashboard</p>

          {error && (
            <div className="flex items-center gap-2 bg-red-50 border border-red-200 rounded-lg px-4 py-3 mb-5 text-red-700 text-sm">
              <i className="ti ti-alert-circle text-base flex-shrink-0" />
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <div>
              <label className="text-xs font-medium text-gray-600 mb-1.5 block">Username</label>
              <div className="relative">
                <i className="ti ti-user absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-base" />
                <input
                  type="text"
                  value={username}
                  onChange={e => setUsername(e.target.value)}
                  placeholder="Enter username"
                  className="w-full h-10 pl-9 pr-3 text-sm border border-gray-200 rounded-lg bg-gray-50 focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-50 focus:bg-white"
                />
              </div>
            </div>

            <div>
              <label className="text-xs font-medium text-gray-600 mb-1.5 block">Password</label>
              <div className="relative">
                <i className="ti ti-lock absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-base" />
                <input
                  type={showPass ? 'text' : 'password'}
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  placeholder="Enter password"
                  className="w-full h-10 pl-9 pr-10 text-sm border border-gray-200 rounded-lg bg-gray-50 focus:outline-none focus:border-brand-500 focus:ring-2 focus:ring-brand-50 focus:bg-white"
                />
                <button type="button" onClick={() => setShowPass(!showPass)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600">
                  <i className={`ti ${showPass ? 'ti-eye-off' : 'ti-eye'} text-base`} />
                </button>
              </div>
            </div>

            <button type="submit" disabled={loading}
              className="w-full h-10 bg-brand-500 hover:bg-brand-600 text-white text-sm font-medium rounded-lg flex items-center justify-center gap-2 disabled:opacity-50 mt-1">
              <i className="ti ti-login text-base" />
              {loading ? 'Signing in...' : 'Sign in'}
            </button>
          </form>

          <div className="flex items-center gap-3 my-5">
            <div className="flex-1 h-px bg-gray-200" />
            <span className="text-xs text-gray-400">demo credentials</span>
            <div className="flex-1 h-px bg-gray-200" />
          </div>

          <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
            <div className="text-xs font-medium text-gray-400 uppercase tracking-wide mb-3">Try it out</div>
            <div className="flex flex-col gap-2 mb-3">
              {[['Username', 'admin'], ['Password', 'admin123']].map(([k, v]) => (
                <div key={k} className="flex items-center justify-between">
                  <span className="text-xs text-gray-500">{k}</span>
                  <span onClick={() => k === 'Username' ? setUsername(v) : setPassword(v)}
                    className="text-xs font-medium bg-white border border-gray-200 px-2 py-1 rounded cursor-pointer hover:border-brand-500 hover:text-brand-600">
                    {v}
                  </span>
                </div>
              ))}
            </div>
            <button onClick={fillDemo}
              className="w-full py-2 bg-white border border-gray-200 rounded-lg text-xs text-gray-500 hover:bg-brand-50 hover:border-brand-500 hover:text-brand-600 flex items-center justify-center gap-2">
              <i className="ti ti-bolt text-sm" />
              Fill demo credentials
            </button>
          </div>

          <p className="text-center text-xs text-gray-400 mt-6">
            Don't have an account?{' '}
            <Link to="/register" className="text-brand-600 font-medium hover:underline">Sign up</Link>
          </p>
        </div>
      </div>
    </div>
  )
}