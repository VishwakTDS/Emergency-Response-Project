import React from "react";

const IncidentUploadForm = ({ file, lat, lon, setFile, setLat, setLon, handleSubmit, response, errors, loading }) => (
  <div>
    {/* Header */}
    <header className="mb-8 text-center">
      <h1 className="text-3xl font-extrabold text-white tracking-tight mb-2">Emergency Response Portal</h1>
      <p className="text-gray-300">Upload incident details and location for rapid response</p>
    </header>
    <div className="bg-gray-900 bg-opacity-80 rounded-lg shadow-lg p-8 max-w-md mx-auto border-2 border-red-500">
      <h2 className="text-2xl font-bold mb-6 text-white text-center">Emergency Incident Upload</h2>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4" autoComplete="off">
        <div>
          <label htmlFor="incident-file" className="sr-only">Upload File</label>
          <input
            id="incident-file"
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            className="text-white focus:outline-none focus:ring-2 focus:ring-red-400 w-full"
            aria-invalid={!!errors?.file}
            aria-describedby={errors?.file ? "file-error" : undefined}
          />
          {errors?.file && <p id="file-error" className="text-red-400 text-sm mt-1">{errors.file}</p>}
        </div>
        <div>
          <label htmlFor="latitude" className="block text-gray-200 mb-1">Latitude</label>
          <input
            id="latitude"
            type="text"
            placeholder="Latitude"
            value={lat}
            onChange={(e) => setLat(e.target.value)}
            className="bg-gray-800 text-white rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-400 w-full"
            aria-invalid={!!errors?.lat}
            aria-describedby={errors?.lat ? "lat-error" : undefined}
            inputMode="decimal"
            autoComplete="off"
          />
          {errors?.lat && <p id="lat-error" className="text-red-400 text-sm mt-1">{errors.lat}</p>}
        </div>
        <div>
          <label htmlFor="longitude" className="block text-gray-200 mb-1">Longitude</label>
          <input
            id="longitude"
            type="text"
            placeholder="Longitude"
            value={lon}
            onChange={(e) => setLon(e.target.value)}
            className="bg-gray-800 text-white rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-400 w-full"
            aria-invalid={!!errors?.lon}
            aria-describedby={errors?.lon ? "lon-error" : undefined}
            inputMode="decimal"
            autoComplete="off"
          />
          {errors?.lon && <p id="lon-error" className="text-red-400 text-sm mt-1">{errors.lon}</p>}
        </div>
        <button
          type="submit"
          className="bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded transition-colors disabled:opacity-60 focus:outline-none focus:ring-2 focus:ring-red-400"
          disabled={loading}
        >
          {loading ? "Submitting..." : "Submit"}
        </button>
      </form>
      {response && (
        <div className="mt-6 bg-gray-800 rounded p-4 text-white">
          <h3 className="font-semibold mb-2">Server Response:</h3>
          <pre className="whitespace-pre-wrap break-words">{JSON.stringify(response, null, 2)}</pre>
        </div>
      )}
    </div>
    {/* Footer */}
    <footer className="mt-10 text-center text-gray-400 text-sm">
      &copy; {new Date().getFullYear()} Emergency Response Project. All rights reserved.
    </footer>
  </div>
);

export default IncidentUploadForm; 