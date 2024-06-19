import { useState } from "react";
import Model from "../../interfaces/saved_model";
import service from "../../services/service";
import Forecast from "./forecast";
import Predictions from "../../interfaces/predictions";

export default function ModelComponent(props: Model) {
    const [showGraph, setShowGraph] = useState(false);
    const [predict, setPredict] = useState(false)
    const [loading, setLoading] = useState(false);
    const [status, setStatus] = useState(props.status);
    const [predictions, setPredictions] = useState<Predictions>({history: [], predictions: []})

    const handleShowForecast = async () => {
        setShowGraph((prev) => !prev);
        if(!predict){
            setPredict(true)
            const data = await service.forecast(props.id, 1000)
            setPredictions({"history": data.history, "predictions": data.predictions})
            setPredict(false)
        }
    };

    const handleDeployModel = async () => {
        setLoading(true);
        try {
            const response = await service.deployModel(props.id);
            if (response.status === 200) {
                setStatus("deployed");
            }
        } catch (error) {
            console.error('Error deploying model:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="model">
            <div className="model-content">
                <div className="model-info">
                    <div className="model-info-text">
                        <span className="model-name">{props.model_name}</span>
                        <span className="model-type">{props.model_type}</span>
                        <span className="model-type">Dataset: SPX.csv</span>
                    </div>
                </div>
                <div className="model-status">
                    {status === "deployed" ? (
                        <>
                            <span className="status-icon-deployed" title="Deployed">●</span>
                            <span className="status-text">Deployed</span>
                        </>
                    ) : (
                        <>
                            <span className="status-icon-notdeployed" title="Not Deployed">●</span>
                            <span className="status-text">Not Deployed</span>
                        </>
                    )}
                </div>
            </div>

            {status !== "deployed" ? (
                <button className="show-forecast-button" onClick={handleDeployModel} disabled={loading}>
                        Deploy model
                </button>
            ) : (
                <div>
                   
                    {showGraph ? (
                        <>
                            <button className="show-forecast-button" onClick={handleShowForecast}>
                                Hide Forecast
                            </button>
                            <div className="forecast-graph">
                                <Forecast history={predictions?.history} predictions={predictions?.predictions} loading={predictions.history.length==0}/>
                            </div>
                        </>
                    ) : (
                        <button className="show-forecast-button" onClick={handleShowForecast}>
                            Show Forecast
                        </button>
                    )}
                </div>
            )}
        </div>
    );
}
