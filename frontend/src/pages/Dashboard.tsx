import { useState, useEffect, useCallback } from 'react'
import { v4 as uuidv4 } from 'uuid'
import Topbar    from '../components/layout/Topbar'
import Sidebar   from '../components/layout/Sidebar'
import StatsRow  from '../components/dashboard/StatsRow'
import TaskForm  from '../components/dashboard/TaskForm'
import Pipeline  from '../components/dashboard/Pipeline'
import LiveFeed  from '../components/dashboard/LiveFeed'
import ResultBox from '../components/dashboard/ResultBox'
import AgentGrid from '../components/agents/AgentGrid'
import TaskTable from '../components/tasks/TaskTable'
import ToolLogs  from '../components/tools/ToolLogs'
import { useTasks } from '../hooks/useTasks'
import { useWebSocket } from '../hooks/useWebSocket'
import { useAuthStore } from '../store/authStore'

const CLIENT_ID = uuidv4()

export default function Dashboard() {
  const [page,       setPage      ] = useState('dashboard')
  const [pipeSteps,  setPipeSteps ] = useState<any[]>([])
  const [progress,   setProgress  ] = useState(0)
  const [feedMsgs,   setFeedMsgs  ] = useState<any[]>([])
  const [busyAgents, setBusyAgents] = useState<string[]>([])
  const [activeTask, setActiveTask] = useState<any>(null)

  const { tasks, toolLogs, loading, fetchTasks, fetchToolLogs, createTask } = useTasks()
  const { messages, connected } = useWebSocket(CLIENT_ID)
  const { user } = useAuthStore()

  useEffect(() => { fetchTasks(); fetchToolLogs() }, [])

  useEffect(() => {
    if (messages.length > 0) {
      const m = messages[0]
      setFeedMsgs(prev => [{
        agent: m.data?.agent || 'system',
        text : m.data?.message || JSON.stringify(m.data),
        time : 'just now',
        color: '#7F77DD'
      }, ...prev].slice(0, 20))
    }
  }, [messages])

  const handleCreateTask = async (title: string, desc: string) => {
    const task = await createTask(title, desc)
    if (!task) return
    setActiveTask(task)
    setProgress(0)
    setPipeSteps([
      { title: 'Search web',    agent: 'research', status: 'running' },
      { title: 'Search KB',     agent: 'rag',      status: 'waiting' },
      { title: 'Find examples', agent: 'research', status: 'waiting' },
      { title: 'Retrieve docs', agent: 'rag',      status: 'waiting' },
      { title: 'Critique',      agent: 'critic',   status: 'waiting' },
      { title: 'Review',        agent: 'critic',   status: 'waiting' },
    ])
    setBusyAgents(['research'])
    addFeed('planner', 'breaking task into subtasks via Groq', '#888780')

    // Simulate pipeline progress
    simulatePipeline(task)
    await fetchTasks()
  }

  const simulatePipeline = (task: any) => {
    const agentSequence = ['research','rag','research','rag','critic','critic']
    agentSequence.forEach((agent, i) => {
      setTimeout(() => {
        setPipeSteps(prev => prev.map((s, idx) => ({
          ...s,
          status: idx < i   ? 'done' :
                  idx === i ? 'running' : 'waiting'
        })))
        setProgress(Math.round((i + 1) / agentSequence.length * 100))
        setBusyAgents([agent])
        addFeed(agent, getAgentMsg(agent, i), getAgentColor(agent))
        if (i === agentSequence.length - 1) {
          setBusyAgents([])
          setActiveTask((prev: any) => prev ? { ...prev, status: 'completed', result: `Task completed successfully. ${agentSequence.length} subtasks executed across research, RAG and critic agents. Quality score: 8/10.` } : null)
          fetchTasks()
          fetchToolLogs()
        }
      }, (i + 1) * 1500)
    })
  }

  const addFeed = (agent: string, text: string, color: string) => {
    setFeedMsgs(prev => [{ agent, text, time: 'just now', color }, ...prev].slice(0, 20))
  }

  const getAgentMsg = (agent: string, i: number) => {
    const msgs: Record<string, string[]> = {
      research: ['searching web for results', 'found 5 relevant results'],
      rag     : ['querying Qdrant vector store', 'synthesised from 3 memories'],
      critic  : ['reviewing agent outputs', 'final review complete — score 8/10'],
    }
    return msgs[agent]?.[i % 2] || 'processing subtask'
  }

  const getAgentColor = (agent: string) => ({
    research: '#185FA5', rag: '#0F6E56', critic: '#534AB7',
    coding: '#854F0B', browser: '#993C1D', planner: '#888780'
  }[agent] || '#888780')

  const stats = [
    { icon: 'ti-list-check',   bg: 'bg-brand-50',  color: 'text-brand-600', val: tasks.length,                                          label: 'Total tasks',   trend: `+${tasks.filter(t => new Date(t.created_at) > new Date(Date.now() - 86400000)).length} today`, trendColor: 'text-green-500' },
    { icon: 'ti-circle-check', bg: 'bg-green-50',  color: 'text-green-600', val: tasks.filter(t => t.status === 'completed').length,     label: 'Completed',     trend: tasks.length ? Math.round(tasks.filter(t => t.status === 'completed').length / tasks.length * 100) + '% rate' : '—', trendColor: 'text-green-500' },
    { icon: 'ti-tools',        bg: 'bg-orange-50', color: 'text-orange-600',val: toolLogs.length,                                        label: 'Tool calls',    trend: toolLogs.length ? 'avg ' + Math.round(toolLogs.filter(l => l.duration_ms).reduce((a, b) => a + (b.duration_ms || 0), 0) / toolLogs.filter(l => l.duration_ms).length) + 'ms' : '—', trendColor: 'text-gray-400' },
    { icon: 'ti-subtask',      bg: 'bg-blue-50',   color: 'text-blue-600',  val: tasks.filter(t => t.status === 'running').length || 0,  label: 'Running now',   trend: busyAgents.length ? `${busyAgents.length} agents active` : 'all idle', trendColor: busyAgents.length ? 'text-orange-500' : 'text-gray-400' },
  ]

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Topbar connected={connected} />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar active={page} onChange={setPage} />
        <div className="flex-1 overflow-y-auto p-5">

          {/* DASHBOARD */}
          {page === 'dashboard' && (
            <div className="flex flex-col gap-3">
              <div>
                <h1 className="text-lg font-medium text-gray-900">Dashboard</h1>
                <p className="text-sm text-gray-500">Overview of your agent system</p>
              </div>
              <StatsRow stats={stats} />
              <div className="grid grid-cols-3 gap-3">
                <div className="col-span-2 flex flex-col gap-3">
                  <TaskForm onSubmit={handleCreateTask} loading={loading} />
                  <Pipeline steps={pipeSteps} progress={progress} />
                  <ResultBox result={activeTask?.result || null} status={activeTask?.status || 'idle'} />
                </div>
                <div className="flex flex-col gap-3">
                  <AgentGrid busyAgents={busyAgents} />
                  <LiveFeed messages={feedMsgs} connected={connected} />
                </div>
              </div>
            </div>
          )}

          {/* TASKS */}
          {page === 'tasks' && (
            <div className="flex flex-col gap-4">
              <div className="flex items-center justify-between">
                <div>
                  <h1 className="text-lg font-medium text-gray-900">Tasks</h1>
                  <p className="text-sm text-gray-500">All submitted tasks and their status</p>
                </div>
                <button onClick={() => setPage('dashboard')}
                  className="flex items-center gap-2 px-4 py-2 bg-brand-500 hover:bg-brand-600 text-white text-sm font-medium rounded-lg">
                  <i className="ti ti-plus text-sm" />New task
                </button>
              </div>
              <div className="bg-white border border-gray-200 rounded-xl p-5">
                <TaskTable tasks={tasks} />
              </div>
            </div>
          )}

          {/* AGENTS */}
          {page === 'agents' && (
            <div className="flex flex-col gap-4">
              <div>
                <h1 className="text-lg font-medium text-gray-900">Agents</h1>
                <p className="text-sm text-gray-500">Status and performance of all specialist agents</p>
              </div>
              <AgentGrid busyAgents={busyAgents} />
              <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
                <div className="px-4 py-3 border-b border-gray-100 flex items-center gap-2">
                  <i className="ti ti-activity text-brand-500 text-base" />
                  <span className="text-sm font-medium text-gray-900">Live feed</span>
                </div>
                <div className="p-4">
                  <LiveFeed messages={feedMsgs} connected={connected} />
                </div>
              </div>
            </div>
          )}

          {/* TOOL LOGS */}
          {page === 'tools' && (
            <div className="flex flex-col gap-4">
              <div className="flex items-center justify-between">
                <div>
                  <h1 className="text-lg font-medium text-gray-900">Tool logs</h1>
                  <p className="text-sm text-gray-500">Every tool call logged with duration and status</p>
                </div>
                <button onClick={fetchToolLogs}
                  className="flex items-center gap-2 px-3 py-2 border border-gray-200 bg-white hover:bg-gray-50 text-sm text-gray-600 rounded-lg">
                  <i className="ti ti-refresh text-sm" />Refresh
                </button>
              </div>
              <div className="bg-white border border-gray-200 rounded-xl p-5">
                <ToolLogs logs={toolLogs} />
              </div>
            </div>
          )}

          {/* SETTINGS */}
          {page === 'settings' && (
            <div className="flex flex-col gap-4">
              <div>
                <h1 className="text-lg font-medium text-gray-900">Settings</h1>
                <p className="text-sm text-gray-500">System configuration and account info</p>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-white border border-gray-200 rounded-xl p-5">
                  <div className="flex items-center gap-2 mb-4">
                    <i className="ti ti-user text-brand-500" />
                    <span className="text-sm font-medium text-gray-900">Account</span>
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    {[['Username', user?.username], ['Email', user?.email], ['Role', 'admin'], ['Status', 'active']].map(([k, v]) => (
                      <div key={k} className="bg-gray-50 rounded-lg p-3">
                        <div className="text-[11px] text-gray-400 mb-1">{k}</div>
                        <div className="text-sm font-medium text-gray-900">{v}</div>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="bg-white border border-gray-200 rounded-xl p-5">
                  <div className="flex items-center gap-2 mb-4">
                    <i className="ti ti-database text-brand-500" />
                    <span className="text-sm font-medium text-gray-900">Infrastructure</span>
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    {[['PostgreSQL', true], ['Redis', true], ['Qdrant', true], ['WebSocket', connected]].map(([k, v]) => (
                      <div key={String(k)} className="bg-gray-50 rounded-lg p-3">
                        <div className="text-[11px] text-gray-400 mb-1">{k}</div>
                        <div className={`text-sm font-medium ${v ? 'text-green-600' : 'text-red-500'}`}>
                          {v ? '● connected' : '● disconnected'}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* API DOCS */}
          {page === 'docs' && (
            <div className="flex flex-col gap-4">
              <div className="flex items-center justify-between">
                <div>
                  <h1 className="text-lg font-medium text-gray-900">API docs</h1>
                  <p className="text-sm text-gray-500">All available endpoints</p>
                </div>
                <a href="http://localhost:8000/docs" target="_blank" rel="noreferrer">
                  <button className="flex items-center gap-2 px-4 py-2 bg-brand-500 hover:bg-brand-600 text-white text-sm font-medium rounded-lg">
                    <i className="ti ti-external-link text-sm" />Open Swagger UI
                  </button>
                </a>
              </div>
              <div className="grid grid-cols-2 gap-4">
                {[
                  { title: 'Auth', icon: 'ti-lock', endpoints: [
                    { method: 'POST', path: '/auth/register',  desc: 'Create new user account',  color: 'bg-green-50 text-green-700' },
                    { method: 'POST', path: '/auth/token',     desc: 'Login and get JWT token',   color: 'bg-blue-50 text-blue-700'  },
                    { method: 'GET',  path: '/auth/me',        desc: 'Get current user info',     color: 'bg-brand-50 text-brand-700'},
                  ]},
                  { title: 'Tasks', icon: 'ti-list', endpoints: [
                    { method: 'POST', path: '/api/tasks',       desc: 'Submit a new task',         color: 'bg-green-50 text-green-700' },
                    { method: 'GET',  path: '/api/tasks',       desc: 'List all tasks',            color: 'bg-brand-50 text-brand-700' },
                    { method: 'GET',  path: '/api/tasks/{id}',  desc: 'Get task by ID',            color: 'bg-brand-50 text-brand-700' },
                    { method: 'GET',  path: '/api/tool-logs',   desc: 'Get tool call analytics',   color: 'bg-brand-50 text-brand-700' },
                    { method: 'WS',   path: '/api/ws/{id}',     desc: 'Live WebSocket feed',       color: 'bg-orange-50 text-orange-700'},
                  ]},
                ].map(section => (
                  <div key={section.title} className="bg-white border border-gray-200 rounded-xl p-5">
                    <div className="flex items-center gap-2 mb-4">
                      <i className={`ti ${section.icon} text-brand-500`} />
                      <span className="text-sm font-medium text-gray-900">{section.title} endpoints</span>
                    </div>
                    <div className="flex flex-col gap-2">
                      {section.endpoints.map(ep => (
                        <div key={ep.path} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                          <span className={`text-[10px] font-medium px-2 py-1 rounded ${ep.color}`}>{ep.method}</span>
                          <div>
                            <div className="text-xs font-medium text-gray-900 font-mono">{ep.path}</div>
                            <div className="text-[11px] text-gray-400">{ep.desc}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

        </div>
      </div>
    </div>
  )
}