import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Send, Loader2 } from 'lucide-react';
import type { RootState, AppDispatch } from '../../app/store';
import { setQuery, submitQuery } from './querySlice';

export default function QueryPanel() {
    const dispatch = useDispatch<AppDispatch>();
    const { query, status } = useSelector((state: RootState) => state.query);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (query.trim()) {
            dispatch(submitQuery(query));
        }
    };

    const isLoading = status === 'loading';

    return (
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
            <h2 className="text-lg font-semibold text-slate-800 mb-4 flex items-center gap-2">
                <span className="w-8 h-8 bg-blue-100 text-blue-600 rounded-lg flex items-center justify-center text-sm">You</span>
                User Request
            </h2>

            <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                    <textarea
                        value={query}
                        onChange={(e) => dispatch(setQuery(e.target.value))}
                        placeholder="E.g., Check stock for headphones or What is the return policy?"
                        className="w-full h-32 p-4 text-slate-700 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none resize-none bg-slate-50 placeholder:text-slate-400"
                        disabled={isLoading}
                    />
                </div>

                <div className="flex justify-between items-center">
                    <div className="flex gap-2">
                        {['Check Pricing', 'Low Stock?', 'Return Policy'].map((sample) => (
                            <button
                                key={sample}
                                type="button"
                                onClick={() => dispatch(setQuery(sample))}
                                className="text-xs px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-600 rounded-full transition-colors"
                                disabled={isLoading}
                            >
                                {sample}
                            </button>
                        ))}
                    </div>

                    <button
                        type="submit"
                        disabled={isLoading || !query.trim()}
                        className="flex items-center gap-2 px-6 py-2.5 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white rounded-lg font-medium transition-all"
                    >
                        {isLoading ? (
                            <>
                                <Loader2 className="animate-spin" size={18} />
                                Processing...
                            </>
                        ) : (
                            <>
                                <Send size={18} />
                                Submit Request
                            </>
                        )}
                    </button>
                </div>
            </form>
        </div>
    );
}
