// import { StrictMode } from 'react'
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
import { PasswordResetMessageSent } from './features/users/pages/PasswordResetRequestSubmitted ';
import { PasswordResetEmailForm } from './features/users/pages/PasswordResetEmailForm';
import { PasswordResetForm } from './features/users/pages/PasswordResetForm';
import { PasswordResetComplete } from './features/users/pages/PasswordResetComplete';
import { PasswordResetIncomplete } from './features/users/pages/PasswordResetIncomplete';
import { Top } from './features/tasks/Top';
import { NotFoundPage } from './shared/components/pages/NotFoundPage';
import { ProtectedRoute } from './features/users/auth/ProtectedRoute';
import { PublicOnlyRoute } from './features/users/auth/PublicOnlyRoute';
import { Logout } from './features/users/pages/Logout';
import { StrictMode } from 'react';
import { TaskRegistrationForm } from './features/tasks/TaskRegistrationForm';


const router = createBrowserRouter([
  {
    path: "/",
    element: <PublicOnlyRoute><Login /></PublicOnlyRoute>,
  }, {
    path: "/user-registration",
    element: <PublicOnlyRoute><AccountRegistrationForm /></PublicOnlyRoute>,
  }, {
    path: "/user-registration/confirm",
    element: <PublicOnlyRoute><AccountRegistrationConfirm /></PublicOnlyRoute>,
  }, {
    path: "/user-registration/complete",
    element: <PublicOnlyRoute><AccountRegistrationComplete /></PublicOnlyRoute>
  }, {
    path: "/user-registration/incomplete",
    element: <PublicOnlyRoute><AccountRegistrationIncomplete /></PublicOnlyRoute>
  }, {
    path: "/password-reset-email-form",
    element: <PublicOnlyRoute><PasswordResetEmailForm /></PublicOnlyRoute>
  }, {
    path: "/password-reset-message-sent",
    element: <PublicOnlyRoute><PasswordResetMessageSent /></PublicOnlyRoute>
  }, {
    path: "/password-reset",
    element: <PublicOnlyRoute><PasswordResetForm /></PublicOnlyRoute>
  }, {
    path: "/password-reset-complete",
    element: <PublicOnlyRoute><PasswordResetComplete /></PublicOnlyRoute>
  }, {
    path: "/password-reset-incomplete",
    element: <PublicOnlyRoute><PasswordResetIncomplete /></PublicOnlyRoute>
  }, {
    path: "/not-found",
    element: <PublicOnlyRoute><NotFoundPage /></PublicOnlyRoute>
  }, {
    path: "/top",
    element: <ProtectedRoute><Top /></ProtectedRoute>
  },{
    path: "/tasks-registration",
    element:<ProtectedRoute><TaskRegistrationForm /></ProtectedRoute>
  },  {
    path: "/logout",
    element: <Logout />
  }
]);
createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
  </StrictMode>
)
