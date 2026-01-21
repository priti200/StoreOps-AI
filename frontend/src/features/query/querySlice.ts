import { createSlice, createAsyncThunk, type PayloadAction } from '@reduxjs/toolkit';
import apiClient from '../../services/apiClient';

interface AgentReasoning {
    agent_name: string;
    messages: string[];
}

interface ToolCall {
    tool: string;
    input: string;
    output: string;
}

interface QueryResponse {
    intent: string;
    agents_used: string[];
    agent_reasoning: Record<string, AgentReasoning>;
    tools_called: ToolCall[];
    safety_decision: string;
    logs: string[];
    raw_output: any;
    response: string; // The final answer
}

interface QueryState {
    query: string;
    status: 'idle' | 'loading' | 'succeeded' | 'failed';
    error: string | null;
    data: QueryResponse | null;
}

const initialState: QueryState = {
    query: '',
    status: 'idle',
    error: null,
    data: null,
};

export const submitQuery = createAsyncThunk(
    'query/submit',
    async (queryText: string) => {
        const response = await apiClient.post('/query', { query: queryText });
        return response.data;
    }
);

const querySlice = createSlice({
    name: 'query',
    initialState,
    reducers: {
        setQuery: (state, action: PayloadAction<string>) => {
            state.query = action.payload;
        },
        resetState: (state) => {
            state.status = 'idle';
            state.data = null;
            state.error = null;
        }
    },
    extraReducers: (builder) => {
        builder
            .addCase(submitQuery.pending, (state) => {
                state.status = 'loading';
                state.error = null;
            })
            .addCase(submitQuery.fulfilled, (state, action) => {
                state.status = 'succeeded';
                state.data = action.payload;
            })
            .addCase(submitQuery.rejected, (state, action) => {
                state.status = 'failed';
                state.error = action.error.message || 'An error occurred';
            });
    },
});

export const { setQuery, resetState } = querySlice.actions;
export default querySlice.reducer;
