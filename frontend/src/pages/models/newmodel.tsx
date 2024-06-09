import { Button, Modal, Backdrop, Fade, Box, Typography, TextField, MenuItem } from "@mui/material";
import Model from "../../interfaces/created_model";
import { useState } from "react";
import service from "../../services/service";

export default function NewModel({ onAddModel }: { onAddModel: (model: Model) => void }) {
    const userid = "1" //localStorage.getItem("userid")
    const [open, setOpen] = useState(false);
    const [newModel, setNewModel] = useState<Model>({ model_name: "", model_type: "", data_path: "", userid: parseInt(userid) });

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

    const handleAddModel = async () => {
        try {
            onAddModel(newModel); // Call the onAddModel callback with the new model
            handleClose()
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
                            name="datapath"
                            onChange={handleModelChange}
                            sx={{ mt: 2 }}
                        />
                        <button className="add-model" onClick={handleAddModel}>Add Model</button>
                    </Box>
                </Fade>
            </Modal>
        </>
    );
}
