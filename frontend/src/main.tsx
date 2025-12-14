// import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import { Login } from "./features/users/pages/Login";

const router = createBrowserRouter([
    {
    path: "/",
    element: <Login />,
  }
]);
createRoot(document.getElementById('root')!).render(
  <RouterProvider router={router} />
)
