import { useSelector } from 'react-redux';
import { Bot, Brain, CheckCircle2 } from 'lucide-react';
import type { RootState } from '../../app/store';

export default function AgentTimeline() {
    const { data, status } = useSelector((state: RootState) => state.query);

    if (status !== 'succeeded' || !data) {
        if (status === 'loading') {
            return (
                <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 h-64 flex items-center justify-center">
                    <div className="text-center">
                        <div className="animate-pulse bg-slate-200 h-10 w-10 rounded-full mx-auto mb-3"></div>
                        <p className="text-slate-400 text-sm">Waiting for agents...</p>
                    </div>
                </div>
            );
        }
        return null;
    }

    const agents = data.agents_used || [];
    const reasoning = data.agent_reasoning || {};

    return (
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
            <div className="p-4 border-b border-slate-100 bg-slate-50 flex justify-between items-center">
                <h2 className="font-semibold text-slate-800 flex items-center gap-2">
                    <Brain size={18} className="text-purple-600" />
                    Agent Reasoning Flow
                </h2>
                <span className="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded-full border border-purple-200">
                    {agents.length} Steps
                </span>
            </div>

            <div className="p-6 relative">
                <div className="absolute left-9 top-6 bottom-6 w-0.5 bg-slate-200"></div>

                <div className="space-y-8 relative">
                    {agents.map((agent, index) => {
                        const agentData = reasoning[agent];
                        let colorClass = "bg-blue-600";
                        let icon = <Bot size={16} className="text-white" />;

                        if (agent === "Store Knowledge Agent") colorClass = "bg-indigo-600";
                        if (agent === "Operations Agent") colorClass = "bg-orange-600";
                        if (agent === "Safety Agent") {
                            colorClass = "bg-green-600";
                            icon = <CheckCircle2 size={16} className="text-white" />;
                        }

                        return (
                            <div key={index} className="flex gap-4 group">
                                <div className={`relative z-10 w-10 h-10 rounded-full ${colorClass} flex items-center justify-center shadow-md ring-4 ring-white`}>
                                    {icon}
                                </div>

                                <div className="flex-1 bg-white border border-slate-200 rounded-lg p-4 shadow-sm group-hover:border-blue-200 group-hover:shadow-md transition-all">
                                    <div className="flex justify-between items-start mb-2">
                                        <h3 className="font-semibold text-slate-900">{agent}</h3>
                                        <span className="text-xs text-slate-400 font-mono">STEP {index + 1}</span>
                                    </div>

                                    {agentData && agentData.messages && agentData.messages.length > 0 ? (
                                        <div className="space-y-2">
                                            {agentData.messages.map((msg, i) => (
                                                <p key={i} className="text-sm text-slate-600 leading-relaxed pl-3 border-l-2 border-slate-100">
                                                    {msg}
                                                </p>
                                            ))}
                                        </div>
                                    ) : (
                                        <p className="text-sm text-slate-400 italic">Task completed successfully.</p>
                                    )}
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    );
}
