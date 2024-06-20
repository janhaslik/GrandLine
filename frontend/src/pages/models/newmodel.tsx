import { Modal, Backdrop, Fade, Box, Typography, TextField, MenuItem } from "@mui/material";
import Model from "../../interfaces/created_model";
import { useState } from "react";
import service from "../../services/service";

export default function NewModel({ onAddModel }: { onAddModel: (model: Model) => void}) {
    const userid = "1" //localStorage.getItem("userid")
    const [open, setOpen] = useState(false);
    const [newModel, setNewModel] = useState<Model>({ model_name: "", model_type: "", data_path: "", userid: parseInt(userid), data_date: "", data_output: "" });
    const [file, setFile] = useState<File | null>(null)

    const handleOpen = () => setOpen(true);
    const handleClose = () => setOpen(false);

    const typeOptions = [
        { option: "ARIMA" },
        { option: "LSTM" },
    ];

    const style = {
        position: 'absolute' as 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: 400,
        bgcolor: 'background.paper',
        boxShadow: 24,
        p: 4,
        display: 'flex',
        flexDirection: 'column',
    };

    const handleModelChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setNewModel({
            ...newModel,
            [e.target.name]: e.target.value
        });
    }

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if(e.target.files){
            setFile(e.target.files[0])
        }
    }

    const handleAddModel = async () => {
        try {
            if(file){
                const formData = new FormData()
                formData.append('dataset', file)
                
                const data_path=await service.uploadDataset(formData)
                
                const addModel={
                    ...newModel,
                    data_path: data_path
                }

                onAddModel(addModel);
                handleClose()
            }
        } catch (error) {
            console.error("Failed to add model", error);
        }
    }

    return (
        <>
            <button className="add-model" onClick={handleOpen}>Add Model</button>
            <Modal
                aria-labelledby="spring-modal-title"
                aria-describedby="spring-modal-description"
                open={open}
                onClose={handleClose}
                closeAfterTransition
                slots={{ backdrop: Backdrop }}
                slotProps={{
                    backdrop: {
                        TransitionComponent: Fade,
                    },
                }}
            >
                <Fade in={open}>
                    <Box sx={style}>
                        <Typography id="spring-modal-title" variant="h6" component="h2">
                            New Model
                        </Typography>
                        <TextField
                            type="text"
                            label="Name"
                            name="model_name"
                            value={newModel.model_name}
                            onChange={handleModelChange}
                            sx={{ mt: 2 }}
                        />
                        <TextField
                            type="option"
                            label="Type"
                            name="model_type"
                            select
                            value={newModel.model_type}
                            onChange={handleModelChange}
                            sx={{ mt: 2 }}
                        >
                            {typeOptions.map((typeOption) => (
                                <MenuItem key={typeOption.option} value={typeOption.option}>
                                    {typeOption.option}
                                </MenuItem>
                            ))}
                        </TextField>
                        <TextField
                            type="file"
                            name="data_path"
                            onChange={handleFileChange}
                            sx={{ mt: 2 }}
                        />
                        <Box display="flex" flexDirection="row" gap={2} sx={{mt: 2}}>
                            <TextField type="text" name="data_date" label="Date Field" onChange={handleModelChange}/>
                            <TextField type="text" name="data_output" label="Output Field" onChange={handleModelChange}/>
                        </Box>
                        <button className="add-model" onClick={handleAddModel}>Add Model</button>
                    </Box>
                </Fade>
            </Modal>
        </>
    );
}
