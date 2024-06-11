import { Divider } from "@mui/material"

export default function Profile() {
    return (
        <>
            <div className="profile-container">
                <h1 className="profile-header">Profile</h1>
                <Divider sx={{mb: 3}}/>
                <div className="profile-info">
                    <div className="profile-item">
                        <span className="profile-label">Username:</span>
                        <span className="profile-value">JoeMama69</span>
                    </div>
                    <div className="profile-item">
                        <span className="profile-label">Email:</span>
                        <span className="profile-value">joe@mama.com</span>
                    </div>
                </div>
            </div>
        </>
    );
}
