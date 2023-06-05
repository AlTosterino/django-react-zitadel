import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import { AuthProvider } from "oidc-react";

const oidcConfig = {
  authority: "http://localhost:8080",
  clientId: "", // REPLACE
  responseType: "code",
  redirectUri: "http://localhost:5173",
  scope: "openid profile email",
  autoSignIn: false,
};
const renderApp = () =>
  ReactDOM.createRoot(document.getElementById("root")).render(
    <React.StrictMode>
      <AuthProvider {...oidcConfig}>
        <App />
      </AuthProvider>
    </React.StrictMode>
  );

renderApp();
