import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import ImageUpload from '../components/ImageUpload';
import ResultCard from '../components/ResultCard';
import { predictPlantDisease } from '../services/api'; // Import your new API helper

const Home = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);

  const handlePredict = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setPrediction(null);
    setErrorMsg(null);

    try {
      // Call the real FastAPI backend service
      const data = await predictPlantDisease(selectedFile);
      setPrediction(data);
    } catch (err) {
      setErrorMsg(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen overflow-hidden bg-slate-950 text-slate-100 selection:bg-emerald-500/30">
      {/* Ambient Glass Glow Orbs */}
      <div className="pointer-events-none absolute -top-24 left-1/4 h-96 w-96 rounded-full bg-emerald-500/15 blur-[120px]" />
      <div className="pointer-events-none absolute right-1/4 bottom-0 h-80 w-80 rounded-full bg-teal-500/10 blur-[120px]" />

      <Navbar />

      <main className="relative z-10 mx-auto flex max-w-2xl flex-col items-center justify-center px-6 py-10">
        {/* Header Branding */}
        <div className="mb-8 text-center">
          <h2 className="bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-3xl font-extrabold tracking-tight text-transparent">
            Plant Disease Detection
          </h2>
          <p className="mt-2 text-sm text-slate-400">
            Upload a clear photo of your plant leaf to instantly analyze and diagnose health conditions.
          </p>
        </div>

        {/* Main Central Upload Console */}
        <div className="w-full rounded-3xl border border-white/10 bg-white/[0.04] p-6 shadow-2xl backdrop-blur-2xl">
          <ImageUpload
            onImageSelect={(file) => {
              setSelectedFile(file);
              setPrediction(null);
              setErrorMsg(null);
            }}
          />

          {errorMsg && (
            <div className="mt-4 rounded-xl border border-red-500/30 bg-red-500/10 p-3 text-center text-xs text-red-300">
              {errorMsg}
            </div>
          )}

          <button
            onClick={handlePredict}
            disabled={!selectedFile || loading}
            className={`mt-6 flex w-full items-center justify-center gap-2 rounded-xl py-3.5 text-sm font-semibold transition-all duration-200 ${
              !selectedFile || loading
                ? 'cursor-not-allowed border border-white/5 bg-white/5 text-slate-500'
                : 'bg-gradient-to-r from-emerald-500 to-teal-500 text-slate-950 shadow-lg shadow-emerald-500/25 hover:brightness-110 active:scale-[0.99]'
            }`}
          >
            {loading ? 'Analyzing Plant Health...' : 'Detect Disease'}
          </button>
        </div>

        {/* Dynamic Results Card */}
        {(loading || prediction) && (
          <div className="mt-6 w-full animate-fade-in">
            <ResultCard result={prediction} loading={loading} />
          </div>
        )}
      </main>
    </div>
  );
};

export default Home;