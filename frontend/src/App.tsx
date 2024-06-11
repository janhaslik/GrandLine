import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import MainLayout from "./components/MainLayout.tsx";
import Models from "./pages/models/models.tsx"
import './App.css'
import Login from "./pages/user/login.tsx";
import { useAuth } from "./hooks/auth.ts";
import Register from "./pages/user/register.tsx";
import Profile from "./pages/user/profile.tsx";
import Settings from "./pages/user/settings.tsx";

function App() {
  const auth = useAuth()

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          <Route index />
        </Route>
        <Route path="/login" element={<Login/>}/>
        <Route path="/register" element={<Register/>}/>
        <Route
          path="/models"
          element={auth.isLoggedIn() ? <MainLayout /> : <Navigate to="/login" replace />}
        >
          <Route index element={<Models />} />
        </Route>
        <Route
          path="/profile"
          element={auth.isLoggedIn() ? <MainLayout /> : <Navigate to="/login" replace />}
        >
          <Route index element={<Profile />} />
          <Route path='settings' element={<Settings/>}/>
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App;
