export default interface Model{
    id: number
    model_name: string;
    model_type: string;
    status: "deployed" | "not deployed"
}