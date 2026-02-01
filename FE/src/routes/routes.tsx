import { createBrowserRouter } from "react-router";

import App from "../App.tsx";
import BlankLayout from "../components/layout/BlankLayout.tsx";
import RouterErrorHandler from "../components/Error/RouterErrorHandler.tsx";
import Home from "../pages/Home/Home.tsx";
import Problems from "../pages/Problems/Problems.tsx";
import Settings from "../pages/Settings/Settings.tsx";
import User from "../pages/User/User.tsx";

const router = createBrowserRouter([
    {
      path: "/",
      element: <App />,
      errorElement: <RouterErrorHandler />,
      children: [
        {
          // 헤더가 없는 레이아웃
          element: <BlankLayout />,
          children: [
            {
              path: "",
              element: <Home />,
            },
            {
              path: "problems",
              element: <Problems />,
            },
            {
              path: "settings",
              element: <Settings />,
            },
            {
              path: "user",
              element: <User />,
            },
          ],
        },
      ],
    },
  ]);

  export default router;