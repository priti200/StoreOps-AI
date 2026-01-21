import { useSelector } from 'react-redux';
import { Wrench } from 'lucide-react';
import type { RootState } from '../../app/store';

export default function ToolInvocationPanel() {
    const { data } = useSelector((state: RootState) => state.query);

    if (!data || !data.tools_called || data.tools_called.length === 0) return null;

    return (
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
            <div className="p-4 border-b border-slate-100 bg-slate-50 flex items-center justify-between">
                <h2 className="font-semibold text-slate-800 flex items-center gap-2">
                    <Wrench size={18} className="text-orange-600" />
                    Tool Invocations
                </h2>
                <span className="text-xs bg-orange-100 text-orange-700 px-2 py-1 rounded-full border border-orange-200">
                    {data.tools_called.length} Calls
                </span>
            </div>

            <div className="divide-y divide-slate-100">
                {data.tools_called.map((tool, index) => {
                    // Handle both string (simple name) and object (detailed) formats
                    const toolName = typeof tool === 'string' ? tool : tool.tool;
                    const toolInput = typeof tool === 'string' ? 'Input details unavailable in current mode' : tool.input;
                    const toolOutput = typeof tool === 'string' ? 'Output details unavailable in current mode' : tool.output;

                    return (
                        <div key={index} className="p-6 hover:bg-slate-50 transition-colors">
                            <div className="flex items-center gap-2 mb-3">
                                <span className="text-sm font-medium px-2 py-0.5 rounded bg-slate-100 text-slate-600 border border-slate-200">
                                    {toolName}
                                </span>
                                <span className="text-xs text-slate-400">invoked by Operations Agent</span>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div className="bg-slate-50 rounded-lg p-3 border border-slate-200">
                                    <h4 className="text-xs font-semibold text-slate-500 uppercase mb-2">Input</h4>
                                    <pre className="text-xs text-slate-700 font-mono whitespace-pre-wrap overflow-x-auto">
                                        {toolInput}
                                    </pre>
                                </div>

                                <div className="bg-blue-50 rounded-lg p-3 border border-blue-100">
                                    <h4 className="text-xs font-semibold text-blue-500 uppercase mb-2">Output</h4>
                                    <pre className="text-xs text-blue-900 font-mono whitespace-pre-wrap overflow-x-auto">
                                        {toolOutput}
                                    </pre>
                                </div>
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
