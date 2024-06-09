import { useEffect, useState } from "react";
import ModelInterface from "../../interfaces/saved_model";
import ModelCreatedInterface from "../../interfaces/created_model";
import "../../style/models.css";
import ModelComponent from "./model";
import NewModel from "./newmodel";
import service from "../../services/service";

export default function Models() {
    const [models, setModels] = useState<ModelInterface[]>([]);
    
    const fetchData = async () => {
        try {
            const data = await service.getModels();
            setModels(data);
        } catch (error) {
            console.error("Failed to fetch models", error);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const handleAddModel = async (model: ModelCreatedInterface) => {
        try {
            await service.addModel(model);
            fetchData();
        } catch (error) {
            console.error("Failed to add model", error);
        }
    };

    return (
        <div className="models-page">
            <h1 className="title">My Models</h1>
            <h3 className="subtitle">View and manage your ML Models</h3>
            <NewModel onAddModel={handleAddModel} />
            <div className="models">
                {models.map((model, index) => (
                    <ModelComponent 
                        key={index} 
                        model_name={model.model_name} 
                        model_type={model.model_type} 
                        status={model.status}
                    />
                ))}
            </div>
        </div>
    );
}
