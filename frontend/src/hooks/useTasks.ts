import { useState, useCallback } from 'react'
import { tasksApi } from '../api/client'

export interface Task {
  id         : string
  title      : string
  description: string | null
  status     : 'pending' | 'running' | 'completed' | 'failed'
  result     : string | null
  created_at : string
  updated_at : string
}

export interface ToolLog {
  id         : string
  tool_name  : string
  agent_name : string
  task_id    : string | null
  status     : string
  duration_ms: number | null
  created_at : string
}

export function useTasks() {
  const [tasks,    setTasks   ] = useState<Task[]>([])
  const [toolLogs, setToolLogs] = useState<ToolLog[]>([])
  const [loading,  setLoading ] = useState(false)
  const [error,    setError   ] = useState<string | null>(null)

  const fetchTasks = useCallback(async () => {
    try {
      const res = await tasksApi.list()
      setTasks(res.data)
    } catch {}
  }, [])

  const fetchToolLogs = useCallback(async () => {
    try {
      const res = await tasksApi.toolLogs()
      setToolLogs(res.data)
    } catch {}
  }, [])

  const createTask = async (title: string, description: string) => {
    setLoading(true)
    setError(null)
    try {
      const res = await tasksApi.create(title, description)
      setTasks(prev => [res.data, ...prev])
      return res.data
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create task')
    } finally {
      setLoading(false)
    }
  }

  return { tasks, toolLogs, loading, error, fetchTasks, fetchToolLogs, createTask }
}