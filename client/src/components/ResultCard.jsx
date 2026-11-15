import React from 'react';

const ResultCard = ({ result, loading }) => {
  if (loading) {
    return (
      <div className="flex h-full min-h-[260px] flex-col items-center justify-center rounded-3xl border border-white/10 bg-white/[0.03] p-6 backdrop-blur-2xl">
        <div className="h-10 w-10 animate-spin rounded-full border-2 border-emerald-500/20 border-t-emerald-400" />
        <p className="mt-4 text-sm font-medium text-slate-300">Running neural inference...</p>
        <p className="mt-1 text-xs text-slate-500">Extracting leaf pathology features</p>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="flex h-full min-h-[260px] flex-col items-center justify-center rounded-3xl border border-dashed border-white/10 bg-white/[0.02] p-6 text-center backdrop-blur-xl">
        <div className="mb-3 rounded-full border border-white/10 bg-white/5 p-3 text-slate-400">
          <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.75" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <p className="text-sm font-medium text-slate-300">Awaiting Specimen</p>
        <p className="mt-1 max-w-[220px] text-xs text-slate-500">
          Upload a leaf photo and run diagnostics to view confidence metrics here.
        </p>
      </div>
    );
  }

  const formattedName = result.class.replace(/___/g, ' — ').replace(/_/g, ' ');
  const isHealthy = result.class.toLowerCase().includes('healthy');

  return (
    <div className="flex h-full flex-col justify-between rounded-3xl border border-white/15 bg-gradient-to-b from-white/[0.07] to-white/[0.02] p-6 shadow-2xl backdrop-blur-2xl">
      <div>
        <div className="flex items-center justify-between">
          <span className="text-[11px] font-semibold tracking-wider text-slate-400 uppercase">
            Diagnostic Report
          </span>
          <span
            className={`rounded-full border px-2.5 py-0.5 text-[11px] font-semibold ${
              isHealthy
                ? 'border-emerald-500/30 bg-emerald-500/15 text-emerald-300'
                : 'border-amber-500/30 bg-amber-500/15 text-amber-300'
            }`}
          >
            {isHealthy ? 'Healthy Tissue' : 'Pathogen Detected'}
          </span>
        </div>

        <h3 className="mt-4 text-xl font-bold leading-snug text-white">
          {formattedName}
        </h3>
      </div>

      <div className="mt-6 rounded-2xl border border-white/10 bg-slate-950/50 p-4">
        <div className="flex items-baseline justify-between">
          <span className="text-xs font-medium text-slate-400">Model Confidence</span>
          <span className="text-lg font-bold text-emerald-400">{result.confidence}%</span>
        </div>

        <div className="mt-2.5 h-2 w-full overflow-hidden rounded-full bg-white/10">
          <div
            className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-teal-300 shadow-[0_0_12px_rgba(16,185,129,0.6)] transition-all duration-700 ease-out"
            style={{ width: `${result.confidence}%` }}
          />
        </div>
      </div>
    </div>
  );
};

export default ResultCard;