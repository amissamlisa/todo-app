import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import { Login } from "./features/users/pages/Login";
import {AccountRegistrationConfirm } from "./features/users/pages/AccountRegistrationConfirm"
import { AccountRegistrationForm } from './features/users/pages/AccountRegistrationForm';
import { AccountRegistrationComplete } from './features/users/pages/AccountRegistrationComplete';

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
  },{
    path: "/user-registration/complete",
    element: <AccountRegistrationComplete/>
  }
]);
createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
)
