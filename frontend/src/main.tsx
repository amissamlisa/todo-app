import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import { Login } from "./features/users/pages/Login";
import { AccountRegistrationConfirm } from "./features/users/pages/AccountRegistrationConfirm"
import { AccountRegistrationForm } from './features/users/pages/AccountRegistrationForm';
import { AccountRegistrationComplete } from './features/users/pages/AccountRegistrationComplete';
import { AuthProvider } from './features/users/auth/AuthProvider';
import { AccountRegistrationIncomplete } from './features/users/pages/AccountRegistrationIncomplete';
import { PasswordReset } from './features/users/pages/PasswordReset';

const router = createBrowserRouter([
  {
    path: "/",
    element: <Login />,
  }, {
    path: "/user-registration",
    element: <AccountRegistrationForm />,
  }, {
    path: "/user-registration/confirm",
    element: <AccountRegistrationConfirm />,
  }, {
    path: "/user-registration/complete",
    element: <AccountRegistrationComplete />
  },{
    path: "/user-registration/incomplete",
    element: <AccountRegistrationIncomplete />
  },{
    path: "/password-reset",
    element: <PasswordReset />
  }
]);
createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
  </StrictMode>
)
