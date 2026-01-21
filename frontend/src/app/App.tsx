import PageLayout from '../shared/layout/PageLayout';
import QueryPanel from '../features/query/QueryPanel';
import AgentTimeline from '../features/agents/AgentTimeline';
import ToolInvocationPanel from '../features/tools/ToolInvocationPanel';
import SafetyPanel from '../features/safety/SafetyPanel';
import LogsPanel from '../features/logs/LogsPanel';

function App() {
  return (
    <PageLayout>
      <div className="grid grid-cols-1 xl:grid-cols-12 gap-8">

        {/* Left Column: Input and Logs */}
        <div className="xl:col-span-4 space-y-6">
          <QueryPanel />
          <LogsPanel />
        </div>

        {/* Right Column: Agent Execution Flow */}
        <div className="xl:col-span-8 space-y-6">
          <SafetyPanel />
          <AgentTimeline />
          <ToolInvocationPanel />
        </div>

      </div>
    </PageLayout>
  )
}

export default App;
