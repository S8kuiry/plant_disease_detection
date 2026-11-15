import React, { useState } from 'react';

const ImageUpload = ({ onImageSelect }) => {
  const [preview, setPreview] = useState(null);
  const [isDragging, setIsDragging] = useState(false);

  const processFile = (file) => {
    if (file && file.type.startsWith('image/')) {
      setPreview(URL.createObjectURL(file));
      onImageSelect(file);
    }
  };

  const handleFileChange = (e) => {
    processFile(e.target.files[0]);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    processFile(e.dataTransfer.files[0]);
  };

  const handleClear = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setPreview(null);
    onImageSelect(null);
  };

  return (
    <div className="w-full">
      <label
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        className={`group relative flex h-60 w-full cursor-pointer flex-col items-center justify-center overflow-hidden rounded-2xl border transition-all duration-300 ${
          isDragging
            ? 'border-emerald-400 bg-emerald-500/10 shadow-[0_0_30px_rgba(16,185,129,0.2)]'
            : 'border-white/10 bg-slate-900/60 hover:border-emerald-400/40 hover:bg-slate-900/80'
        }`}
      >
        {preview ? (
          <div className="relative flex h-full w-full items-center justify-center p-3">
            {/* object-contain ensures the entire leaf image is fully visible without cropping */}
            <img
              src={preview}
              alt="Leaf Specimen"
              className="max-h-full max-w-full rounded-xl object-contain shadow-md"
            />
            <button
              type="button"
              onClick={handleClear}
              className="absolute top-4 right-4 rounded-lg border border-white/15 bg-slate-950/80 px-3 py-1.5 text-xs font-semibold text-slate-200 backdrop-blur-md transition hover:bg-red-500/80 hover:text-white shadow-lg"
            >
              Change Image
            </button>
          </div>
        ) : (
          <div className="flex flex-col items-center px-6 text-center">
            <div className="mb-3 flex h-12 w-12 items-center justify-center rounded-2xl border border-white/10 bg-white/5 text-emerald-400 shadow-inner transition-transform duration-300 group-hover:-translate-y-1 group-hover:border-emerald-400/30">
              <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="1.75"
                  d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                />
              </svg>
            </div>
            <p className="text-sm font-medium text-slate-200">
              Drop leaf image here or <span className="text-emerald-400 underline decoration-emerald-400/40 underline-offset-4">browse</span>
            </p>
            <p className="mt-1 text-xs text-slate-500">Supports PNG, JPG, JPEG</p>
          </div>
        )}
        <input type="file" className="hidden" accept="image/*" onChange={handleFileChange} />
      </label>
    </div>
  );
};

export default ImageUpload;