import { useSelector } from 'react-redux';
import { ShieldCheck, ShieldAlert, Shield } from 'lucide-react';
import type { RootState } from '../../app/store';

export default function SafetyPanel() {
    const { data } = useSelector((state: RootState) => state.query);

    if (!data) return null;

    const decision = data.safety_decision || 'UNKNOWN';
    let badgeColor = 'bg-slate-100 text-slate-700 border-slate-200';
    let icon = <Shield size={24} />;

    if (decision === 'APPROVED') {
        badgeColor = 'bg-green-100 text-green-700 border-green-200';
        icon = <ShieldCheck size={32} className="text-green-600" />;
    } else if (decision === 'REVIEW_REQUIRED') {
        badgeColor = 'bg-amber-100 text-amber-700 border-amber-200';
        icon = <ShieldAlert size={32} className="text-amber-600" />;
    }

    // Extract safety reasoning if available in logs or hardcoded reasoning map
    // For MVP, we often find it in the messages of Safety Agent
    const safetyReasoning = data.agent_reasoning?.['Safety Agent']?.messages?.[0] || "Safety checks passed successfully based on read-only action policy.";

    return (
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex items-start gap-4">
            <div className="p-3 bg-slate-50 rounded-full border border-slate-100 shrink-0">
                {icon}
            </div>

            <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                    <h2 className="font-semibold text-slate-800 text-lg">Safety Decision</h2>
                    <span className={`text-xs px-3 py-1 font-bold rounded-full border ${badgeColor}`}>
                        {decision}
                    </span>
                </div>

                <p className="text-slate-600 leading-relaxed text-sm">
                    {safetyReasoning}
                </p>

                {decision === 'REVIEW_REQUIRED' && (
                    <div className="mt-4 p-4 bg-amber-50 border border-amber-200 rounded-lg">
                        <h4 className="text-sm font-semibold text-amber-800 mb-1">Human Action Required</h4>
                        <p className="text-xs text-amber-900 mb-3">This action modifies store state and requires manual approval.</p>
                        <div className="flex gap-2">
                            <button className="px-3 py-1.5 bg-amber-600 hover:bg-amber-700 text-white text-xs font-semibold rounded shadow-sm transition-colors">
                                Approve Action
                            </button>
                            <button className="px-3 py-1.5 bg-white border border-amber-300 text-amber-800 hover:bg-amber-100 text-xs font-semibold rounded shadow-sm transition-colors">
                                Reject
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
