interface DataPoint{
    date: Date
    price: number
}

export default interface Predictions{
    history: DataPoint[]
    predictions: DataPoint[]
}