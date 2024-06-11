import { useState } from "react";
import { Switch, Divider } from "@mui/material";

export default function Settings() {
  const [notificationSound, setNotificationSound] = useState(true);
  const [darkMode, setDarkMode] = useState(false);
  const [emailNotifications, setEmailNotifications] = useState(true);

  return (
    <>
      <div className="settings-container">
        <h1 className="settings-header">Settings</h1>
        <Divider sx={{ mb: 3 }} />
        <div className="settings-options">
          <div className="settings-option">
            <span className="settings-label">Notification Sound:</span>
            <Switch
              checked={notificationSound}
              onChange={() => setNotificationSound(!notificationSound)}
              color={notificationSound ? "primary" : "secondary"}
            />
          </div>
          <div className="settings-option">
            <span className="settings-label">Dark Mode:</span>
            <Switch
              checked={darkMode}
              onChange={() => setDarkMode(!darkMode)}
              color={darkMode ? "primary" : "secondary"}
            />
          </div>
          <div className="settings-option">
            <span className="settings-label">Email Notifications:</span>
            <Switch
              checked={emailNotifications}
              onChange={() => setEmailNotifications(!emailNotifications)}
              color={emailNotifications ? "primary" : "secondary"}
            />
          </div>
        </div>
      </div>
    </>
  );
}
