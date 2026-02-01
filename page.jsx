// This part goes inside your return() function where you display results
<div className="max-w-4xl mx-auto p-8 bg-white shadow-xl rounded-2xl border border-gray-100">
  
  {/* 1. The New Status Header */}
  <div className="flex items-center justify-between border-b pb-6 mb-6">
    <div>
      <h1 className="text-2xl font-bold text-gray-800">Verification Audit</h1>
      <p className="text-sm text-gray-500">System scan complete</p>
    </div>
    <div className={`px-6 py-2 rounded-full font-bold text-lg ${
      status === 'True' ? 'bg-green-100 text-green-700' : 
      status === 'Not True' ? 'bg-red-100 text-red-700' : 'bg-gray-100 text-gray-700'
    }`}>
      {status === 'True' ? '✅ True' : status === 'Not True' ? '❌ Not True' : '❓ Inconclusive'}
    </div>
  </div>

  {/* 2. Authenticity Index (Formerly Confidence) */}
  <div className="mb-8">
    <div className="flex justify-between mb-2">
      <span className="text-sm font-semibold text-gray-600">Authenticity Index</span>
      <span className="text-sm font-bold text-blue-600">{authenticity_index * 100}% Real</span>
    </div>
    <div className="w-full bg-gray-200 rounded-full h-2.5">
      <div className="bg-blue-600 h-2.5 rounded-full" style={{ width: `${authenticity_index * 100}%` }}></div>
    </div>
  </div>

  {/* 3. Summary Section */}
  <div className="mb-8 p-4 bg-blue-50 rounded-lg">
    <h3 className="text-sm font-bold text-blue-800 uppercase mb-2">Summary</h3>
    <p className="text-gray-700 leading-relaxed">{summary}</p>
  </div>

  {/* 4. Master Explainer Section */}
  <div className="border-t pt-6">
    <h3 className="text-sm font-bold text-gray-500 uppercase mb-4">Master Explainer</h3>
    <div className="prose prose-slate max-w-none text-gray-800 bg-gray-50 p-6 rounded-xl border border-dashed border-gray-300">
      {master_explainer}
    </div>
  </div>
</div>