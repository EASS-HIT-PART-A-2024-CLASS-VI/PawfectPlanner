import React, { useContext } from "react";
import { AppBar, Toolbar, Button } from "@mui/material";
import { Link } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

function Navbar() {
  const { isAuthenticated, logout } = useContext(AuthContext);

  return (
    <AppBar position="static">
      {/* Center all items on the toolbar */}
      <Toolbar sx={{ justifyContent: "center" }}>
        <Button color="inherit" component={Link} to="/">Home</Button>
        <Button color="inherit" component={Link} to="/profile">Pet Profile</Button>
        <Button color="inherit" component={Link} to="/reminders">Reminders</Button>
        <Button color="inherit" component={Link} to="/treatments">Treatments</Button>
        <Button color="inherit" component={Link} to="/vet-locator">Find a Vet</Button>
        <Button color="inherit" component={Link} to="/gemini-service">Gemini Chat</Button>
        {isAuthenticated ? (
          <>
            <Button color="inherit" component={Link} to="/dashboard">Dashboard</Button>
            <Button color="inherit" onClick={logout}>Logout</Button>
          </>
        ) : (
          <>
            <Button color="inherit" component={Link} to="/login">Login</Button>
            <Button color="inherit" component={Link} to="/signup">Sign Up</Button>
          </>
        )}
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;
