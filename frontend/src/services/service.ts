import created_model from "../interfaces/created_model"

async function getModels() {
    const userid = 1; // Or use sessionStorage.getItem("grandline_userid")

    const response = await fetch(`http://127.0.0.1:5000/models?userid=${userid}`);
    const data = await response.json();
    return data.models;
}

async function addModel(model: created_model) {
    const response = await fetch(`http://127.0.0.1:5000/models`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(model)
    });

    return await response.json();
}

export default { getModels, addModel };
