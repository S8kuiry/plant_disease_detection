import React from 'react';

const Navbar = () => {
  return (
    <header className="sticky top-0 z-50 border-b border-white/10 bg-slate-950/60 backdrop-blur-xl">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-3.5">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-emerald-400 to-teal-600 shadow-lg shadow-emerald-500/20">
            <span className="text-lg">🌿</span>
          </div>
          <div>
            <h1 className="text-base font-bold tracking-tight text-white">
              AgriGuard <span className="text-emerald-400">AI</span>
            </h1>
            <p className="text-[11px] text-slate-400">MobileNetV2 Vision Engine</p>
          </div>
        </div>

        <div className="flex items-center gap-2 rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1 backdrop-blur-md">
          <span className="relative flex h-2 w-2">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-500"></span>
          </span>
          <span className="text-xs font-medium text-emerald-300">API Ready</span>
        </div>
      </div>
    </header>
  );
};

export default Navbar;