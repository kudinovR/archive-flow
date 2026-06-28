import { BrowserRouter, Routes, Route } from "react-router";
import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import NotfoundPage from "./pages/NotfoundPage";

function App() {
  return (
    <>
      <h1 className="p-2 text-center text-4xl border-b-2 border-gray-300">
        Archiv Flow
      </h1>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LoginPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="*" element={<NotfoundPage />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
