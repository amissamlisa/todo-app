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
import { PasswordResetMessageSent } from './features/users/pages/PasswordResetMessageSent';
import { PasswordResetEmailForm } from './features/users/pages/PasswordResetEmailForm';

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
    path: "/password-reset-email-form",
    element: <PasswordResetEmailForm />
  },{
    path: "/password-reset-message-sent",
    element: <PasswordResetMessageSent />
  }
]);
createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
  </StrictMode>
)
