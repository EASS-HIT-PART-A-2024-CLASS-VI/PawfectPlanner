// File: frontend/src/components/Navbar.jsx
import React, { useContext } from "react";
import { AppBar, Toolbar, Button } from "@mui/material";
import { Link, useLocation } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

/**
 * Decide if the current route matches the link exactly.
 */
function isActiveRoute(pathname, linkPath) {
  return pathname === linkPath;
}

function Navbar() {
  const { isAuthenticated, logout } = useContext(AuthContext);
  const location = useLocation();

  return (
    <AppBar position="static">
      <Toolbar sx={{ justifyContent: "center", gap: 2 }}>
        <Button
          color="inherit"
          component={Link}
          to="/"
          sx={{
            backgroundColor: isActiveRoute(location.pathname, "/")
              ? "rgba(255, 255, 255, 0.2)"
              : "inherit",
          }}
        >
          Home
        </Button>
        <Button
          color="inherit"
          component={Link}
          to="/dashboard"
          sx={{
            backgroundColor: isActiveRoute(location.pathname, "/dashboard")
              ? "rgba(255, 255, 255, 0.2)"
              : "inherit",
          }}
        >
          Dashboard
        </Button>
        <Button
          color="inherit"
          component={Link}
          to="/reminders"
          sx={{
            backgroundColor: isActiveRoute(location.pathname, "/reminders")
              ? "rgba(255, 255, 255, 0.2)"
              : "inherit",
          }}
        >
          Reminders
        </Button>
        <Button
          color="inherit"
          component={Link}
          to="/treatments"
          sx={{
            backgroundColor: isActiveRoute(location.pathname, "/treatments")
              ? "rgba(255, 255, 255, 0.2)"
              : "inherit",
          }}
        >
          Treatments
        </Button>
        <Button
          color="inherit"
          component={Link}
          to="/services"
          sx={{
            backgroundColor: isActiveRoute(location.pathname, "/services")
              ? "rgba(255, 255, 255, 0.2)"
              : "inherit",
          }}
        >
          Locate Services
        </Button>
        <Button
          color="inherit"
          component={Link}
          to="/pawfectgpt"
          sx={{
            backgroundColor: isActiveRoute(location.pathname, "/pawfectgpt")
              ? "rgba(255, 255, 255, 0.2)"
              : "inherit",
          }}
        >
          Pawfect GPT
        </Button>
        {isAuthenticated ? (
          <Button color="inherit" onClick={logout}>
            Logout
          </Button>
        ) : (
          <>
            <Button
              color="inherit"
              component={Link}
              to="/login"
              sx={{
                backgroundColor: isActiveRoute(location.pathname, "/login")
                  ? "rgba(255, 255, 255, 0.2)"
                  : "inherit",
              }}
            >
              Login
            </Button>
            <Button
              color="inherit"
              component={Link}
              to="/signup"
              sx={{
                backgroundColor: isActiveRoute(location.pathname, "/signup")
                  ? "rgba(255, 255, 255, 0.2)"
                  : "inherit",
              }}
            >
              Sign Up
            </Button>
          </>
        )}
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;
