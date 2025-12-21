// import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import { Login } from "./features/users/pages/Login";
import { RegistrationForm } from "./features/users/pages/RegistrationForm"

const router = createBrowserRouter([
  {
    path: "/",
    element: <Login />,
  }, {
    path: "/user-registration",
    element: <RegistrationForm />,
  }
]);
createRoot(document.getElementById('root')!).render(
  <RouterProvider router={router} />
)
