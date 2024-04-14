import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";

import Navbar from "./components/Navbar";
import { AuthProvider } from "./context/AuthContext"
import LogInPage from "./views/LogInPage";
import PrivateRoute from "./utils/PrivateRoute";
import RegisterPage from "./views/RegisterPage";
import InboxPage from "./views/InboxPage";

function App() {
	return (
		<BrowserRouter>
			<AuthProvider>
				<Navbar />
				<Routes>
					<Route path="/login" Component={LogInPage} />
					<Route path="/register" Component={RegisterPage} />
					<Route path="/inbox" element={<PrivateRoute><InboxPage /></PrivateRoute>} />
					<Route path="/inbox/:userId" element={<PrivateRoute><InboxPage /></PrivateRoute>} />
					<Route exact path="/" element={<Navigate to="/inbox" replace />} />
				</Routes>
			</AuthProvider>
		</BrowserRouter>
	);
}

export default App;
