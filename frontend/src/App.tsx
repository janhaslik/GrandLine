import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainLayout from "./components/MainLayout.tsx";
import Models from "./pages/models/models.tsx"

import './App.css'

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={<MainLayout />}
        >
          <Route index/>
        </Route>
        <Route
          path="/models"
          element={<MainLayout />}
        >
          <Route index element={<Models />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
