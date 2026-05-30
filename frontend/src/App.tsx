import './App.css'

function App() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-slate-100">
      <div className="p-8 bg-white rounded-2xl shadow-xl text-center">
        <h1 className="text-3xl font-bold text-blue-600">
          Tailwind CSS が導入されました
        </h1>
        <p className="mt-2 text-gray-500">
          スタイリングが正常に適用されていれば、このカードが中央に表示されます。
        </p>
      </div>
    </div>
  )
}

export default App