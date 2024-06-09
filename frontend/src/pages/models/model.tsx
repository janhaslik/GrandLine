import { useState } from "react";
import Model from "../../interfaces/saved_model";

export default function ModelComponent(props: Model) {
    const [showGraph, setShowGraph] = useState(false);

    const handleShowForecast = () => {
        setShowGraph((prev)=>!prev);
    };

    const handleDeployModel = () => {

    }

    return (
        <div className="model">
            <div className="model-content">
                <div className="model-info">
                    <span className="model-name">{props.model_name}</span>
                    <span className="model-type">{props.model_type}</span>
                </div>
                <div className="model-status">
                {
                    props.status === "deployed" ? (
                        <>
                            <span className="status-icon-deployed" title="Deployed">●</span>
                            <span className="status-text">Deployed</span>
                        </>
                    ) : (
                        <>
                            <span className="status-icon-notdeployed" title="Not Deployed">●</span>
                            <span className="status-text">Not Deployed</span>
                        </>
                    )
                }
                </div>
            </div>

            {props.status === "not deployed" ? (
                <button className="show-forecast-button" onClick={handleDeployModel}>
                    Deploy model
                </button>
            ) : (
            <div>
                <button className="show-forecast-button" onClick={handleShowForecast}>
                    Show Forecast
                </button>
                {showGraph && (
                    <div className="forecast-graph">
                    </div>
                )}
            </div>
            )}
        </div>
    );
}
